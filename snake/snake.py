import pygame
import random

pygame.init()

width = 800
height = 600 

screen = pygame.display.set_mode((width, height))

#variables and their initialization
score = 0
fruit_eaten = False 
level = 1  # level
speed = 200  # initial speed
food_timer = 0  # timer for food disappearance

head_square = [100, 100] 

squares = [[30, 100], [40, 100], [50, 100], [60, 100], 
           [70, 100], [80, 100], [90, 100], [100, 100]]

# food types with different weights (points)
food_types = [
    {"color": (0, 255, 0), "points": 10, "lifetime": 15000},  # green food
    {"color": (255, 0, 0), "points": 15, "lifetime": 15000},  # red food
    {"color": (0, 0, 255), "points": 20, "lifetime": 15000}   # blue food
]

# generate random position and type for food
def generate_food():
    while True:
        fr_x = random.randrange(0, width // 10) * 10
        fr_y = random.randrange(0, height // 10) * 10
        if [fr_x, fr_y] not in squares:
            return {"position": [fr_x, fr_y], "type": random.choice(food_types), "spawn_time": pygame.time.get_ticks()}

fruit = generate_food()

direction = "right"
next_dir = "right"

done = False

def game_over():
    global done
    done = True
    font = pygame.font.SysFont("times new roman", 45)
    text_surface = font.render(f"Game Over! Score: {score}, Level: {level}", True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.delay(4000)
    pygame.quit()
    exit()

# start of gameplay loop
while not done:
    # gameplay event conditions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                next_dir = "down"
            if event.key == pygame.K_UP:
                next_dir = "up"
            if event.key == pygame.K_LEFT:
                next_dir = "left"
            if event.key == pygame.K_RIGHT:
                next_dir = "right"

    # scene logic
    if next_dir == "right" and direction != "left":
        direction = "right"
    if next_dir == "up" and direction != "down":
        direction = "up"
    if next_dir == "left" and direction != "right":
        direction = "left"
    if next_dir == "down" and direction != "up":
        direction = "down"

    # move the snake
    if direction == "right":
        head_square[0] += 10
    if direction == "left":
        head_square[0] -= 10
    if direction == "up":
        head_square[1] -= 10
    if direction == "down":
        head_square[1] += 10

    # checking for border (wall) collision
    if head_square[0] < 0 or head_square[0] >= width or head_square[1] < 0 or head_square[1] >= height:
        game_over()

    # move the snake's body
    new_square = [head_square[0], head_square[1]]
    squares.append(new_square)
    squares.pop(0)

    # check if the snake eats the food
    if head_square == fruit["position"]:
        fruit_eaten = True
        score += fruit["type"]["points"]
        squares.insert(0, squares[0])  # grow the snake
        
        # increase level every 30 points
        if score % 30 == 0:
            level += 1
            speed = max(50, speed - 20)
            pygame.time.delay(speed)

    # generate new food if eaten or if it disappears after time
    if fruit_eaten or pygame.time.get_ticks() - fruit["spawn_time"] > fruit["type"]["lifetime"]:
        fruit = generate_food()
        fruit_eaten = False

    # drawing section
    screen.fill((0, 0, 0))

    # display score and level
    score_font = pygame.font.SysFont("times new roman", 20)
    score_surface = score_font.render(f"Score: {score} | Level: {level}", True, (128, 128, 128))
    score_rect = score_surface.get_rect()
    screen.blit(score_surface, score_rect)

    # draw food
    pygame.draw.circle(screen, fruit["type"]["color"], (fruit["position"][0] + 5, fruit["position"][1] + 5), 5)

    # draw snake
    for el in squares:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(el[0], el[1], 10, 10))

    pygame.display.flip()
    pygame.time.delay(speed)

pygame.quit()