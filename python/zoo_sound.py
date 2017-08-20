""" Python script to play wav files based on GPIO signals"""

import pyaudio
import wave
import sys
import threading
import time
import random
import math
import RPi.GPIO as GPIO

g_chunk       = 1024
g_gpio_pins   = {'monkey':26,'elephant':20}
g_switch      = {'monkey':False,'elephant':True}

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

    def run(self):
        print '=== Generating animal voice of ' + self._animal + ' ==='
        while True:
            if(g_switch[self._animal]):
                l_wavfile_name = self._wavfiles[int(math.floor((random.random()*self._num_files)))]
                print 'Playing...: ' + l_wavfile_name

                l_wavfile = wave.open(l_wavfile_name, 'rb')
                l_pyaudio = pyaudio.PyAudio()
                l_stream = l_pyaudio.open(
                    format  = l_pyaudio.get_format_from_width(l_wavfile.getsampwidth()),
                    channels= l_wavfile.getnchannels(),
                    rate    = l_wavfile.getframerate(),
                    output  = True)
                l_data = l_wavfile.readframes(g_chunk)

                # Making sound
                while len(l_data) > 0:
                    l_stream.write(l_data)
                    l_data = l_wavfile.readframes(g_chunk)

                # Close the device
                l_stream.stop_stream()
                l_stream.close()
                l_pyaudio.terminate()

                g_switch[self._animal] = False
            
            time.sleep(0.1)

if __name__ == '__main__':

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

    while True:
        time.sleep(60)
