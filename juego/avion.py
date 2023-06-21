import pygame
import random
from constantes import *

class Avion(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load("Imagenes/enemigo.png")
        self.image = pygame.transform.scale(self.imagen, (120, 120))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 650)
        self.rect.y = random.randint(-150, -150)
    
    def update(self):
        self.rect.y += 2
        if self.rect.top > PANTALLA_LARGO + 10:
            self.rect.x = random.randint(0, 650)
            self.rect.y = random.randint(-50, -50)