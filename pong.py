'''
Oliver-Haworth
15.12.25 - 16.12.25
'''
import pygame
import random

# pygame setup
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# paddle settings
paddle_width = 40
paddle_height = 150

left_paddle_pos = pygame.Vector2(0, screen.get_height() / 2)
right_paddle_pos = pygame.Vector2(screen.get_width(), screen.get_height() / 2)

# ball
ball_size = 20
ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_velocity = pygame.Vector2(400, 400)

# scores
player1_score = 0 
player2_score = 0 

# font
score_font = pygame.font.Font(None, 100)

# sounds
paddle = pygame.mixer.Sound("paddle.wav")
effect = pygame.mixer.Sound("score.wav")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000
    screen.fill("black")

    # --- CENTER DOTTED LINE ---
    line_width = 8
    line_height = 20
    gap = 15
    center_x = screen.get_width() // 2 - line_width // 2

    for y in range(0, screen.get_height(), line_height + gap):
        pygame.draw.rect(screen, "white", (center_x, y, line_width, line_height))

    # --- CONTROLS ---
    keys = pygame.key.get_pressed()

    # Left Paddle
    if keys[pygame.K_w]:
        left_paddle_pos.y -= 600 * dt
    if keys[pygame.K_s]:
        left_paddle_pos.y += 600 * dt

    # Right Paddle
    if keys[pygame.K_UP]:
        right_paddle_pos.y -= 600 * dt
    if keys[pygame.K_DOWN]:
        right_paddle_pos.y += 600 * dt 

    # Keep paddles on screen
    left_paddle_pos.y = max(paddle_height / 2, min(left_paddle_pos.y, screen.get_height() - paddle_height / 2))
    right_paddle_pos.y = max(paddle_height / 2, min(right_paddle_pos.y, screen.get_height() - paddle_height / 2))

    # --- BALL MOVEMENT ---
    ball_pos += ball_velocity * dt

    # --- COLLISION RECTANGLES ---
    player_rect = pygame.Rect(0, 0, paddle_width, paddle_height)
    player_rect.center = left_paddle_pos
    
    player2_rect = pygame.Rect(0, 0, paddle_width, paddle_height)
    player2_rect.center = right_paddle_pos

    ball_rect = pygame.Rect(0, 0, ball_size, ball_size)
    ball_rect.center = ball_pos

    # --- BALL BOUNCE OFF EDGES ---
    if ball_rect.top <= 0 or ball_rect.bottom >= screen.get_height():
        ball_velocity.y *= -1

    # --- PADDLE COLLISION ---
    speed_up = 100

    if ball_rect.colliderect(player_rect) and ball_velocity.x < 0:
        paddle.play()
        ball_velocity.x *= -1
        ball_velocity.x += speed_up
        ball_velocity.y += speed_up

    if ball_rect.colliderect(player2_rect) and ball_velocity.x > 0:
        paddle.play()
        ball_velocity.x *= -1
        ball_velocity.x -= speed_up
        ball_velocity.y -= speed_up

    # --- SCORING ---
    if ball_rect.left <= 0:
        player2_score += 1
        effect.play()
        ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        ball_velocity.x = random.choice((-400, 400))
        ball_velocity.y = random.choice((-400, 400))

    elif ball_rect.right >= screen.get_width():
        player1_score += 1
        effect.play()
        ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        ball_velocity.x = random.choice((-400, 400))
        ball_velocity.y = random.randint(-400, 400)


    # --- DRAWING ---
    pygame.draw.rect(screen, "white", player_rect)
    pygame.draw.rect(screen, "white", player2_rect)
    pygame.draw.rect(screen, "white", ball_rect)

    # Scores
    player1_text = score_font.render(str(player1_score), True, (255, 255, 255))
    screen.blit(player1_text, (screen.get_width() // 4, 10))

    player2_text = score_font.render(str(player2_score), True, (255, 255, 255))
    screen.blit(player2_text, (screen.get_width() * 3 // 4, 10))

    pygame.display.flip()

pygame.quit()



