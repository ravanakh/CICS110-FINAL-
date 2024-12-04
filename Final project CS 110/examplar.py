import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Dungeon Adventure")

# Set up fonts
font = pygame.font.Font(None, 36)

# Player class (simplified)
class Player:
    def __init__(self):
        self.health = 100
        self.max_health = 100
        self.damage = 10
        self.defense = 5
        self.position = (400, 300)  # Center of the screen

    def draw(self):
        # Draw player health bar
        pygame.draw.rect(screen, (255, 0, 0), (50, 50, self.health, 30))

    def attack(self, enemy):
        damage = max(0, self.damage - enemy.defense)
        enemy.health -= damage
        return f"You dealt {damage} damage!"

# Enemy class (simplified)
class Enemy:
    def __init__(self):
        self.health = 50
        self.damage = 5
        self.defense = 2

    def draw(self):
        # Draw enemy as a simple rectangle
        pygame.draw.rect(screen, (0, 0, 255), (500, 300, self.health, 30))

# Game loop
def game_loop():
    player = Player()
    enemy = Enemy()

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear screen

        # Draw player and enemy
        player.draw()
        enemy.draw()

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(player.attack(enemy))

        # Update the display
        pygame.display.update()

        # Delay for a smooth loop
        pygame.time.delay(100)

# Start the game loop
game_loop()

# Quit Pygame
pygame.quit()