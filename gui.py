import pygame
import pygame_gui
import sys
from Starter import Starter

# Initialize Pygame and Pygame GUI Manager
pygame.init()
pygame.display.set_caption("Algorithm Visualizer")

# Colors
WHITE = (255, 255, 255)
GRAY = (70, 70, 70)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WIN = (50, 125, 50)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

# Create the starter object
starter = Starter("test.txt")

# Get the agent and grid details from the starter object
grid_size = [starter.treebased.width, starter.treebased.length]
agent_pos = (starter.treebased.root.x, starter.treebased.root.y)
goals = [(starter.treebased.goalx, starter.treebased.goaly)]
walls = [(wall.x, wall.y) for wall in starter.treebased.wallnodes]
height = 450
cell_size = (height) // grid_size[0] 
cell_width = cell_size
cell_height = cell_size
grid_width = cell_size * grid_size[1]
total_width = grid_width + 200  # Additional 200 pixels for control panel
screen = pygame.display.set_mode((total_width, height))
manager = pygame_gui.UIManager((total_width, height))
button_height = int(height * 0.1)  # 5% of the screen height





# Define control panel area and components for algorithm selection

algorithm_buttons = {
    "BFS": pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(grid_width + 10, 50, 180, button_height),
        text='BFS',
        manager=manager
    ),
    "DFS": pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(grid_width + 10, 85, 180, button_height),
        text='DFS',
        manager=manager
    ),
    "A Star": pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(grid_width + 10, 120, 180, button_height),
        text='AStar',
        manager=manager
    ),
    "GBFS": pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(grid_width + 10, 155, 180, button_height),
        text='GBFS',
        manager=manager
    ),
    "Uniform Cost": pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(grid_width + 10, 190, 180, button_height),
        text='Uniform Cost',
        manager=manager
    ),
    "Iterative Deepening DFS": pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(grid_width + 10, 225, 180, button_height),
        text='Iterative Deepening DFS',
        manager=manager
    )
}
# Track the selected algorithm
selected_algorithm = "BFS"  # Default selection

# Create a label for displaying the step count
steps_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(grid_width + 10, height * 0.75, 180, button_height),
    text='Number of Nodes: 0',
    manager=manager
)

play_button_ui = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(grid_width + 10, height*.85, 80, button_height), text='Play', manager=manager)
stop_button_ui = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(grid_width + 110, height*.85, 85, button_height), text='Stop/Reset', manager=manager)


# Helper function to update the cell with color and redraw
def update_cell(x, y, color):
    rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
    current_color = color
    if (x, y) == agent_pos:
        current_color = RED
    elif (x, y) in goals:
        current_color = WIN
    pygame.draw.rect(screen, current_color, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)
    pygame.display.update(rect)  # Update only the modified rect

def draw_initial_state():
    """Draws the initial state of the grid, only once or upon reset."""
    screen.fill(BLACK)  # Fill the entire screen to reset
    for y in range(grid_size[0]):
        for x in range(grid_size[1]):
            rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
            color = WHITE
            if (x, y) in walls:
                color = GRAY
            elif (x, y) == agent_pos:
                color = RED
            elif (x, y) in goals:
                color = GREEN
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
    pygame.display.update()  # Update the whole screen

def main_loop():
    global selected_algorithm  # So we can modify the global variable
    running = True
    algorithm_running = False
    last_update_time = 0
    current_step = 0
    path = []
    visited = []
    clock = pygame.time.Clock()

    draw_initial_state()

    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element in algorithm_buttons.values():
                    for button in algorithm_buttons.values():
                        button.unselect()
                    event.ui_element.select()
                    selected_algorithm = event.ui_element.text
                elif event.ui_element == play_button_ui:
                    starter.reset_nodes()
                    path, visited, steps = starter.nodes_for_gui(str(selected_algorithm))
                    # Clear and update the steps label
                    rect = pygame.Rect(grid_width + 10, height * 0.75, 180, button_height)
                    pygame.draw.rect(screen, BLACK, rect)  # Assuming background is BLACK
                    steps_label.set_text(f'Number of Nodes: {steps}')
                    steps_label.rebuild()
                    if path and visited:
                        current_step = 0
                        last_update_time = pygame.time.get_ticks()
                        algorithm_running = True
                elif event.ui_element == stop_button_ui:
                    algorithm_running = False
                    draw_initial_state()  # Redraw initial state when stopped
                    steps_label.set_text('Number of Nodes: 0')  # Reset the step count label


            manager.process_events(event)

        manager.update(time_delta)

        if algorithm_running and pygame.time.get_ticks() - last_update_time > 200:
            if current_step < len(visited):
                node = visited[current_step]
                update_cell(node[0], node[1], YELLOW)
                current_step += 1
                last_update_time = pygame.time.get_ticks()
            elif current_step < len(path) + len(visited):
                node = path[current_step - len(visited)]
                update_cell(node[0], node[1], ORANGE)
                current_step += 1
                last_update_time = pygame.time.get_ticks()
            else:
                algorithm_running = False

        manager.draw_ui(screen)
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_loop()

