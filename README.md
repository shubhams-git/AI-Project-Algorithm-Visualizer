# Robot Navigation Software

## Overview
This Robot Navigation software simulates a robot navigating through a grid-based environment, aiming to reach a designated goal while avoiding obstacles. The project implements various tree-based search algorithms to explore different pathfinding techniques in artificial intelligence.

## Features
- **Multiple Search Algorithms**: Includes BFS, DFS, A*, Greedy Best-First Search, and custom strategies like Depth-Limited DFS and Hill Climbing.
- **Automated Testing Framework**: Facilitates the evaluation of algorithms against predefined scenarios to ensure robustness and efficiency.
- **Graphical User Interface**: Built using Pygame, provides a real-time visual representation of the navigation process, enhancing user interaction and understanding.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Pygame
- Pygame GUI
- Installation of Python and necessary libraries.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/robot-navigation.git

2. Navigate to the cloned repository:
    cd robot-navigation

3. Install required Python packages:
    pip install -r requirements.txt


## Usage
To run the program, navigate to the project directory and execute the following in the command line:
    python Run.py <text_file_name>.txt <Algorithm name>

Replace <text_file_name>.txt with the path to your grid configuration file, and <Algorithm name> with one of the supported algorithms: BFS, DFS, GBFS, AS, CUS1, or CUS2.

Running the GUI
To launch the graphical interface:
    python gui.py <text_file_name>.txt

Tests
To run automated tests across various scenarios:
    python tests.py

This will generate test cases and run them through the configured algorithms, outputting a summary of results.

Contributing
Contributions are welcome, and any contributions you make are greatly appreciated. If you have a suggestion that would make this better, please fork the repo and create a pull request.

License
Distributed under the MIT License. See LICENSE for more information.

Acknowledgements
    This project is inspired by the algorithms provided by AimaCode.
    Special thanks to resources that helped in understanding and implementing the Pygame library and subprocess module in Python.


### Notes:
- **Repository URL**: Make sure to replace `https://github.com/yourusername/robot-navigation.git` with the actual URL to your GitHub repository.
- **License**: If you decide to use a license other than MIT, update this section accordingly and make sure the license text is available in your repository, typically in a file named `LICENSE`.
- **Requirements File**: If your project has external dependencies, ensure that a `requirements.txt` file is present in the repository and lists all necessary packages.

This README provides a comprehensive guide to your project, making it easy for others to understand, use, or contribute to your work.
