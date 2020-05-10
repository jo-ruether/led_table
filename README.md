# Overview
In this repository you find the software running our self-build LED table.

## Features
* Control the table either via a **TelegramBot** or a **USB Gamepad** 
* **Spotify Connect integration** to display album art of currently played song on the table
* Display an awesome good-looking **clock**.
* Color your  life with **ColorFade**. A simple screen saver.
* Play **Tetris**. Perfectly fit every block.
* Play **Snake**. Eat as many fruits as you can without eating yourself.

# Project description
## Software architecture

## Hardware architecture

# Developer's Guide
### Naming convention
Use under_score_names, not CamelCase.

### Pixel addressing
The origin of the LED Matrix is located in the upper left corner starting with position (0,0). It is most intuitive to think of a mathematical matrix and therefore use row and col indices. Clearly speaking, **don't use x-y coordinates** as this could be confusing. Contrasting to our addressing convetion, coordinate systems usually set their origin in the bottom left corner and the first index is along the horizontal axis.