# Orange County Traffic Optimization (OCTO)

OCTO is a Python-based project aimed at improving traffic flow in major Florida cities through advanced pathfinding algorithms.

## Features

- **Pathfinding Algorithms**: Implements A* and Dijkstra's algorithms for optimal route calculation.
- **Map Downloading**: Includes functionality to download and process map data.
- **Statistical Analysis**: Provides tools for traffic data analysis and visualization.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/AaronGibson2/OCTO.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd OCTO
   ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

- **Running the Application**:

  ```bash
  python main.py
  ```

- **Downloading Map Data**:

  ```bash
  python downloadMap.py
  ```

## Project Structure

```plaintext
OCTO/
├── GTFO/
├── __pycache__/
├── cache/
├── data/
├── a_star.py
├── app.py
├── dijkstras.py
├── downloadMap.py
├── main.py
├── requirements.txt
├── statWindow.py
```

- **`GTFO/`**: Contains additional resources.
- **`cache/`**: Stores cached data for performance optimization.
- **`data/`**: Includes datasets and map information.
- **`a_star.py`**: Implementation of the A* pathfinding algorithm.
- **`app.py`**: Main application script.
- **`dijkstras.py`**: Implementation of Dijkstra's algorithm.
- **`downloadMap.py`**: Script for downloading and processing map data.
- **`main.py`**: Entry point of the application.
- **`requirements.txt`**: List of required Python packages.
- **`statWindow.py`**: Module for statistical analysis and visualization.
