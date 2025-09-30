

import pygame
import random

# Inicialización
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Atrapa monedas")
clock = pygame.time.Clock()

# Jugador (rectángulo)
jugador = pygame.Rect(ANCHO // 2 - 25, ALTO // 2 - 25, 50, 50)
VEL = 6

# Monedas (círculos representados por rects para colisión)
MONEDA_RADIO = 12
monedas = []
SPAWN_MS = 1100  # cada cuánto aparece una moneda
ULTIMO_SPAWN = 0
MAX_MONEDAS = 8

MONEDA_RADIO_2 = 8
monedas_2 = []
SPAWN_MS_2 = 2000  # cada cuánto aparece una moneda
ULTIMO_SPAWN_2 = 0
MAX_MONEDAS_2 = 2

BOMBA_RADIO = 30
bombas = []
SPAWN_BOMB = 2200  # cada cuánto aparece una moneda
ULTIMO_SPAWN_BOMB = 0
MAX_BOMB = 3


# HUD
fuente = pygame.font.Font(None, 32)
puntos = 0
TIEMPO_TOTAL_MS = 40_000  # 40 segundos
inicio_ms = pygame.time.get_ticks()
inicio_ms_2 = pygame.time.get_ticks()
inicio_ms_bomb = pygame.time.get_ticks()

running = True
while running:
    dt = clock.tick(60)  # ms transcurridos desde el frame anterior
    ahora = pygame.time.get_ticks()
    ahora_2 = pygame.time.get_ticks()
    ahora_bomb = pygame.time.get_ticks()
    # Eventos
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    # Movimiento continuo (WASD o flechas)
    teclas = pygame.key.get_pressed()
    dx = (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) - (teclas[pygame.K_LEFT] or teclas[pygame.K_a])
    dy = (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) - (teclas[pygame.K_UP] or teclas[pygame.K_w])

    jugador.x += int(dx * VEL)
    jugador.y += int(dy * VEL)

    # Limitar a la pantalla
    jugador.clamp_ip(pygame.Rect(0, 0, ANCHO, ALTO))

    # Spawnear monedas cada SPAWN_MS hasta un máximo
    if ahora - ULTIMO_SPAWN >= SPAWN_MS and len(monedas) < MAX_MONEDAS:
        x = random.randint(MONEDA_RADIO, ANCHO - MONEDA_RADIO)
        y = random.randint(MONEDA_RADIO, ALTO - MONEDA_RADIO)
        rect = pygame.Rect(x - MONEDA_RADIO, y - MONEDA_RADIO, MONEDA_RADIO * 2, MONEDA_RADIO * 2)
        monedas.append(rect)
        ULTIMO_SPAWN = ahora

    if ahora_2 - ULTIMO_SPAWN_2 >= SPAWN_MS_2 and len(monedas_2) < MAX_MONEDAS_2:
        x = random.randint(MONEDA_RADIO_2, ANCHO - MONEDA_RADIO_2)
        y = random.randint(MONEDA_RADIO_2, ALTO - MONEDA_RADIO_2)
        rect = pygame.Rect(x - MONEDA_RADIO_2, y - MONEDA_RADIO_2, MONEDA_RADIO_2 * 2, MONEDA_RADIO_2 * 2)
        monedas_2.append(rect)
        ULTIMO_SPAWN_2 = ahora_2

    if ahora_bomb - ULTIMO_SPAWN_BOMB >= SPAWN_BOMB and len(bombas) < MAX_BOMB:
        x = random.randint(BOMBA_RADIO, ANCHO - BOMBA_RADIO)
        y = random.randint(BOMBA_RADIO, ALTO - BOMBA_RADIO)
        rect = pygame.Rect(x - BOMBA_RADIO, y - BOMBA_RADIO, BOMBA_RADIO * 2, BOMBA_RADIO * 2)
        bombas.append(rect)
        ULTIMO_SPAWN_BOMB = ahora_bomb

    # Detectar colisiones jugador-monedas
    recogidas = []
    for i, m in enumerate(monedas):
        if jugador.colliderect(m):
            recogidas.append(i)
            puntos += 1

    recogidas_2 = []
    for i, m in enumerate(monedas_2):
        if jugador.colliderect(m):
            recogidas_2.append(i)
            puntos += 2


    recolect_bombas = []
    for i, m in enumerate(bombas):
        if jugador.colliderect(m):
            recolect_bombas.append(i)
            puntos -= 5

    # Eliminar recogidas (de atrás para adelante)
    for i in reversed(recogidas):
        monedas.pop(i)

    for i in reversed(recogidas_2):
        monedas_2.pop(i)

    for i in reversed(recolect_bombas):
        bombas.pop(i)

    # Tiempo restante
    transcurrido = ahora - inicio_ms
    restante_ms = max(0, TIEMPO_TOTAL_MS - transcurrido)

    if restante_ms == 0:
        # Game Over (pausa breve)
        game_over_txt = pygame.font.Font(None, 64).render("¡Tiempo!", True, (255, 220, 60))
        puntaje_txt = pygame.font.Font(None, 48).render(f"Puntaje: {puntos}", True, (255, 255, 255))


        pantalla.blit(game_over_txt, game_over_txt.get_rect(center=(ANCHO // 2, ALTO // 2 - 30)))
        pantalla.blit(puntaje_txt, puntaje_txt.get_rect(center=(ANCHO // 2, ALTO // 2 + 30)))

        pygame.display.flip()
        pygame.time.delay(1500)
        running = False
        continue  # saltar al siguiente ciclo para no dibujar más

    # --- DIBUJO ---
    pantalla.fill((12, 26, 38))

    # monedas
    for m in monedas:
        pygame.draw.circle(pantalla, (255, 215, 0), m.center, MONEDA_RADIO)

    for m in monedas_2:
        pygame.draw.circle(pantalla, (255, 0, 150), m.center, MONEDA_RADIO_2)

    for m in bombas:
        pygame.draw.circle(pantalla, (255, 0, 0), m.center, BOMBA_RADIO)

        
    # jugador
    pygame.draw.rect(pantalla, (80, 200, 255), jugador, border_radius=6)

    # HUD
    seg = restante_ms // 1000
    hud1 = fuente.render(f"Puntos: {puntos}", True, (255, 255, 255))
    hud2 = fuente.render(f"Tiempo: {seg:02d}s", True, (255, 255, 255))
    pantalla.blit(hud1, (10, 10))
    pantalla.blit(hud2, (10, 40))

    # Actualizar pantalla
    pygame.display.flip()

    if puntos < 0:
        break

pygame.quit()
