import pygame

def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
    WHITE, RED, GREEN, BLUE, BLACK = (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)

    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    layer.fill(WHITE)

    color = BLACK
    clock = pygame.time.Clock()
    
    X, Y, cur_X, cur_Y = -1, -1, -1, -1
    isMouseDown = False
    tool = 'line'
    points = []

    running = True
    while running:
        SCREEN.fill(WHITE)
        SCREEN.blit(layer, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            #colors
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    color = RED
                elif event.key == pygame.K_g:
                    color = GREEN
                elif event.key == pygame.K_b:
                    color = BLUE 
                elif event.key == pygame.K_SPACE:
                    color = BLACK
                #tools
                if event.key == pygame.K_1:
                    tool = 'line'
                elif event.key == pygame.K_2:
                    tool = 'rectangle'
                elif event.key == pygame.K_3:
                    tool = 'circle'
                elif event.key == pygame.K_4:
                    tool = 'eraser'
                elif event.key == pygame.K_5:
                    tool = 'square'
                elif event.key == pygame.K_6:
                    tool = 'right_triangle'
                elif event.key == pygame.K_7:
                    tool = 'equilateral_triangle'
                elif event.key == pygame.K_8:
                    tool = 'rhombus'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                isMouseDown = True
                X, Y = event.pos
                cur_X, cur_Y = event.pos
                if tool == 'line':
                    points.append((X, Y))

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                isMouseDown = False
                if tool == 'rectangle':
                    r = calculateRect(X, Y, cur_X, cur_Y)
                    pygame.draw.rect(layer, color, r, 2)
                elif tool == 'circle':
                    radius = int(((cur_X - X) ** 2 + (cur_Y - Y) ** 2) ** 0.5)
                    pygame.draw.circle(layer, color, (X, Y), radius, 2)
                elif tool == 'line':
                    points.clear()
                elif tool == 'square':
                    size = max(abs(cur_X - X), abs(cur_Y - Y))
                    pygame.draw.rect(layer, color, (X, Y, size, size), 2)
                elif tool == 'right_triangle':
                    pygame.draw.polygon(layer, color, [(X, Y), (cur_X, Y), (X, cur_Y)], 2)
                elif tool == 'equilateral_triangle':
                    height = abs(cur_Y - Y)
                    base = height * (3 ** 0.5)
                    pygame.draw.polygon(layer, color, [(X, cur_Y), (X + base / 2, Y), (X - base / 2, Y)], 2)
                elif tool == 'rhombus':
                    width = abs(cur_X - X)
                    height = abs(cur_Y - Y)
                    pygame.draw.polygon(layer, color, [(X, Y - height // 2), (X + width // 2, Y), (X, Y + height // 2), (X - width // 2, Y)], 2)                    
            if event.type == pygame.MOUSEMOTION:
                cur_X, cur_Y = event.pos
                if isMouseDown:
                    if tool == 'line':
                        points.append((cur_X, cur_Y))
                        points = points[-256:]
                    elif tool == 'eraser':
                        pygame.draw.circle(layer, WHITE, (cur_X, cur_Y), 10)

        if tool == 'line' and len(points) > 1:
            for i in range(len(points) - 1):
                drawLineBetween(layer, i, points[i], points[i + 1], 5, color)

        if isMouseDown and tool == 'rectangle':
            r = calculateRect(X, Y, cur_X, cur_Y)
            temp_layer = layer.copy()
            pygame.draw.rect(temp_layer, color, r, 2)
            SCREEN.blit(temp_layer, (0, 0))

        if isMouseDown and tool == 'circle':
            radius = int(((cur_X - X) ** 2 + (cur_Y - Y)**2) ** 0.5)
            temp_layer = layer.copy()
            pygame.draw.circle(temp_layer, color, (X, Y), radius, 2)
            SCREEN.blit(temp_layer, (0, 0))

        pygame.display.flip()
        clock.tick(60)
# draws a line between points for smooth freehand drawing
def drawLineBetween(surface, i, start, end, width, color):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress = i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(surface, color, (x, y), width)
# calculate rectangle dimensions based on two points
def calculateRect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

main()