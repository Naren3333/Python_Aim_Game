import math
import random
import time
import pygame
from Target import Target


pygame.init()

WIDTH, HEIGHT = 1000, 600

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Aim Trainer Game")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30

BG_COLOUR = (0, 51, 102)
LIVES = 3
TOP_BAD_HEIGHT = 50

LABLE_FONT = pygame.font.SysFont("comicsans", 24)


def draw(win, targets : list[Target]) :
    win.fill(BG_COLOUR)

    for target in targets :
        target.draw(win)
    

def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}:{milli}"

def draw_top_bar(win, elapsed_time,targets_pressed, score, misses):
    pygame.draw.rect(win, "grey", (0,0, WIDTH, TOP_BAD_HEIGHT))
    time_label = LABLE_FONT.render(f"Time : {format_time(elapsed_time)}",1,"black")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABLE_FONT.render(f"Speed: {speed} t/s", 1, "black")

    score_label = LABLE_FONT.render(f"Score: {score}", 1, "black")

    lives_label = LABLE_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(score_label, (450, 5))
    win.blit(lives_label, (650, 5))


def end_screen(win, elapsed_time, targets_pressed, score, clicks) :
    win.fill(BG_COLOUR)
    time_label = LABLE_FONT.render(f"Time : {format_time(elapsed_time)}",1,"white")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABLE_FONT.render(f"Speed: {speed} t/s", 1, "white")

    score_label = LABLE_FONT.render(f"Score: {score}", 1, "white")

    accuracy = round(targets_pressed / clicks *100, 1) if clicks > 0 else 0
    accuracy_label = LABLE_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(score_label, (get_middle(score_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))

    pygame.display.update()

    run = True
    while run :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

def get_middle(surface) :
    return WIDTH/2 - surface.get_width()/2

def main() :
    run = True
    targets = []
    clock = pygame.time.Clock()

    score = 0
    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouth_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get() :
            if event.type == pygame.QUIT: # IF event that happened is quit, then we close the window
                run = False
                break

            if event.type == TARGET_EVENT :
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAD_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1
        
        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1
            
            if click and target.collide(*mouth_pos) : ## * breaks down the tuple mouth_pos = (x,y) --> x,y
                targets.remove(target)
                if target.colour_chosen == "black" : score+=2
                elif target.colour_chosen == "gold" : score+=3
                else: score += 1
                targets_pressed +=1 
        
        if misses >= LIVES:
            end_screen(WIN, elapsed_time, targets_pressed, score, clicks)# end game

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, score, misses)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__" :
    main()
