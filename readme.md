# Serial visualiser for IMU heading

![screenshot of the program](assets/Screenshot%202024-05-25%20200625.png)

## Requirement

Serial must send a string in the format ```Hxxx \r\n``` for the program to pickup and display

## Dependency Installation

```pip install -r requirements.txt```

## Run

Execute the file run.bat, if it does not run, use CLI to cd to the project directory and run:

```python main.py```

## Running arguments (Optional)

|Short form | full form      | type              | description                | Default      |
|-----------|----------------|-------------------|----------------------------|--------------|
|-p         |--com           |string             |COM port to listen to serial| COM3         |
|-r         |--baudrate      |int                |Serial baud rate            | 115200       |