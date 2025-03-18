import math
import random
import time
import pygame
pygame.init()
pygame.mixer.init()

# Game Settings
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Aim Trainer")
BG_COLOR = (0, 25, 40)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (160, 160, 160)
BAR_COLOR = "grey"

# Game Variables
LIVES = 3
TOP_BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont("comicsans", 24)
HIT_SOUND = pygame.mixer.Sound("aim-trainer/hit.wav")
MISS_SOUND = pygame.mixer.Sound("aim-trainer/miss.wav")

# Target Settings
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.5
    COLOR = "red"
    SEC_COLOR = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False
        
        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SEC_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SEC_COLOR, (self.x, self.y), self.size * 0.4)

    def collide(self, x, y): #check if the mouse is on the target
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dis <= self.size

class Button:
    def __init__(self, x, y, width, height , color, text, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

        self.font = pygame.font.SysFont("comicsans", 40)
        self.text_surface = self.font.render(text, True, "white") #text is the string to render, True is to enable anti-aliasing
        self.text_rect = self.text_surface.get_rect(center=self.rect.center) #create a rectangle that surrounds the text "center=self.rect.center" is to center the text. get_rect is to create invisible rect for positioning

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        surface.blit(self.text_surface, self.text_rect) #blit is to draw the text on the surface

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos) #collidepoint is to check if the mouse is on the button. event.pos is the position of the mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True 
        return False

class Checkbox:
    def __init__(self, x, y, size, text,):
        self.rect = pygame.Rect(x, y, size, size) #create a square rect for the checkbox
        self.text = text
        self.size = size
        self.is_checked = False

        self.font = pygame.font.SysFont("comicsans", 24)
        self.text_surface = self.font.render(text, True, "white")
        self.text_rect = self.text_surface.get_rect(midleft=(x + size + 10, y + size//2)) #midleft is to center the text on the left side of the checkbox
        
    def draw(self, surface):
        pygame.draw.rect(surface, "white", self.rect, 2) #2 is the width of the border
        if self.is_checked:
            pygame.draw.rect(surface, "white", 
                            (self.rect.x + 4, self.rect.y + 4, 
                            self.size - 8, self.size - 8)) #create a smaller square inside the checkbox

        surface.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_checked = not self.is_checked
                return True
        return False

def start_screen(win, is_fullscreen=False):
    global WIDTH, HEIGHT, WINDOW, BUTTON_COLOR, BUTTON_HOVER_COLOR

    def update_button_positions():
        easy_button.rect.x = WIDTH//2 - 100
        easy_button.rect.y = HEIGHT//2 - 25
        easy_button.text_rect = easy_button.text_surface.get_rect(center=easy_button.rect.center)
        
        hard_button.rect.x = WIDTH//2 - 100
        hard_button.rect.y = HEIGHT//2 + 35
        hard_button.text_rect = hard_button.text_surface.get_rect(center=hard_button.rect.center)
        
        fullscreen_checkbox.rect.x = WIDTH - 150
        fullscreen_checkbox.rect.y = HEIGHT - 40
        fullscreen_checkbox.text_rect = fullscreen_checkbox.text_surface.get_rect(
            midleft=(fullscreen_checkbox.rect.x + fullscreen_checkbox.size + 10, 
                    fullscreen_checkbox.rect.y + fullscreen_checkbox.size//2))

    win.fill(BG_COLOR)

    easy_button = Button(
        x=WIDTH//2 - 100,  
        y=HEIGHT//2 - 25,  
        width=200,
        height=50,
        text="EASY",
        color=BUTTON_COLOR,      
        hover_color=BUTTON_HOVER_COLOR
    )
    hard_button = Button(
        x=WIDTH//2 - 100,  
        y=HEIGHT//2 + 35,  
        width=200,
        height=50,
        text="HARD",
        color=BUTTON_COLOR,      
        hover_color=BUTTON_HOVER_COLOR
    )
    fullscreen_checkbox = Checkbox(
        x=WIDTH - 150,
        y=HEIGHT - 40,
        size=20,
        text="Fullscreen"
    )
    fullscreen_checkbox.is_checked = is_fullscreen

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if easy_button.handle_event(event):
                running = False  
                return "easy", fullscreen_checkbox.is_checked
            
            if hard_button.handle_event(event): 
                running = False  
                return "hard", fullscreen_checkbox.is_checked

            if fullscreen_checkbox.handle_event(event):
                if fullscreen_checkbox.is_checked:
                    screen_info = pygame.display.Info()
                    WIDTH = screen_info.current_w
                    HEIGHT = screen_info.current_h
                    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    WIDTH = WIDTH
                    HEIGHT = HEIGHT
                    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
                update_button_positions()

        win.fill(BG_COLOR)
        easy_button.draw(win)
        hard_button.draw(win)
        fullscreen_checkbox.draw(win)
        pygame.display.update()

def mode(win, is_fullscreen=False):
    global WIDTH, HEIGHT, WINDOW, BUTTON_COLOR, BUTTON_HOVER_COLOR

    def update_button_positions():
        time_button.rect.x = WIDTH//2 - 100
        time_button.rect.y = HEIGHT//2 - 25
        time_button.text_rect = time_button.text_surface.get_rect(center=time_button.rect.center)
        
        lives_button.rect.x = WIDTH//2 - 100
        lives_button.rect.y = HEIGHT//2 + 35
        lives_button.text_rect = lives_button.text_surface.get_rect(center=lives_button.rect.center)
        
        fullscreen_checkbox.rect.x = WIDTH - 150
        fullscreen_checkbox.rect.y = HEIGHT - 40
        fullscreen_checkbox.text_rect = fullscreen_checkbox.text_surface.get_rect(
            midleft=(fullscreen_checkbox.rect.x + fullscreen_checkbox.size + 10, 
                    fullscreen_checkbox.rect.y + fullscreen_checkbox.size//2))

    win.fill(BG_COLOR)

    time_button = Button(
        x=WIDTH//2 - 100,  
        y=HEIGHT//2 - 25,  
        width=200,
        height=50,
        text="Time",
        color=BUTTON_COLOR,      
        hover_color=BUTTON_HOVER_COLOR
    )
    lives_button = Button(
        x=WIDTH//2 - 100,  
        y=HEIGHT//2 + 35,  
        width=200,
        height=50,
        text="Lives",
        color=BUTTON_COLOR,      
        hover_color=BUTTON_HOVER_COLOR
    )
    fullscreen_checkbox = Checkbox(
        x=WIDTH - 150,
        y=HEIGHT - 40,
        size=20,
        text="Fullscreen"
    )
    fullscreen_checkbox.is_checked = is_fullscreen

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if time_button.handle_event(event):
                running = False  
                return "time", fullscreen_checkbox.is_checked
            
            if lives_button.handle_event(event): 
                running = False  
                return "lives", fullscreen_checkbox.is_checked

            if fullscreen_checkbox.handle_event(event):
                if fullscreen_checkbox.is_checked:
                    screen_info = pygame.display.Info()
                    WIDTH = screen_info.current_w
                    HEIGHT = screen_info.current_h
                    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    WIDTH = WIDTH
                    HEIGHT = HEIGHT
                    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
                update_button_positions()

        win.fill(BG_COLOR)
        time_button.draw(win)
        lives_button.draw(win)
        fullscreen_checkbox.draw(win)
        pygame.display.update()

def draw(win, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)

def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"

def draw_top_bar(win, elapsed_time, target_pressed, misses, mode="lives", clicks=0,):
    pygame.draw.rect(win, BAR_COLOR, (0, 0, WIDTH, TOP_BAR_HEIGHT))

    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")

    speed = round(target_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")

    accuracy = round((target_pressed / (clicks + misses) * 100), 1) if (clicks + misses) > 0 else 100
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "black")

    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(accuracy_label, (400, 5))

    if mode == "lives":
        lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")
        win.blit(lives_label, (700, 5))

def end_screen(win, elapsed_time, target_pressed, clicks, misses):
    win.fill(BG_COLOR)

    box_width = 300
    box_height = 500
    box_x = get_middle(pygame.Surface((box_width,box_height)))
    box_y = 60

    play_again_button = Button(
        x=WIDTH//2 + 170,
        y=300,
        width=200,
        height=65,
        text="Play Again",
        color=BUTTON_COLOR,      
        hover_color=BUTTON_HOVER_COLOR
    )

    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    speed = round(target_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits: {target_pressed}", 1, "white")
    misses_label = LABEL_FONT.render(f"Misses: {misses}", 1, "white")
    accuracy = round((target_pressed / (clicks + misses) * 100), 1) if (clicks + misses) > 0 else 100
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    #making rect background
    transparent_surface = pygame.Surface((box_width,box_height), pygame.SRCALPHA)
    pygame.draw.rect(transparent_surface, (255,255,255,20), (0, 0, box_width, box_height), border_radius=20)

    win.blit(transparent_surface, (box_x, box_y))

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(misses_label, (get_middle(misses_label), 400))
    win.blit(accuracy_label, (get_middle(accuracy_label), 500))

    play_again_button.draw(win)

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                return False
            
            if play_again_button.handle_event(event):
                return True

def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2

def main():
    global WIDTH, HEIGHT, WINDOW

    running = True
    is_fullscreen = False

    while running:
        difficulty, is_fullscreen = start_screen(WINDOW, is_fullscreen)
        modes, is_fullscreen = mode(WINDOW, is_fullscreen)

        if is_fullscreen:
            screen_info = pygame.display.Info()
            WIDTH = screen_info.current_w
            HEIGHT = screen_info.current_h
            WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        else:
            WIDTH = WIDTH
            HEIGHT = HEIGHT
            WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

        targets = []
        clock = pygame.time.Clock()

        target_pressed = 0
        clicks = 0
        misses = 0
        start_time = time.time()
        TIME = 60

        if difficulty == "easy":
            TARGET_INCREMENT = 600
        else:
            TARGET_INCREMENT = 400
            
        pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

        game_running = True
        while game_running:

            clock.tick(60) #run this while loop 60 times per second
            click = False
            mouse_pos = pygame.mouse.get_pos()
            elapsed_time = time.time() - start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    running = False
                    break

                if event.type == TARGET_EVENT:
                    x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                    y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                    target = Target(x, y)
                    targets.append(target)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                    clicks += 1

            for target in targets:
                target.update()

                if target.size <= 0: #if the target size is 0, remove so the targets is not keep getting larger 
                    MISS_SOUND.play()
                    targets.remove(target)
                    misses += 1

                if click and target.collide(*mouse_pos):
                    HIT_SOUND.play()
                    targets.remove(target)
                    target_pressed += 1

            if modes == "time":
                if elapsed_time > TIME:
                    play_again = end_screen(WINDOW, elapsed_time, target_pressed, clicks, misses,)
                    if play_again:
                        game_running = False
                    else:
                        game_running = False
                        running = False
            else:
                if misses >= LIVES:
                    play_again = end_screen(WINDOW, elapsed_time, target_pressed, clicks, misses,)
                    if play_again:
                        game_running = False
                    else:
                        game_running = False
                        running = False

            draw(WINDOW, targets)
            draw_top_bar(WINDOW, elapsed_time, target_pressed, misses, modes, clicks)
            pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
