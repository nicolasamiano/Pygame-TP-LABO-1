import pygame

class Disparos(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load("Imagenes/misil.png")
        self.image = pygame.transform.scale(self.imagen, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()