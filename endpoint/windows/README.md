# Packaging Windows Binary
Package the Windows script into a standalone executable using PyInstaller.

## Prerequisites
Python installed (version 3.8+ recommended)

```powershell
# install PyInstaller
pip install pyinstaller

cd .\endpoint\windows\
pyinstaller -F .\<BINARY_NAME>.py --distpath .\bin

# After running the command, the .exe file will be located in bin\<BINARY_NAME>.exe
```