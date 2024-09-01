import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Thiết lập màn hình
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong AI")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Thanh paddle
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5

# Bóng
BALL_SIZE = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Điểm số
score1 = 0
score2 = 0
font = pygame.font.Font(None, 36)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.is_active = False

    def move(self, ball):
        if self.is_active:
            if self.rect.centery < ball.rect.centery:
                self.rect.y += PADDLE_SPEED
            elif self.rect.centery > ball.rect.centery:
                self.rect.y -= PADDLE_SPEED

            # Giới hạn paddle trong màn hình
            self.rect.y = max(0, min(self.rect.y, HEIGHT - PADDLE_HEIGHT))

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.dx = BALL_SPEED_X * random.choice((1, -1))
        self.dy = BALL_SPEED_Y * random.choice((1, -1))

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Kiểm tra va chạm với cạnh trên và dưới
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

# Tạo đối tượng
paddle1 = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
paddle2 = Paddle(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball()

# Khởi đầu, paddle bên trái active
paddle1.is_active = True

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Di chuyển các đối tượng
    paddle1.move(ball)
    paddle2.move(ball)
    ball.move()

    # Kiểm tra va chạm với paddle và cộng điểm
    if ball.rect.colliderect(paddle1.rect):
        ball.dx *= -1
        score1 += 1
        paddle1.is_active = False
        paddle2.is_active = True
    elif ball.rect.colliderect(paddle2.rect):
        ball.dx *= -1
        score2 += 1
        paddle2.is_active = False
        paddle1.is_active = True

    # Kiểm tra nếu bóng ra ngoài biên
    if ball.rect.left <= 0 or ball.rect.right >= WIDTH:
        ball.reset()
        paddle1.is_active = True
        paddle2.is_active = False

    # Vẽ màn hình
    screen.fill(BLACK)
    paddle1.draw()
    paddle2.draw()
    ball.draw()

    # Hiển thị điểm số
    score_text = font.render(f"LEFT :  {score1}    RIGHT :  {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
