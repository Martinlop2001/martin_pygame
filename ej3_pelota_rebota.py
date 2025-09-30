

import pygame, random, math 

pygame.init()
ANCHO, ALTO = 640, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pelota que rebota")
clock = pygame.time.Clock()
x, y = ANCHO // 2, ALTO // 2
radio = 20
dx, dy = 4, 3 # velocidad por frame

color = (255, 255, 255)

def cambio_color():

    #cambia el color de la pelota
    return(random.randint(0,255), random.randint(0,255), random.randint(0,255))


fuente = pygame.font.Font(None, 36)

rebotes = 0

running = True

vel_maxima = 30

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    # Mover
    x += dx
    y += dy

    #Velocidad
    dx *= 1.005
    dy *= 1.005

    # Rebotar en bordes
    if x - radio <= 0 or x + radio >= ANCHO:
        dx = -dx
        color = cambio_color()  
        rebotes += 1

    if abs(dx) > vel_maxima:
        dx = math.copysign(vel_maxima, dx)

    if y - radio <= 0 or y + radio >= ALTO:
        dy = -dy
        color = cambio_color()
        rebotes += 1

    if abs(dy) > vel_maxima:
        dy = math.copysign(vel_maxima, dy)

    pantalla.fill((0, 0, 0))
    pygame.draw.circle(pantalla, color, (x, y), radio)

    texto = fuente.render(f"Rebotes: ({rebotes})", True, (255, 255, 0))
    pantalla.blit(texto, (20, 20))

    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()   