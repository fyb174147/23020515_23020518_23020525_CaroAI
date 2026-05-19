import pygame

import source.gomoku as gomoku
from gui.button import Button
from gui.interface import GameUI
from source.AI import GomokuAI


MODES = {
    "Human vs AI": {1: "human", -1: "ai"},
    "AI vs Human": {1: "ai", -1: "human"},
    "AI vs AI": {1: "ai", -1: "ai"},
    "Human vs Human": {1: "human", -1: "human"},
}


def make_buttons(game):
    mode_surf = pygame.transform.scale(game.buttonSurf, (150, 45))
    algo_surf = pygame.transform.scale(game.buttonSurf, (135, 45))
    return {
        "Human vs AI": Button(mode_surf, 185, 225, "HUMAN vs AI", 14),
        "AI vs Human": Button(mode_surf, 355, 225, "AI vs HUMAN", 14),
        "AI vs AI": Button(mode_surf, 185, 282, "AI vs AI", 15),
        "Human vs Human": Button(mode_surf, 355, 282, "HUMAN vs HUMAN", 12),
        "minimax": Button(algo_surf, 190, 370, "MINIMAX", 15),
        "alphabeta": Button(algo_surf, 350, 370, "ALPHA-BETA", 14),
        "yes": Button(game.buttonSurf, 210, 320, "YES", 18),
        "no": Button(game.buttonSurf, 330, 320, "NO", 18),
    }


def reset_game(game, old_ai):
    ai = GomokuAI(depth=old_ai.depth)
    ai.ai_mode = old_ai.ai_mode
    game.ai = ai
    game.setupColors()
    return ai


def turn_label(state):
    return "Black" if state == 1 else "White"


def draw_game_screen(game, ai, selected_mode, buttons, game_over=False, status_text=None):
    game.screen.blit(game.board, (0, 0))
    for i in range(15):
        for j in range(15):
            if ai.boardMap[i][j] != 0:
                game.drawPiece(game.colorState[ai.boardMap[i][j]], i, j)

    game.drawStatus(selected_mode, status_text)

    if game_over:
        game.drawResult(tie=(ai.checkResult() == 0))
        buttons["yes"].draw(game.screen)
        buttons["no"].draw(game.screen)


def startGame():
    ai = GomokuAI(depth=3)
    game = GameUI(ai)
    game.setupColors()
    clock = pygame.time.Clock()
    buttons = make_buttons(game)

    selected_mode = "Human vs AI"
    in_menu = True
    game_over = False
    ai_thinking = False
    run = True

    while run:
        clock.tick(60)
        game.screen.blit(game.board, (0, 0))

        if in_menu:
            game.drawMenu(selected_mode)
            for key in ("Human vs AI", "AI vs Human", "AI vs AI", "Human vs Human"):
                buttons[key].draw(game.screen)
            buttons["minimax"].draw(game.screen)
            buttons["alphabeta"].draw(game.screen)
        else:
            actor = MODES[selected_mode][ai.turn]
            status_text = f"{turn_label(ai.turn)} to move"
            if actor == "ai":
                status_text = f"{turn_label(ai.turn)} AI thinking..."
            draw_game_screen(game, ai, selected_mode, buttons, game_over, status_text)

            if not game_over and actor == "ai":
                pygame.display.flip()
                pygame.event.pump()
                ai_thinking = True
                move_i, move_j = gomoku.ai_move(ai, ai.turn)
                pygame.event.clear([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
                ai_thinking = False
                if move_i != -1 and ai.setState(move_i, move_j, ai.turn):
                    ai.turn *= -1
                if ai.checkResult() is not None:
                    game_over = True
                draw_game_screen(game, ai, selected_mode, buttons, game_over)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                if in_menu:
                    if buttons["minimax"].rect.collidepoint(pos):
                        ai.ai_mode = "minimax"
                    elif buttons["alphabeta"].rect.collidepoint(pos):
                        ai.ai_mode = "alphabeta"
                    else:
                        for key in ("Human vs AI", "AI vs Human", "AI vs AI", "Human vs Human"):
                            if buttons[key].rect.collidepoint(pos):
                                selected_mode = key
                                ai.turn = 1
                                in_menu = False
                                break

                elif game_over:
                    if buttons["yes"].rect.collidepoint(pos):
                        ai = reset_game(game, ai)
                        in_menu = True
                        game_over = False
                        ai_thinking = False
                        selected_mode = "Human vs AI"
                    if buttons["no"].rect.collidepoint(pos):
                        run = False

                elif not ai_thinking and MODES[selected_mode][ai.turn] == "human":
                    if gomoku.check_human_move(ai, pos, ai.turn):
                        ai.turn *= -1
                        if ai.checkResult() is not None:
                            game_over = True
                        draw_game_screen(game, ai, selected_mode, buttons, game_over)
                        pygame.display.flip()

        if not in_menu and not game_over and ai.checkResult() is not None:
            game_over = True

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    startGame()
