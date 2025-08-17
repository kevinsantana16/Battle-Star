import pygame
import sys
import random
from db_manager import DBManager    

class Game:
    def __init__(self):
        pygame.init()

        self.width, self.height = 1200, 1000
        self.game_over = False  

        # Database
        self.db = DBManager()
        self.high_score = self.db.get_high_score()

        # Score
        self.score = 0
        self.font = pygame.font.Font(None, 60)
        self.clock = pygame.time.Clock()

        # Screen    
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.image.load("assets/background_3.png")
       
         # Player
        self.player_image = pygame.image.load("assets/nave_111x111_2.png").convert()
        self.player_image.set_colorkey((0, 0, 0))
        self.player_rect = self.player_image.get_rect(center=(600, 700))

        # Enemies
        self.enemy_image = pygame.image.load("assets/rocha_3.png").convert()
        self.enemy_speed = 5
        self.enemy_image.set_colorkey((0, 0, 0))
        self.enemy_rect = self.enemy_image.get_rect(
            topleft=(random.randint(0, self.width - self.enemy_image.get_width()), 50)
        )
        self.enemy_rect_2 = self.enemy_image.get_rect(
            topleft=(random.randint(0, self.width - self.enemy_image.get_width()), 50)
        )

    def enemy_movement(self, enemy_rect):
        enemy_rect.y += self.enemy_speed
        if enemy_rect.top > self.height:
            enemy_rect.x = random.randint(0, self.width - enemy_rect.width)
            enemy_rect.y = -enemy_rect.height
            self.score += 1

        if enemy_rect.collidepoint(self.player_rect.center):
           if self.score > self.high_score:
            self.high_score = self.score
            self.db.save_score(self.high_score)
           self.game_over = True

    def player_movement(self):
        keys = pygame.key.get_pressed()
        player_speed = 15

        if keys[pygame.K_a] and self.player_rect.left > 0:
            self.player_rect.x -= player_speed
        if keys[pygame.K_d] and self.player_rect.right < self.width:
            self.player_rect.x += player_speed
        if keys[pygame.K_w] and self.player_rect.top > 0:
            self.player_rect.y -= player_speed
        if keys[pygame.K_s] and self.player_rect.bottom < self.height:
            self.player_rect.y += player_speed

    def reset_game(self):
        """Reinicia o jogo"""
        self.score = 0
        self.enemy_speed = 10
        self.player_rect.center = (600, 700)
        self.enemy_rect.topleft = (random.randint(0, self.width - self.enemy_image.get_width()), 50)
        self.enemy_rect_2.topleft = (random.randint(0, self.width - self.enemy_image.get_width()), 50)
        self.game_over = False

    def show_game_over_screen(self):
        """Tela de Game Over"""
        self.screen.fill((0, 0, 0))

        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, (255, 215, 0))
        restart_text = self.font.render("Pressione R para Reiniciar ou Q para Sair", True, (200, 200, 200))

        self.screen.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2, 300))
        self.screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 400))
        self.screen.blit(high_score_text, (self.width // 2 - high_score_text.get_width() // 2, 460))
        self.screen.blit(restart_text, (self.width // 2 - restart_text.get_width() // 2, 550))

        pygame.display.flip()

        # Espera por ação do jogador
        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.db.close()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Reiniciar
                        self.reset_game()
                        return
                    elif event.key == pygame.K_q:  # Sair
                        self.db.close()
                        pygame.quit()
                        sys.exit()

def run(self):
    while True:
        
        # Processa eventos antes do movimento
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.db.close()
                pygame.quit()
                sys.exit()

        # Movimento só no jogo ativo
        if not self.game_over:
            self.player_movement()
            self.enemy_speed += 0.01
            self.enemy_movement(self.enemy_rect)
            self.enemy_movement(self.enemy_rect_2)
        
        
        if self.game_over:
            self.show_game_over_screen()

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))

  

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player_image, self.player_rect)
        self.screen.blit(self.enemy_image, self.enemy_rect)
        self.screen.blit(self.enemy_image, self.enemy_rect_2)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    run(game)
