import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side-Scrolling 2D Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game settings
FPS = 60
GRAVITY = 0.5
PLAYER_SPEED = 5
JUMP_FORCE = 10
PROJECTILE_SPEED = 10
ENEMY_SPEED = 2
COLLECTIBLE_SIZE = 20

# Fonts
font = pygame.font.SysFont(None, 36)

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT - 150
        self.vel_y = 0
        self.jumping = False
        self.health = 100
        self.lives = 3
        self.score = 0
    
    def update(self):
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if not self.jumping and keys[pygame.K_SPACE]:
            self.jumping = True
            self.vel_y = -JUMP_FORCE
        
        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        # Check ground collision
        if self.rect.y >= HEIGHT - 150:
            self.rect.y = HEIGHT - 150
            self.jumping = False

    def shoot(self):
        # Shoot projectile
        projectile = Projectile(self.rect.centerx, self.rect.top)
        all_sprites.add(projectile)
        projectiles.add(projectile)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.rect.x += PROJECTILE_SPEED
        if self.rect.right > WIDTH:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 50
    
    def update(self):
        self.rect.x -= ENEMY_SPEED
        if self.rect.right < 0:
            self.kill()

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.image = pygame.Surface((COLLECTIBLE_SIZE, COLLECTIBLE_SIZE))
        if type == "health":
            self.image.fill(GREEN)
        elif type == "life":
            self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type
    
    def update(self):
        if self.rect.right < 0:
            self.kill()

# Level design
def create_level(level):
    for i in range(5):
        enemy = Enemy(random.randint(WIDTH + 100, WIDTH + 500), HEIGHT - 150)
        all_sprites.add(enemy)
        enemies.add(enemy)
    for i in range(3):
        collectible = Collectible(random.randint(WIDTH + 100, WIDTH + 500), HEIGHT - 150, random.choice(["health", "life"]))
        all_sprites.add(collectible)
        collectibles.add(collectible)

# Game Over screen
def game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over! Press 'R' to Restart", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    wait_for_restart()

# Wait for restart
def wait_for_restart():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False

# Main game loop
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

level = 1
create_level(level)

clock = pygame.time.Clock()
running = True
game_over = False

while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                player.shoot()

    if not game_over:
        # Update all sprites
        all_sprites.update()
        
        # Check projectile collisions with enemies
        hits = pygame.sprite.groupcollide(enemies, projectiles, True, True)
        for hit in hits:
            player.score += 10
        
        # Check player collisions with enemies
        hits = pygame.sprite.spritecollide(player, enemies, False)
        for hit in hits:
            player.health -= 10
            if player.health <= 0:
                player.lives -= 1
                player.health = 100
                if player.lives <= 0:
                    game_over = True
        
        # Check player collisions with collectibles
        hits = pygame.sprite.spritecollide(player, collectibles, True)
        for hit in hits:
            if hit.type == "health":
                player.health += 20
                if player.health > 100:
                    player.health = 100
            elif hit.type == "life":
                player.lives += 1

        # Clear screen
        screen.fill(BLACK)

        # Draw all sprites
        all_sprites.draw(screen)
        
        # Draw HUD (health, lives, score)
        health_text = font.render(f"Health: {player.health}", True, WHITE)
        lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
        score_text = font.render(f"Score: {player.score}", True, WHITE)
        screen.blit(health_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(score_text, (10, 90))

        # Update display
        pygame.display.flip()

    else:
        game_over_screen()

pygame.quit()
