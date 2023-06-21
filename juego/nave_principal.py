import pygame

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, vida) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load("Imagenes/avion.png")
        self.escalado = pygame.transform.scale(self.imagen, (120, 120))
        self.rect = self.escalado.get_rect()
        self.rect.center = [x, y]
        self.vida = vida
        self.vida_imagen = pygame.transform.scale(self.imagen, (50, 50))
        self.ultimo_disparo = pygame.time.get_ticks()
        self.score = 0
    
    def actualizar(self, PANTALLA_ANCHO, PANTALLA_LARGO):
        velocidad = 5
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < PANTALLA_ANCHO:
            self.rect.x += velocidad
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= velocidad
        if teclas[pygame.K_DOWN] and self.rect.bottom < PANTALLA_LARGO:
            self.rect.y += velocidad