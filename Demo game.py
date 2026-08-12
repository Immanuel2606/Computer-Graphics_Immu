import sys
import random
import pygame

# Initialize Pygame
pygame.init()

# Display settings
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Star")
clock = pygame.time.Clock()

# Colors
BACKGROUND = (20, 24, 40)
PADDLE_COLOR = (70, 130, 240)
STAR_COLOR = (255, 215, 0)
WHITE = (255, 255, 255)

# Game Variables
score = 0
font = pygame.font.SysFont("Arial", 28, bold=True)

# Player Paddle (x, y, width, height)
paddle = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 40, 100, 15)
paddle_speed = 8

# Falling Star
star_radius = 12
star_x = random.randint(star_radius, WIDTH - star_radius)
star_y = 0
star_speed = 5

# Main Loop
running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Movement Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # 3. Update Game Logic
    star_y += star_speed

    # Check collision between star and paddle
    star_rect = pygame.Rect(
        star_x - star_radius, star_y - star_radius, star_radius * 2, star_radius * 2
    )
    if paddle.colliderect(star_rect):
        score += 1
        star_y = 0
        star_x = random.randint(star_radius, WIDTH - star_radius)
        star_speed += 0.3  # Gradually increase speed

    # Reset star if it falls past the bottom
    if star_y > HEIGHT:
        star_y = 0
        star_x = random.randint(star_radius, WIDTH - star_radius)

    # 4. Drawing
    screen.fill(BACKGROUND)

    # Draw Paddle and Star
    pygame.draw.rect(screen, PADDLE_COLOR, paddle, border_radius=5)
    pygame.draw.circle(screen, STAR_COLOR, (star_x, star_y), star_radius)

    # Render Score UI
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()