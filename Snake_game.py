# TASK - 2  SNAKE GAME
import pygame , random , os

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 25

# Colors
COLORS = {
    "background": (64, 224, 208),
    "snake": (34, 139, 34),
    "food": (0, 225, 0),
    "text": (54, 69, 79),
    "gradient1": (0, 191, 255),
    "gradient2": (0, 255, 255),}

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 20)
menu_font = pygame.font.SysFont("comicsansms", 25)

def display_message(msg, color, y_offset=0):
    message = menu_font.render(msg, True, color)
    screen.blit(message, [(WIDTH - message.get_width()) // 2, (HEIGHT // 2) + y_offset])

# Food types
food_types = [
    {"name": "Apple", "color": (255, 59, 48), "shape": "circle"},
    {"name": "Carrot", "color": (237, 145, 33), "shape": "ellipse"},
    {"name": "Cheese", "color": (255, 223, 0), "shape": "triangle"},
    {"name": "Cookie", "color": (210, 180, 140), "shape": "rectangle"},
]
current_food_type = random.choice(food_types)

def draw_food(screen, food_type, x, y):
    if food_type["shape"] == "circle":
        pygame.draw.circle(screen, food_type["color"], (x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
    elif food_type["shape"] == "ellipse":
        pygame.draw.ellipse(screen, food_type["color"], (x, y + BLOCK_SIZE // 3 , BLOCK_SIZE, BLOCK_SIZE // 1.25 ))
    elif food_type["shape"] == "triangle":
        points = [
            (x + BLOCK_SIZE // 2, y),                    
            (x, y + BLOCK_SIZE),                       
            (x + BLOCK_SIZE, y + BLOCK_SIZE),          
        ]
        pygame.draw.polygon(screen, food_type["color"], points)
    elif food_type["shape"] == "rectangle":
        pygame.draw.rect(screen, food_type["color"], (x, y, BLOCK_SIZE , BLOCK_SIZE )) 
        
# For collision (or Obstacles)
def draw_screen_border(screen):
    border_thickness = 4  
    border_color = (0, 100, 0)  

    # Top border
    pygame.draw.rect(screen, border_color, [0, 0, WIDTH, border_thickness])
    # Bottom border
    pygame.draw.rect(screen, border_color, [0, HEIGHT - border_thickness, WIDTH, border_thickness])
    # Left border
    pygame.draw.rect(screen, border_color, [0, 0, border_thickness, HEIGHT])
    # Right border
    pygame.draw.rect(screen, border_color, [WIDTH - border_thickness, 0, border_thickness, HEIGHT])

obstacles = [
    (random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE), random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE))
    for _ in range(9)
]

def draw_obstacles(screen, obstacles):
    for obs_x, obs_y in obstacles:
        pygame.draw.rect(screen, (75, 0, 130), [obs_x, obs_y, BLOCK_SIZE, BLOCK_SIZE]) 
        
def check_for_collision(x,y):
    return (x < border_thickness or x >= WIDTH  -  border_thickness or y <  border_thickness or y >= HEIGHT -  border_thickness )
        
# For high_score
HIGH_SCORE_FILE = "highscore.txt"
def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

# Bg_selection Menu
def background_menu():
    selected_option = 0
    options = ["Thematic", "Gradient"]

    while True:
        screen.fill(COLORS["background"])
        display_message(" SELECT BACKGROUND :", COLORS["text"], -50)
        for i, option in enumerate(options):
            color = COLORS["snake"] if i == selected_option else COLORS["text"]
            display_message(option, color, i * 50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected_option].lower()
        pygame.display.update()

def draw_gradient_background(screen, color1, color2):
    for y in range(HEIGHT):
        r = color1[0] + (color2[0] - color1[0]) * y // HEIGHT
        g = color1[1] + (color2[1] - color1[1]) * y // HEIGHT
        b = color1[2] + (color2[2] - color1[2]) * y // HEIGHT
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def draw_thematic_background(screen):  
    screen.fill((10, 10, 50))
    
    for _ in range(100):  
        star_x = random.randint(0, WIDTH)
        star_y = random.randint(0, HEIGHT)
        star_size = random.randint(1, 3)  
        pygame.draw.circle(screen, (255, 255, 255), (star_x, star_y), star_size)

    # Add a moon 
    moon_x, moon_y = WIDTH - 100, 100  
    moon_radius = 40
    pygame.draw.circle(screen, (255, 255, 150), (moon_x, moon_y), moon_radius)

# For snake block
def draw_snake(screen, snake_list, direction):
    segment_colors = [(34, 139, 34), (0, 255, 0)]  
    # For body
    for index, segment in enumerate(snake_list[:-1]):
        color = segment_colors[index % 2]  
        center_x = segment[0] + BLOCK_SIZE // 2
        center_y = segment[1] + BLOCK_SIZE // 2
        pygame.draw.circle(screen, color, (center_x, center_y), BLOCK_SIZE // 2)

    # For drawing head_with_face block
    head_x, head_y = snake_list[-1]
    head_center_x = head_x + BLOCK_SIZE // 2
    head_center_y = head_y + BLOCK_SIZE // 2
    pygame.draw.circle(screen, COLORS["snake"], (head_center_x, head_center_y), BLOCK_SIZE // 2)

    # Add_eyes 
    eye_color = (20, 20, 20)
    eye_size = BLOCK_SIZE // 7
    eye_offset = BLOCK_SIZE // 4
    if direction == "UP":
        pygame.draw.circle(screen, eye_color, (head_center_x - eye_offset, head_center_y - eye_offset), eye_size)
        pygame.draw.circle(screen, eye_color, (head_center_x + eye_offset, head_center_y - eye_offset), eye_size)
    elif direction == "DOWN":
        pygame.draw.circle(screen, eye_color, (head_center_x - eye_offset, head_center_y + eye_offset), eye_size)
        pygame.draw.circle(screen, eye_color, (head_center_x + eye_offset, head_center_y + eye_offset), eye_size)
    elif direction == "LEFT":
        pygame.draw.circle(screen, eye_color, (head_center_x - eye_offset, head_center_y - eye_offset), eye_size)
        pygame.draw.circle(screen, eye_color, (head_center_x - eye_offset, head_center_y + eye_offset), eye_size)
    elif direction == "RIGHT":
        pygame.draw.circle(screen, eye_color, (head_center_x + eye_offset, head_center_y - eye_offset), eye_size)
        pygame.draw.circle(screen, eye_color, (head_center_x + eye_offset, head_center_y + eye_offset), eye_size)

# Main Game Loop
def game_loop(background_type):
    global current_food_type
    high_score = load_high_score()
    score = 0
    snake_speed = 7

    x, y = WIDTH // 2, HEIGHT // 2
    snake_list = [[x, y]]
    snake_length = 1
    direction = "STOP"

    food_x = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
    food_y = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)

    game_over = False
    motivational_message_timer = 0
    warning_message_timer = 0

    while not game_over:
        if background_type == "gradient":
            draw_gradient_background(screen, COLORS["gradient1"], COLORS["gradient2"])
        elif background_type == "thematic":
            draw_thematic_background(screen)
        else:
            screen.fill(COLORS["background"])

        draw_screen_border(screen)
        draw_obstacles(screen, obstacles)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"

        if direction != "STOP":
            if direction == "LEFT":
                x -= BLOCK_SIZE
            elif direction == "RIGHT":
                x += BLOCK_SIZE
            elif direction == "UP":
                y -= BLOCK_SIZE
            elif direction == "DOWN":
                y += BLOCK_SIZE

            if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or [x, y] in snake_list:
                game_over = True
            if (x, y) in obstacles:
                game_over = True

            snake_list.append([x, y])
            if len(snake_list) > snake_length:
                del snake_list[0]

            if x == food_x and y == food_y:
                score += 1
                snake_length += 1
                food_x = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
                food_y = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
                current_food_type = random.choice(food_types)

                if score % 5 == 0:
                    motivational_message_timer = 10

        for obs_x, obs_y in obstacles:
            if abs(x - obs_x) < BLOCK_SIZE * 2 and abs(y - obs_y) < BLOCK_SIZE * 2:
                warning_message_timer = 20
                
        draw_food(screen, current_food_type, food_x, food_y, )
        draw_snake(screen, snake_list, direction)

        if motivational_message_timer > 0:
            display_message("Great job! Keep going!", (0, 100, 0))
            motivational_message_timer -= 1

        if warning_message_timer > 0:
            display_message("Watch out for obstacles!", (255, 0, 0), 40)
            warning_message_timer -= 1

        score_text = font_style.render(f"Score: {score}", True, COLORS["text"])
        screen.blit(score_text, [10, 10])

        pygame.display.update()
        pygame.time.Clock().tick(snake_speed)

    pygame.quit()

# Start Game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" FOOD MANIA SNAKE GAME ")
selected_background = background_menu()
game_loop(selected_background)
