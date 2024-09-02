# 🧠 **MinesweeperAI: Plug and play data structures and algorithms**

Welcome to the project, a Python-based Minesweeper game with an AI solver.

## 🚀 Current Version: v1.21

### ✨ What's New in v1.21

- **Merged Game and Performance Stats:**

    Combined the Game Stats and Performance Stats panels into a single, streamlined UI panel. This change improves the clarity and aesthetics of the game's interface, providing users with all the relevant information in one place.
- 
    Dynamic Scaling of Text, Flags, and Mines: Implemented dynamic scaling for the text, flag, and mine icons on the board, which now adjusts according to the cell size. This ensures that all visual elements remain clear and proportionate, regardless of the board's dimensions.
    Improved User-Selected Start Cell Logic: Refined the logic for user-selected starting positions to ensure more consistent and accurate starting cell placement, aligning with the intended user preferences.
    Reworked Random Cell Selection: Updated the random cell choice logic to address the AI's tendency to encounter a "wall" of mines. The AI now attempts to strategically bypass this "wall," improving its chances of selecting a safer cell and successfully solving the board.
    Renamed Game: The game has been rebranded as MinesweeperAI: Plug and Play Data Structures and Algorithms, reflecting its focus on customizable and experiment-friendly AI configurations.


### ✨ **What's New in v1.1**
- **🔧 Code Refactoring**
  - Rebuilt the structure of the code base, extracting all classes into their own Python files and rebuilding the object references.
  - The following encapsulation process has been implemented:
    - Setters and getters implemented where another class is interacting with the data
    - Internally, classes handle their data directly 
  
- **🤖 Automation**
  - Enabled **full automation** of gameplay, eliminating the need for manual interactions.
  
- **🎨 Graphical Enhancements**
  - Introduced **graphical representation** for flagging mines, enhancing the visual experience.
  
- **🔢 User Input**
  - Added functionality allowing users to **adjust board size** through intuitive input.

---

## 📅 **Future Updates**

### v1.2 (Planned)
- **🔧 Code Refactoring**
  - Complete the code restructuring by sharing the workload of run_game.py across the other classes where appropriate.
  - Ensure the entire codebase is PEP8 compliant.
- **🖥️ User Interface Improvements**
  - Display the **live knowledge base** directly on the screen.
  - Show an **inference logic table** in action during gameplay.
  - Display the number of iterations the `add_knowledge` function takes to solve the puzzle.
  
- **🔍 Complexity Calculation**
  - Introduce a **complexity calculator** to evaluate the computational effort required for different board configurations.

### v1.3 (Planned)
- **🎨 UI Overhaul**
  - A complete **user interface overhaul** to provide a more intuitive and visually appealing experience.

---

## ⚙️ **Project Setup**

### **Prerequisites**
- **Python 3.x**
- **Pygame**

### **Installation Steps**
1. **Clone the Repository**:

   git clone https://github.com/AlexJarvis1210/MinesweeperAI

2. Navigate to the Project Directory:

cd MinesweeperAI

Install Required Packages:

    pip install -r requirements.txt

🎮 How to Play

Run the game with the following command:


    python run_game.py

Enjoy the fully automated Minesweeper experience, or test your skills by adjusting the board size and taking control`!

📚 Acknowledgements

This project was initially inspired by coursework from Harvard's CS50AI program. While the initial structure and problem were based on the course, the current codebase has been significantly expanded and rewritten, representing original work. The original code that passed the CS50 tests is available in the v1.0 branch.

📜 License

This project is licensed under the MIT License. For more details, please take a look at the LICENSE file.

For a detailed list of changes and updates, please look at the CHANGELOG.
