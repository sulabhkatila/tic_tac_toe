import pygame
import tictactoe as ttt
import time
import sys

pygame.init()

# Set size of the window
size = width, height = 700, 500

screen = pygame.display.set_mode(size)

# Set font sizes
m_font = pygame.font.Font("OpenSans-Regular.ttf", 32)
l_font = pygame.font.Font("OpenSans-Regular.ttf", 50)
move_font = pygame.font.Font("OpenSans-Regular.ttf", 70)

user = None
board = ttt.initial_state()
ai_turn = False

# Set Colors
black = (0, 0, 0)
white = (255, 255, 255)

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    screen.fill(white)

    # Let user choose a player.
    if user is None:

        # Mkae the buttons
        gameXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        gameX = m_font.render("Play as X", True, black)
        gameXRect = gameX.get_rect()
        gameXRect.center = gameXButton.center
        pygame.draw.rect(screen, white, gameXButton)
        screen.blit(gameX, gameXRect)

        gameOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        gameO = m_font.render("Play as O", True, black)
        gameORect = gameO.get_rect()
        gameORect.center = gameOButton.center
        pygame.draw.rect(screen, white, gameOButton)
        screen.blit(gameO, gameORect)

        # Check for button clicks
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if gameXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif gameOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

        # Make the title
        window_title = l_font.render("Tic-Tac-Toe", True, black)
        window_title2 = l_font.render("X goes 1st and O goes Second", True, black)
        window_titleRect = window_title.get_rect()
        window_titleRect.center = ((width / 2), 50)
        screen.blit(window_title, window_titleRect)

    else:

        # Make the tictactoe play area
        tile_size = 80
        tile_origin = (width / 2 - (1.75 * tile_size),
                       height / 2 - (1.75 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, black, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = move_font.render(board[i][j], True, black)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                window_title = f"Tie."
            else:
                if winner == user:
                    window_title = "You Win!"
                else:
                    window_title = "You Loose!"
        elif user == player:
            window_title = f"Your turn"
        else:
            window_title = f"Computer's Turn"
        window_title = l_font.render(window_title, True, black)
        window_titleRect = window_title.get_rect()
        window_titleRect.center = ((width / 2), 40)
        screen.blit(window_title, window_titleRect)

        # Check for computer's move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.7)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for the user's move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = m_font.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False

    pygame.display.flip()