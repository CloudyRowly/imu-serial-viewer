# Serial visualiser for IMU heading

![screenshot of the program](assets/Screenshot%202024-05-25%20200625.png)

## Dependency Installation

```pip install -r requirements.txt```

## Running arguments (Optional)

|Short form | full form      | type              | description                                                           | Default                             | optional |
|-----------|----------------|-------------------|-----------------------------------------------------------------------|-------------------------------------|----------|
|-p         |--com          |string               |COM port to listen to serial                                                  | COM3                                 |[X]       |
|-r         |--baudrate          |int                |Serial baud rate                                   | 115200                   |[X]       |