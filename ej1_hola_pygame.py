

import pygame 
pygame.init() 
ANCHO, ALTO = 640, 480 
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Practico 1 PyGame")
fuente = pygame.font.Font(None, 48)
texto = fuente.render("Buenassss", True, (255, 255, 255))
texto2 = fuente.render("Martin López", True, (255, 255, 255)) 
rect_texto = texto.get_rect(center=(ANCHO // 2, ALTO // 2)) 
rect_texto2 = pygame.Rect(100, 100, 60, 60) # x, y, ancho, alto
clock = pygame.time.Clock()
vel = 1
running = True 
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
            running = False
    

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]: rect_texto2.x -= vel
    if teclas[pygame.K_RIGHT]: rect_texto2.x += vel
    if teclas[pygame.K_UP]: rect_texto2.y -= vel
    if teclas[pygame.K_DOWN]: rect_texto2.y += vel

    # Limitar dentro de la ventana
    if rect_texto2.left < 0: rect_texto2.left = 0
    if rect_texto2.right > ANCHO: rect_texto2.right = ANCHO
    if rect_texto2.top < 0: rect_texto2.top = 0
    if rect_texto2.bottom > ALTO: rect_texto2.bottom = ALTO


    pantalla.fill((250, 0, 0)) 
    pantalla.blit(texto, rect_texto) 
    pantalla.blit(texto2, rect_texto2) 
    pygame.display.flip() 
clock.tick(60)
pygame.quit() 