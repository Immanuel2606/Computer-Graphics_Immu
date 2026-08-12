import sys
import pygame

# 1. Initialize Pygame
pygame.init()

# 2. Set up the display window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_set_mode if hasattr(
    pygame.display, "set_set_mode"
) else pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw Shapes with Pygame")

# 3. Define Colors (RGB format)
BG_COLOR = (240, 240, 240)  # Light Gray
RECT_COLOR = (70, 130, 180)  # Steel Blue
CIRCLE_COLOR = (220, 20, 60)  # Crimson Red

# 4. Main Game Loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background screen
    screen.fill(BG_COLOR)

    # --- Draw Shapes ---

    # Draw and fill a Rectangle: (screen, color, (x, y, width, height))
    pygame.draw.rect(screen, RECT_COLOR, (150, 200, 200, 150))

    # Draw and fill a Circle: (screen, color, (center_x, center_y), radius)
    pygame.draw.circle(screen, CIRCLE_COLOR, (550, 275), 80)

    # Update the display
    pygame.display.flip()

# 5. Quit Pygame safely
pygame.quit()
sys.exit()