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
        pygame.display.set_caption('Caro AI - Minimax / Alpha-Beta')
        self.board = pygame.image.load(os.path.join("assets", 'board.jpg')).convert()
        self.blackPiece = pygame.image.load(os.path.join("assets", 'black_piece.png')).convert_alpha()
        self.whitePiece = pygame.image.load(os.path.join("assets", 'white_piece.png')).convert_alpha()
        self.menuBoard = pygame.image.load(os.path.join("assets", "menu_board.png")).convert_alpha()
        self.buttonSurf = pygame.transform.scale(pygame.image.load(os.path.join("assets", "button.png")), (110, 45))

    def drawMenu(self, game_mode): 
        menu_board = pygame.transform.scale(self.menuBoard, (460, 360)) 
        rect = menu_board.get_rect(center = self.screen.get_rect().center)
        title_font = pygame.font.SysFont("arial", 26, bold=True)
        font = pygame.font.SysFont("arial", 17, bold=True)
        small_font = pygame.font.SysFont("arial", 14, bold=True)
        title = title_font.render("CARO AI", True, "white")
        menu_board.blit(title, (230 - title.get_width() // 2, 28))
        menu_board.blit(font.render("Select play mode", True, "white"), (45, 82))
        menu_board.blit(font.render("Select AI algorithm", True, "white"), (45, 225))
        menu_board.blit(
            small_font.render(f"Mode: {game_mode} | Algorithm: {self.ai.ai_mode.upper()}", True, "yellow"),
            (45, 322),
        )
        self.screen.blit(menu_board, rect)

    def drawPiece(self, color, i, j):
        x, y = self.mapping[(i,j)]
        img = self.blackPiece if color == 'black' else self.whitePiece
        self.screen.blit(img, (x - PIECE/2, y - PIECE/2))

    def drawStatus(self, game_mode, status_text=None):
        panel = pygame.Surface((SIZE, 34), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 120))
        font = pygame.font.SysFont("arial", 14, bold=True)
        turn_name = "Black" if self.ai.turn == 1 else "White"
        if status_text is None:
            status_text = f"{turn_name} to move"
        text = f"{game_mode} | {status_text} | {self.ai.ai_mode.upper()} depth {self.ai.depth}"
        if self.ai.nodes_visited:
            text += f" | Last nodes: {self.ai.nodes_visited}"
        panel.blit(font.render(text, True, "white"), (12, 8))
        self.screen.blit(panel, (0, SIZE - 34))

    def drawResult(self, tie=False):
        menu_board = pygame.transform.scale(self.menuBoard, (420, 220))
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

            winner = self.ai.getWinner()
            render_winner = font.render(winner.upper(), True, 'yellow')
            menu_board.blit(render_winner, (width//2 - render_winner.get_width()//2, 55))
        
        restart_font = pygame.font.SysFont('arial', 18, bold=True)
        restart_text = 'DO YOU WANT TO PLAY AGAIN?'
        render_restart = restart_font.render(restart_text, True, 'white')
        menu_board.blit(render_restart, (width//2 - render_restart.get_width()//2, 100))

        self.screen.blit(menu_board, (SIZE//2 - width//2, 50))

    def restartChoice(self, pos):
        # Tọa độ nút YES/NO dựa trên bảng drawResult
        # YES (200, 200), NO (340, 200) - Bạn có thể điều chỉnh tọa độ này trong play.py
        pass

    def setupColors(self):
        self.colorState[1] = 'black'
        self.colorState[-1] = 'white'
