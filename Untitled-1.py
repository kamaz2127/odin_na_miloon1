from pygame import *
import sys

init()
mixer.init()

WIDTH, HEIGHT = 800, 600
SCREEN = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Вікторина на мільйон")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (10, 10, 50)
LIGHT_BLUE = (135, 150, 250)
GOLD = (218, 165, 32)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

FONT_BIG = font.Font(None, 70)
FONT_MAIN = font.Font(None, 40)
FONT_UI = font.Font(None, 30)

# Завантаження картинок (переконайся, що bg.png, btn_play.png, btn_exit.png є в папці)
bg_img = transform.scale(image.load("bg.png"), (WIDTH, HEIGHT))
btn_play_img = transform.scale(image.load("btn_play.png"), (200, 60))
btn_exit_img = transform.scale(image.load("btn_exit.png"), (200, 60))

# Завантаження звукових ефектів
snd_wrong = mixer.Sound("lose sound 1_0.wav")
snd_correct = mixer.Sound("Picked Coin Echo.wav")
snd_clock = mixer.Sound("clock.ogg")

# Назви файлів фонової музики
MUSIC_MENU = "MyVeryOwnDeadShip.ogg" 
# ВАЖЛИВО: впиши повну назву файлу для питань, бо на скріншоті вона обрізана
MUSIC_GAME = "lets-see-q1-extra-large.mp3" 
# ВАЖЛИВО: розпакуй win music 1.zip і впиши сюди назву аудіофайлу, який був усередині
MUSIC_WIN = "win music 1-2.mp3" 

current_music = ""

quiz_data = [
    {"q": "Яка планета найближча до Сонця?", "opts": ["Венера", "Земля", "Марс", "Меркурій"], "c": 3},
    {"q": "Яка наука вивчає живі організми?", "opts": ["Фізика", "Хімія", "Біологія", "Астрономія"], "c": 2},
    {"q": "Скільки ніг має комаха?", "opts": ["4", "6", "8", "10"], "c": 1},
    {"q": "Яка речовина має хімічну формулу H₂O?", "opts": ["Кисень", "Вуглекислий газ", "Вода", "Водень"], "c": 2},
    {"q": "Який орган людини відповідає за перекачування крові?", "opts": ["Легені", "Печінка", "Мозок", "Серце"], "c": 3},
    {"q": "Яка одиниця вимірювання сили в системі SI?", "opts": ["Ват", "Паскаль", "Ньютон", "Джоуль"], "c": 2},
    {"q": "Хто сформулював закон всесвітнього тяжіння?", "opts": ["Альберт Ейнштейн", "Галілео Галілей", "Ісаак Ньютон", "Нікола Тесла"], "c": 2},
    {"q": "Який газ переважає в атмосфері Землі?", "opts": ["Кисень", "Вуглекислий газ", "Азот", "Аргон"], "c": 2},
    {"q": "Яка частинка має негативний електричний заряд?", "opts": ["Протон", "Нейтрон", "Атом", "Електрон"], "c": 3},
    {"q": "Яка наука вивчає спадковість і мінливість організмів?", "opts": ["Екологія", "Генетика", "Анатомія", "Мікробіологія"], "c": 1}
]

prize_money = [100, 300, 500, 1000, 5000, 10000, 100000, 500000, 750000, 1000000]

state = "menu"
current_q = 0
game_sub_state = "play"
selected_option = -1
timer_start = 0

def draw_text(text, font_obj, color, x, y):
    text_surf = font_obj.render(str(text), True, color)
    rect = text_surf.get_rect(center=(x, y))
    SCREEN.blit(text_surf, rect)

def draw_btn(rect, text, bg_color):
    draw.rect(SCREEN, bg_color, rect, border_radius=10)
    draw.rect(SCREEN, LIGHT_BLUE, rect, 3, border_radius=10)
    draw_text(text, FONT_UI, WHITE, rect.centerx, rect.centery)

clock = time.Clock()
running = True

while running:
    SCREEN.blit(bg_img, (0, 0))
    mx, my = mouse.get_pos()
    
    clicked = False
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                clicked = True

    if state == "menu":
        if current_music != "menu":
            mixer.music.load(MUSIC_MENU)
            mixer.music.play(-1)
            current_music = "menu"

        #draw_text("Вікторина на мільйон", FONT_BIG, LIGHT_BLUE, WIDTH//2, 150)
        
        btn_play = Rect(WIDTH//2 - 100, 250, 200, 60)
        btn_exit = Rect(WIDTH//2 - 100, 350, 200, 60)
        
        SCREEN.blit(btn_play_img, btn_play.topleft)
        SCREEN.blit(btn_exit_img, btn_exit.topleft)
        draw_text("", FONT_UI, WHITE, btn_play.centerx, btn_play.centery)
        draw_text("", FONT_UI, WHITE, btn_exit.centerx, btn_exit.centery)
        
        if clicked:
            if btn_play.collidepoint(mx, my):
                state = "game"
                current_q = 0
                game_sub_state = "play" 
            elif btn_exit.collidepoint(mx, my):
                running = False
                
    elif state == "game":
        if current_music != "game":
            mixer.music.load(MUSIC_GAME)
            mixer.music.play(-1)
            current_music = "game"
        SCREEN.fill(DARK_BLUE)
        data = quiz_data[current_q]
        
        draw_text(f"Питання {current_q + 1} | {prize_money[current_q]} $", FONT_UI, GOLD, WIDTH//2, 50)
        q_rect = Rect(50, 100, 700, 120)
        draw.rect(SCREEN, LIGHT_BLUE, q_rect, border_radius=15)
        draw.rect(SCREEN, GOLD, q_rect, 3, border_radius=15)
        draw_text(data["q"], FONT_MAIN, WHITE, WIDTH//2, 160)
        
        coords = [
            Rect(50, 300, 330, 80), Rect(420, 300, 330, 80),
            Rect(50, 420, 330, 80), Rect(420, 420, 330, 80)
        ]
        
        current_time = time.get_ticks()
        
        for i, rect in enumerate(coords):
            btn_color = (20, 20, 60)
            
            if game_sub_state == "play":
                if rect.collidepoint(mx, my):
                    btn_color = LIGHT_BLUE
                if clicked and rect.collidepoint(mx, my):
                    selected_option = i
                    game_sub_state = "wait"
                    timer_start = current_time
                    snd_clock.play(-1) # Запуск звуку годинника
                    
            elif game_sub_state == "wait":
                if i == selected_option:
                    btn_color = GOLD
                    
            elif game_sub_state == "reveal":
                if i == selected_option:
                    if selected_option == data["c"]:
                        btn_color = GREEN
                    else:
                        btn_color = RED
                if i == data["c"]:
                    btn_color = GREEN
                    
            draw_btn(rect, f"{['A', 'B', 'C', 'D'][i]}: {data['opts'][i]}", btn_color)

        if game_sub_state == "wait":
            if current_time - timer_start > 2000:
                game_sub_state = "reveal"
                timer_start = current_time
                snd_clock.stop() # Зупинка звуку годинника
                
                # Відтворення звуку правильної/неправильної відповіді
                if selected_option == data["c"]:
                    snd_correct.play()
                else:
                    snd_wrong.play()
                
        elif game_sub_state == "reveal":
            if current_time - timer_start > 2000:
                if selected_option == data["c"]:
                    if current_q < len(quiz_data) - 1:
                        current_q += 1
                        game_sub_state = "play"
                    else:
                        state = "win"
                else:
                    state = "lose"

    elif state == "win":
        SCREEN.fill(DARK_BLUE)
        if current_music != "win":
            mixer.music.load(MUSIC_WIN)
            mixer.music.play(-1)
            current_music = "win"

        draw_text("ПЕРЕМОГА!", FONT_BIG, GREEN, WIDTH//2, 200)
        draw_text(f"Ви виграли {prize_money[-1]} $", FONT_MAIN, WHITE, WIDTH//2, 300)
        
        btn_menu = Rect(WIDTH//2 - 100, 450, 200, 60)
        col = LIGHT_BLUE if btn_menu.collidepoint(mx, my) else (20, 20, 60)
        draw_btn(btn_menu, "В МЕНЮ", col)
        
        if clicked and btn_menu.collidepoint(mx, my):
            state = "menu"

    elif state == "lose":
        SCREEN.fill(DARK_BLUE)
        if current_music != "lose":
            mixer.music.stop()
            current_music = "lose"

        draw_text("НЕПРАВИЛЬНО!!!", FONT_BIG, RED, WIDTH//2, 200)
        draw_text("Повернення в меню...", FONT_MAIN, WHITE, WIDTH//2, 300)
        
        btn_menu = Rect(WIDTH//2 - 100, 450, 200, 60)
        col = LIGHT_BLUE if btn_menu.collidepoint(mx, my) else (20, 20, 60)
        draw_btn(btn_menu, "В МЕНЮ", col)
        
        if clicked and btn_menu.collidepoint(mx, my):
            state = "menu"

    display.flip()
    clock.tick(60)

quit()