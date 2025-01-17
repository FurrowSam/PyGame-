import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load the dinosaur image
dinosaur_img = pygame.image.load("dinosaur.png")

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge the Falling Blocks!")

# Clock to control frame rate
clock = pygame.time.Clock()

# Player settings
player_width, player_height = 50, 50
player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60
player_speed = 7

# Block settings
block_width, block_height = 50, 50
block_speed = 5
blocks = []  # List of falling blocks

# Score
score = 0

# Font for displaying score
font = pygame.font.SysFont("Arial", 30)

# Main game loop
running = True
while running:
    screen.fill(WHITE)  # Clear screen with white background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed

    # Create new blocks at random positions
    if random.randint(1, 30) == 1:  # Lower the number for more blocks
        new_block = pygame.Rect(random.randint(0, SCREEN_WIDTH - block_width), 0, block_width, block_height)
        blocks.append(new_block)

    # Move blocks and check for collision
    for block in blocks[:]:
        block.y += block_speed
        if block.colliderect((player_x, player_y, player_width, player_height)):
            running = False  # End game if collision occurs
        if block.y > SCREEN_HEIGHT:
            blocks.remove(block)
            score += 1

    # Scale the image to match the player's size if necessary
    dinosaur_img = pygame.transform.scale(dinosaur_img, (player_width, player_height))

    # Draw player as a dinosaur
    screen.blit(dinosaur_img, (player_x, player_y))

    # Draw blocks
    for block in blocks:
        pygame.draw.rect(screen, RED, block)

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
