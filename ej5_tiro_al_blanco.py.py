

import pygame
import random

pygame.init()

ANCHO, ALTO = 900, 540
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tiro al blanco")
clock = pygame.time.Clock()

# HUD
fuente = pygame.font.Font(None, 32)
grande = pygame.font.Font(None, 64)

# Ocultar cursor; usaremos una mira dibujada
pygame.mouse.set_visible(False)

# ------------------------------
# Clase Diana (círculos móviles)
# ------------------------------
class Diana:
    def __init__(self):
        self.radio = random.randint(18, 28)
        self.y = random.randint(100, ALTO - 100)
        self.x = random.randint(self.radio + 40, ANCHO - self.radio - 40)
        self.vel = random.choice([3, 4, 5])
        self.dir = random.choice([-1, 1])  # izquierda/derecha
        if self.radio <= 20:
            self.color = (220, 0, 0)  # Rojo para dianas pequeñas
            self.valor = 2
        else:
            self.color = (220, 60, 90)
            self.valor = 1

    def update(self):
        self.x += self.dir * self.vel
        if self.x - self.radio <= 40 or self.x + self.radio >= ANCHO - 40:
            self.dir *= -1

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (self.x, self.y), self.radio)
        pygame.draw.circle(
            surf, (255, 255, 255), (self.x, self.y),
            max(4, self.radio // 2), width=2
        )

    def colisiona(self, pos):
        mx, my = pos
        dx = mx - self.x
        dy = my - self.y
        return dx * dx + dy * dy <= self.radio * self.radio


# Definimos una clase para la diana vertical
class DianaVertical(Diana):
    def __init__(self):
        super().__init__()
        self.x = random.randint(100, ANCHO - 100)
        self.y = random.randint(self.radio + 40, ALTO - self.radio - 40)
        self.vel = random.choice([3, 4, 5])
        self.dir = random.choice([-1, 1])  # arriba/abajo

    def update(self):
        self.y += self.dir * self.vel
        if self.y - self.radio <= 40 or self.y + self.radio >= ALTO - 40:
            self.dir *= -1

# Definimos una clase para la diana diagonal
class DianaDiagonal(Diana):
    def __init__(self):
        super().__init__()
        self.x = random.randint(self.radio + 40, ANCHO - self.radio - 40)
        self.y = random.randint(self.radio + 40, ALTO - self.radio - 40)
        self.vel_x = random.choice([2, 3, 4])
        self.vel_y = random.choice([2, 3, 4])
        self.dir_x = random.choice([-1, 1])
        self.dir_y = random.choice([-1, 1])

    def update(self):
        self.x += self.dir_x * self.vel_x
        self.y += self.dir_y * self.vel_y
        if self.x - self.radio <= 40 or self.x + self.radio >= ANCHO - 40:
            self.dir_x *= -1
        if self.y - self.radio <= 40 or self.y + self.radio >= ALTO - 40:
            self.dir_y *= -1



# ------------------------------
# Inicialización de juego
# ------------------------------
dianas = [Diana() for _ in range(2)]
dianas += [DianaVertical() for _ in range(2)]
dianas += [DianaDiagonal() for _ in range(2)]

# Stats
aciertos = 0
intentos = 0
tiempo_ms = None
inicio_ms = pygame.time.get_ticks()

running = True

ultimo_disparo_ms = -1000
pos_disparo = (0, 0)

COOLDOWN_MS = 150

# ------------------------------
# Bucle principal
# ------------------------------
while running:
    dt = clock.tick(60)
    ahora = pygame.time.get_ticks()

    # Eventos
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            intentos += 1
            pos = pygame.mouse.get_pos()
            golpe = False
            for i, d in enumerate(dianas):
                if d.colisiona(pos):
                    aciertos += d.valor

                    golpe = True
                    # Respawn de la diana
                    dianas[i] = type(d)()
                    break

            ultimo_disparo_ms = ahora
            pos_disparo = pos

    # Tiempo restante
    #restante = max(0, tiempo_ms - (ahora - inicio_ms))
    #if restante == 0:
        # Resultado final
    #    acc = (aciertos / intentos * 100) if intentos > 0 else 0.0
    #    pantalla.fill((20, 20, 20))
    #    fin = grande.render("¡Tiempo!", True, (255, 220, 60))
    #    res = fuente.render(
    #        f"Aciertos: {aciertos} Intentos: {intentos} Precisión: {acc:.1f}%",
    #        True, (255, 255, 255)
    #    )
    #    pantalla.blit(fin, fin.get_rect(center=(ANCHO // 2, ALTO // 2 - 24)))
    #    pantalla.blit(res, res.get_rect(center=(ANCHO // 2, ALTO // 2 + 24)))
    #    pygame.display.flip()
    #    pygame.time.delay(2000)
    #    running = False
    #    continue

    # UPDATE
    for d in dianas:
        d.update()

    # DRAW
    pantalla.fill((15, 28, 40))

    # Zona de seguridad a los costados
    pygame.draw.rect(pantalla, (30, 45, 60), (0, 0, 40, ALTO))
    pygame.draw.rect(pantalla, (30, 45, 60), (ANCHO - 40, 0, 40, ALTO))

    # Dibujar dianas
    for d in dianas:
        d.draw(pantalla)

    # HUD
    acc = (aciertos / intentos * 100) if intentos > 0 else 0.0
    #seg = restante // 1000
    hud1 = fuente.render(f"Puntos: {aciertos}", True, (255, 255, 255))
    hud2 = fuente.render(f"Intentos: {intentos}", True, (255, 255, 255))
    hud3 = fuente.render(f"Precisión: {acc:.1f}%", True, (255, 255, 255))
    hud4 = fuente.render(f"Tiempo: MODO DE PRUEBA", True, (255, 255, 255))

    pantalla.blit(hud1, (10, 8))
    pantalla.blit(hud2, (10, 34))
    pantalla.blit(hud3, (10, 60))
    pantalla.blit(hud4, (10, 86))

    # Mira (crosshair)
    mx, my = pygame.mouse.get_pos()
    if ahora - ultimo_disparo_ms < COOLDOWN_MS:
        pygame.draw.circle(pantalla, (255, 0, 0), pos_disparo, 22, width=4)

    pygame.draw.circle(pantalla, (255, 255, 255), (mx, my), 12, width=2)
    pygame.draw.line(pantalla, (255, 255, 255), (mx - 18, my), (mx - 4, my), width=2)
    pygame.draw.line(pantalla, (255, 255, 255), (mx + 4, my), (mx + 18, my), width=2)
    pygame.draw.line(pantalla, (255, 255, 255), (mx, my - 18), (mx, my - 4), width=2)
    pygame.draw.line(pantalla, (255, 255, 255), (mx, my + 4), (mx, my + 18), width=2)

    pygame.display.flip()

pygame.quit()
