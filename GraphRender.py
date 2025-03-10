import pygame
import os
import re

class GraphRender:
    def __init__(self, image_folder, algorithm, screen_width=800, screen_height=600):
        self.image_folder = image_folder
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image_files = []
        self.current_image_index = 0
        self.algorithm = algorithm
        self.screen = None

        pygame.init()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Navegar entre Imagens")

        self.load_images()

    def load_images(self):
        """Carrega e organiza as imagens na pasta em ordem numérica"""
        self.image_files = [f for f in os.listdir(self.image_folder) if re.match(r'graph_iteration_\d+_' + re.escape(self.algorithm), f)]

        self.image_files.sort(key=self.extract_iteration_number)

        if not self.image_files:
            print("Nenhuma imagem encontrada na pasta.")
            pygame.quit()
            exit()

    def extract_iteration_number(self, filename):
        """Extrai o número de iteração de um nome de arquivo"""
        match = re.search(r'graph_iteration_(\d+)', filename)
        if match:
            return int(match.group(1))
        return -1

    def display_image(self, image_path):
        """Exibe a imagem na tela"""
        image = pygame.image.load(image_path)
        image = pygame.transform.smoothscale(image, (self.screen_width, self.screen_height))
        self.screen.fill((255, 255, 255)) 
        self.screen.blit(image, (0, 0))
        pygame.display.update()

    def navigate(self):
        """Loop principal para navegação entre imagens"""
        self.display_image(os.path.join(self.image_folder, self.image_files[self.current_image_index]))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
                    elif event.key == pygame.K_RIGHT:
                        self.current_image_index = (self.current_image_index + 1) % len(self.image_files)

                    self.display_image(os.path.join(self.image_folder, self.image_files[self.current_image_index]))

            pygame.time.Clock().tick(60)

        pygame.quit()

