import random
import sys

import pygame

pygame.init()

# Configurações da tela
WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong - 2 Jogadores")

clock = pygame.time.Clock()

# Cores
BLACK = (15, 15, 20)
WHITE = (240, 240, 240)
GRAY = (80, 80, 90)

# Fontes
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)

# Configurações dos jogadores
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 110
PADDLE_SPEED = 7

player1 = pygame.Rect(40, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

player2 = pygame.Rect(
    WIDTH - 55, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT
)

# Bola
BALL_SIZE = 16
ball = pygame.Rect(
    WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE
)

ball_speed = 5
ball_dx = random.choice([-1, 1])
ball_dy = random.choice([-1, 1])

# Placar
score1 = 0
score2 = 0
MAX_SCORE = 10


def reset_ball():
    global ball_speed, ball_dx, ball_dy

    ball.center = (WIDTH // 2, HEIGHT // 2)

    ball_speed = 5
    ball_dx = random.choice([-1, 1])
    ball_dy = random.uniform(-0.7, 0.7)

    if abs(ball_dy) < 0.2:
        ball_dy = 0.3


def move_ball():
    global ball_speed, ball_dx, ball_dy
    global score1, score2

    ball.x += int(ball_dx * ball_speed)
    ball.y += int(ball_dy * ball_speed)

    # Colisão com as paredes superior e inferior
    if ball.top <= 0:
        ball.top = 0
        ball_dy = abs(ball_dy)

    if ball.bottom >= HEIGHT:
        ball.bottom = HEIGHT
        ball_dy = -abs(ball_dy)

    # Colisão com o jogador 1
    if ball.colliderect(player1) and ball_dx < 0:
        ball.left = player1.right

        ball_dx = abs(ball_dx)

        impacto = (ball.centery - player1.centery) / (PADDLE_HEIGHT / 2)
        ball_dy += impacto * 0.35

        ball_speed *= 1.10

    # Colisão com o jogador 2
    if ball.colliderect(player2) and ball_dx > 0:
        ball.right = player2.left

        ball_dx = -abs(ball_dx)

        impacto = (ball.centery - player2.centery) / (PADDLE_HEIGHT / 2)
        ball_dy += impacto * 0.35

        ball_speed *= 1.10

    # Limita a velocidade vertical para manter o jogo controlável
    ball_dy = max(-1.5, min(1.5, ball_dy))

    # Pontuação
    if ball.right < 0:
        score2 += 1
        reset_ball()

    if ball.left > WIDTH:
        score1 += 1
        reset_ball()


def draw():
    screen.fill(BLACK)

    # Linha central
    for y in range(0, HEIGHT, 30):
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 2, y, 4, 15))

    # Jogadores
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)

    # Bola
    pygame.draw.ellipse(screen, WHITE, ball)

    # Placar
    text1 = font.render(str(score1), True, WHITE)
    text2 = font.render(str(score2), True, WHITE)

    screen.blit(text1, (WIDTH // 4, 30))
    screen.blit(text2, (WIDTH * 3 // 4, 30))

    # Identificação dos controles
    controls1 = small_font.render("W/A - S/D", True, GRAY)
    controls2 = small_font.render("SETAS", True, GRAY)

    screen.blit(controls1, (25, HEIGHT - 35))
    screen.blit(controls2, (WIDTH - 110, HEIGHT - 35))

    pygame.display.flip()


# Loop principal
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Jogador 1: WASD
    if keys[pygame.K_w] or keys[pygame.K_a]:
        player1.y -= PADDLE_SPEED

    if keys[pygame.K_s] or keys[pygame.K_d]:
        player1.y += PADDLE_SPEED

    # Jogador 2: Setas
    if keys[pygame.K_UP]:
        player2.y -= PADDLE_SPEED

    if keys[pygame.K_DOWN]:
        player2.y += PADDLE_SPEED

    # Impede as barras de saírem da tela
    player1.clamp_ip(screen.get_rect())
    player2.clamp_ip(screen.get_rect())

    move_ball()

    # Verifica vitória
    if score1 >= MAX_SCORE or score2 >= MAX_SCORE:
        winner = "Jogador 1" if score1 >= MAX_SCORE else "Jogador 2"

        screen.fill(BLACK)

        victory = font.render(f"{winner} venceu!", True, WHITE)

        restart = small_font.render(
            "Pressione R para jogar novamente ou ESC para sair", True, WHITE
        )

        screen.blit(victory, victory.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))

        screen.blit(restart, restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

        pygame.display.flip()

        waiting = True

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        score1 = 0
                        score2 = 0
                        player1.centery = HEIGHT // 2
                        player2.centery = HEIGHT // 2
                        reset_ball()
                        waiting = False

                    if event.key == pygame.K_ESCAPE:
                        running = False
                        waiting = False

            clock.tick(60)

        continue

    draw()

pygame.quit()
sys.exit()
