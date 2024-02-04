import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 800, 600  # Larger window size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Advanced Bouncing Ball Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Load images
paddle_image = pygame.image.load("paddle.png").convert()
paddle_image = pygame.transform.scale(paddle_image, (150, 20))
brick_image = pygame.image.load("brick.png").convert()
brick_image = pygame.transform.scale(brick_image, (60, 20))
ball_image = pygame.image.load("ball.png").convert()
ball_image = pygame.transform.scale(ball_image, (20, 20))

# Load audio files
hit_sound = pygame.mixer.Sound("hit.wav")
brick_break_sound = pygame.mixer.Sound("brick_break.wav")

# Paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = paddle_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = (screen_width // 2, screen_height - 10)

    def update(self):
        # Set paddle position to the mouse x-coordinate
        self.rect.x = pygame.mouse.get_pos()[0] - self.rect.width / 2
        # Keep the paddle within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))

# Brick class
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = brick_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ball_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (screen_width // 2 - 10, 0)
        self.speed_x = random.choice([-3, -2, 2, 3])  # Dynamic ball speed
        self.speed_y = 3

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off the walls
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x = -self.speed_x

        if self.rect.top < 0:
            self.speed_y = -self.speed_y

        # Reset ball if it hits the bottom
        if self.rect.top > screen_height:
            return True  # Indicates that the ball hit the bottom

# Create sprite groups
all_sprites = pygame.sprite.Group()
bricks_group = pygame.sprite.Group()

# Create player, ball, and add to sprite groups
paddle = Paddle()
ball = Ball()
all_sprites.add(paddle, ball)

# Game variables
clock = pygame.time.Clock()
score = 0
combo = 0
spawn_rate = 60  # Adjust the spawn rate based on the level
regenerate_time = 5000  # Time in milliseconds for bricks to regenerate

# Regenerate bricks function
def regenerate_bricks():
    bricks_group.empty()  # Clear existing bricks
    for row in range(5):
        for col in range(10):
            brick = Brick(col * 80, row * 20)  # Adjusted brick spacing
            all_sprites.add(brick)
            bricks_group.add(brick)

# Initial brick generation
regenerate_bricks()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update
    all_sprites.update()

    # Check for collisions between the paddle and the ball
    hit = pygame.sprite.collide_rect(paddle, ball)
    if hit:
        # Bounce off the paddle
        ball.speed_y = -abs(ball.speed_y)
        # Increase the score by 5 when the ball is hit
        score += 5
        combo += 1
        hit_sound.play()
        print("Score:", score, "Combo:", combo)

    # Check for collisions between the ball and bricks
    brick_hit = pygame.sprite.spritecollide(ball, bricks_group, True)
    if brick_hit:
        # Bounce off the bricks
        ball.speed_y = -ball.speed_y
        brick_break_sound.play()
        score += 10 * len(brick_hit)
        combo = 0
        print("Score:", score)

    # Check if the ball hits the bottom
    if ball.update():
        # Deduct points and reset the ball for the next attempt
        score -= 5
        combo = 0
        print("Score:", score)
        # Create a new ball
        ball = Ball()
        all_sprites.add(ball)

    # Regenerate bricks after a certain time
    if pygame.time.get_ticks() % regenerate_time == 0:
        regenerate_bricks()

    # Draw
    screen.fill(black)
    all_sprites.draw(screen)

    # Display score and combo
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, white)
    combo_text = font.render("Combo: " + str(combo), True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(combo_text, (screen_width - 150, 10))

    # Refresh display
    pygame.display.flip()

    # Set frames per second
    clock.tick(60)
