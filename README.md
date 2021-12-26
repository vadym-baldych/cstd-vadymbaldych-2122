# cstd-vadymbaldych-2122

- **Student**: Vadym Baldych
- **Student number**: 1
- **Group**: KI-47

## Task: 
Create *Tic-Tac-Toe* game.
HW interface - SPI.
Data drive format XML.

## DB installation:
Download SQL Server Developer installation from https://www.microsoft.com/en-us/sql-server/sql-server-downloads.
During installation click on "New SQL Server stand-alone installation...".
In "Feature Selection" tab check "Database Engine Services".
Copy your server name and replace {YOUR-SERVER-NAME} with it in config.py.

## How to build:
- Install Python 3 and above (*https://www.python.org/downloads/*).
- Install Arduino CLI (*https://arduino.github.io/arduino-cli/0.20/installation/*).
- Tests will run automatically before the build.
- Place *arduino-cli.exe* inside the project folder (along with build.bat).
- Adjust the second line in build.bat **"set COM_PORT="COM3"**. Replace **COM3** with your COM port which is used by your Arduino board.
- Run *build.bat*.

## Added:
- Added statistics for X and O. Data stored in file.
- Added AI. Man VS AI is working now. AI realized using minimax algorithm.
For AI to make a turn you need to click.