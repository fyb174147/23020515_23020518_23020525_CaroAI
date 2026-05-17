# File: play.py
import pygame
import source.gomoku as gomoku
from gui.interface import *
from source.AI import *
from gui.button import Button

def startGame():
    ai = GomokuAI(depth=3)
    game = GameUI(ai)
    clock = pygame.time.Clock()

    # Nút bấm menu
    btn_black = Button(game.buttonSurf, 200, 255, "BLACK", 20)
    btn_white = Button(game.buttonSurf, 340, 255, "WHITE", 20)
    btn_mini = Button(game.buttonSurf, 200, 345, "MINIMAX", 16)
    btn_alpha = Button(game.buttonSurf, 340, 345, "ALPHA-BETA", 16)
    
    # Nút bấm End Screen
    btn_yes = Button(game.buttonSurf, 210, 320, "YES", 18)
    btn_no = Button(game.buttonSurf, 330, 320, "NO", 18)

    run = True
    in_menu = True
    game_over = False

    while run:
        clock.tick(60)
        game.screen.blit(game.board, (0, 0)) # Luôn vẽ nền
        
        if in_menu:
            game.drawMenu()
            btn_black.draw(game.screen); btn_white.draw(game.screen)
            btn_mini.draw(game.screen); btn_alpha.draw(game.screen)
        else:
            # Vẽ các quân cờ đang có trên bàn
            for i in range(15):
                for j in range(15):
                    if ai.boardMap[i][j] != 0:
                        game.drawPiece(game.colorState[ai.boardMap[i][j]], i, j)
            
            # Lượt AI (chỉ chạy khi chưa kết thúc)
            if ai.turn == 1 and not game_over:
                move_i, move_j = gomoku.ai_move(ai)
                ai.setState(move_i, move_j, 1)
                ai.turn = -1
            
            # Vẽ thông báo kết quả
            if game_over:
                game.drawResult(tie=(ai.checkResult() == 0))
                btn_yes.draw(game.screen)
                btn_no.draw(game.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                
                if in_menu:
                    if btn_mini.rect.collidepoint(pos): ai.ai_mode = "minimax"
                    if btn_alpha.rect.collidepoint(pos): ai.ai_mode = "alphabeta"
                    if btn_black.rect.collidepoint(pos) or btn_white.rect.collidepoint(pos):
                        game.checkColorChoice(btn_black, btn_white, pos)
                        if ai.turn == 1: ai.firstMove(); ai.turn = -1
                        in_menu = False
                
                elif game_over:
                    # Xử lý nút bấm YES/NO
                    if btn_yes.rect.collidepoint(pos):
                        startGame() # Chơi ván mới
                        return      # Thoát vòng lặp hiện tại để tránh đệ quy chồng chéo
                    elif btn_no.rect.collidepoint(pos):
                        run = False
                
                elif ai.turn == -1:
                    # Lượt người đánh
                    if gomoku.check_human_move(ai, pos):
                        ai.turn = 1

        # Cập nhật trạng thái kết thúc
        if not in_menu and not game_over:
            if ai.checkResult() is not None:
                game_over = True

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    startGame()