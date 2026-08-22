import pygame
import math

pygame.init()

# Window
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle with Two Blue Stripes")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)

clock = pygame.time.Clock()

# Circle settings
cx, cy = WIDTH // 2, HEIGHT // 2
radius = 135

# Stripe settings
stripe_width = 42
stripe_length = 330

# Angle of the stripes
angle = math.radians(-13)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # White background
    screen.fill(WHITE)

    # Black circle
    pygame.draw.circle(
        screen,
        BLACK,
        (cx, cy),
        radius
    )

    # Stripe surface
    stripe_surface = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    def stripe_on_surface(y_offset):

        # Direction along the stripe
        dx = math.cos(angle)
        dy = math.sin(angle)

        # Perpendicular direction
        px = -dy
        py = dx

        # Stripe center
        sx = cx
        sy = cy + y_offset

        # Half dimensions
        half_length = stripe_length / 2
        half_width = stripe_width / 2

        # Four corners
        points = [
            (
                sx - dx * half_length - px * half_width,
                sy - dy * half_length - py * half_width
            ),
            (
                sx + dx * half_length - px * half_width,
                sy + dy * half_length - py * half_width
            ),
            (
                sx + dx * half_length + px * half_width,
                sy + dy * half_length + py * half_width
            ),
            (
                sx - dx * half_length + px * half_width,
                sy - dy * half_length + py * half_width
            )
        ]

        # Blue stripe
        pygame.draw.polygon(
            stripe_surface,
            (0, 100, 255, 255),
            points
        )

    # Two blue stripes
    # Distance between centers = 120 pixels
    stripe_on_surface(-60)
    stripe_on_surface(60)

    # Circle mask
    circle_mask = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    pygame.draw.circle(
        circle_mask,
        (255, 255, 255, 255),
        (cx, cy),
        radius
    )

    # Keep stripes inside the circle
    stripe_surface.blit(
        circle_mask,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_MULT
    )

    # Draw stripes
    screen.blit(
        stripe_surface,
        (0, 0)
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()