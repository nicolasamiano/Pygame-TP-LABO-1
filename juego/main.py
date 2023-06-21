import pygame
import random
from nave_principal import Jugador
from base_dato import *
from disparos import Disparos
from tanque import Tanque
from avion import Avion
from variables_imagenes import *
from constantes import *
from disparos_enemigos import Disparos_Enemigos

pygame.init()

# Sonido
pygame.mixer.init()
sonido = pygame.mixer.Sound("Sonidos/danger_zone.ogg")
sonido_explosion = pygame.mixer.Sound("Sonidos/explosion.mp3")
sonido_misil = pygame.mixer.Sound("Sonidos/sonido_misil.mp3")
sonido.set_volume(0.3)
sonido_explosion.set_volume(0.2)
sonido_misil.set_volume(0.2)
sonido.play(-1)

# Ventana
pantalla = pygame.display.set_mode([PANTALLA_ANCHO, PANTALLA_LARGO])
pygame.display.set_caption("Air Conflict")
frames = pygame.time.Clock()

# Instancias
jugador = Jugador(int(PANTALLA_LARGO / 2), PANTALLA_ANCHO - 200, 3)
jugador_grupo = pygame.sprite.Group()
jugador_grupo.add(jugador)
lista_jugador = [jugador]
disparos_grupo = pygame.sprite.Group()
enemigos_grupo_avion = pygame.sprite.Group()
enemigos_grupo_tanque = pygame.sprite.Group()
disparos_enemigos_grupo = pygame.sprite.Group()
for i in range(4):
    tanque = Tanque()
    enemigos_grupo_tanque.add(tanque)
for i in range(3):
    avion_enemigo = Avion()
    enemigos_grupo_avion.add(avion_enemigo)

# Variables
y = 0
ejecutar = True
ultimo_disparo_enemigo = pygame.time.get_ticks()
cooldown_enemigo = 800
estado = "menu"
cooldown_jugador = 600
usuario = ''

# Genero DB
generar_tabla()

# Main
while ejecutar:
    frames.tick(FPS)
    if estado == "menu":
        rect_boton_jugar = pygame.draw.rect(pantalla, (255, 255, 255), (270, 340, 280, 110))
        rect_boton_score = pygame.draw.rect(pantalla, (255, 255, 255), (270, 530, 265, 110))
        pantalla.blit(fondo_menu, (0, 0))
        pantalla.blit(fondo_titulo, (150, 50))
        font_nombre_titulo = pygame.font.SysFont("Arial", 90)
        titulo = "Air Conflict"
        texto_titulo = font_nombre_titulo.render(titulo, True, (255, 255, 255))
        pantalla.blit(texto_titulo, (180, 100))
        pantalla.blit(boton_jugar, (rect_boton_jugar.x, rect_boton_jugar.y - 5))
        pantalla.blit(fondo_score, (rect_boton_score.x + 10, rect_boton_score.y + 5))
        font_nombre_score = pygame.font.SysFont("Arial", 42)
        texto_score = "Ver Puntajes"
        texto_menu_score = font_nombre_score.render(texto_score, True, (255, 255, 255))
        pantalla.blit(texto_menu_score, (290, 560))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutar = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_boton_jugar.collidepoint(evento.pos):
                    estado = "jugando"
                if rect_boton_score.collidepoint(evento.pos):
                    estado = "score"
    elif estado == "jugando":
        
        # Fondo en movimiento
        if jugador.vida > 0:
            y_resto = y % fondo.get_rect().height
            pantalla.blit(fondo,(0, y_resto - fondo.get_rect().height))
            y += 1
            if y_resto < PANTALLA_LARGO:
                pantalla.blit(fondo, (0, y_resto))
            
            # Respawn de enemigos
            if len(enemigos_grupo_tanque) < 4:
                for i in range(1):
                    tanque = Tanque()
                    enemigos_grupo_tanque.add(tanque)
            if len(enemigos_grupo_avion) < 3:
                for i in range(1):
                    avion_enemigo = Avion()
                    enemigos_grupo_avion.add(avion_enemigo)
            
            # Disparos del enemigo
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - ultimo_disparo_enemigo > cooldown_enemigo:
                enemigo_tanque = random.choice(enemigos_grupo_tanque.sprites())
                enemigo_avion = random.choice(enemigos_grupo_avion.sprites())
                disparo_enemigo_avion = Disparos_Enemigos(enemigo_avion.rect.centerx, enemigo_avion.rect.bottom)
                disparo_enemigo_tanque = Disparos_Enemigos(enemigo_tanque.rect.centerx, enemigo_tanque.rect.bottom)
                disparos_enemigos_grupo.add(disparo_enemigo_avion)
                disparos_enemigos_grupo.add(disparo_enemigo_tanque)
                ultimo_disparo_enemigo = tiempo_actual

            # Puntaje en el juego
            font_juego_puntaje = pygame.font.SysFont("Arial", 48)
            puntaje = "Score: {0}".format(jugador.score)
            texto_puntaje = font_juego_puntaje.render(puntaje, True, (0, 0, 0))
            pantalla.blit(texto_puntaje, (10, 900))

            # Barra de Vida
            pygame.draw.rect(pantalla, (0, 255, 0), (15, (830), 150, 51))
            if jugador.vida == 3:
                pantalla.blit(jugador.vida_imagen, (15, 830))
                pantalla.blit(jugador.vida_imagen, (65, 830))
                pantalla.blit(jugador.vida_imagen, (115, 830))
            if jugador.vida == 2:
                pantalla.blit(jugador.vida_imagen, (15, 830))
                pantalla.blit(jugador.vida_imagen, (65, 830))
            if jugador.vida == 1:
                pantalla.blit(jugador.vida_imagen, (15, 830))
            
            # Pegar superficie del Jugador
            pantalla.blit(jugador.escalado, (jugador.rect.x, jugador.rect.y))
            
            # Disparos del Jugador
            teclas = pygame.key.get_pressed()
            tiempo = pygame.time.get_ticks()
            if teclas[pygame.K_z] and tiempo - jugador.ultimo_disparo > cooldown_jugador:
                disparos = Disparos(jugador.rect.centerx, jugador.rect.top)
                disparos_grupo.add(disparos)
                jugador.ultimo_disparo = tiempo
                sonido_misil.play()

            # Colisiones
            if pygame.sprite.groupcollide(disparos_grupo, enemigos_grupo_avion, True, True):
                jugador.score += 10
                sonido_explosion.play()
            if pygame.sprite.groupcollide(disparos_grupo, enemigos_grupo_tanque, True, True):
                jugador.score += 5
                sonido_explosion.play()
            if pygame.sprite.groupcollide(enemigos_grupo_tanque, jugador_grupo, True, False):
                jugador.vida -= 1
                jugador.score += 5
                sonido_explosion.play()
            if pygame.sprite.groupcollide(enemigos_grupo_avion, jugador_grupo, True, False):
                jugador.vida -= 1
                jugador.score += 10
                sonido_explosion.play()
            if pygame.sprite.groupcollide(disparos_enemigos_grupo, jugador_grupo, True, False):
                jugador.vida -= 1
                sonido_explosion.play()

            # Actualizar
            jugador.actualizar(PANTALLA_ANCHO, PANTALLA_LARGO)
            disparos_grupo.update()
            enemigos_grupo_avion.update()
            enemigos_grupo_tanque.update()
            disparos_enemigos_grupo.update()

            # Pegar Superficie
            disparos_enemigos_grupo.draw(pantalla)
            disparos_grupo.draw(pantalla)
            enemigos_grupo_avion.draw(pantalla)
            enemigos_grupo_tanque.draw(pantalla)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutar = False
        else:
            rect_boton_replay = pygame.draw.rect(pantalla, (255, 255, 255), (270, 340, 280, 110))
            rect_boton_score = pygame.draw.rect(pantalla, (255, 255, 255), (270, 530, 265, 110))
            pantalla.blit(fondo_gameover, (0, 0))
            pantalla.blit(fondo_score, (rect_boton_score.x + 10, rect_boton_score.y + 5))
            pantalla.blit(boton_jugar_denuevo, (rect_boton_replay.x, rect_boton_replay.y))
            pantalla.blit(titulo_gameover, (150, -80))
            fonto_nombre_volver = pygame.font.SysFont("Arial", 42)
            texto_volver = "Volver Inicio"
            texto_volver_boton = fonto_nombre_volver.render(texto_volver, True, (255, 255, 255))
            pantalla.blit(texto_volver_boton, (290, 560))
            sonido.stop()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutar = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_BACKSPACE:
                        usuario = usuario[0:-1]
                    else:
                        usuario += evento.unicode
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if rect_boton_replay.collidepoint(evento.pos):
                        estado = "jugando"
                        jugador.vida = 3
                        sonido.play(-1)
                        if len(usuario) > 0:
                            subir_tabla(usuario, jugador.score)
                        jugador.score = 0
                        usuario = ''
                        enemigos_grupo_tanque.empty()
                        enemigos_grupo_avion.empty()
                        disparos_enemigos_grupo.empty()
                    if rect_boton_score.collidepoint(evento.pos):
                        estado = "menu"
                        jugador.vida = 3
                        sonido.play(-1)
                        if len(usuario) > 0:
                            subir_tabla(usuario, jugador.score)
                        jugador.score = 0
                        usuario = ''
                        enemigos_grupo_tanque.empty()
                        enemigos_grupo_avion.empty()
                        disparos_enemigos_grupo.empty()
            rect_usuario = pygame.Rect(290, 700, 250,60)
            pygame.draw.rect(pantalla, (0, 0, 0), rect_usuario)
            font_input = pygame.font.SysFont("arial", 30)
            font_input_surface = font_input.render(usuario, True, (255, 255, 255))
            pantalla.blit(font_input_surface,(rect_usuario.x, rect_usuario.y))
    elif estado == "score":
        rect_boton_volver = pygame.draw.rect(pantalla, (255, 255, 255), (0, 0, 100, 110))
        lista_scores = ordenar_scores()
        pantalla.blit(fondo_menu_score, (0, 0))
        i = 100
        for e_lista in lista_scores:
            font_nombre_usuario = pygame.font.SysFont("Arial", 30)
            texto_usuario = e_lista[1]
            texto_menu_usuario = font_nombre_usuario.render(texto_usuario, True, (0, 0, 255))
            score_font = pygame.font.SysFont("Arial", 30)
            score_menu = "{0}".format(e_lista[2])
            score_menu_render = score_font.render(score_menu, True, (0, 0, 255))
            i += 80
            pantalla.blit(texto_menu_usuario, (170, i))
            pantalla.blit(score_menu_render, (500, i))
            font = pygame.font.SysFont("Arial", 70)
            texto = "TOP SCORES"
            texto_render = font.render(texto, True, (0, 0, 255))
            pantalla.blit(texto_render, (150, 50))
            pantalla.blit(boton_volver, (rect_boton_volver.x, rect_boton_volver.y))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutar = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_boton_volver.collidepoint(evento.pos):
                    estado = "menu"

    pygame.display.flip()
pygame.quit()