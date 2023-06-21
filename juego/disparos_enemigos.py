import pygame

class Disparos_Enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load("Imagenes/misil_enemigo.png")
        self.image = pygame.transform.scale(self.imagen, (50, 75))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 3
        if self.rect.bottom < -400:
            self.kill()