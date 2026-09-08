import pygame
import sys

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flowchart - Addition of Two Numbers")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 180, 255)
GREEN = (100, 220, 120)
YELLOW = (255, 220, 100)
RED = (255, 120, 120)

# Font
font = pygame.font.Font(None, 32)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # START - Oval
    pygame.draw.ellipse(screen, GREEN, (300, 30, 200, 60))
    pygame.draw.ellipse(screen, BLACK, (300, 30, 200, 60), 3)

    text = font.render("START", True, BLACK)
    screen.blit(text, (365, 48))

    # Arrow 1
    pygame.draw.line(screen, BLACK, (400, 90), (400, 130), 3)
    pygame.draw.polygon(screen, BLACK, [(400, 140), (390, 125), (410, 125)])

    # INPUT - Parallelogram
    input_points = [
        (250, 140),
        (550, 140),
        (520, 210),
        (220, 210)
    ]

    pygame.draw.polygon(screen, BLUE, input_points)
    pygame.draw.polygon(screen, BLACK, input_points, 3)

    text = font.render("Input A and B", True, BLACK)
    screen.blit(text, (300, 165))

    # Arrow 2
    pygame.draw.line(screen, BLACK, (400, 210), (400, 250), 3)
    pygame.draw.polygon(screen, BLACK, [(400, 260), (390, 245), (410, 245)])

    # PROCESS - Rectangle
    pygame.draw.rect(screen, YELLOW, (250, 260, 300, 70))
    pygame.draw.rect(screen, BLACK, (250, 260, 300, 70), 3)

    text = font.render("Sum = A + B", True, BLACK)
    screen.blit(text, (320, 283))

    # Arrow 3
    pygame.draw.line(screen, BLACK, (400, 330), (400, 370), 3)
    pygame.draw.polygon(screen, BLACK, [(400, 380), (390, 365), (410, 365)])

    # OUTPUT - Parallelogram
    output_points = [
        (250, 380),
        (550, 380),
        (520, 450),
        (220, 450)
    ]

    pygame.draw.polygon(screen, RED, output_points)
    pygame.draw.polygon(screen, BLACK, output_points, 3)

    text = font.render("Display Sum", True, BLACK)
    screen.blit(text, (320, 405))

    # Arrow 4
    pygame.draw.line(screen, BLACK, (400, 450), (400, 490), 3)
    pygame.draw.polygon(screen, BLACK, [(400, 500), (390, 485), (410, 485)])

    # END - Oval
    pygame.draw.ellipse(screen, GREEN, (300, 500, 200, 60))
    pygame.draw.ellipse(screen, BLACK, (300, 500, 200, 60), 3)

    text = font.render("END", True, BLACK)
    screen.blit(text, (370, 518))

    pygame.display.flip()

pygame.quit()
sys.exit()