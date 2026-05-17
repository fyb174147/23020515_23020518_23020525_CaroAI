import pygame
import os
import source.utils as utils

SIZE, PIECE, N, MARGIN = 540, 32, 15, 23
GRID = (SIZE - 2 * MARGIN) / (N-1)

class GameUI(object):
    def __init__(self, ai):
        self.ai = ai
        self.colorState = {} 
        self.mapping = utils.create_mapping()
        pygame.init()
        self.screen = pygame.display.set_mode((SIZE, SIZE))
        pygame.display.set_caption('Caro AI - Level 2')
        self.board = pygame.image.load(os.path.join("assets", 'board.jpg')).convert()
        self.blackPiece = pygame.image.load(os.path.join("assets", 'black_piece.png')).convert_alpha()
        self.whitePiece = pygame.image.load(os.path.join("assets", 'white_piece.png')).convert_alpha()
        self.menuBoard = pygame.image.load(os.path.join("assets", "menu_board.png")).convert_alpha()
        self.buttonSurf = pygame.transform.scale(pygame.image.load(os.path.join("assets", "button.png")), (110, 45))

    def drawMenu(self): 
        menu_board = pygame.transform.scale(self.menuBoard, (400, 250)) 
        rect = menu_board.get_rect(center = self.screen.get_rect().center)
        font = pygame.font.SysFont("arial", 20, bold=True)
        menu_board.blit(font.render('CHOOSE YOUR COLOR:', True, 'white'), (50, 30))
        menu_board.blit(font.render(f'MODE: {self.ai.ai_mode.upper()}', True, 'yellow'), (50, 130))
        self.screen.blit(menu_board, rect)

    def drawPiece(self, color, i, j):
        x, y = self.mapping[(i,j)]
        img = self.blackPiece if color == 'black' else self.whitePiece
        self.screen.blit(img, (x - PIECE/2, y - PIECE/2))

    def drawResult(self, tie=False):
        # Khôi phục bảng thông báo gốc dùng menuBoard
        menu_board = pygame.transform.scale(self.menuBoard, (400, 200))
        width, height = menu_board.get_size()
        font = pygame.font.SysFont('arial', 25, True)
        
        if tie:
            text = "IT'S A TIE! "
            render_text = font.render(text, True, 'white')
            menu_board.blit(render_text, (width//2 - render_text.get_width()//2, 40))
        else:
            text = 'THE WINNER IS: '
            render_text = font.render(text, True, 'white')
            menu_board.blit(render_text, (width//2 - render_text.get_width()//2, 20))

            winner = self.ai.getWinner() #
            render_winner = font.render(winner.upper(), True, 'yellow')
            menu_board.blit(render_winner, (width//2 - render_winner.get_width()//2, 55))
        
        restart_font = pygame.font.SysFont('arial', 18, bold=True)
        restart_text = 'DO YOU WANT TO PLAY AGAIN?'
        render_restart = restart_font.render(restart_text, True, 'white')
        menu_board.blit(render_restart, (width//2 - render_restart.get_width()//2, 100))

        # Vẽ bảng lên màn hình tại vị trí trung tâm phía trên
        self.screen.blit(menu_board, (SIZE//2 - width//2, 50))

    def restartChoice(self, pos):
        # Tọa độ nút YES/NO dựa trên bảng drawResult
        # YES (200, 200), NO (340, 200) - Bạn có thể điều chỉnh tọa độ này trong play.py
        pass

    def checkColorChoice(self, button_black, button_white, pos):
        """Thiết lập màu quân cờ và lượt đi dựa trên nút bấm"""
        if button_black.rect.collidepoint(pos):
            self.colorState[-1] = 'black' # Người chơi (Player -1) chọn Đen
            self.colorState[1] = 'white'  # Máy (AI 1) chọn Trắng
            self.ai.turn = -1             # Người đi trước
        elif button_white.rect.collidepoint(pos):
            self.colorState[-1] = 'white' # Người chơi chọn Trắng
            self.colorState[1] = 'black'  # Máy chọn Đen
            self.ai.turn = 1              # Máy đi trước