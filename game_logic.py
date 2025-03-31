import random
def set_board():
    """ایجاد صفحه بازی با اندازه مشخص و پر کردن دو خانه اول."""
    global score 
    score = 0 
    board = [[0] * 4 for _ in range(4)]
    fill_board(board)
    fill_board(board)
    return board

def fill_board(board):
    """پر کردن خانه‌های خالی"""
    empty_cells = [(row, column) for row in range(4) for column in range(4) if board[row][column] == 0]
    if empty_cells:  # اگر خانه خالی وجود داشت
        row, column = random.choice(empty_cells)  # یکی از خانه‌های خالی را به صورت تصادفی انتخاب می‌کند
        board[row][column] = 2 if random.random() < 0.9 else 4

def compress(board):
    """فشرده‌سازی صفحه (حذف صفرها و جابجایی اعداد به سمت چپ)"""
    new_board = [[0] * 4 for _ in range(4)]
    for row in range(4):
        pos = 0
        for column in range(4):
            if board[row][column] != 0:
                new_board[row][pos] = board[row][column]
                pos += 1
    return new_board

score = 0  # مقداردهی اولیه امتیاز
def merge(board, score):
    """ادغام اعداد مشابه در هر ردیف"""
    for row in range(4):
        for column in range(3):
            if board[row][column] == board[row][column + 1] and board[row][column] != 0:
                board[row][column] *= 2
                board[row][column + 1] = 0
                score += board[row][column]
    return board, score

def reverse(board):
    """معکوس کردن ترتیب خانه‌ها"""
    return [row[::-1] for row in board]

def transpose(board):
    """جابجا کردن سطرها و ستون‌ها"""
    new_board = [[0] * 4 for _ in range(4)]
    for row in range(4):
        for column in range(4):
            new_board[row][column] = board[column][row]
    return new_board

def move_left(board):
    """حرکت به چپ"""
    global score
    compressed = compress(board)
    merged, score = merge(compressed, score)
    final_board = compress(merged)
    return final_board, score

def move_right(board):
    """حرکت به راست"""
    reversed_board = reverse(board)
    moved_board, score = move_left(reversed_board)
    return reverse(moved_board), score

def move_up(board):
    """حرکت به بالا"""
    transposed_board = transpose(board)
    moved_board, score = move_left(transposed_board)
    return transpose(moved_board), score

def move_down(board):
    """حرکت به پایین"""
    transposed_board = transpose(board)
    moved_board, score = move_right(transposed_board)
    return transpose(moved_board),score

def board_completed(board):
    """بررسی پر شدن صفحه"""
    for row in board:
        if 0 in row:
            return False
    return True

def any_move(board):
    """بررسی امکان حرکت بیشتر"""
    for row in range(4):
        for column in range(3):
            if board[row][column] == board[row][column + 1]:
                return False
    for row in range(3):
        for column in range(4):
            if board[row][column] == board[row + 1][column]:
                return False
    return True

def win(board):
    """بررسی برد"""
    for row in board:
        if 2048 in row:
            return True
    return False
