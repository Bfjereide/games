import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
ENEMY_HEALTH = 3

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # Grassy ground color
BLUE = (0, 0, 255)
RED = (255, 0, 0)    # Health bar color
BLACK = (0, 0, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, ground):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 100
        self.change_x = 0
        self.change_y = 0
        self.on_ground = False
        self.ground = ground  # Hold reference to ground object

    def update(self):
        self.calc_grav()
        self.apply_movement()

    def apply_movement(self):
        self.rect.x += self.change_x

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width
        
        self.rect.y += self.change_y

        # Check if on ground
        if self.rect.colliderect(self.ground.rect):
            self.rect.y = self.ground.rect.top - self.rect.height
            self.change_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def calc_grav(self):
        if not self.on_ground:
            self.change_y += GRAVITY

    def jump(self):
        if self.on_ground:
            self.change_y += JUMP_STRENGTH
            self.on_ground = False

# Ground class
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT - 50

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - 150
        self.rect.y = SCREEN_HEIGHT - 100
        self.health = ENEMY_HEALTH

    def update(self, player):
        if self.health > 0:
            # Move away from player
            if self.rect.x < player.rect.x:
                self.rect.x += 2.5  # Half the speed of player (5)
            else:
                self.rect.x -= 2.5

            # Keep the enemy within screen bounds
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x > SCREEN_WIDTH - self.rect.width:
                self.rect.x = SCREEN_WIDTH - self.rect.width

    def take_damage(self):
        self.health -= 1
        if self.health < 0:
            self.health = 0

# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Platformer with Enemy")
clock = pygame.time.Clock()

# Create ground instance
ground = Ground()

# Create player instance and pass the ground reference
player = Player(ground)

# Create enemy instance
enemy = Enemy()

# Group for all sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(ground)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key states
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.change_x = -5
    elif keys[pygame.K_RIGHT]:
        player.change_x = 5
    else:
        player.change_x = 0

    # Jump handling
    if keys[pygame.K_SPACE]:
        player.jump()

    # Check for collision with enemy
    if pygame.sprite.collide_rect(player, enemy):
        if player.change_y > 0:  # Jumping on the enemy
            enemy.take_damage()
            player.change_y = JUMP_STRENGTH  # Bounce off the enemy
        else:
            # Handle player hit (optional)
            pass

    # Update
    all_sprites.update()
    enemy.update(player)

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Draw the enemy health bar
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 40, 10, 80, 10))
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 40, 10, 80 * (enemy.health / ENEMY_HEALTH), 10))
    font = pygame.font.Font(None, 36)
    text = font.render("BOSS", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 25))
    screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(FPS)
