import random
#so we initialize the boarder here .....
def initialize_board():
    return {1: ' ', 2: ' ', 3: ' ',
            4: ' ', 5: ' ', 6: ' ',
            7: ' ', 8: ' ', 9: ' '}
#we print the border (i thought i could make like this to make it more beautiful)...
def printBoard(board):
    print("   1   2   3 ")
    print(" +---+---+---+")
    print(f"1| {board[1]} | {board[2]} | {board[3]} |")
    print(" +---+---+---+")
    print(f"2| {board[4]} | {board[5]} | {board[6]} |")
    print(" +---+---+---+")
    print(f"3| {board[7]} | {board[8]} | {board[9]} |")
    print(" +---+---+---+")
    print()
#to check the free space...
def spaceIsFree(board, position):
    return board[position] == ' '
#to insert the letter like *X* an *O*...
def insertLetter(board, letter, position):
    if spaceIsFree(board, position):
        board[position] = letter
        printBoard(board)
    else:
        print("Can't insert there!")
        position = int(input("Please enter a new position: "))
        insertLetter(board, letter, position)
#so we check for win here and draw...and the player movement ..
def checkForWin(board):
    win_combinations = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],
        [1, 4, 7], [2, 5, 8], [3, 6, 9],
        [1, 5, 9], [7, 5, 3]
    ]
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return True
    return False

def checkDraw(board):
    return all(board[position] != ' ' for position in board)

def playerMove(board, player_name, player_mark):
    while True:
        position = int(input(f"{player_name}, enter the position (1-9) for your move: "))
        if position in board and spaceIsFree(board, position):
            insertLetter(board, player_mark, position)
            break
        else:
            print("Invalid position! Try again.")
#so i just putter a function when everytime the user wants to play he can choose yes or no ...
def play_again():
    while True:
        answer = input("Do you want to play again? (yes/no): ").lower()
        if answer == 'yes':
            return True
        elif answer == 'no':
            return False
        else:
            print("Please enter 'yes' or 'no'!")
#as teacher mentioned on the exercise we can put the '\n" or ":" so i did that
def get_valid_player_name(player_num):
    while True:
        try:
            player_name = input(f"Enter the name of Player {player_num}: ")
            if '\n' in player_name or ':' in player_name:
                raise ValueError("Player name cannot contain '\n' or ':'")
            return player_name
        except ValueError as e:
            print(e)
#ahm so that we cna creat our file name to store ...
def get_valid_file_name():
    while True:
        try:
            file_name = input("Enter the file name to save the scores: ")
            if '\n' in file_name or ':' in file_name:
                raise ValueError("File name cannot contain '\n' or ':'")
            return file_name
        except ValueError as e:
            print(e)
#gives us the result
def update_scores(scores, player_name, result):
    if player_name in scores:
        scores[player_name] += result
    else:
        scores[player_name] = result
#it saves the scores on the file
def write_scores_to_file(file_name, scores):
    with open(file_name, 'w') as file:
        for player_name, score in scores.items():
            file.write(f"{player_name}: {score}\n")
# it reads 
def read_scores_from_file(file_name):
    scores = {}
    try:
        with open(file_name, 'r') as file:
            for line in file:
                player_name, score = line.strip().split(': ')
                scores[player_name] = int(score)
    except FileNotFoundError:
        pass
    return scores

players = [('X', ''), ('O', '')]
#we just initialize the game and yeah thats it ...
while True:
    board = initialize_board()
    printBoard(board)

    players[0] = (get_valid_player_name(1), 'X')
    players[1] = (get_valid_player_name(2), 'O')

    file_name = get_valid_file_name()
    scores = read_scores_from_file(file_name)

    turn = 0
    while True:
        current_player_name, current_player_mark = players[turn]
        print(f"{current_player_name}, it's your turn!")
        playerMove(board, current_player_name, current_player_mark)

        if checkForWin(board):
            print(f"{current_player_name} wins!")
            update_scores(scores, current_player_name, 2)
            update_scores(scores, players[(turn + 1) % 2][0], 0)
            break
        elif checkDraw(board):
            print("It's a draw!")
            update_scores(scores, players[0][0], 1)
            update_scores(scores, players[1][0], 1)
            break

        turn = (turn + 1) % 2

    write_scores_to_file(file_name, scores)

    if not play_again():
        break
