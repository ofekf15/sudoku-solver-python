import random

SUCCESS_FINISH = "SUCCESS_FINISH"
FINISH_FAILURE = "FINISH_FAILURE"
NOT_FINISH = "NOT_FINISH"
Board_not_legit = "Board is not legit!"



def crate_empty_board ():               # יוצר ומחזיר לוח ריק
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append(-1)
        board.append(row)
    return board


def has_duplicates(sudoku_board):                   # פונקצייה בודקת האם יש כפיליות בכל הלוח
    # בדיקת כפילויות בשורות
    for i in range(9):
        seen = set()
        for j in range(9):
            num = sudoku_board[i][j]
            if num != -1:
                if num in seen:
                    return True
                seen.add(num)


    for j in range(9):                          #בדיקת כפיליות בטור ובשורה
        seen = set()
        for i in range(9):
            num = sudoku_board[i][j]
            if num != -1:
                if num in seen:
                    return True
                seen.add(num)

    for box_row in range(0, 9, 3):                            # בדיקת כפילויות בריבועים 3x3
        for box_col in range(0, 9, 3):
            seen = set()
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    num = sudoku_board[i][j]
                    if num != -1:
                        if num in seen:
                            return True
                        seen.add(num)
    return False


def full_board(board):                  # בודקת אם הלוח מלא
    for i in range(9):
        for j in range(9):
            if board[i][j] == -1:
                return False
    return True


def remove_possible_square(possibilities, num, row, col):           # מסיר את האופציות הלא רלוונטיות בריבוע 3X3
    square_row = row - row % 3
    square_col = col - col % 3
    for i in range(square_row, square_row + 3):
        for j in range(square_col, square_col + 3):
            if possibilities[i][j] is not None and num in possibilities[i][j]:
                possibilities[i][j].remove(num)
    return possibilities


def one_stage(sudoku_board, possibilities):                 #פונקציה שממלאה את הלוח עד לוח תקין או לא, או עד האופציה האחרונה
    while True:
        changed_something = False
        min_len = 10
        coordinate = (0, 0)

        for i in range(9):
            for j in range(9):

                if sudoku_board[i][j] == -1:                #אם משבצת ריקה ואין אופציות נחזיר פייל
                    if possibilities[i][j] is None:
                        return FINISH_FAILURE
                    elif len(possibilities[i][j]) == 1:         #אם יש אופציה אחת למילוי משבצת נעדכן זאת
                        num = possibilities[i][j][0]
                        sudoku_board[i][j] = num
                        possibilities[i][j] = []                # מאפסים את האפשרויות לאחר מילוי
                        changed_something = True

                                                            # הסרת המספר מהאפשרויות בשורה, עמודה וריבוע
                        for col in range(9):
                            if num in possibilities[i][col]:
                                possibilities[i][col].remove(num)
                        for row in range(9):
                            if num in possibilities[row][j]:
                                possibilities[row][j].remove(num)
                        remove_possible_square(possibilities, num, i, j)
                    elif 0 < len(possibilities[i][j]) < min_len:
                        min_len = len(possibilities[i][j])
                        coordinate = (i, j)

        if not changed_something:                       # אם לא נעשה שינוי

            if full_board(sudoku_board):                   #נבדוק האם לוח מלא
                if has_duplicates(sudoku_board):            # אם יש כפיליות נחזיר בהתאם
                    return FINISH_FAILURE
                else:
                    return SUCCESS_FINISH                   #אחרת בהתאם
            return coordinate, NOT_FINISH


def fill_board(sudoku_board, possibilities):
    digit = 10
    result = one_stage(sudoku_board, possibilities)
    if result == SUCCESS_FINISH:                        #אם הלוח כבר טוב
        return SUCCESS_FINISH
    elif result == FINISH_FAILURE:                        #אם הלוח כבר נכשל
        return FINISH_FAILURE
    else:
        coordinate = result[0]
        row, col = coordinate


        if possibilities[row][col] is None or len(possibilities[row][col]) == 0:        #אם אין אופציות נחזיר בהתאם
            return FINISH_FAILURE


        while digit not in possibilities[row][col]:                 # קלט מהמשתמש עד שיבחר מספר הנמצא ברשימת האפשרויות
            digit_str = input("Enter a number from this list " + str(possibilities[row][col]) + ": ")
            if digit_str.isdigit():                             #נבדוק שזה באמת מספר
                digit = int(digit_str)
            else:
                print("its not a number")

        sudoku_board[row][col] = digit                      # מעדכן את הלוח בפועל עם המספר שהמשתמש בחר
        possibilities[row][col] = []                        # מרוקן את אפשרויות המשבצת כי היא כבר מולאה


        for c in range(9):                                     # הסרת המספר מהאפשרויות בשורה
            if digit in possibilities[row][c]:
                possibilities[row][c].remove(digit)

        for r in range(9):                                      # הסרת האפשרויות בטור
            if digit in possibilities[r][col]:
                possibilities[r][col].remove(digit)

        remove_possible_square(possibilities, digit, row, col)      # הסרת אפשרויות מהריבוע

        if has_duplicates(sudoku_board):                            #בדיקת כפיליות
            return FINISH_FAILURE

        return fill_board(sudoku_board, possibilities)


def options(sudoku_board, loc):                 #פונקצייה המחזירה את האופציות שאפשר לשים באותו מיקום
    options_list = list(range(1, 10))
    row, col = loc
    if sudoku_board[row][col] != -1:
        return []

    for num in sudoku_board[row]:               #מסיר איברים מהשורה
        if num in options_list:
            options_list.remove(num)


    for i in range(9):                          #מסיר איברים מהטור
        num = sudoku_board[i][col]
        if num in options_list:
            options_list.remove(num)


    square_row = row - row % 3
    square_col = col - col % 3
    for i in range(square_row, square_row + 3):             # מסיר איברים מהריבוע 3X3
        for j in range(square_col, square_col + 3):
            num = sudoku_board[i][j]
            if num in options_list:
                options_list.remove(num)

    if len(options_list) == 0:                              #אם אין אופציות מחזיר בהתאם
        return None
    return options_list                                     #אם יש אופציות מחזיר בהתאם


def possible_digits(sudoku_board):                          #יוצרת רשימה 9X9 המכילה בכל משבצת רשימה של אופציות חוקיות
    possibilities_board = [[None for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if sudoku_board[i][j] != -1:                        #אם משבצת תפוסה נעדכן רשימה ריקה
                possibilities_board[i][j] = []
            else:
                opts = options(sudoku_board, (i, j))
                possibilities_board[i][j] = opts
    return possibilities_board

def create_random_board(sudoku_board):
    N = random.randrange(10,20)
    locations = []
    for row in range(9):                            #בניית הרשימה בגודל 81 שמאחסנת את המיקומים הריקים של לוח הסודוקו
        for col in range(9):
            locations.append((row, col))
    for i in range(N):
        K = random.randrange(len(locations))                  # בוחר משבצת אקראית מכל הרשימה
        loc = locations[K]                          # נאחסן את המיקום במשנה
        locations.remove(loc)                       # נסיר את המיקום מהאופציות שלנו
        row, col = loc                              # נאחסן את השורה ואת הטור בנפרד
        valid_options = options(sudoku_board, loc)     #נבדוק את האופציות שלנו בשורה טור וריבוע
        if not valid_options:
            continue
        random_number = random.choice(valid_options)        # נקבל מספר אקראי מאופציות האפשריות
        sudoku_board[row][col] = random_number              #נעדכן את הלוח



def print_board(sudoku_board):                  #פונקציה מדפיסה את הלוח סודוקו באופן מסויים
    horizontal_line = "-" * 35  # קו מפריד אופקי באורך מתאים

    print(horizontal_line)  # קו עליון
    for row in sudoku_board:
        row_str = "|"
        for cell in row:
            if cell == -1:
                row_str += "   |"  # תא ריק
            else:
                row_str += f" {cell} |"
        print(row_str)
        print(horizontal_line)  # הדפסת קו מפריד לאחר כל שורה

def print_board_to_file(sudoku_board, file_name):   #פונקצייה מדפיסה את הלוח באופן מסויים לתוך קובץ טקסט
    horizontal_line = "-" * 35
    with open(file_name, "a") as f:
        f.write(horizontal_line + "\n")
        for row in sudoku_board:
            row_str = "|"
            for cell in row:
                if cell == -1:
                    row_str += "   |"
                else:
                    row_str += f" {cell} |"
            f.write(row_str + "\n")
            f.write(horizontal_line + "\n")


def program_to_text(final_board, final_result):             #פונקציה שמוסיפה לקובץ טקסט את התוצאה התאימה
    if final_result == SUCCESS_FINISH:
        with open(solved_sudoku, "a") as f:
            f.write("Here is the solved board:\n")  # כותבים הודעה לקובץ
        print_board_to_file(final_board, solved_sudoku)  # מדפיסים את הלוח לקובץ
        with open(solved_sudoku, "a") as f:
            f.write("\n")

    elif final_result == FINISH_FAILURE:
        if has_duplicates(final_board):
            with open(solved_sudoku, "a") as f:
                f.write("Board is not legit!\n")  # לוח לא חוקי
                f.write("\n")
        else:
            with open(solved_sudoku, "a") as f:
                f.write("Board is unsolvable\n")  # לוח לא פתיר
                f.write("\n")

example_board = [[5,3,-1,-1,7,-1,-1,-1,-1],
 [6,-1,-1,-1,-1,-1,1,-1,-1],
 [-1,-1,9,-1,-1,-1,-1,6,-1],
 [-1,-1,-1,-1,6,-1,-1,-1,3],
 [-1,-1,-1,8,-1,3,-1,-1,1],
 [-1,-1,-1,-1,-1,-1,-1,-1,-1],
 [-1,6,-1,-1,-1,-1,-1,-1,-1],
 [-1,-1,-1,-1,1,-1,-1,-1,-1],
 [-1,-1,-1,-1,8,-1,-1,-1,9]]

perfect_board = [[5,3,4,6,7,8,9,1,2],
 [6,7,2,1,9,5,3,4,8],
 [1,9,8,3,4,2,5,6,7],
 [8,5,9,7,6,1,4,2,3],
 [4,2,6,8,5,3,7,9,1],
 [7,1,3,9,2,4,8,5,6],
 [9,6,1,5,3,7,2,8,4],
 [2,8,7,4,1,9,6,3,5],
 [3,4,5,2,8,6,1,7,9]]

impossible_board = [[5,1,6,8,4,9,7,3,2],
 [3,-1,7,6,-1,5,-1,-1,-1],
 [8,-1,9,7,-1,-1,-1,6,5],
 [1,3,5,-1,6,-1,9,-1,7],
 [4,7,2,5,9,1,-1,-1,6],
 [9,6,8,3,7,-1,-1,5,-1],
 [2,5,3,1,8,6,-1,7,4],
 [6,8,4,2,-1,7,5,-1,-1],
 [7,9,1,-1,5,-1,6,-1,8]]

bug_board = [[5,3,4,6,7,8,9,1,2],
 [6,7,2,1,9,5,3,4,9],
 [1,9,8,3,4,2,5,6,7],
 [8,5,9,7,6,1,4,2,3],
 [4,2,6,8,5,3,7,9,1],
 [7,1,3,9,2,4,8,5,6],
 [9,6,1,5,3,7,2,8,4],
 [2,8,7,4,1,9,6,3,5],
 [3,4,5,2,8,6,1,7,9]]

interesting_board = [[5,3,4,6,7,8,9,1,2],
 [6,7,2,1,9,5,3,4,8],
 [1,9,8,3,4,2,5,6,7],
 [-1,-1,-1,7,6,1,4,2,3],
 [-1,-1,-1,8,5,3,7,9,1],
 [-1,-1,-1,9,2,4,8,5,6],
 [-1,-1,-1,-1,3,7,2,8,4],
 [-1,-1,-1,-1,1,9,6,3,5],
 [-1,-1,-1,-1,8,6,1,7,9]]

random_board = (crate_empty_board())
solved_sudoku = "solved_sudoku.txt"
with open(solved_sudoku, "w") as f:
    f.write("Sudoku Solver Results:\n\n")
create_random_board(random_board)

board = example_board
possibilities = possible_digits(board)
result = fill_board(board,possibilities)

program_to_text(board,result)

print("finish")

board = perfect_board
possibilities = possible_digits(board)
result = fill_board(board,possibilities)

program_to_text(board,result)

print("finish")

board = impossible_board
possibilities = possible_digits(board)
result = fill_board(board,possibilities)

program_to_text(board,result)

print("finish")

board = bug_board
possibilities = possible_digits(board)
result = fill_board(board,possibilities)

program_to_text(board,result)

print("finish")

board = interesting_board
possibilities = possible_digits(board)
result = fill_board(board,possibilities)

program_to_text(board,result)

print("finish")

board = random_board
possibilities = possible_digits(board)
result = fill_board(board,possibilities)

program_to_text(board,result)

print("finish")




