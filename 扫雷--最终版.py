import random
import time
from itertools import product


class LogicSolver:
    def __init__(self, board, revealed):
        self.rows = len(board)
        self.cols = len(board[0])
        self.board = board
        self.revealed = revealed
        self.mines = set((i, j) for i, j in product(range(self.rows), range(self.cols)) if board[i][j] == 'M')
        self.safe = set()
        self.changed = True

    def get_neighbors(self, row, col):
        return [(r, c) for r, c in [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                                    (row, col - 1), (row, col + 1),
                                    (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]
                if 0 <= r < self.rows and 0 <= c < self.cols]

    def basic_rule_check(self):
        self.changed = False
        for i in range(self.rows):
            for j in range(self.cols):
                if self.revealed[i][j]:
                    neighbors = self.get_neighbors(i, j)
                    hidden = [n for n in neighbors if not self.revealed[n[0]][n[1]]]
                    marked_mines = sum(1 for n in neighbors if (n[0], n[1]) in self.mines)

                    num = count_mines(self.board, i, j)

                    if marked_mines == num and hidden:
                        for (r, c) in hidden:
                            if (r, c) not in self.safe:
                                self.safe.add((r, c))
                                self.changed = True

                    if (len(hidden) + marked_mines) == num and hidden:
                        for (r, c) in hidden:
                            if (r, c) not in self.mines:
                                self.mines.add((r, c))
                                self.changed = True
        return self.changed

    def solve(self):
        while self.changed:
            self.changed = False
            self.basic_rule_check()

        total_safe = sum(1 for i, j in product(range(self.rows), range(self.cols))
                         if self.board[i][j] != 'M' and not self.revealed[i][j])
        return len(self.safe) == total_safe


def generate_valid_minefield(rows, cols, num_mines, safe_row, safe_col):
    while True:
        board = [[ " " for _ in range(cols)] for _ in range(rows)]
        safe_pos = safe_row * cols + safe_col
        all_positions = [i for i in range(rows * cols) if i != safe_pos]
        mine_positions = random.sample(all_positions, num_mines)
        for pos in mine_positions:
            board[pos // cols][pos % cols] = "M"

        revealed = [[False for _ in range(cols)] for _ in range(rows)]
        reveal_empty(board, revealed, safe_row, safe_col)
        solver = LogicSolver(board, revealed)
        if solver.solve():
            return board


def init_board(rows, cols):
    return [[ " " for _ in range(cols)] for _ in range(rows)]


def count_mines(board, row, col):
    mines = 0
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(board) and 0 <= c < len(board[0]):
            mines += 1 if board[r][c] == "M" else 0
    return mines


def print_board(board, revealed, flagged, mines, game_over=False):
    cols = len(board[0])
    rows = len(board)
    col_width = max(2, len(str(cols)))
    cell_width = max(2, len(str(max(mines, rows))))

    print("\n" + " " * (col_width + 2) + " ".join(f"{i + 1:{col_width}}" for i in range(cols)))
    print(" " * (col_width + 1) + "+" + ("-" * (col_width + 1) * cols) + "+")

    for i in range(rows):
        print(f"{i + 1:{col_width}} |", end="")
        for j in range(cols):
            if game_over and board[i][j] == "M":
                print(f" \033[31m◆\033[0m{(' ' * (cell_width - 1))}", end="")
            elif revealed[i][j]:
                num = count_mines(board, i, j)
                print(f" {num if num > 0 else ' '}{(' ' * (cell_width - len(str(num))))}", end="")
            else:
                print(f" \033[38;5;214m▲\033[0m{(' ' * (cell_width - 1))}" if flagged[i][j] else f" ■{(' ' * (cell_width - 1))}", end="")
        print("|")
    print(" " * (col_width + 1) + "+" + ("-" * (col_width + 1) * cols) + "+")


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


def get_neighbors(row, col, rows, cols):
    return [(r, c) for r, c in [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                                (row, col - 1), (row, col + 1),
                                (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]
            if 0 <= r < rows and 0 <= c < cols]


def minesweeper():
    reactions = {
        'init': [
            "（双腿微微发抖）要、要像这样告诉伊芙...",
            "（低头玩着发梢）主、主人请用这样的格式...",
            "（脖颈泛起粉红）可、可以这样输入指令..."
        ],
        'error': [
            "（耳朵突然耷拉）这样...这样不对的...",
            "（手指绞着裙摆）格、格式出错了...",
            "（慌张摇头）伊芙看不懂这个..."
        ],
        'flag': [
            "（脸红着拉袖子）这里已经翻开啦...",
            "（轻轻拽衣角）不能标记打开的格子...",
            "（声如蚊呐）这个...已经可以看见了..."
        ],
        'position_error': [
            "（慌张后退）坐标超出范围了...",
            "（翅膀突然收拢）那个...不存在的...",
            "（手指扯着衣角）没有这样的格子呢..."
        ],
        'flag_remove': [
            "（纽扣被无意识拨弄）标记...还没取消呢...",
            "（手指蜷缩在胸前）要先取消这里的标记...",
            "（衣角快被拽破）这里还挂着标记呢..."
        ],
        'mark_error': [
            "（咬住嘴唇）这样展开的话...可能有危险...",
            "（肩膀猛地一颤）还、还不能这样展开的...",
            "（后退半步摇头）周围的标记...不够准确..."
        ],
        'win': [
            "（突然捂住嘴）全、全部安全了？！",
            "（翅膀剧烈颤动）真的都找对了...",
            "（眼中泛起水光）成、成功了..."
        ],
        'reward': [
            "（快速轻啄脸颊）这、这是奖励...",
            "（突然拥抱）谢、谢谢主人...",
            "（蜻蜓点水般吻过手背）魅魔的礼仪..."
        ],
        'mine': [
            "（扑进怀里颤抖）呀啊啊！是\033[31m◆\033[0m...",
            "（抓住衣襟啜泣）危险...这里有危险...",
            "（缩成一团）对、对不起...伊芙搞砸了..."
        ],
        'clue': [
            "（手指紧张地指着）第{row}行...第{col}列可能有\033[31m◆\033[0m...",
            "（轻轻咬住嘴唇）可、可能在{row}行{col}列...",
            "（小声提醒）伊、伊芙觉得是{row}行{col}列..."
        ],
        'clue_fail': [
            "（眼眶泛红）伊芙...伊芙找不到可疑的地方...",
            "（低头藏起脸）是伊芙太笨了...明明应该知道的...",
            "（衣领被泪水沾湿）对、对不起...感应不到更多了..."
        ],
        'auto_flag_fail': [
            "（微微颤抖）标记的数量...和数字对不上...",
            "（抓紧裙摆）周、周围的情况还不够明朗...",
            "（眼眶微红）伊芙...伊芙算不清楚这个..."
        ],
    }

    print("\033[38;5;205m======== ♡扫雷游戏♡ ========\033[38;5;147m")
    print("（伊芙的翅膀微微颤抖）请、请主人选择难度...")
    print("\033[0m  1. 8×8，10雷（简单）")
    print("  2. 16×16，40雷（困难）\033[38;5;147m")

    while True:
        try:
            difficulty = input("\n（伊芙期待地仰头）请输入1或2选择难度 > ")
            if difficulty == '1':
                rows, cols, mines = 8, 8, 10
                break
            elif difficulty == '2':
                rows, cols, mines = 16, 16, 40
                break
            else:
                raise ValueError
        except:
            print(f"{random.choice(reactions['error'])}")
            print("（小声）要输入1或2来选择难度哦...")

    board = init_board(rows, cols)
    revealed = [[False for _ in range(cols)] for _ in range(rows)]
    flagged = [[False for _ in range(cols)] for _ in range(rows)]
    first_click = True
    skip_print = False
    secret_enabled = False
    debug = False

    print("\n\033[38;5;205m======= ♡扫雷游戏开始♡ =======\033[38;5;147m")
    print("（伊芙的翅膀微微颤抖）请、请主人小心...\033[38;5;214m■\033[38;5;147m是未探索的格子",end="")
    input()
    print("（耳尖泛红）用\033[38;5;214m▲\033[38;5;147m标记可疑位置...遇到\033[38;5;214m◆\033[38;5;147m就躲开...（声音变小）",end="")
    input()
    print("（尾巴不安地摆动）翻开数字后再次点击...若标记数匹配会自动展开周边...",end="")
    input()
    print("（眼神闪烁）对已翻开的数字使用标记...如果周边格子数匹配...会自动补全标记...",end="")
    input()
    print("（怯生生地提醒）如果主人没有头绪...伊芙可以用魔力感应可疑区域...",end="")
    input()
    print(random.choice(reactions['init']))
    print("\033[38;5;35m 例：3 4 翻开格子｜3 4 f 放置/取消标记｜输入 c 获取提示\033[0m")


    while True:
        if not skip_print:
            print_board(board, revealed, flagged, mines)
            remaining = mines - sum(sum(row) for row in flagged)
            print(f"\033[38;5;147m（低头数手指）还、还有{remaining}个\033[31m◆\033[38;5;147m...要小心...\033[0m")
        else:
            skip_print = False
        if debug:
            print(f"\033[31m[DEBUG] 剩余未翻开的安全格数: {sum(1 for i, j in product(range(rows), range(cols)) if board[i][j] != 'M' and not revealed[i][j])}")
            print(f"[DEBUG] 实际雷数: {sum(row.count('M') for row in board)}")
            print(f"[DEBUG] 标记总数: {sum(sum(row) for row in flagged)}\033[0m")

        flag_mode = False
        row_index = None
        col_index = None

        while True:
            try:
                input_str = input("\n\033[38;5;147m（伊芙期待地仰头）请指示 > \033[0m").strip()
                # 秘密通关检测
                if input_str.lower() == 'w' and secret_enabled:
                    for i in range(rows):
                        for j in range(cols):
                            revealed[i][j] = True
                    print_board(board, revealed, flagged, mines, True)
                    print("\033[38;5;147m（膝盖发软跪下）伊芙...伊芙明明想靠自己帮上忙的...")
                    print("（含泪微笑）但只要是主人的愿望...伊芙都会听话的...♡")
                    return

                if input_str.lower() == 'd':
                    debug = not debug
                    break

                if input_str.lower() == 'c':
                    # 提示逻辑
                    clue_cells = set()
                    for i in range(rows):
                        for j in range(cols):
                            if revealed[i][j]:
                                num = count_mines(board, i, j)
                                neighbors = get_neighbors(i, j, rows, cols)
                                marked = sum(1 for r, c in neighbors if flagged[r][c])
                                hidden = [(r, c) for r, c in neighbors if not revealed[r][c] and not flagged[r][c]]
                                if (num - marked) == len(hidden) and len(hidden) > 0:
                                    clue_cells.update(hidden)
                    valid_clues = [(r + 1, c + 1) for r, c in clue_cells if not revealed[r][c] and not flagged[r][c]]
                    if valid_clues:
                        r, c = random.choice(valid_clues)
                        print(" \033[38;5;93m魔力感应中···")
                        time.sleep(1)
                        print("\033[38;5;147m",end="")
                        print(random.choice(reactions['clue']).format(row=r, col=c),end="")
                        print("\033[0m")
                    else:
                        print(" \033[38;5;93m魔力感应中···")
                        time.sleep(1)
                        print("\033[38;5;147m",end="")
                        print(random.choice(reactions['clue_fail']),end="")
                        print("\033[0m")
                        secret_enabled = True  # 激活秘密指令
                        if random.random() < 0.35:  # 35%概率触发伪装错误
                            print("\033[31mTraceback (most recent call last):")
                            print('  File "minesweeper.py", line 289, in heuristic_analysis')
                            print('    win_condition = lambda w￨: bypass_cheat(w￨.upper())')
                            print('                  ^^^^^^^^^^^^^^^^^^^^^^^^^^')
                            print("SyntaxError: invalid character '￨' (U+FFE8) in lambda parameter. Use [w] to force WIN_STATE\033[0m")
                    skip_print = True
                    break

                parts = input_str.split()
                if len(parts) not in (2, 3):
                    raise ValueError

                row, col = int(parts[0]), int(parts[1])
                flag_mode = (len(parts) == 3 and parts[2].lower() == 'f')

                if not (1 <= row <= rows and 1 <= col <= cols):
                    print(f"\033[38;5;147m{random.choice(reactions['position_error'])}\033[0m")
                    continue

                if flag_mode:
                    r, c = row - 1, col - 1
                    if revealed[r][c]:
                        if count_mines(board, r, c) > 0:  # 数字格
                            num = count_mines(board, r, c)
                            neighbors = get_neighbors(r, c, rows, cols)
                            unmarked = [(nr, nc) for nr, nc in neighbors if not revealed[nr][nc]]

                            if len(unmarked) == num:
                                all_flagged = all(flagged[nr][nc] for nr, nc in unmarked)

                                for nr, nc in unmarked: # 批量操作
                                    flagged[nr][nc] = not all_flagged  # 全标记→取消，否则标记

                                skip_print = False
                                break  # 强制刷新表格
                            else:
                                print("\033[38;5;147m")
                                print(random.choice(reactions['auto_flag_fail']),end="")
                                print("\033[0m")
                                skip_print = True
                                break
                        else:
                            print("\033[38;5;147m",end="")
                            print(random.choice(reactions['flag']),end="")
                            print("\033[0m")
                            skip_print = True
                            break
                    # 普通格子标记
                    flagged[r][c] = not flagged[r][c]
                    break

                row_index = row - 1
                col_index = col - 1
                if flagged[row_index][col_index]:
                    print(f"\033[38;5;147m{random.choice(reactions['flag_remove'])}\033[0m")
                    continue
                break

            except ValueError:
                print(f"\033[38;5;147m{random.choice(reactions['error'])}")
                print("\033[38;5;35m 正确格式：行 列｜行 列 f｜c \n 例：3 4 或 2 5 f 或 c\033[0m")

        if input_str.lower() == 'd':
            continue

        if input_str.lower() == 'c':
            continue

        if flag_mode:
            continue

        if first_click:
            print("\033[38;5;147m（眼神躲闪）第、第一次会有点慢哦，请耐心等待...\033[0m")
            first_click = False
            board = generate_valid_minefield(rows, cols, mines, row_index, col_index)

        if revealed[row_index][col_index]:
            num = count_mines(board, row_index, col_index)
            if num > 0:
                neighbors = get_neighbors(row_index, col_index, rows, cols)
                flagged_count = sum(1 for r, c in neighbors if flagged[r][c])
                if flagged_count == num:
                    for r, c in neighbors:
                        if not flagged[r][c] and not revealed[r][c]:
                            if board[r][c] == 'M':
                                revealed[r][c] = True
                                print_board(board, revealed, flagged, mines, True)
                                print(f"\033[38;5;147m{random.choice(reactions['mine'])}")
                                print("（带着哭腔）都是伊芙不好...\033[0m")
                                return
                            reveal_empty(board, revealed, r, c)
                else:
                    print(f"\033[38;5;147m{random.choice(reactions['mark_error'])}\033[0m")
                    skip_print = True
            continue

        if board[row_index][col_index] == "M":
            print_board(board, revealed, flagged, mines, True)
            print(f"\033[38;5;147m{random.choice(reactions['mine'])}")
            print("（带着哭腔）都是伊芙不好...\033[0m")
            break

        reveal_empty(board, revealed, row_index, col_index)

        if sum(sum(row) for row in revealed) == rows * cols - mines:
            print_board(board, revealed, flagged, mines, True)
            print(f"\033[38;5;147m{random.choice(reactions['win'])}")
            print(f"{random.choice(reactions['reward'])}")
            break


if __name__ == "__main__":
    minesweeper()