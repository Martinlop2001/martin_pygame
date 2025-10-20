

import sys
from pathlib import Path
import pygame
import db

WIDTH, HEIGHT = 640, 360
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pygame + SQLite Demo")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.state = "ask_name" # ask_name -> play -> leaderboard
        self.name = ""
        self.score = 0
        self.level = 1
        # Base de datos
        self.conn = db.connect()
        db.init_db(self.conn)

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if self.state == "ask_name":
                    self.handle_name_event(event)
                elif self.state == "play":
                    self.handle_play_event(event)
                elif self.state == "leaderboard":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.reset()
            self.screen.fill((30, 30, 30))
            if self.state == "ask_name":
                self.draw_name()
            elif self.state == "play":
                self.update_play(dt)
                self.draw_play()
            elif self.state == "leaderboard":
                self.draw_leaderboard()
            pygame.display.flip()

    # --- Estados ---
    def handle_name_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.key == pygame.K_RETURN:
                if self.name.strip():
                    self.state = "play"
            else:
                ch = event.unicode
                if ch.isprintable() and len(self.name) < 20:
                    self.name += ch

    def handle_play_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.finish_game()
            elif event.key == pygame.K_SPACE:
                self.score += 10
            elif event.key == pygame.K_RIGHT:
                self.score += 1
            elif event.key == pygame.K_LEFT and self.score > 0:
                self.score -= 1

    def update_play(self, dt):
        # Sumar puntos lentamente con el tiempo (demo)
        self.score += int(5 * dt)

    def draw_name(self):
        t1 = self.font.render("Ingresa tu nombre y presiona\nENTER:", True, (220, 220, 220))
        t2 = self.font.render(self.name + "|", True, (180, 255, 180))
        self.screen.blit(t1, (40, 120))
        self.screen.blit(t2, (40, 160))

    def draw_play(self):
        t1 = self.font.render(f"Jugador: {self.name} Nivel:\n{self.level}", True, (220, 220, 220))
        t2 = self.font.render(f"Puntaje: {self.score} [ESPACIO +10, → +1, ← -1,\nESC termina]", True, (220, 220, 220))
        self.screen.blit(t1, (20, 20))
        self.screen.blit(t2, (20, 60))

    def draw_leaderboard(self):
        t1 = self.font.render("Top 10 puntajes", True, (220, 220, 40))
        self.screen.blit(t1, (20, 20))
        rows = db.top_n(self.conn, 10)
        y = 60
        for idx, row in enumerate(rows, start=1):
            line = f"{idx}. {row['nombre']:<12}\n{row['puntaje']:>5} (Nivel {row['nivel']})"
            t = self.font.render(line, True, (220, 220, 220))
            self.screen.blit(t, (40, y))
            y += 26
        t2 = self.font.render("[ENTER] para jugar de nuevo", True, (180, 180, 255))
        self.screen.blit(t2, (20, y + 20))

    def finish_game(self):
        jugador_id = db.get_or_create_jugador(self.conn, self.name.strip())
        db.registrar_puntuacion(self.conn, jugador_id, self.score, self.level)
        self.state = "leaderboard"

    def reset(self):
        self.name = ""
        self.score = 0
        self.level = 1
        self.state = "ask_name"

    def quit(self):
        try:
            self.conn.close()
        except Exception:
            pass
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()