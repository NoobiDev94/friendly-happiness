# Friendly Happiness The Game - Manual do Jogo

## Visão Geral
Friendly Happiness é um jogo roguelike onde você explora masmorras, derrota monstros e avança por 5 andares desafiadores. O objetivo é sobreviver a todos os andares e derrotar todos os inimigos!

## Comandos
- **Setas (↑ ↓ ← →)**: Movimentar o herói
- **Barra de ESPAÇO**: Atacar monstros próximos
- **ESC**: Voltar ao menu durante o jogo
- **SPACE no menu**: Iniciar novo jogo
- **Clique do Mouse**: Selecionar opções no menu

## Interface do Jogo

### Durante a Jogatória:
```
[● ● ●]               [● ● ●]         Floor: 1/5
[Vida ]               [Vidas]         Score: 150
```

1. **Corações Vermelhos (Esquerda Superior)**:
   - Representam sua vida atual
   - Cada coração cheio = 1 ponto de vida
   - Corações escuros = vida perdida

2. **Círculos Amarelos (Direita Superior)**:
   - Representam suas vidas restantes
   - Você começa com 3 vidas
   - Ao morrer, perde uma vida e renasce

3. **Informações de Andar e Pontuação**:
   - `Floor: X/5`: Andar atual / total
   - `Score: Y`: Pontuação acumulada

4. **Indicador de Imunidade**:
   - Aparece após renascer: `Immune: Xs`
   - Você fica invencível por 3 segundos após morrer
   - Herói fica semi-transparente durante este período

## Monstros

### Goblin
- **Aparição**: Andares 1-5
- **Características**:
  - Vida: 2 pontos
  - Dano: 1 ponto
  - Velocidade: Média
- **Pontuação**: 10 × andar atual

### Orc
- **Aparição**: Andares 3-5
- **Características**:
  - Vida: 4 pontos
  - Dano: 2 pontos
  - Velocidade: Lenta
- **Pontuação**: 20 × andar atual

## Sistema de Andares

| Andar | Dificuldade | Inimigos               | Recompensa ao Avançar |
|-------|-------------|------------------------|-----------------------|
| 1     | Fácil       | Apenas Goblins         | +1 vida              |
| 2     | Moderada    | Apenas Goblins         | +1 vida              |
| 3     | Difícil     | Goblins e Orcs         | +1 vida              |
| 4     | Desafiador  | Mais Orcs              | +1 vida              |
| 5     | Extremo     | Muitos Orcs e Goblins  | Vitória!             |

## Estratégias
1. Mantenha distância dos inimigos quando estiver com pouca vida
2. Ataque quando estiver bem próximo dos monstros
3. Use os 3 segundos de imunidade após renascer para se reposicionar
4. Priorize derrotar Orcs primeiro (dão mais pontos mas são mais perigosos)
5. Avance de andar assim que possível para recuperar vida

## Telas Especiais

### Vitória
- Aparece ao completar o 5º andar
- Mostra sua pontuação final
- Pressione SPACE para jogar novamente

### Game Over
- Aparece quando suas vidas acabam
- Mostra sua pontuação final
- Pressione SPACE para tentar novamente
