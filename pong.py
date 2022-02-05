import pygame, sys, random

class Block(pygame.sprite.Sprite):
    def __init__(self, path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect( center=(pos_x, pos_y) )

class Player(Block):
    def __init__(self, path, pos_x, pos_y, speed):
        super().__init__(path, pos_x, pos_y)
        self.speed = speed
        self.movement = 0
    
    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
    
    def update(self):
        self.rect.y += self.movement
        self.screen_constrain()

class Ball(Block):
    def __init__(self, path, pos_x, pos_y, speed_x, speed_y, paddles):
        super().__init__(path, pos_x, pos_y)
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.paddles = paddles
        self.score_time = 0
        self.active = False
    
    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.speed_y *= -1
        
        if pygame.sprite.spritecollide(self, self.paddles, False):
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect

            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.speed_y *= -1
    
    def reset_ball(self):
        self.score_time = pygame.time.get_ticks()

        self.active = False
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        self.rect.center = (screen_width/2, screen_height/2) 

    def restart_counter(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.score_time > 2100:
            self.active = True
    
    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            self.collisions()
        else:
            self.restart_counter()

class Opponent(Block):
    def __init__(self, path, pos_x, pos_y, speed):
        super().__init__(path, pos_x, pos_y)
        self.speed = speed

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self):
        if self.rect.centery < ball_sprite.sprite.rect.centery:
            self.rect.y += self.speed
        if self.rect.centery > ball_sprite.sprite.rect.centery:
            self.rect.y -= self.speed
        
        self.screen_constrain()

class GameManager:
    def __init__(self, ball_group, paddle_group):
        self.ball_group = ball_group
        self.paddle_group = paddle_group
        self.player_score = 0
        self.opponent_score = 0
    
    def run_game(self):
        # Drawing the Objects
        screen.blit(background, (0, 0))
        
        self.show_score()

        paddle_group.draw(screen)
        ball_sprite.draw(screen)
        
        # Updating the Objects
        paddle_group.update() 
        ball_sprite.update()

        self.reset_ball()

    def show_score(self):
        player_score = font.render(str(self.player_score), False, (255, 255, 255))
        player_score_rect = player_score.get_rect( center=(screen_width/2 - 40, screen_height/2) )

        opponent_score = font.render(str(self.opponent_score), False, (255, 255, 255))
        opponent_score_rect = opponent_score.get_rect( center=(screen_width/2 + 40, screen_height/2) )
    
        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()

# General Setup
pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong 2')

background = pygame.image.load('./bg.png')

# Game Variables
font = pygame.font.SysFont('Early GameBoy.ttf', 38)

# Game Objects
player = Player('./paddle_green.png', 30, screen_height/2, 4.5)
opponent = Opponent('./paddle_blue.png', screen_width - 30, screen_height/2, 4.5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('./ball.png', screen_width/2, screen_height/2, 5.5, 5.5, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

gamemanager = GameManager(ball_sprite, paddle_group)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.movement -= player.speed
            if event.key == pygame.K_DOWN:
                player.movement += player.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.movement += player.speed
            if event.key == pygame.K_DOWN:
                player.movement -= player.speed
        
    gamemanager.run_game()

    pygame.display.flip()
    clock.tick(60)