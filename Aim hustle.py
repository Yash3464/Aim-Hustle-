import pygame
import random
import tkinter as tk
from tkinter import messagebox

# Setup Tkinter
root = tk.Tk()
root.title("AIM HUSTLE")

# Function to start the game with the selected level
def start_game(level):
    root.withdraw()  
    score = game(level)
    messagebox.showinfo("Game Over", f"Your score: {score}%")

# Main game function
def game(level):
    pygame.init()
    WHITE = (240, 255, 255)
    BLACK = (0, 0, 0)

    WIDTH, HEIGHT = 1100, 750
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AIM HUSTLE")

    background_image = pygame.image.load('background2.jpg').convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    agent_image = pygame.image.load('circle.png').convert_alpha()
    agent_image = pygame.transform.scale(agent_image, (80, 80))

    # Target class
    class Target(pygame.sprite.Sprite):
        def _init_(self):
            super()._init_()
            self.image = agent_image
            self.rect = self.image.get_rect()

            # Define the movement area boundaries
            movement_area_x_min = 100  # Minimum x position
            movement_area_x_max = WIDTH - 100  # Maximum x position
            movement_area_y_min = 100  # Minimum y position
            movement_area_y_max = HEIGHT - 100  # Maximum y position

            # Set the target's initial position within the defined movement area
            self.rect.center = (
                random.randint(movement_area_x_min, movement_area_x_max),
                random.randint(movement_area_y_min, movement_area_y_max)
            )

    score = 0
    total_clicks = 0

    clock = pygame.time.Clock()
    all_targets = pygame.sprite.Group()
    target_timer = 0

    # Set target interval based on difficulty level
    if level == "beginner":
        target_interval = 1000
    elif level == "intermediate":
        target_interval = 800
    elif level == "hard":
        target_interval = 500

    game_duration = 40000  # 40 seconds
    start_time = pygame.time.get_ticks()
    running = True

    while running:
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                total_clicks += 1
                pos = pygame.mouse.get_pos()
                for target in all_targets:
                    if target.rect.collidepoint(pos):
                        score += 1
                        target.kill()

        current_time = pygame.time.get_ticks()
        if current_time - start_time >= game_duration:
            running = False

        # Spawn new target at intervals
        if current_time - target_timer > target_interval:
            all_targets.empty()
            all_targets.add(Target())
            target_timer = current_time

        all_targets.draw(screen)

        # Display score and total clicks
        font = pygame.font.Font(None, 30)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (360, 30))

        click_text = font.render(f"Total Clicks: {total_clicks}", True, WHITE)
        screen.blit(click_text, (630, 30))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

    # Calculate accuracy score, avoiding division by zero
    if total_clicks > 0:
        return round(score / total_clicks * 100, 2)
    else:
        return 0

# Tkinter UI for difficulty selection
label = tk.Label(root, text="Select Level: ")
label.pack()

var = tk.StringVar(root)
beginner_button = tk.Radiobutton(root, text="Beginner", variable=var, value="beginner")
beginner_button.pack()

intermediate_button = tk.Radiobutton(root, text="Intermediate", variable=var, value="intermediate")
intermediate_button.pack()

hard_button = tk.Radiobutton(root, text="Hard", variable=var, value="hard")
hard_button.pack()

start_button = tk.Button(root, text="Start", command=lambda: start_game(var.get()))
start_button.pack()

root.mainloop(