import pygame
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions and Settings
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
INITIAL_FPS = 6  # Starting FPS (slower snake speed)
MAX_FPS = 12  # Maximum FPS (faster snake speed)
SPEED_INCREMENT = 5  # FPS increment step
SCORE_THRESHOLD = 50  # Score threshold for speed increase

# Colors
BLACK = (0, 0, 0)
NEON_GREEN = (57, 255, 20)
NEON_PINK = (255, 20, 147)
NEON_BLUE = (0, 191, 255)
WHITE = (255, 255, 255)

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont('Arial', 24)
game_over_font = pygame.font.SysFont('Arial', 36)

# Functions
def spawn_food():
    """Spawn food at a random position on the grid, avoiding the snake's body."""
    while True:
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        if (x, y) not in snake:  # Ensure food doesn't spawn on snake's body
            return (x, y)

def show_text(text, font, color, position):
    """Display text on the screen."""
    render = font.render(text, True, color)
    screen.blit(render, position)

def game_over_screen(score):
    """Display the Game Over screen."""
    screen.fill(BLACK)
    show_text("GAME OVER", game_over_font, NEON_PINK, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    show_text(f"Final Score: {score}", font, NEON_BLUE, (WIDTH // 2 - 100, HEIGHT // 2))
    show_text("Press 'C' to Play Again or 'Q' to Quit", font, WHITE, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
    pygame.display.flip()

def reset_game():
    """Reset the game state to start a new game."""
    global snake, direction, food, score, current_fps
    snake = [(WIDTH // 2, HEIGHT // 2)]  # Starting position
    direction = (0, -BLOCK_SIZE)  # Starting direction (Up)
    food = spawn_food()
    score = 0
    current_fps = INITIAL_FPS  # Start with initial speed

# Initialize Game State
reset_game()

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, BLOCK_SIZE):
                direction = (0, -BLOCK_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -BLOCK_SIZE):
                direction = (0, BLOCK_SIZE)
            elif event.key == pygame.K_LEFT and direction != (BLOCK_SIZE, 0):
                direction = (-BLOCK_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-BLOCK_SIZE, 0):
                direction = (BLOCK_SIZE, 0)

    # Update Snake Position
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)

    # Check Collisions
    if new_head == food:
        score += 10
        food = spawn_food()  # Spawn new food
        # Check if the score threshold is reached for speed increase
        if score >= SCORE_THRESHOLD and current_fps < MAX_FPS:
            current_fps += SPEED_INCREMENT  # Increase snake speed by 5 FPS
            SCORE_THRESHOLD += 50  # Increase threshold for the next speed increment
    else:
        snake.pop()  # Remove the tail unless food is eaten

    # Check for Game Over (collisions with wall or self)
    if (new_head[0] < 0 or new_head[1] < 0 or
        new_head[0] >= WIDTH or new_head[1] >= HEIGHT or
        new_head in snake[1:]):
        game_over_screen(score)
        pygame.display.flip()

        # Wait for the user to press 'C' to continue or 'Q' to quit
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_input = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:  # Press 'C' to continue
                        reset_game()
                        waiting_for_input = False
                    elif event.key == pygame.K_q:  # Press 'Q' to quit
                        running = False
                        waiting_for_input = False
        break

    # Draw Everything
    screen.fill(BLACK)
    
    # Draw Food
    pygame.draw.rect(screen, NEON_PINK, (*food, BLOCK_SIZE, BLOCK_SIZE))
    
    # Draw Snake
    for block in snake:
        pygame.draw.rect(screen, NEON_GREEN, (*block, BLOCK_SIZE, BLOCK_SIZE))
    
    # Draw Score
    show_text(f"Score: {score}", font, NEON_BLUE, (10, 10))

    # Refresh Display
    pygame.display.flip()
    clock.tick(current_fps)  # Control the game speed (snake speed)

# Quit Pygame
pygame.quit()
