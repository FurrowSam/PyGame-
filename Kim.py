import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000

# Colors
PINK = (255, 192, 203)
BLACK = (0, 0, 0)

# Load the dinosaur image
dinosaur_img = pygame.image.load("dinosaur.png")

# Load the meteorite image
meteorite_img = pygame.image.load("meteorite.png")  

# Load the bullet image and scale it to desired size
bullet_img_original = pygame.image.load("heart_bullets.png")
bullet_width, bullet_height = 20, 40  # Set dimensions for the bullet
bullet_img = pygame.transform.scale(bullet_img_original, (bullet_width, bullet_height))

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge and Shoot the Meteorites!")

# Clock to control frame rate
clock = pygame.time.Clock()

# Player settings
player_width, player_height = 75, 75
player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - player_height
player_speed = 7

# Meteorite settings
meteorite_width, meteorite_height = 75, 75
meteorite_speed = 5
meteorites = []  # List of falling meteorites

# Bullet settings
bullet_speed = 10
bullets = []  # List of bullets

# Score
score = 0

# Font for displaying score
font = pygame.font.SysFont("Arial", 30)

# Main game loop
running = True
while running:
    screen.fill(PINK)  # Clear screen with pink background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Shoot bullet when spacebar is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                new_bullet = pygame.Rect(
                    player_x + player_width // 2 - bullet_width // 2,  # Center bullet horizontally
                    player_y,  # Start at the top of the player
                    bullet_width,
                    bullet_height,
                )
                bullets.append(new_bullet)

    # Get key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed

    # Create new meteorites at random positions
    if random.randint(1, 30) == 1:  # Lower the number for more meteorites
        new_meteorite = pygame.Rect(
            random.randint(0, SCREEN_WIDTH - meteorite_width),
            0,
            meteorite_width,
            meteorite_height,
        )
        meteorites.append(new_meteorite)

    # Move meteorites and check for collision with the player
    for meteorite in meteorites[:]:
        meteorite.y += meteorite_speed
        if meteorite.colliderect((player_x, player_y, player_width, player_height)):
            running = False  # End game if collision occurs
        if meteorite.y > SCREEN_HEIGHT:
            meteorites.remove(meteorite)
            score += 1

    # Move bullets
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        # Remove bullets that go off-screen
        if bullet.y < 0:
            bullets.remove(bullet)

    # Check for bullet-meteorite collisions
    for bullet in bullets[:]:
        for meteorite in meteorites[:]:
            if bullet.colliderect(meteorite):
                meteorites.remove(meteorite)  # Remove the meteorite
                bullets.remove(bullet)  # Remove the bullet
                score += 1  # Increase the score
                break

    # Scale the dinosaur image to match the player's size if necessary
    dinosaur_img_scaled = pygame.transform.scale(dinosaur_img, (player_width, player_height))
    screen.blit(dinosaur_img_scaled, (player_x, player_y))

    # Draw meteorites (as images)
    for meteorite in meteorites:
        meteorite_img_scaled = pygame.transform.scale(meteorite_img, (meteorite_width, meteorite_height))
        screen.blit(meteorite_img_scaled, (meteorite.x, meteorite.y))

    # Draw bullets (as images)
    for bullet in bullets:
        screen.blit(bullet_img, (bullet.x, bullet.y))

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
