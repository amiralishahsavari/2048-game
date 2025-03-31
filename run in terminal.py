import curses
import random
from game_logic import*
def draw_board(stdscr, board, score):
    """رسم صفحه بازی"""
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    for r in range(4):
        for c in range(4):
            value = str(board[r][c]) if board[r][c] != 0 else '.'
            row_pos = r * 2
            col_pos = c * 7
            if row_pos < height - 1 and col_pos < width - 7:
                stdscr.addstr(row_pos, col_pos, value, curses.color_pair(1))  # نمایش مقادیر در موقعیت مناسب
    stdscr.addstr(height - 2, 0, f"Score: {score}", curses.color_pair(1))  # نمایش امتیاز در پایین صفحه
    stdscr.refresh()

def main(stdscr):
    """حلقه اصلی بازی و مدیریت ورودی کاربر"""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    board = set_board()
    score = 0  # مقداردهی اولیه امتیاز
    draw_board(stdscr, board, score)
    
    height, width = stdscr.getmaxyx()

    while True:
        key = stdscr.getch()
        new_board = None
        if key == curses.KEY_LEFT:
            new_board, score = move_left(board)
        elif key == curses.KEY_RIGHT:
            new_board, score = move_right(board)
        elif key == curses.KEY_UP:
            new_board, score = move_up(board)
        elif key == curses.KEY_DOWN:
            new_board, score = move_down(board)
        
        if new_board and new_board != board:
            board = new_board
            fill_board(board)  # پر کردن خانه جدید

        draw_board(stdscr, board, score)
        
        # بررسی وضعیت بازی
        if any_move(board) == False and board_completed(board):
            # اطمینان از اینکه متن در داخل ترمینال قرار دارد
            if height > 10 and width > 20:  # ابعاد ترمینال را چک می‌کنیم
                stdscr.addstr(0, 0, "Game Over!", curses.color_pair(1))
                stdscr.addstr(1, 0, f"Your score: {score}", curses.color_pair(1))  # نمایش امتیاز
            stdscr.refresh()
            stdscr.getch()
            break

# اجرای بازی با curses
curses.wrapper(main)
