# Robot Navigation Software

## Overview
This Robot Navigation software simulates a robot navigating through a grid-based environment, aiming to reach a designated goal while avoiding obstacles. The project implements various tree-based search algorithms to explore different pathfinding techniques in artificial intelligence.

## Frameworks and Languages

### Python
The core of this project is developed using Python. The model uses Object-Oriented Programming (OOP) in Python to implement the basic setup.

### Pygame
Pygame is a set of Python modules designed for writing video games. In this project, Pygame provides the tools necessary to render the graphical interface, allowing for the visualization of the navigation algorithms.

### Pygame GUI
Pygame GUI is an extension of Pygame that facilitates the creation of user interfaces in applications that use Pygame. It provides an easier and more structured way to create buttons, text boxes, and other GUI elements, which are used extensively in this project to control the algorithm's parameters and visualize their effects interactively.


## Features
- **Multiple Search Algorithms**: Includes BFS, DFS, A*, Greedy Best-First Search, Depth-Limited DFS and Hill Climbing.
- **Automated Testing Framework**: Facilitates the evaluation of algorithms against predefined scenarios to ensure robustness and efficiency.
- **Graphical User Interface**: Built using Pygame, the algorithm visualiser provides a visual representation of the navigation process, enhancing user interaction and understanding.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Installation of Python and necessary libraries.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/shubhams-git/AI-Project-Algorithm-Visualizer.git

2. Navigate to the cloned repository:
    ```bash
    cd AI-Project-Algorithm-Visualizer

3. Install required Python packages:
    ```bash
    pip install -r requirements.txt


### Usage
1. To run the program, navigate to the project directory and execute the following in the command line:
    ```bash
    python Run.py <text_file_name>.txt <Algorithm name>

- Replace **<text_file_name>.txt** with the path to your grid configuration file, and **<Algorithm name>** with one of the supported algorithms: BFS, DFS, GBFS, AS, CUS1, or CUS2.

### Running the GUI
1. To launch the graphical interface:
    ```bash
    python gui.py <text_file_name>.txt
- Replace **<text_file_name>.txt** with the path to your grid configuration file

### Tests
1. To run automated tests across various scenarios:
    ```bash
    python tests.py

This will generate test cases and run them through the configured algorithms, outputting a summary of results.

## Contributing
Contributions are welcome, and any contributions you make are greatly appreciated. If you have a suggestion that would make this better, please fork the repo and create a pull request.



## Acknowledgements
    Special thanks to resources that helped in understanding and implementing the Pygame library and subprocess module in Python.
    - https://pygame-gui.readthedocs.io/en/latest/
    - https://www.pygame.org/docs/
    - https://github.com/aimacode/aima-python


### Notes:
**Requirements File**: 
- Easily install all required dependencies by running **pip install -r requirements.txt**, ensuring that the correct versions of Pygame and Pygame GUI are installed, facilitating a smooth setup and run of the project.

    ```bash
    pygame==2.5.2
    pygame-gui==0.6.10


