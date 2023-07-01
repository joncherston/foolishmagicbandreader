# magicbandreader
Reads magic bands and plays sounds and lights up leds, just like the real thing.
Use webhook URLS to trigger IOT devices.
Thanks to foolishmortalbuilders for initial creation of the project from which this fork was created.

# NOTE
This is a development branch, looking to correct memory leak, buffer underrun, and xdg environment runtime errors as well as the sound issues that accompany those errors.  
This branch is also looking to optimize for a raspberry pi zero w to reduce hardware costs.

Sound files are not included. Either supply your own mp3 sound files or search the internet for the files you would like to use.

# 3D Printer pieces:
Find the pieces to make this model on thingiverse:
https://www.thingiverse.com/thing:4271417
I am actively working on development of model casing including component brackets

# Upgrade
If you are upgrading from a previous version, be sure to re-run the install script to pick up the new required files:
sudo sh install.sh. 

BACKUP YOUR magicband.py BEFORE UPGRADING so you don't lose you sequences configurations! You'll need to migrate any old configurations that were stored in the magicband.py file to the new settings.conf file.

# New Features

* All configurations are now stored in settings.conf file instead of editing the python file directly.
* New color support including rainbow (see example config for details) Make sure you are using the newest color names.
* Webhook support for turning on lights or opening locks when a magic band is played
* Multiple sequence support per individual magic bands. (A single magicband can have multiple sequences assigned to it.)

#Basic wiring:
* Connect PIXEL LEDS to  DATA on GPIO-18 (pin 12), pixel GnD to GND (pin 6) and pixel positive to +5v (pin 2)
* Connect USB RFID reader
* Connect Speaker via HDMI connector (ONBOARD SPEAKER WILL NOT WORK DUE TO Pixel LEDS!)
* For additional sound use a small amp (wiring instructions to come)

# Installation

* See YouTube video https://youtu.be/HJ8CTLgmcSk  (UPDATED video coming June 15th 2020) 

* Install Raspbian lite onto pi. BE SURE TO INSTALL THE LITE VERSION: https://www.raspberrypi.org/downloads/raspberry-pi-os/ 
* Either use the advanced settings option when installing Raspbian onto the SD Card, Add ssh file and wpa_supplicant.conf to boot partition for wireless SSH access, or log directly into Pi
* sudo apt install git
* git clone https://github.com/joncherston/foolishmagicbandreader.git
* cd foolishmagicbandreader
* sudo sh install.sh  (this will take awhile)
* cp * /home/pi/.
* sudo reboot now
* log back into pi
* add sound files
* sudo nano /home/pi/settings.conf. and edit the led counts for your build
* sudo nano /etc/rc.local
  * Before the exit 0 line add:
  * (cd /home/pi; sudo python3 magicband.py &)
* sudo reboot now

See videos for more details
Note: if you are using the older videos to follow along, the main difference with the latest code is the settings.conf. Updated videos coming soon. 

# Config

Set the ring_pixels and mickey_pixel counts to the correct value

# Troubleshooting

If the install fails, try running this command first:
sudo apt-get update
If you have difficulty with connecting to your network, use nmcli: http://www.intellamech.com/RaspberryPi-projects/rpi_nmcli.html



