


import pygame
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mover con flechas")
clock = pygame.time.Clock()
jugador = pygame.Rect(100, 100, 60, 60) # x, y, ancho, alto
vel = 10
running = True

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
# Leer estado de teclas (movimiento continuo)
    teclas = pygame.key.get_pressed()

    
    if teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]:
        vel = 20
    else:
        vel = 10

    if teclas[pygame.K_LEFT]: jugador.x -= vel
    if teclas[pygame.K_RIGHT]: jugador.x += vel
    if teclas[pygame.K_UP]: jugador.y -= vel
    if teclas[pygame.K_DOWN]: jugador.y += vel

    # Limitar dentro de la ventana
    if jugador.left < 0: jugador.left = 0
    if jugador.right > ANCHO: jugador.right = ANCHO
    if jugador.top < 0: jugador.top = 0
    if jugador.bottom > ALTO: jugador.bottom = ALTO

    pantalla.fill((250, 0, 0)) 
    pygame.draw.rect(pantalla, (0, 0, 255), jugador)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()