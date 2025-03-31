import pygame 
import time
import os
import sys 
import json
from data_handler import *
from game_logic import *

pygame.init() #تنظیمات اولیه pygame 
WINDOW_SIZE = 600
INFO_BAR_HEIGHT = 50
CELL_SIZE = (WINDOW_SIZE - INFO_BAR_HEIGHT) // 4
height = 600
screen = pygame.display.set_mode((height , WINDOW_SIZE))#((CELL_SIZE * 4, WINDOW_SIZE))
pygame.display.set_caption("2048")
icon_path = "icon_path.jpg"
icon_image = pygame.image.load(icon_path)
pygame.display.set_icon(icon_image)
timer = pygame.time.Clock()
fps = 60
FONT_SIZE = 36
FONT = pygame.font.SysFont("Arial" , FONT_SIZE)

music_enabled = True 

TILE_COLORS = {0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    "light text" : (249 , 246 , 242),
    "dark text" :(119 , 110 , 101),
    "other" : (0 , 0 , 0),
    "bg" : (120 , 100 , 90)}


def draw_board(screen, board, tile_colors, start_time, score):
    """رسم صفحه بازی و نوار اطلاعات."""
    pygame.draw.rect(screen , TILE_COLORS["bg"] , [ 0 , 0 , 600 , 600] , 0 , 10 )
    for i in range (4) :
        for j in range(4) :
            value = board [i][j]
            if value > 8 :
                value_color = TILE_COLORS["light text"]
            else : 
                value_color = TILE_COLORS["dark text"]
            color = TILE_COLORS.get(value , TILE_COLORS["other"])

            rect_x = j * CELL_SIZE + 10
            rect_y = i * CELL_SIZE + INFO_BAR_HEIGHT + 10 

            pygame.draw.rect(screen , color , [j * CELL_SIZE + 10 , i * CELL_SIZE + INFO_BAR_HEIGHT + 10,
                                                CELL_SIZE-20 , CELL_SIZE-20] , 0 , 5)
            
            pygame.draw.rect(screen , "black" , [j * CELL_SIZE + 10 , i * CELL_SIZE + INFO_BAR_HEIGHT + 10,
                                                CELL_SIZE-20 , CELL_SIZE-20] , 2 , 5)
            
            # نمایش مقدار خانه (عدد داخل مربع)
            if value != 0:
                font_size = 60 - (4 * len(str(value)))  # تنظیم اندازه فونت بر اساس تعداد ارقام
                font = pygame.font.Font(None, font_size)
                value_text = font.render(str(value), True, value_color)

                # تنظیم متن در مرکز کاشی
                text_rect = value_text.get_rect(center=(rect_x + (CELL_SIZE - 20) // 2, 
                                                        rect_y + (CELL_SIZE - 20) // 2))

                screen.blit(value_text, text_rect)

            elapsed_time = int(time.time() - start_time)
            time_text = FONT.render(f"Time: {elapsed_time}s", True, (255, 255, 255))
            screen.blit(time_text, (10, 10))  # قرار دادن تایمر در گوشه بالای سمت چپ

            score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (350, 10))  # قرار دادن امتیاز در گوشه بالا سمت راست

def handle_game_events(board, start_time, data, score):
    """مدیریت رویدادهای بازی."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game_data(board, start_time, data, score)
            pygame.quit()
            sys.exit() 
        elif event.type == pygame.KEYDOWN :
            new_board = None
            if event.key == pygame.K_ESCAPE : # pressing the key esc
                save_game_data(board , start_time , data , score)
                homepage_loop()
            elif event.key == pygame.K_LEFT:
                new_board, score = move_left(board)
            elif event.key == pygame.K_RIGHT:
                new_board, score = move_right(board)
            elif event.key == pygame.K_UP:
                new_board, score = move_up(board)
            elif event.key == pygame.K_DOWN:
                new_board, score = move_down(board)
            
            if new_board and new_board != board:
                board = new_board
                fill_board(board)
        
    return board, score

def save_game_data(board, start_time, data, score):
    """ذخیره اطلاعات بازی (امتیاز و زمان)."""
    elapsed_time = int(time.time() - start_time)  # محاسبه زمان سپری شده
    # ساخت رکورد جدید برای ذخیره در فایل
    new_record = {
        "score": score,
        "time": elapsed_time 
    }

    # اضافه کردن رکورد جدید به داده‌های موجود (data)
    data.append(new_record)

    save_data(data)  # استفاده از تابع save_data برای ذخیره رکوردها

    # ذخیره وضعیت بازی (در صورت نیاز به بازگشت به صفحه اصلی)
    game_state = {
        "board": board,
        "elapsed_time": elapsed_time,
        "score": score,
    }

    # ذخیره وضعیت بازی در فایل JSON
    with open("save_data.json", "w") as file:
        json.dump(game_state, file)

def check_game_status(board, start_time, score):
    """بررسی وضعیت بازی (برد یا باخت)."""
    data = load_data()  # بارگذاری داده‌ها از فایل
    if win(board):
        save_game_data(board, start_time, data, score)  # ذخیره وضعیت بازی در صورت نیاز
        show_message(screen, "you win!")
        homepage_loop()  # بازگشت به منو
    elif board_completed(board) and any_move(board):
        save_game_data(board, start_time, data, score)  # ذخیره وضعیت بازی در صورت نیاز
        show_message(screen, "game over!")
        homepage_loop()  # بازگشت به منو
        
def game_loop(board=None):
    """حلقه اصلی بازی."""
    try:
        with open("save_data.json", "r") as file:
            game_state = json.load(file)
            board = game_state["board"]
            elapsed_time = game_state.get("elapsed_time", 0)
            score = game_state["score"]
            start_time = time.time() - elapsed_time
    except FileNotFoundError:
        board = set_board()
        start_time = time.time()
        score = 0

    data = load_data()

    while True:
        draw_board(screen, board, TILE_COLORS, start_time, score)
        pygame.display.update()
        check_game_status(board, start_time, score)  # بررسی برد یا باخت
        board, score = handle_game_events(board, start_time, data, score)

def get_selected_option():
    """تعیین گزینه انتخاب‌شده توسط کاربر از منو."""
    mouse_pos = pygame.mouse.get_pos()
    menu_options = ["New Game","Continue", "Records", "Quit"]
    
    # موقعیت Y هر گزینه منو
    for i, option in enumerate(menu_options):
        option_y = INFO_BAR_HEIGHT + 100 + i * 50  # محاسبه موقعیت Y گزینه
        if (WINDOW_SIZE // 2 - 100 <= mouse_pos[0] <= WINDOW_SIZE // 2 + 100) and \
           (option_y - 25 <= mouse_pos[1] <= option_y + 25):
            return option
    return None

def homepage_loop():
    """حلقه اصلی صفحه اصلی بازی."""
    setup_music()

    while True:
        screen.fill((220 , 224 , 245))
        display_title("2048")
        timer.tick(fps)

        display_menu(["New Game","Continue", "Records", "Quit"])
        display_music_status(music_enabled)
        pygame.display.update()

        handle_homepage_events()

def setup_music():
    """تنظیمات موسیقی."""
    global music_enabled
    music_enabled = load_music_state()  

    if music_enabled:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("Dmusic.mp3")
            pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

    return music_enabled

    
def draw_button(screen, text, font, color, hover_color, rect, hovered):
    """رسم دکمه با قابلیت hover."""
    if hovered:
        pygame.draw.rect(screen, hover_color, rect)
    else:
        pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def display_title(title, font_size=72):
    """نمایش عنوان بازی."""
    font = pygame.font.Font(None, font_size)
    text = font.render(title, True, (255 , 204 , 0))
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, (INFO_BAR_HEIGHT // 2) +40))
    screen.blit(text, text_rect)    

def display_menu(menu_options):
    """نمایش گزینه‌های منو."""
    font = pygame.font.Font(None, 48)
    mouse_x , mouse_y = pygame.mouse.get_pos()

    for i, option in enumerate(menu_options):
        text = font.render(option, True, (204 , 153 , 0))
        text_rect = text.get_rect(center=(height/2 ,INFO_BAR_HEIGHT + 100 + i * 50))
        if text_rect.collidepoint(mouse_x , mouse_y) :
            text = font.render(option , True , (0 , 0 , 250))
        screen.blit(text, text_rect)

def display_music_status(music_enabled):
    """نمایش وضعیت موسیقی با قابلیت هاور و تغییر رنگ."""
    font = pygame.font.Font(None, 48)  # یکسان‌سازی فونت با منو
    mouse_x, mouse_y = pygame.mouse.get_pos()  # دریافت موقعیت ماوس

    # محاسبه محل متن موسیقی
    quit_y = INFO_BAR_HEIGHT + 100 + 3 * 50  # Quit در موقعیت i=3 است
    music_y = quit_y + 50  # دکمه‌ی موسیقی را 50 پیکسل پایین‌تر قرار می‌دهیم

    # محاسبه مستطیل متن برای تشخیص هاور
    status_text = f"Music: {'ON' if music_enabled else 'OFF'}"
    status_text_render = font.render(status_text, True, (204 , 153 , 0))  # رنگ پیش‌فرض
    status_text_rect = status_text_render.get_rect(center=(WINDOW_SIZE // 2, music_y + 40))

    # بررسی هاور
    if status_text_rect.collidepoint(mouse_x, mouse_y):
        status_text_render = font.render(status_text, True, (0, 0, 250))  # تغییر رنگ به آبی
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # تغییر نشانگر ماوس به حالت کلیک
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # بازگرداندن نشانگر ماوس

    screen.blit(status_text_render, status_text_rect)  # نمایش متن موسیقی

    return status_text_rect  # برای بررسی کلیک روی دکمه

def handle_homepage_events():
    """مدیریت رویدادهای کاربر.""" 
    global music_enabled 

    button_rect = display_music_status(music_enabled)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # بررسی کلیک روی دکمه موسیقی
            if button_rect.collidepoint(mouse_x, mouse_y):

                music_enabled = not music_enabled
                save_music_state(music_enabled)
                setup_music()

            handle_menu_selection(get_selected_option())

def records_loop():
    """حلقه صفحه رکوردها."""
    while True:
        screen.fill((220, 224, 245))  # پس‌زمینه‌ی صفحه رکوردها
        back_button_rect = display_back_button()  # رسم دکمه‌ی "Back"
        display_records(load_data())  
        pygame.display.update()  # بروزرسانی صفحه

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):  # اگر روی "Back" کلیک شد
                    homepage_loop()  # بازگشت به صفحه اصلی

def display_records(top_scores):
    """نمایش رکوردها (5 رکورد برتر بر اساس امتیاز و زمان)."""
    screen.fill((220, 224, 245))  # پس‌زمینه مشابه صفحه اصلی

    # نمایش دکمه‌ی برگشت
    back_button_rect = display_back_button()

    # تنظیمات فونت
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)
    
    # عنوان صفحه رکوردها
    title_text = title_font.render("Top 5 Scores", True, (0, 0, 0))
    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))

    # مرتب‌سازی رکوردها:
    top_scores_sorted = sorted(top_scores, key=lambda x: (-x['score'], x['time']))

    start_y = 150  # موقعیت شروع نمایش رکوردها
    for i, record in enumerate(top_scores_sorted[:5]):  
        score = record.get('score', 0)
        time = record.get('time', 0)
        score_text = font.render(f"{i+1}. Score: {score} - Time: {time}s", True, (0, 0, 0), (255, 204, 0))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, start_y + i * 50))
    
    pygame.display.update()  # بروزرسانی صفحه
    
    return back_button_rect  # موقعیت دکمه را برمی‌گرداند

def display_back_button() :
    """نمایش دکمه برگشت به خانه و بررسی کلیک روی آن."""
    font = pygame.font.Font(None, 48)
    mouse_x, mouse_y = pygame.mouse.get_pos()  # دریافت موقعیت ماوس

    # تعیین رنگ دکمه (تغییر رنگ هنگام هاور)
    normal_color = (255, 255, 255)  # رنگ عادی
    hover_color = (255, 204, 0)  # رنگ هنگام هاور

    button_rect = pygame.Rect(WINDOW_SIZE // 2 - 50, WINDOW_SIZE // 2 + 100, 100, 50)  # مستطیل دکمه

    # بررسی اگر ماوس روی دکمه باشد، رنگ تغییر کند
    if button_rect.collidepoint(mouse_x, mouse_y):
        color = hover_color
    else:
        color = normal_color

    button_text = font.render("Back", True, color)
    button_text_rect = button_text.get_rect(center=button_rect.center)

    pygame.draw.rect(screen, (50, 50, 50), button_rect, border_radius=10)  # رسم مستطیل دکمه
    screen.blit(button_text, button_text_rect)  # نمایش متن دکمه


    return button_rect  # موقعیت دکمه را برمی‌گرداند

def handle_records_events():
    """مدیریت رویدادهای صفحه رکوردها (مانند بستن پنجره)."""
    back_button_rect = display_back_button()  # دکمه را نمایش بده و مستطیل آن را بگیر

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if back_button_rect.collidepoint(event.pos):  # بررسی کلیک روی دکمه
                homepage_loop()  # بازگشت به صفحه اصلی

def show_message(screen, message):
    """نمایش پیام برد یا باخت با افکت محو شدن (Fade-in & Fade-out)."""
    overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
    overlay.fill((0, 0, 0))  # رنگ پس‌زمینه سیاه
    font = pygame.font.Font(None, 90)  # بزرگ‌تر کردن فونت
    text = font.render(message, True, (255, 255, 0))  # رنگ زرد برای جلب توجه
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))

# مرحله اول: صفحه کمی تیره شود و همزمان پیام نمایش داده شود
    overlay.set_alpha(120)  # تنظیم شفافیت برای تاریک شدن ملایم
    screen.blit(overlay, (0, 0))
    screen.blit(text, text_rect)
    pygame.display.update()
    time.sleep(2)  # نمایش پیام برای 2 ثانیه
    
    # مرحله دوم: اجرای افکت fade-in (ظاهر شدن پیام به‌آرامی)
    for alpha in range(0, 256, 15):  
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(50)
    
    time.sleep(1)  # ثابت ماندن پیام برای 1 ثانیه
    
    # مرحله سوم: اجرای افکت fade-out (محو شدن پیام به‌آرامی)
    for alpha in range(255, -1, -50):  
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(50)

def handle_menu_selection(selected_option):
    """مدیریت انتخاب گزینه."""
    if selected_option == "New Game":
        if os.path.exists("save_data.json") :
            os.remove("save_data.json")

        game_loop()
    elif selected_option == "Records":
        records_loop()
    elif selected_option == "Quit":
        pygame.quit()
        sys.exit()
    elif selected_option == "Continue" :
        game_loop()