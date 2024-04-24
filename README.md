# Robot Navigation Software

## Overview
This Robot Navigation software simulates a robot navigating through a grid-based environment, aiming to reach a designated goal while avoiding obstacles. The project implements various tree-based search algorithms to explore different pathfinding techniques in artificial intelligence.

## Features
- **Multiple Search Algorithms**: Includes BFS, DFS, A*, Greedy Best-First Search, Depth-Limited DFS and Hill Climbing.
- **Automated Testing Framework**: Facilitates the evaluation of algorithms against predefined scenarios to ensure robustness and efficiency.
- **Graphical User Interface**: Built using Pygame, the algorithm visualiser provides a visual representation of the navigation process, enhancing user interaction and understanding.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Pygame
- Pygame GUI
- Installation of Python and necessary libraries.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/shubhams-git/Intro_to_AI_assignment_1.git

2. Navigate to the cloned repository:
    cd robot-navigation

3. Install required Python packages:
    pip install -r requirements.txt


### Usage
1. To run the program, navigate to the project directory and execute the following in the command line:
    ```bash
    python Run.py text_file_name.txt <Algorithm name>

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



Acknowledgements
    Special thanks to resources that helped in understanding and implementing the Pygame library and subprocess module in Python.


### Notes:
**Requirements File**: 
- Open a text editor.
- Paste the below content into the editor.
- Save the file as requirements.txt in the root directory of your project.

    ```bash
    pygame==2.1.2
    pygame-gui==0.5.7


