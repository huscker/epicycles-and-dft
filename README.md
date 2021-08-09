# Epicycles and DFT
Simple visualisation of Fourier transform in 3 modes  
![](http://huscker.github.io/various/epicycles-and-dft.gif)
## Installation
#### Ubuntu
Install python3:  
`sudo apt update`  
`sudo apt install python3 python3-pip`  
Install dependencies:  
`pip3 install numpy scipy pygame`  
#### Arch Linux
Install python3:  
`pacman -Sy python python-pip`  
Install dependencies:  
`pip3 install numpy scipy pygame`  
## Usage
`python main.py`
#### Controls:
Left mouse click enables mouse movement  
Right mouse click add new points    
  
Keyboard actions:
- ESC - exit app
- F1 - show info
- E - clear points
- R or ENTER - refresh fourier transform
- M - cycle through modes
- SPACE - stop time
- S - stop showing user added points

Mouse move based:
- C - enter scale changing mode

Mousewheel move based:
- P - change peak detection threshold
- T - change timescale
- D - change spacing for second mode
- N - change number of points to render
