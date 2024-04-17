import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 800
screen = pygame.display.set_mode((width, height))

# Colors
WHITE = (255, 255, 255)
GRAY = (70, 70, 70)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

# Grid dimensions
grid_size = 20  # 20x20 grid
cell_size = width // grid_size

def draw_grid(walls, agent_pos, goal_pos):
    for x in range(grid_size):
        for y in range(grid_size):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if (x, y) in walls:
                pygame.draw.rect(screen, GRAY, rect)
            elif (x, y) == agent_pos:
                pygame.draw.rect(screen, RED, rect)
            elif (x, y) == goal_pos:
                pygame.draw.rect(screen, GREEN, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Draw grid lines

def update_cell(x, y, color):
    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, color, rect)

def main():
    # Example positions (customize these)
    walls = {(1, 1), (1, 2), (2, 1)}
    agent_pos = (0, 0)
    goal_pos = (19, 19)
    
    clock = pygame.time.Clock()

    # Initial drawing
    screen.fill(BLACK)
    draw_grid(walls, agent_pos, goal_pos)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dummy pathfinding update for demonstration
        for x in range(grid_size):
            for y in range(grid_size):
                if (x, y) not in walls and (x, y) != agent_pos and (x, y) != goal_pos:
                    update_cell(x, y, YELLOW)  # Visited
                    pygame.display.flip()
                    pygame.time.delay(50)

        # Final path (example)
        for i in range(grid_size):
            update_cell(i, i, ORANGE)  # Path
            pygame.display.flip()
            pygame.time.delay(100)

        running = False  # Stop after one full display

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
