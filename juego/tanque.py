import pygame
import random
from constantes import *

class Tanque(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load("Imagenes/tank.png")
        self.image = pygame.transform.scale(self.imagen, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(110, 600)
        self.rect.y = random.randint(0, 50)
    
    def update(self):
        self.rect.y += 2
        if self.rect.top > PANTALLA_LARGO + 10:
            self.rect.x = random.randint(110, 600)
            self.rect.y = random.randint(0, 50)