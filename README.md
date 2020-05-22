This repository contains software to drive games and apps on a 12x12 Matrix of WS2812B-LEDs. It handles different inputs such as USB hardware or Telegram bots and displays the output on a real LED matrix or a simulation.

1. [Features](#features)
2. [Project description](#project-description)
   * [Hardware architecture](#hardware-architecture)
   * [Software architecture](#software-architecture)
3. [Developer's Guide](#developers-guide)

## Features
* Control the table either via a **TelegramBot** or a **USB Gamepad** 
* **Ready-to-use simulator** makes development possible even when your table isn't built yet 
* **Spotify Connect integration** to display album art of currently played song on the table
* Display an awesome-looking **clock**.
* Color your  life with **ColorFade**. A simple screen saver.
* Play **Tetris**. Perfectly fit every block.
* Play **Snake**. Eat as much fruit as you can without eating yourself.

# Project description
## Hardware architecture
A [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) is used to control the table and to manage user interactions. The small single-board computer with a footprint of only 65mm x 35mm lets you hide the control unit in a small box unobtrusively attached to the table. Despite of its size it features a fully functional Linux system perfectly fitted for Python scripts while providing necessary interfaces like wireless LAN and USB.

![Hardware architecture](./img/hardware_architecture.svg)


## Software architecture
There are different kinds of classes making up the software as a whole. Each program part has its own function and each part can be (de-)activated separately (excluding the *Helpers*). `main.py` starts up to three threads and creates the helper classes.

![Sotware architecture](./img/software_architecture.svg)

### Application
The main thread executing the games has its entry point in `Menu.py`. Besides printing the game's icons, the Menu class also starts all other games and then waits for their return. The application thread is mainly manipulating the output matrix.

### Helpers
The *Helpers* are part of the `core` module and simply class instances passed to the threads. Note that there are no threads wrapping the *Helpers*.

The **Postman** handles the communcation between the threads.

The **ConfigHandler** provides read and write access for all program parts to the central config file.

The **Output** is a intermediate layer for writing Pixels to the table. There are two different output classes available in the submodule `output`. Either the hardware table is controlled or the output can be redirected to a simulator.

### Input Classes
Currently there are two ways of receiving user input. Either a game controller can be attached to the Pi via USB or commands can be send to the table via Telegram. Just call the TelegramBot running on your table (every table needs its own Bot id) and he/she/it will explain everything to you.

Both input classes publish input events via the Postman.

# Developer's Guide
In general, the python PIP guidelines are followed.

## Naming convention
Use under_score_names, not CamelCase.

## Pixel addressing
The origin of the LED Matrix is located in the upper left corner starting with position (0,0). It is most intuitive to think of a mathematical matrix and therefore use row and col indices. Clearly speaking, **don't use x-y coordinates** as this could be confusing. Contrasting to our addressing convetion, coordinate systems usually set their origin in the bottom left corner and the first index is along the horizontal axis.
