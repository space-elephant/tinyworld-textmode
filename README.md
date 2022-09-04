# tinyworld-textmode
[T in Y World](http://radar.spacebar.org/f/a/weblog/comment/1/1081) is a game where users create levels, and levels contain rules to control other elements of the level. T in Y world was originally created by Tom7 for Ludam Dare 23, using flash. Flash is dead, so I remade it to run in the terminal on modern operating systems.

## Installation

### Download
Click the green "Code" button then "Download zip", or
```
git clone https://github.com/space-elephant/tinyworld-textmode.git
```

### Dependencies  
You'll need to have [Python](https://www.python.org/downloads) installed, then install these dependencies with [pip](https://pip.pypa.io/en/stable/getting-started/):
```bash
pip3 install requests
pip3 install argparse
# pyrebase is optional -- you only need it to play online levels
pip3 install pyrebase # Linux & MacOS 
pip3 install pyrebase4 # Windows
pip3 install windows-curses # only on Windows
```

### Running
On Linux & MacOS, in the terminal, `cd` to the tinyworld-textmode directory then
```
./play.py
```
On Windows, you should be able to directly double-click `play.py`, or in CMD
```
.\play.py
```
