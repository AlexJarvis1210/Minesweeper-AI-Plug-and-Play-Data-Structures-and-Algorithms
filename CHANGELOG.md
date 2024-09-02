Changelog

All notable changes to this project will be documented in this file.

[v1.21] - 28/08/2024

Added:

    Merged Game and Performance Stats: Combined the Game Stats and Performance Stats panels into a single, streamlined UI panel. This change improves the clarity and aesthetics of the game's interface, providing users with all the relevant information in one place.
    Dynamic Scaling of Text, Flags, and Mines: Implemented dynamic scaling for the text, flag, and mine icons on the board, which now adjusts according to the cell size. This ensures that all visual elements remain clear and proportionate, regardless of the board's dimensions.

Changed:

    Improved User-Selected Start Cell Logic: Refined the logic for user-selected starting positions to ensure more consistent and accurate starting cell placement, aligning with the intended user preferences.
    Reworked Random Cell Selection: Updated the random cell choice logic to address the AI's tendency to encounter a "wall" of mines. The AI now attempts to strategically bypass this "wall," improving its chances of selecting a safer cell and successfully solving the board.
    Renamed Game: The game has been rebranded as MinesweeperAI: Plug and Play Data Structures and Algorithms, reflecting its focus on customisable and experiment-friendly AI configurations.

[v1.20] - 27/08/2024

Added:

    User-Selected Starting Position: Added a feature enabling users to select the starting position on the board, allowing for fairer testing and comparison of the search algorithms.
    Knowledge Hashing and Sorting: Updated knowledge statements to be hashable and sortable, improving the performance of search algorithms and AI decision-making processes.
    Enhanced UI with Rounded Buttons: Upgraded the UI by adding rounded edges to all buttons. A helper function was introduced in the create_button method, allowing adjustable rounded corners, providing a smoother and more modern interface.
    Additional Statistics Display: Implemented additional stats in the UI to provide more insights into the AI's performance and decision-making process.

Changed:

    Board State Management: Improved the logic to accurately determine if a new game has started or if the options button has been clicked. This ensures the Board State button reflects the correct game state, enhancing user experience.
    Risk-Based Cell Selection: Removed this logic as it was causing unexpected bottlenecking. Will look to implement a better version at a later date.

Fixed:

    AI Mine Flagging: Resolved an issue where the AI occasionally failed to flag mines correctly, ensuring more accurate gameplay.

[v1.15] - 22/08/2024

Added:

    Enhanced Safe Cell Selection: Introduced the safe_cells_data_structures class, which provides different data structures (FIFO, LIFO, Sorted, Random) for selecting the next safe cell during gameplay. This modular approach allows for experimentation with various strategies to influence AI behaviour and performance.
    Risk-Based Random Selection: Improved the AI’s random move logic by parsing the knowledge data to identify and prioritize low-risk cells (under 25% mine probability). High-risk cells (25% or higher probability) are excluded from the potential selection pool, reducing the likelihood of the AI hitting a mine.
    
Changed:

    Board State Management: Implemented logic to correctly determine the game state based on whether a new game has started or the options button has been clicked. This ensures the Board State button reflects the accurate state, providing a more intuitive user experience.
    UI Enhancement - Rounded Buttons: Updated all buttons across the game UI with rounded edges, enhancing the overall aesthetic. A new helper function was added to the create_button method, allowing for adjustable rounded corners on all buttons, contributing to a smoother and more modern interface.

[v1.14] - 19/08/2024

Added:

    Board State Option: Introduced a new "Board State" option in the Options Menu, allowing players to toggle between starting a new game or using a previously saved board. This addition facilitates fairer testing of search algorithms by ensuring they operate on identical board states.
    Multiple Search Algorithms: Implemented several new search algorithms within the AI logic, allowing users to select and experiment with different strategies directly from the game’s menu.
    Performance Stats Panel: Added a "Performance Stats" toggle in the Options Menu that enables or disables the display of live algorithm statistics during gameplay. This feature provides insights into the AI's decision-making process, helping players better understand the algorithm's efficiency.

Changed:

    Options Menu Layout: Reorganized the Options Menu to include the new "Board State" option and search algorithm selection. The layout was adjusted to maintain a clean and intuitive interface, accommodating these new features while preserving user experience.
    Game Initialization: Enhanced the game initialization logic to support both new and existing board states, ensuring a seamless transition between different gameplay modes. This change also ensures that the selected algorithm is correctly initialized with the chosen board state.
    Play Button Logic: Updated the logic tied to the "Play Game" button to account for the selected board state, ensuring the game starts with the correct settings.
    UI Refactoring: Refactored UI components to support the integration of buttons and input boxes within table cells. This improvement enhances the flexibility of the UI, allowing for more dynamic and interactive menu elements.



[v1.13] - 15/08/2024

Added

    New Fonts: Integrated new fonts into the game to enhance the user interface's visual appeal.
    Colour Control: Implemented centralised colour control within the UI class, allowing for easier modification of the game's colour scheme.

Changed

    Font Management: Streamlined the font system by moving font management logic from the Game class to the UI class. This change simplifies the selection of fonts and sizes, ensuring consistency across the entire game.
    Click per Turn Logic: Improved the "Click per Turn" game speed option, which requires the player to click the button for every AI turn. The associated logic in the main game loop and menu button has been refined for better user interaction.

Fixed

    Menu Button Logic: Resolved issues with the "Click per Turn" button, ensuring that the correct speed options are applied during gameplay.

[v1.12] - 13/08/2024

Changed

    Final Code Refactor: Performed a comprehensive refactor of the entire codebase, ensuring all classes, methods, and variables adhere to PEP8 standards for improved readability and maintainability.
    Code Readability: Rewrote all variable and method names to be more descriptive, aligning with best practices and enhancing code clarity.
    Artefact and Duplicate Code Removal: Removed all duplicate and unnecessary code, streamlining the codebase for optimal performance and reduced complexity.
    Class Structure and Modularity: Enhanced the modularity of the project by refining the interactions between classes, ensuring better encapsulation and a more cohesive code structure.

[v1.11] - 13/08/2024
Added

    UI Refactor: The UI has been fully extracted into a separate UI class, making the code more modular and easier to maintain. This class handles all UI elements, such as buttons, labels, and input boxes.
    Speed Button: Replaced the previous dropdown menu with a Speed Button, allowing users to cycle through "Normal", "Fast", and "Insane" game speeds.
    Game State Refactor: The game logic has been divided into three distinct classes:
        RunGame: Handles the main game loop and integrates with the Game and UI classes.
        Game: Manages the state of the game, including the board, mines, and AI.
        UI: Manages all user interface elements, including buttons and input fields.

Fixed

    Speed Button Functionality: Fixed the issue where the speed button was not cycling through the speed options correctly. It now functions as expected, updating the game speed when clicked.
    UI Element Initialization: Addressed issues where certain UI elements were not properly initialized, causing errors during gameplay. All UI components are now correctly set up during initialization.
    Button Placement: Adjusted button placement to ensure consistency across different screen sizes. Buttons are now fixed in the top-right corner of the screen, aligned horizontally.

Changed

    Code Modularity: Significant refactoring of the codebase, improving modularity by splitting responsibilities among the RunGame, Game, and UI classes. This change enhances code maintainability and readability.
    Class Interaction: Streamlined the interaction between classes by using getters and setters where appropriate, ensuring data encapsulation and reducing direct manipulation of class attributes.

[v1.1] - 11/08/2024
Added

    Code Refactoring: Rebuilt the structure of the code base, extracting all classes into their own Python files and rebuilding the object references.
        Implemented encapsulation processes:
            Setters and getters for class interactions.
            Internal data handling by classes themselves.
    Full Automation: Enabled full automation of gameplay, removing the need for manual interaction.
    Graphical Enhancements: Added graphical representation for flagged mines, enhancing the visual experience.
    User Input for Board Size: Added functionality to adjust board size via user input, allowing for customized gameplay.2

[v1.02] - 10/08/2024
Added

    Dynamic Board Resizing: Introduced dynamic board resizing to adapt to different screen resolutions, including 1080p (1920x1080) resolution.
        The game board now occupies 2/3 of the screen width, centered within a game box.
        The right 1/3 of the screen is reserved for buttons and future data displays.
    AI Playthrough Mode: Implemented a feature where the AI can play through the entire game after a single click of the "AI Move" button, playing until the game is won or lost.
    Final Cell Reveal Animation: Added a visual effect where the AI reveals all remaining cells in a row-by-row, left-to-right fashion when it detects that it has won the game.
    User Input Options: Added user input fields on the menu screen to allow users to specify board size, number of mines, and game speed.
        The game speed can now be adjusted via a dropdown menu with options for "Normal", "Fast", and "Insane" speeds.
        Default values of 8x8 for board size and mines are pre-filled in the input fields.
    Tab and Enter Navigation: Added keyboard navigation to the menu screen, allowing users to navigate between input fields using the Tab key and to change game speed or start the game with the Enter key.

Fixed

    Consistent AI Move Speed: Adjusted AI movement speed to be consistent at approximately 2 moves per second, eliminating janky speed changes during gameplay.
    Font Scaling: Improved font scaling for cell numbers, ensuring they dynamically adjust in size relative to the cell size, especially on larger boards.
    Screen Update Handling: Resolved issues with screen updates, ensuring flags and cells are revealed smoothly and in real-time as the AI makes moves.
    Input Field Alignment: Corrected the alignment of input fields, dropdowns, and labels on the menu screen to ensure a clean and consistent layout.
    Dropdown Functionality: Fixed issues with the game speed dropdown menu, ensuring that the speed option changes correctly when clicked.

Changed

    Screen Resolution: Updated the game screen to 1080p (1920x1080) to provide a full HD gaming experience.
    Code Refactoring: Simplified and optimized several methods:
        compute_board_size Method: Refactored to calculate board dimensions and cell sizes dynamically based on the current screen and game box size.
        draw_board Method: Updated to use the new board origin points and ensure consistent board centering.
        AI Move Handling: Removed redundant code in AI move handling to ensure smooth gameplay and animation.
        Input Handling: Improved the handling of user inputs and interactions on the menu screen, including better focus management and error handling for invalid inputs.

[v1.01] - 08/08/2024
Added

    Knowledge Base Management: Implemented the add_knowledge method to update the AI's knowledge base with new cell and mine information.
    Automated Gameplay: Introduced full automation of gameplay, removing the need for manual clicks.
    Graphical Enhancements: Added visual indicators for flagged mines, improving the user experience.
    User Input for Board Size: Enabled user input to adjust the board size dynamically, allowing for customized game setups.

Fixed

    Mine Count Inferences: Corrected logical errors that caused incorrect mine count inferences, ensuring the AI's knowledge base is accurate.
    Index Errors: Fixed issues where manipulating the knowledge list during iterations caused index errors, improving stability.
    Safe Cell and Mine Handling: Improved how the AI handles known safe cells and mines when updating its knowledge base.

Changed

    Refactoring: Major refactor of the codebase to use setters and getters where appropriate, enhancing encapsulation and code organization.
    Knowledge Base Optimization: Improved the clean_and_sort_knowledge_base method for more efficient management of the AI's knowledge base.
    Inference Logic: Enhanced the check_and_mark_cells method to better identify and mark safe cells and mines.
    Loop Structure Improvements: Refined the loop structure to ensure all possible inferences are made before concluding the add_knowledge method.
    Class Structure: Split classes into separate files for better organization:
        minesweeper.py for the main game logic.
        ai.py for the Minesweeper AI.
        sentence.py for the Sentence class.
