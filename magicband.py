#!/usr/bin/env python
from __future__ import print_function
import argparse
import binascii
import logging
import hashlib
import struct
#import ndef
import hmac
import cli
import sys
import os
import time
import board
import neopixel
import time
import os.path
from os import path
import random 
import configparser
from json import dumps
from httplib2 import Http

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

config = configparser.ConfigParser()
config.read('settings.conf')
print_band_id = bool(config.get('Settings', 'print_band_id'))
reverse_circle = bool(config.get('Settings', 'reverse_circle'))
ring_pixels = int(config.get('Settings', 'ring_pixels'))
mickey_pixels = int(config.get('Settings', 'mickey_pixels'))

COLOR_GREEN = eval(config.get('Settings', 'COLOR_GREEN'))
COLOR_RED = eval(config.get('Settings', 'COLOR_RED'))
COLOR_BLUE = eval(config.get('Settings', 'COLOR_BLUE'))
COLOR_WHITE = eval(config.get('Settings', 'COLOR_WHITE'))
COLOR_PURPLE = eval(config.get('Settings', 'COLOR_PURPLE'))
COLOR_LIGHTBLUE = eval(config.get('Settings', 'COLOR_LIGHTBLUE'))
COLOR_STITCH = eval(config.get('Settings', 'COLOR_STITCH'))
COLOR_GRAY = eval(config.get('Settings', 'COLOR_GRAY'))
COLOR_YELLOW = eval(config.get('Settings', 'COLOR_YELLOW'))

sequences = eval(config.get('Settings', 'sequences'))

# GPIO Pin (Recommend GPIO18)
pixel_pin = board.D18

######### DON'T EDIT BELOW THIS LINE ##########################

if sys.version_info.major < 3:
    sys.exit("This script requires Python 3")

log = logging.getLogger('main')

log.setLevel(logging.CRITICAL)

# Pre init helps to get rid of sound lag
pygame.mixer.pre_init(44100, -16, 1, 512 )
pygame.mixer.init()
pygame.init()

class MagicBand(cli.CommandLineInterface):
    def __init__(self):
        self.RING_LIGHT_SIZE = 4
        self.total_pixels = ring_pixels+mickey_pixels
        self.ring_pixels = ring_pixels
        self.pixels = neopixel.NeoPixel(pixel_pin, self.total_pixels, brightness=1.0, auto_write=False, pixel_order=neopixel.RGB)
        self.rdwr_commands = { }
        self.playStartupSequence() 
        parser = ArgumentParser(
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description="")
        super(MagicBand, self).__init__(parser, groups="rdwr dbg card clf")

    def on_rdwr_startup(self, targets):
        return targets

    # play startup sequence
    def playStartupSequence(self):
        for x in range(0,3):
            self.do_lights_on(COLOR_WHITE)
            time.sleep(.5)
            self.do_lights_off()
            time.sleep(.5)

    # Preload sound
    def loadSound(self, fname):
        if fname == '':
            return False
        if not path.exists(fname):
            print("Missing sound file :" + fname)
            return False
        return True

    def loadWebHook(self, fname):
        if fname == '':
            return False
        if not path.exists(fname):
            print("Missing Webhook :" + fname)
            return False
        return True

    # play sound
    def playSound(self, fname):
        pygame.mixer.music.load(fname)
        pygame.mixer.music.play()
     

    # Returns bandid values if that bandid exists, otherwise returns random 'any*'  
    def lookupBand(self, bandid):
        if bandid in sequences:
            return sequences.get(bandid)

        # bandid not found, return a random sound that begins with 'any'
        lst = [] 
        for key,ele in sequences.items():
            if key.startswith('any'):
                lst.append(ele)
        randomsound = random.choice(lst)
        return randomsound 

    def on_rdwr_connect(self, tag):
        bandid = str(binascii.hexlify(tag.identifier),"utf-8") 
        if print_band_id == True:
            print("MagicBandId = " + bandid)
        sequence = self.lookupBand(bandid)
        self.playSequence(sequence)


    def playSequence(self, sequence):
        ringSoundFound = self.loadSound(sequence.get('spin_sound')) 
        soundFound = self.loadSound(sequence.get('sound'))
        webhookFound = self.loadWebHook(sequence.get('webhook'))
        if ringSoundFound == True:
            self.playSound(sequence.get('spin_sound'))

        self.do_lights_circle(sequence.get('color_ring'), reverse_circle)

        if soundFound == True:
            self.playSound(sequence.get('sound')) 

        if webhookFound == True:
           message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
           http_obj = Http()
           response = http_obj.request(
              uri=self.loadWebHook(sequence.get('webhook')),
              method='POST',
              headers=message_headers,
              body=dumps(bot_message),
           )
           print(response)

        # All lights on
        self.do_lights_on_fade(sequence.get('color_mouse'))
        time.sleep(sequence.get('hold_seconds'))
        self.do_lights_off_fade() 
        self.pixels.brightness = 1.0
        return True

    def on_card_startup(self, target):
        # Nothing needed
        log.info("Listening for magicbands")

    def color_chase(self, color, wait, reverse):
        size = self.RING_LIGHT_SIZE
        for i in range(self.ring_pixels+size+1):
            for x in range(1, size):
                if (x+i) <= self.ring_pixels:
                    pixelNum = x + i
                    if reverse == True:
                        pixelNum = self.ring_pixels- (pixelNum - 1)
                    self.pixels[pixelNum] = color
            if (i > size) :
                off = (i-size)
                if reverse == True:
                    off = self.ring_pixels- (off - 1)
                self.pixels[off] = 0
            self.pixels.show()
            time.sleep(wait)

    def do_lights_circle(self,color, reverse):
        #self.color_chase(color,.01, reverse)
        self.color_chase(color,.01, reverse)
        self.color_chase(color,.001, reverse)
        self.color_chase(color,.0001, reverse)
        self.color_chase(color,.0001, reverse)

    def do_lights_on(self, color):
        for i in range(self.total_pixels):
            self.pixels[i] = color
        self.pixels.show()

    def do_lights_on_fade(self, color):
        for i in range(self.total_pixels):
            self.pixels[i] = color
        j = .01
        for x in range(100):
            j = j + .01
            self.pixels.brightness = j
            self.pixels.show()
            time.sleep(.001)

    def do_lights_off_fade(self):
        j = 1.01
        for x in range(100):
            j = j - .01
            self.pixels.brightness = j
            self.pixels.show()
            time.sleep(.0005)
        self.do_lights_off()

    def do_lights_off(self):
        for i in range(self.total_pixels):
            self.pixels[i] = 0
        self.pixels.show()

    def run(self):
        while self.run_once():
            log.info('.')

class ArgparseError(SystemExit):
    def __init__(self, prog, message):
        super(ArgparseError, self).__init__(2, prog, message)

    def __str__(self):
        return '{0}: {1}'.format(self.args[1], self.args[2])

class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgparseError(self.prog, message)


if __name__ == '__main__':
    try:
        MagicBand().run()
    except ArgparseError as e:
        print("exception")
        print(e)
        _prog = e.args[1].split()
    else:
        sys.exit(0)

