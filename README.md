# nyc-subway-sign
Display subway arrivals times on an LED Matrix via Raspberry Pi. Now if only the trains can run on time...

## Overview
The MTA provides public [real time feeds](https://api.mta.info/#/subwayRealTimeFeeds) for each of its subway lines. This project uses:
- a FastAPI backend to send requests and parse responses from the real time feeds 
- a TypeScript frontend to display responses (train times, line names, etc.) on a LED Matrix via the [rpi-led-matrix](https://www.npmjs.com/package/rpi-led-matrix) package

## Materials
Below is a list of materials and where to find them. 

1. [**Raspberry Pi**](https://www.adafruit.com/product/4292)

    The specific model used within photos is the Raspberry Pi 4 Model B (2GB RAM). If you plan to use the linked matrix bonnet, be sure to choose a model that has a 40-pin GPIO header. [**As of writing, the matrix bonnet does not yet support the Raspberry Pi 5.**](https://github.com/hzeller/rpi-rgb-led-matrix/issues/1603). 


2. [**LED Matrix**](https://www.adafruit.com/product/2278)
    
    Times are displayed on a single 64x32 LED Matrix. If you plan to chain multiple displays together, your power supply needs will change. Check your LED matrix specs for power needs.

3. [**Adafruit HAT / Matrix Bonnet**](https://www.adafruit.com/product/3211)
    
    Connects the 40-pin GPIO header on the Raspberry Pi to the LED Matrix. "Plug and play", no need to solder. 

4. **Power Supplies**

    - [5V 3A USB C](https://www.amazon.com/gp/product/B08523QCT6/) to power the Raspberry Pi
    - [5V 4A Wall Adapter](https://www.amazon.com/gp/product/B087LY41PV/) to power one LED Matrix


5. [**MicroSD Card**](https://www.amazon.com/gp/product/B08TJTB8XS/)
    
    Needed to install Raspberry Pi OS.


## Running via Docker Compose
After initial set up for your Raspberry Pi, you will need to install Docker. Instructions are dependent on your version of Raspberry Pi OS. 

- [64-bit instructions](https://docs.docker.com/engine/install/debian/) *version used in photos*
- [32-bit instructions](https://docs.docker.com/engine/install/raspberry-pi-os/)

Both the frontend and backend of the sign run on Docker containers. The `docker-compose` file sets environment variables that control:

- The specific station to get times for via `GTFS_STOP_ID`
- Minimum time to arrival in minutes via `MIN_MINS`
- Maximum time to arrival in minutes via `MAX_MINS`

After setting these to your preferences, build and run the containers on your Raspberry Pi. After the backend application is healthy, the frontend begins making requests to fetch times from the MTA API. Check the `subway-stations.csv` file to find your station's `GTFS_STOP_ID`.

*A note: You may need to use `sudo` before calling `docker`*

```
sudo docker compose build # build the images
sudo docker compose up # start the containers
```
