import math
import random
from pygame import Rect

WIDTH = 800
HEIGHT = 600
CELL = 64  # Tamanho da célula para o movimento grid-based

music_enabled = True
sound_enabled = True
game_state = "menu"  # menu, play, game_over

class Entity:
    def __init__(self, cell_x, cell_y, idle_frames, walk_frames, speed=160):
        # Posição lógica (células) e visual (pixels)
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.x = cell_x * CELL + CELL // 2
        self.y = cell_y * CELL + CELL // 2
        self.idle_frames = idle_frames
        self.walk_frames = walk_frames
        self.speed = speed
        # Alvo em pixels
        self.target_x = self.x
        self.target_y = self.y
        # Animação
        self.frame_index = 0
        self.frame_timer = 0.0
        self.frame_interval = 0.12
        self.actor = Actor(self.idle_frames[0], (self.x, self.y))
        self.actor.anchor = ("center", "center")

    # Define célula alvo (clamp para não sair da tela)
    def set_target_cell(self, nx, ny):
        nx = max(0, min(nx, WIDTH // CELL - 1))
        ny = max(0, min(ny, HEIGHT // CELL - 1))
        self.cell_x = nx
        self.cell_y = ny
        self.target_x = nx * CELL + CELL // 2
        self.target_y = ny * CELL + CELL // 2

    # Chegou no alvo?
    def at_target(self):
        return abs(self.x - self.target_x) < 1 and abs(self.y - self.target_y) < 1

    # Movimento suave: avança proporcional a dt
    def update_move(self, dt):
        if not self.at_target():
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                step = min(self.speed * dt, dist)
                self.x += dx / dist * step
                self.y += dy / dist * step

    # Atualiza animação baseada no estado (idle/walk)
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
        # Animação de idle (2 frames)
        idle = [f"hero_idle_{i}" for i in (1, 2)]
        # Animação de walk (4 frames)
        walk = [f"hero_walk_{i}" for i in (1, 2, 3, 4)]
        super().__init__(cell_x, cell_y, idle, walk, speed=220)

    # Move apenas quando chegar no destino
    def move_dir(self, dx, dy):
        if self.at_target():
            nx = self.cell_x + dx
            ny = self.cell_y + dy
            self.set_target_cell(nx, ny)

class Enemy(Entity):
    def __init__(self, cell_x, cell_y, territory=2):
        # Animação de parado
        idle = [f"enemy_idle_{i}" for i in (1, 2)]
        # Animação de walk
        walk = [f"enemy_walk_{i}" for i in (1, 2, 3, 4)]
        super().__init__(cell_x, cell_y, idle, walk, speed=120)
        self.home_x = cell_x
        self.home_y = cell_y
        self.territory = territory  # Raio de movimento
        self.cooldown = random.uniform(0.2, 1.2)  # Tempo entre movimentos

    # Escolhe célula aleatória dentro do território
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