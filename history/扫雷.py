import random


def init_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def count_mines(board, row, col):
    mines = 0
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(board) and 0 <= c < len(board[0]):
            mines += 1 if board[r][c] == "M" else 0
    return mines


def print_board(board, revealed, game_over=False):
    cols = len(board[0])
    print("\n    " + " ".join(f"{i+1:1}" for i in range(cols)))
    print("  +" + "--" * cols + "-+")
    for i in range(len(board)):
        print(f"{i+1:1} |", end="")
        for j in range(cols):
            if game_over and board[i][j] == "M":
                print(" M", end="")
            elif revealed[i][j]:
                num = count_mines(board, i, j)
                print(f" {num if num > 0 else ' '}", end="")
            else:
                print(" ?", end="")
        print(" |")
    print("  +" + "--" * cols + "-+")


def reveal_empty(board, revealed, row, col):
    if not (0 <= row < len(board)) or not (0 <= col < len(board[0])) or revealed[row][col]:
        return
    revealed[row][col] = True
    if count_mines(board, row, col) != 0:
        return
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        reveal_empty(board, revealed, row + dr, col + dc)


def minesweeper():
    rows, cols, mines = 8, 8, 10
    board = init_board(rows, cols)
    revealed = [[False] * cols for _ in range(rows)]
    first_click = True

    print("===== 扫雷游戏 =====")
    print(f"输入行列号（1-{rows}），用空格分隔")
    print("例如：3 4 表示第3行第4列")

    while True:
        print_board(board, revealed)
        # 内部循环处理输入直到正确
        while True:
            try:
                input_str = input("请输入行列号：")
                row, col = map(int, input_str.split())
                if not (1 <= row <= rows and 1 <= col <= cols):
                    print(f"请输入1-{rows}范围内的数字！")
                else:
                    # 转换为0-based索引
                    row -= 1
                    col -= 1
                    break
            except:
                print("请输入两个整数，用空格分隔！")

        # 首次点击特殊处理
        if first_click:
            first_click = False
            # 生成安全的雷区
            safe_pos = row * cols + col
            all_positions = [i for i in range(rows * cols) if i != safe_pos]
            mine_positions = random.sample(all_positions, mines)
            board = init_board(rows, cols)
            for pos in mine_positions:
                board[pos // cols][pos % cols] = "M"

        if board[row][col] == "M":
            print_board(board, revealed, game_over=True)
            print("游戏结束！你触发了一个地雷！")
            break

        reveal_empty(board, revealed, row, col)

        if sum(sum(row) for row in revealed) == rows * cols - mines:
            print_board(board, revealed, game_over=True)
            print("恭喜！你找到了所有安全区域！")
            break


if __name__ == "__main__":
    minesweeper()