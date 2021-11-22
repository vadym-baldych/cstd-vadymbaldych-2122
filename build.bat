@echo off
set COM_PORT="COM4"

pip install pyinstaller
pip install pyserial
pip install xmltodict
pip install pygame

arduino-cli core install arduino:avr

rmdir /s /q "./client/build"
xcopy "client/src/assets" "client/build/assets" /s /e /y /i
pyinstaller --noconsole --onefile "client/src/main.py" --name tictactoe --specpath ./client/build/spec --distpath ./client/build --workpath ./client/build/work

arduino-cli.exe compile --fqbn arduino:avr:uno ./server/src
arduino-cli.exe upload --port %COM_PORT% --fqbn arduino:avr:uno ./server/src
