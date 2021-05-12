import os
import pygame
import random
pygame.font.init()

FPS = 60
WIDTH, HEIGHT = 900, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
START = 0
BORDER_THICKNESS = 5
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survive")
PLAYER_RECT = (WIDTH//2, HEIGHT//2, 15, 15)
PLAYER = pygame.Rect(PLAYER_RECT)

ATTACKERS = []
END_FONT = pygame.font.SysFont('comicsans', 50)

HIT = pygame.USEREVENT + 1
# end of global variable declaration

def draw_window(MOVE):
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, RED, PLAYER)
    draw_border()
    attacker_movement(MOVE)
    pygame.display.update()

def draw_border():
    pygame.draw.rect(WIN, BLACK, (START, START, BORDER_THICKNESS, HEIGHT)) # left border
    pygame.draw.rect(WIN, BLACK, (WIDTH - BORDER_THICKNESS, START, BORDER_THICKNESS, HEIGHT)) # right border
    pygame.draw.rect(WIN, BLACK, (START, START, WIDTH, BORDER_THICKNESS)) # upper border
    pygame.draw.rect(WIN, BLACK, (START, HEIGHT - BORDER_THICKNESS, WIDTH, BORDER_THICKNESS)) # lower border

def movement_handler(Keys_Pressed, PLAYER_SPEED):
    if (Keys_Pressed[pygame.K_w] and PLAYER.y - PLAYER_SPEED > 0):
            PLAYER.y -= PLAYER_SPEED
    if (Keys_Pressed[pygame.K_s] and PLAYER.y + PLAYER.height + PLAYER_SPEED < HEIGHT):
        PLAYER.y += PLAYER_SPEED
    if (Keys_Pressed[pygame.K_a] and PLAYER.x - PLAYER_SPEED > 0):
        PLAYER.x -= PLAYER_SPEED
    if (Keys_Pressed[pygame.K_d] and PLAYER.x + PLAYER.width + PLAYER_SPEED < WIDTH):
        PLAYER.x += PLAYER_SPEED

def attacker_spawner():
    first = random.randint(1, 2) # X or Y
    second = random.randint(1, 2) # Start or End
    if first == 1:
        location = random.randint(0, 90)
        if second == 1:
            second = HEIGHT - BORDER_THICKNESS - 10
        else:
            second = BORDER_THICKNESS
        ATTACKER = (location * BORDER_THICKNESS * 2, second, 10, 10)
    if first == 2:
        location = random.randint(0, 50)
        if second == 1:
            second = WIDTH - BORDER_THICKNESS - 10
        else:
            second = BORDER_THICKNESS
        ATTACKER = (second, BORDER_THICKNESS * 2 * location, 10, 10)
    current_attacker = pygame.Rect(ATTACKER)
    pygame.draw.rect(WIN, BLUE, ATTACKER)
    ATTACKERS.append(current_attacker)

def attacker_movement(MOVE):
    for attacker in ATTACKERS:
        if PLAYER.colliderect(attacker):
            pygame.event.post(pygame.event.Event(HIT))
        each_attacker_movement(attacker, MOVE)  
        pygame.draw.rect(WIN, BLUE, attacker)

def each_attacker_movement(attacker, MOVE):
    # handling x direction
    if attacker.x < PLAYER.x:
        attacker.x += MOVE
    else:
        attacker.x -= MOVE
    # handling y direction
    if attacker.y < PLAYER.y:
        attacker.y += MOVE
    else: attacker.y -= MOVE
    
def gameover(SCORE):
    WIN.fill(WHITE)
    draw_border()
    draw_text = END_FONT.render("You Got Your Cheeks Clapped!", 1, BLACK)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    
    pygame.display.update()
    pygame.time.delay(1500)
    WIN.fill(WHITE)
    draw_border()
    draw_text = END_FONT.render("Score: " + str(SCORE), 1, BLACK)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 + 30 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    print(SCORE)

def main():
    condition = True
    clock = pygame.time.Clock()
    TIME = 0
    SCORE = 0
    PLAYER_SPEED = 5
    MOVE = 2
    while(condition):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                condition = False
            if event.type == HIT:
                gameover(SCORE)
        Keys_Pressed = pygame.key.get_pressed()
        movement_handler(Keys_Pressed, PLAYER_SPEED)       
        draw_window(MOVE)
        TIME += 1
        if TIME % 180 == 0:
            if TIME % (180 * 5) == 0:
                MOVE += 1
            if TIME % (180 * 8) == 0:
                PLAYER_SPEED += 1
            attacker_spawner()
            SCORE += 1
        
        
    pygame.quit()



if __name__ == "__main__":
    main()