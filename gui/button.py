import pygame 
class Button():
    def __init__(self, image, x_pos, y_pos, text_input, font_size):
        self.image, self.x_pos, self.y_pos = image, x_pos, y_pos
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.font = pygame.font.SysFont("arial", font_size, bold=True)
        self.text_str = text_input
        
    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        color = "yellow" if self.rect.collidepoint(pos) else "white"
        text_surf = self.font.render(self.text_str, True, color)
        surface.blit(self.image, self.rect)
        surface.blit(text_surf, text_surf.get_rect(center=(self.x_pos, self.y_pos)))