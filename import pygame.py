import pygame

pygame.init()
screen = pygame.display.set_mode((900, 650))
pygame.display.set_caption("Reflection and Shearing Transformations")
font = pygame.font.SysFont("consolas", 20, bold=True)
small_font = pygame.font.SysFont("consolas", 15)

TOP = (12, 20, 40)
BOTTOM = (50, 10, 45)
CYAN = (0, 255, 220)
CORAL = (255, 90, 120)
LIME = (150, 255, 90)
WHITE = (240, 240, 250)


def draw_gradient_bg(surface, top_color, bottom_color):
    h = surface.get_height()
    for y in range(h):
        t = y / h
        color = tuple(int(top_color[i] + (bottom_color[i] - top_color[i]) * t) for i in range(3))
        pygame.draw.line(surface, color, (0, y), (surface.get_width(), y))


def fill_polygon_alpha(surface, points, color, alpha):
    alpha_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.polygon(alpha_surface, (*color, alpha), points)
    surface.blit(alpha_surface, (0, 0))


def draw_dashed_line(surface, color, start, end, width=1, dash=8, gap=6):
    x1, y1 = start
    x2, y2 = end
    total = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    if total == 0:
        return
    dx, dy = (x2 - x1) / total, (y2 - y1) / total
    dist = 0
    draw_seg = True
    while dist < total:
        seg_len = dash if draw_seg else gap
        seg_end = min(dist + seg_len, total)
        if draw_seg:
            pygame.draw.line(surface, color,
                              (x1 + dx * dist, y1 + dy * dist),
                              (x1 + dx * seg_end, y1 + dy * seg_end), width)
        dist = seg_end
        draw_seg = not draw_seg


triangle = [(200, 200), (300, 200), (250, 100)]


def transform(points, matrix):
    result = []
    for x, y in points:
        nx = matrix[0][0] * x + matrix[0][1] * y
        ny = matrix[1][0] * x + matrix[1][1] * y
        result.append((round(nx), round(ny)))
    return result


reflection_x = [[1, 0, 0], [0, -1, 0], [0, 0, 1]]

shx = 0.5
shear_x = [[1, shx, 0], [0, 1, 0], [0, 0, 1]]

reflected = transform(triangle, reflection_x)
sheared = transform(triangle, shear_x)

reflected = [(x, 500 - y) for x, y in reflected]

running = True
while running:
    draw_gradient_bg(screen, TOP, BOTTOM)

    title = font.render("Reflection and Shearing", True, CYAN)
    screen.blit(title, (20, 15))

    draw_dashed_line(screen, (150, 150, 170), (0, 400), (900, 400))

    fill_polygon_alpha(screen, triangle, WHITE, 60)
    pygame.draw.polygon(screen, WHITE, triangle, 3)

    fill_polygon_alpha(screen, reflected, CORAL, 60)
    pygame.draw.polygon(screen, CORAL, reflected, 3)

    fill_polygon_alpha(screen, sheared, LIME, 60)
    pygame.draw.polygon(screen, LIME, sheared, 3)

    legend = [("Original", WHITE), ("Reflected (X-axis)", CORAL), ("Sheared", LIME)]
    ly = 55
    for label, color in legend:
        pygame.draw.circle(screen, color, (30, ly), 6)
        screen.blit(small_font.render(label, True, color), (45, ly - 9))
        ly += 25

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()