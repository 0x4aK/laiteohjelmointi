# RaspiMonitor

School project.

## Requirements

- Raspberry Pi 2b +
- Sense HAT add-on board
- Python3.6

## Installation

Before installing, make sure you have **sense-hat** installed:

```
sudo apt-get update
sudo apt-get install sense-hat
```

After installing **sense-hat** install RaspiMonitor from **dist** folder:

```
sudo pip3 install RaspiMonitor-1.0.0-py3-none-any.whl
```

## Usage

To run **RaspiMonitor**, use:

```
sudo raspimonitor
```

To install/remove **RaspiMonitor** as a **systemd** service, use

```
sudo raspimonitor [enable/disable]
```

This will install **RaspiMonitor** as a service, and will run on boot.
