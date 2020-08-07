# Addendum

This is mostly the excellent code written by [Enzo SR](https://github.com/e-sr/moonboard) with some modifications:
- Used a Raspberry Pi Zero W
- Added some scripts to halt/resume using a push (arcade) button

Here are some notes for reference:

## setup

Latest raspbian lite (headless). Clone the repository and make sure run.sh runs ok. requirements_...W.txt has a pip freeze of what it looks like.
- The SPI pins used are pin 19 - BCM 10 (MOSI), and pin 23 - BCM 11 (SCLK)
- The power/halt button uses pin 5 - BCM 3 (SCL), and any ground
- I used an LED wired from pin 8 - BCM 14 (TXD) to a ground to show power on/off as the system takes ~1 min to initialize

## other notes

install python3, python3-dev
install pip, easy_install3.7 requests
    sudo easy_install 3.7 websockets
    sudo /usr/bin/python3 -m pip  install python-periphereal
enable spi in raspi-config

There are two services that need to run: 
- moonboard.service (fires up run.sh which in turn runs run.py)
- com.moonboard.service (fires up moonboard_BLE_service.py)

# moonboard

This project contain software (written in python) and informations to build a led system for the MOONBOARD using a raspberrypi with integrated Bluetooth.

## Original led box

The [moonboard](https://www.moonboard.com/) smartphone app is build to work with the [moonboard led box](https://moonclimbing.com/moonboard-led-system.html) togheter (via BLE) for displaying the problems.

In this project we emulate the behaviour of the box. More details in the `ble` folder.

## LED stripes

The led used are **addressable LED** stripes. There are many type of them: ws281x, ws2801, apa102,...  

I use WS2801(4 wires with clock line) led, buyed on Aliexpress. There are plenty of suppliers. For the Mooonboard a led spacing of at last 20cm is necessary. I asked the supplier to produce the led with a custom lenght of 23 cm. I get the leds for about 25$/50pcs.   

You  will also need a powersupply to power the leds 
The led are wired directly to the raspberry without level shifting.

The led are driven by a raspberry using the SPI interface and the [bibliopixel]() python library. 


## Hardware used

- raspberry pi 3B+. 
- 200 ws2801 LED 
- power supply [meanwell mdr-60-5](https://www.meanwell.com/webapp/product/search.aspx?prod=MDR-60)


## Software
linux os, python > 3.6 (see `requirements.txt`), bluez 

### BLE process

The BLE of the raspberry is setup to act as the moonboard led box. When a problem is sent from the app to the raspberry a signal containing the problems holds is send on the dbus.
More details in the `ble` folder.

### Led driving process

This process listen on the dbus for new problem signals and display the problem on the strips when new problems are available. This part is implemented on the script `run.py`.

To have the script running at startup a systemd service has to be started. See `scripts/run.sh` and `services/moonbard.service`.


*************

## OLD, TODO, ...

- **moonboard backend service**: backend service to the moonboard app. Add `services/moonboard.service`.  
  
- **nginx service**: Webserver serving the moonboard app. See next section.  

- **optional, app client service**: you can access moonboard app using the rpi browser. To automate it at startup. Add `services/kiosk_browser.service`.  
  
To Add and start a service see `services/install_service.sh`

### Install and setup  nginx

See [Deploy your React & .NET Core Apps on Linux using Nginx and Supervisor](https://hackernoon.com/deploy-your-react-net-core-apps-on-linux-using-nginx-and-supervisor-5a29d0b6ef94)
- install nginx `sudo apt install nginx`. 
- configure nginx:   
    - open file `sudo nano /etc/nginx/sites-available/default`
    - append content  
        ```
        server {
            listen 80 default_server;
            listen [::]:80 default_server;
            # Some comments...
            root /var/www/html;  # STATIC FILE LOCATION
            # Some comments...
            index index.html index.htm index.nginx-debian.html;
            server_name _;
            location / {
                    # Some comments...
                    try_files $uri /index.html;   # ADD THIS
            }
            # Some comments...
        }
        ```  

 - copy react app folder `/buils`  to  `/var/www/html`
 - restart nginx server `sudo systemctl restart nginx.service`. See `scripts/move_build.sh` script.
