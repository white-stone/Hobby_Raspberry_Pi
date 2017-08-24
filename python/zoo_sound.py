""" Python script to play wav files based on GPIO signals"""

#import pyaudio
#import wave
import pygame
import sys
import threading
import time
import random
import math
import RPi.GPIO as GPIO

g_chunk       = 1024*1024
g_animals     = ['monkey','elephant']
g_gpio_pins   = {'monkey':26,'elephant':20}
g_switch      = {'monkey':False,'elephant':False,'ambience':True}

class GPIOMonitorThread(threading.Thread):
    """ Thread to monitor GPIOs """
    def __init__(self, animal):
        print 'Setting up GPIO monitor for ' + animal
        super(GPIOMonitorThread, self).__init__()
        self._animal = animal
        self._pin    = g_gpio_pins[animal]
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._pin,GPIO.IN)

    def run(self):
        print 'Starting GPIO monitor for ' + self._animal
        while True:
            if(GPIO.input(self._pin)):
                g_switch[self._animal] = True
                print self._animal + ' is ON'
            else:
                g_switch[self._animal] = False               
            time.sleep(0.1)

class AnimalVoiceThread(threading.Thread):
    """ Thread to generate animal voice """
    
    def __init__(self, animal, num_files):
        super(AnimalVoiceThread, self).__init__()
        self._animal    = animal
        self._num_files = num_files
        self._wavfiles  = []
        for suffix in range(0,self._num_files):
            self._wavfiles.append('/home/pi/wav/' + animal + '_' + str(suffix) + '.wav')
        print 'Sound file name(s) is/are ' + str(self._wavfiles)
        self._sound = []
        for l_wavfile in self._wavfiles:
            self._sound.append(pygame.mixer.Sound(l_wavfile))

    def run(self):
        print '=== Generating animal voice of ' + self._animal + ' ==='
        while True:
            print 'Loop of ' + self._animal
            if(g_switch[self._animal]):
                l_index   = int(math.floor((random.random()*self._num_files)))                
                l_channel = self._sound[l_index].play()
                while (l_channel.get_busy()):
                    time.sleep(0.1)
                    print '>'                
                g_switch[self._animal] = False         
            time.sleep(0.1)

if __name__ == '__main__':

    """ Initialize sound library """
    pygame.mixer.init()
    
    """ Ambience """
    ambience_sound = AnimalVoiceThread('ambience',1)
    ambience_sound.start()
    
    """ Monkey """
    monkey_switch = GPIOMonitorThread('monkey')
    monkey_switch.start()
    monkey_voice   = AnimalVoiceThread('monkey',3)
    monkey_voice.start()

    """ Elephant """
    elephant_switch = GPIOMonitorThread('elephant')
    elephant_switch.start()
    elephant_voice = AnimalVoiceThread('elephant',2)
    elephant_voice.start()
