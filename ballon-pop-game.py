import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Pop")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Load and scale background image
background_img = pygame.image.load(r"C:\Users\Hp\Downloads\Games\Games\Ballon Pop\background.jpeg").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Balloon class
class Balloon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = random.randint(20, 50)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, random.choice([RED, BLUE, GREEN, YELLOW, PURPLE, CYAN]), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.radius * 2)
        self.rect.y = HEIGHT
        self.speed = random.uniform(1, 5)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
            global missed_balloons
            missed_balloons += 1

# Function to display the game-over screen with animated text
def game_over_screen():
    screen.fill(WHITE)
    game_over_text = font.render("Game Over", True, (0, 0, 0))
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    try_again_text = font.render("Press any key to try again", True, (0, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                return

        # Draw pulsing game over text
        screen.fill(WHITE)
        scale = 1.0 + 0.05 * (pygame.time.get_ticks() % 1000 / 1000.0)
        scaled_game_over_text = pygame.transform.scale(game_over_text, (int(game_over_text.get_width() * scale), int(game_over_text.get_height() * scale)))
        screen.blit(scaled_game_over_text, (WIDTH // 2 - scaled_game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(try_again_text, (WIDTH // 2 - try_again_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

# Game variables
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
score = 0
missed_balloons = 0
font = pygame.font.Font(None, 36)

# Main game loop
running = True
while running:
    if missed_balloons >= 10:
        game_over_screen()
        score = 0
        missed_balloons = 0
        all_sprites.empty()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for balloon in all_sprites:
                if balloon.rect.collidepoint(pos):
                    balloon.kill()
                    score += 1

    # Spawn new balloons
    if random.random() < 0.02:
        all_sprites.add(Balloon())

    # Update
    all_sprites.update()

    # Draw
    screen.blit(background_img, (0, 0))

    all_sprites.draw(screen)

    # Draw pulsing score text
    scale = 1.0 + 0.05 * (pygame.time.get_ticks() % 1000 / 1000.0)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    scaled_score_text = pygame.transform.scale(score_text, (int(score_text.get_width() * scale), int(score_text.get_height() * scale)))
    screen.blit(scaled_score_text, (10, 10))

    missed_text = font.render(f"Missed: {missed_balloons}", True, (0, 0, 0))
    screen.blit(missed_text, (10, 50))

    # Refresh display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
