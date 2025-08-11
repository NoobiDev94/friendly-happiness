import math
import random
from pygame import Rect
import pgzrun

WIDTH, HEIGHT = 800, 600
CELL = 32
FLOORS = 5
game_state = "menu"
current_floor = 1
score = 0
enemies = []
music_enabled = True
sound_enabled = True
lives = 3

class Entity:
    def __init__(self, cell_x, cell_y, idle_frames, walk_frames, speed=160):
        self.cell_x, self.cell_y = cell_x, cell_y
        self.x = cell_x * CELL + CELL // 2
        self.y = cell_y * CELL + CELL // 2
        self.idle_frames = idle_frames
        self.walk_frames = walk_frames
        self.speed = speed
        self.target_x, self.target_y = self.x, self.y
        self.frame_index = 0
        self.frame_timer = 0.0
        self.frame_interval = 0.12
        self.actor = Actor(self.idle_frames[0], (self.x, self.y))
        self.actor.anchor = ("center", "center")

    def set_target_cell(self, nx, ny):
        nx = max(0, min(nx, WIDTH // CELL - 1))
        ny = max(0, min(ny, HEIGHT // CELL - 1))
        self.cell_x, self.cell_y = nx, ny
        self.target_x = nx * CELL + CELL // 2
        self.target_y = ny * CELL + CELL // 2

    def at_target(self):
        return abs(self.x - self.target_x) < 1 and abs(self.y - self.target_y) < 1

    def update_move(self, dt):
        if not self.at_target():
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                step = min(self.speed * dt, dist)
                self.x += dx / dist * step
                self.y += dy / dist * step

    def update_animation(self, dt):
        moving = not self.at_target()
        frames = self.walk_frames if moving else self.idle_frames
        self.frame_timer += dt
        if self.frame_timer >= self.frame_interval:
            self.frame_timer -= self.frame_interval
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.actor.image = frames[self.frame_index]
        self.actor.pos = (round(self.x), round(self.y))

    def update(self, dt):
        self.update_move(dt)
        self.update_animation(dt)

    def draw(self):
        self.actor.draw()

class Hero(Entity):
    def __init__(self, cell_x, cell_y):
        super().__init__(cell_x, cell_y, 
                        [f"hero_idle_{i}" for i in (1, 2)],
                        [f"hero_walk_{i}" for i in (1, 2, 3, 4)],
                        speed=220)
        self.health = self.max_health = 3
        self.attack_cooldown = 0
        self.attack_power = 1
        self.is_attacking = False
        self.invincible = False
        self.invincible_timer = 0

    def move_dir(self, dx, dy):
        if self.at_target():
            self.set_target_cell(self.cell_x + dx, self.cell_y + dy)
            
    def start_attack(self):
        if self.attack_cooldown <= 0:
            self.is_attacking = True
            self.attack_cooldown = 0.5
            return True
        return False
            
    def update(self, dt):
        super().update(dt)
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            if self.attack_cooldown <= 0.25:
                self.is_attacking = False
        
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False
                self.actor.opacity = 255

class Enemy(Entity):
    def __init__(self, cell_x, cell_y, enemy_type="goblin"):
        types = {
            "goblin": {"health": 2, "damage": 1, "speed": 120, "xp": 1},
            "orc": {"health": 4, "damage": 2, "speed": 100, "xp": 2}
        }
        self.type = enemy_type
        self.stats = types[enemy_type]
        self.health = self.stats["health"]
        idle = [f"{enemy_type}_idle_{i}" for i in (1, 2)]
        walk = [f"{enemy_type}_walk_{i}" for i in (1, 2, 3, 4)]
        super().__init__(cell_x, cell_y, idle, walk, self.stats["speed"])
        self.home_x, self.home_y = cell_x, cell_y
        self.territory = 3
        self.cooldown = random.uniform(0.2, 1.2)

    def choose_target(self):
        tx = self.home_x + random.randint(-self.territory, self.territory)
        ty = self.home_y + random.randint(-self.territory, self.territory)
        tx = max(0, min(tx, WIDTH // CELL - 1))
        ty = max(0, min(ty, HEIGHT // CELL - 1))
        self.set_target_cell(tx, ty)

    def update(self, dt):
        if self.at_target():
            self.cooldown -= dt
            if self.cooldown <= 0:
                self.choose_target()
                self.cooldown = 0.4 + random.random() * 1.8
        super().update(dt)
        
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0

hero = Hero(3, 3)
buttons = {
    "start": Rect(300, 200, 200, 50),
    "music": Rect(300, 270, 200, 50),
    "exit": Rect(300, 340, 200, 50)
}

def generate_floor():
    global enemies
    enemies.clear()
    enemy_types = ["goblin"] + (["orc"] if current_floor > 2 else [])
    for _ in range(3 + current_floor):
        cell_x = random.randint(5, WIDTH // CELL - 5)
        cell_y = random.randint(5, HEIGHT // CELL - 5)
        enemies.append(Enemy(cell_x, cell_y, random.choice(enemy_types)))

def start_game():
    global game_state, current_floor, score, lives
    game_state = "play"
    current_floor = score = 0
    lives = 3
    next_floor()

def next_floor():
    global current_floor, game_state
    current_floor += 1
    if current_floor > FLOORS:
        game_state = "victory"
    else:
        generate_floor()
        game_state = "play"
        hero.health = min(hero.max_health, hero.health + 1)
        hero.set_target_cell(3, 3)
        set_music("play", "game")

def set_music(target, type):
    if music_enabled and target == 'play':
        music.play(f'{type}_music.wav')
        music.set_volume(0.6)
    elif target == 'stop':
        music.stop()

def toggle_music():
    global music_enabled
    music_enabled = not music_enabled
    set_music("play", "menu" if game_state == "menu" else "game")

def play_sfx(name):
    if sound_enabled:
        getattr(sounds, name).play()

def update(dt):
    global game_state, score, lives
    
    if game_state != "play": return
        
    hero.update(dt)
    for e in enemies[:]:
        e.update(dt)
        d = math.hypot(hero.x - e.x, hero.y - e.y)
        
        if d < CELL * 0.7 and not hero.invincible:
            if hero.is_attacking:
                if e.take_damage(hero.attack_power):
                    enemies.remove(e)
                    play_sfx("enemy_death")
                    score += 10 * current_floor
            else:
                hero.health -= e.stats["damage"]
                play_sfx("hit")
                if hero.health <= 0:
                    lives -= 1
                    if lives <= 0:
                        game_state = "game_over"
                    else:
                        hero.health = hero.max_health
                        hero.set_target_cell(3, 3)
                        hero.invincible = True
                        hero.invincible_timer = 3.0
                        hero.actor.opacity = 128
                        play_sfx("respawn")
    
    if not enemies:
        next_floor()
        play_sfx("level_up")

def draw_grid():
    for gx in range(0, WIDTH, CELL):
        screen.draw.line((gx, 0), (gx, HEIGHT), (40, 40, 40))
    for gy in range(0, HEIGHT, CELL):
        screen.draw.line((0, gy), (WIDTH, gy), (40, 40, 40))

def draw_menu():
    screen.fill((16, 20, 40))
    screen.draw.text("Friendly Happiness The Game", center=(WIDTH//2, 110), fontsize=56, color="red")
    for name, rect in buttons.items():
        screen.draw.filled_rect(rect, (90, 90, 140))
        screen.draw.rect(rect, "lightblue")
    screen.draw.text("Start Game", center=buttons["start"].center, fontsize=32)
    screen.draw.text(f"Music: {'ON' if music_enabled else 'OFF'}", center=buttons["music"].center, fontsize=24)
    screen.draw.text("Exit", center=buttons["exit"].center, fontsize=32)

def draw_play():
    screen.fill((30, 30, 50))
    draw_grid()
    for i in range(hero.max_health):
        screen.draw.filled_circle((20 + i * 30, 20), 10, "red" if i < hero.health else "darkred")
    for i in range(lives):
        screen.draw.filled_circle((WIDTH - 30 - i * 30, 20), 10, "yellow")
    for e in enemies: e.draw()
    hero.actor.opacity = 128 if hero.invincible else 255
    hero.draw()
    screen.draw.text(f"Floor: {current_floor}/{FLOORS}", (WIDTH-100, 35), color="white")
    screen.draw.text(f"Score: {score}", (WIDTH-100, 55), color="yellow")
    if hero.is_attacking: screen.draw.circle(hero.actor.pos, CELL, "red")
    if hero.invincible: screen.draw.text(f"Immune: {max(0, int(hero.invincible_timer))}s", (WIDTH//2-50, 20), color="cyan")

def draw_game_over():
    screen.fill("black")
    screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2-50), fontsize=72, color="red")
    screen.draw.text(f"Final Score: {score}", center=(WIDTH//2, HEIGHT//2+20), fontsize=36)
    screen.draw.text("Press SPACE to restart", center=(WIDTH//2, HEIGHT//2+70), fontsize=24)

def draw_victory():
    screen.fill("darkblue")
    screen.draw.text("VICTORY!", center=(WIDTH//2, HEIGHT//2-50), fontsize=72, color="gold")
    screen.draw.text(f"Final Score: {score}", center=(WIDTH//2, HEIGHT//2+20), fontsize=36)
    screen.draw.text("Press SPACE to restart", center=(WIDTH//2, HEIGHT//2+70), fontsize=24)

def draw():
    if game_state == "menu": draw_menu()
    elif game_state == "play": draw_play()
    elif game_state == "game_over": draw_game_over()
    elif game_state == "victory": draw_victory()

def on_key_down(key):
    global game_state
    if game_state == "play":
        if key == keys.SPACE: 
            if hero.start_attack(): play_sfx("sword")
        elif key == keys.LEFT: hero.move_dir(-1, 0)
        elif key == keys.RIGHT: hero.move_dir(1, 0)
        elif key == keys.UP: hero.move_dir(0, -1)
        elif key == keys.DOWN: hero.move_dir(0, 1)
        elif key == keys.ESCAPE: 
            game_state = "menu"
            set_music("stop", "")
    elif key == keys.SPACE and game_state in ("game_over", "victory"): start_game()

def on_mouse_down(pos):
    if game_state != "menu": return
    if buttons["start"].collidepoint(pos): start_game()
    elif buttons["music"].collidepoint(pos): 
        toggle_music()
        play_sfx("pickup")
    elif buttons["exit"].collidepoint(pos): quit()

set_music("play", "menu")
pgzrun.go()