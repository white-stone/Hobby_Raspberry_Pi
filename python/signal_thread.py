import sys
import time
import threading
###########################################################
# LED Control for Rei's Homework
###########################################################

# Import PCA9685 module.
sys.path.append('../driver/i2c/pwm/')
import pwm_PCA9685


# Initialise the PCA9685 using the default address (0x40).
pwm = pwm_PCA9685.pwm_PCA9685()
    
# Alternatively specify a different address and/or bus:
#pwm = pwm_PCA9685.PWM_PCA9685(address=0x41, busnum=2)
    
# Definiation of PWM
led_dark = 0
led_full = 4095

servo_min = 200
servo_max = 500

# Channel
led_red1    = 0
led_yellow  = 1
led_green   = 2

led_red2    = 3
led_blue    = 4

servo       = 15

# Set frequency 
pwm.set_pwm_freq(60)


class TrafficSignalThread(threading.Thread):

        """Thread for Traffic Signal"""

        def __init__(self):
            super(TrafficSignalThread, self).__init__()

        def run(self):
            print " === start Trafficignal === "

            pwm.set_pwm(led_red1,   0, led_dark)
            pwm.set_pwm(led_yellow, 0, led_dark)
            pwm.set_pwm(led_green,  0, led_dark)

            while True:
            
                # Move servo on channel O between extremes.
                print('Traffic Signal: Red...\n')
                pwm.set_pwm(led_red1,   0, led_full)
                pwm.set_pwm(led_yellow, 0, led_dark)
                pwm.set_pwm(led_green,  0, led_dark)        
                time.sleep(10)
                print('Traffic Signal: Yellow...\n')
                pwm.set_pwm(led_red1,   0, led_dark)
                pwm.set_pwm(led_yellow, 0, led_full)
                pwm.set_pwm(led_green,  0, led_dark)        
                time.sleep(5)
                print('Traffic Signal: Gree...\n')
                pwm.set_pwm(led_red1,    0, led_dark)
                pwm.set_pwm(led_yellow, 0, led_dark)
                pwm.set_pwm(led_green,  0, led_full)        
                time.sleep(5)
                for count in range(10):
                    pwm.set_pwm(led_green, 0, led_dark)
                    time.sleep(0.25)
                    pwm.set_pwm(led_green, 0, led_full)
                    time.sleep(0.25)
                    pwm.set_pwm(led_green,  0, led_dark)                    

class PoliceLightThread(threading.Thread):

        """Thread for Police Car"""

        def __init__(self):
            super(PoliceLightThread, self).__init__()

        def run(self):
            print " === start Police Car Light === "

            pwm.set_pwm(led_red2, 0, led_dark)
            pwm.set_pwm(led_blue, 0, led_dark)

            while True:
                print('Police: Blue...\n')                                            
                pwm.set_pwm(led_red2, 0, led_dark)
                pwm.set_pwm(led_blue, 0, led_full)            
                time.sleep(0.4)
                print('Police: Red...\n')                            
                pwm.set_pwm(led_red2, 0, led_full)
                pwm.set_pwm(led_blue, 0, led_dark)            
                time.sleep(0.4)

class AirplaneServoThread(threading.Thread):

        """Thread for Police Car"""

        def __init__(self):
            super(AirplaneServoThread, self).__init__()

        def run(self):
            print " === start Airplane Servo === "

            while True:
                print('Airplane: Min...\n')                                                        
                pwm.set_pwm(servo, 0, servo_min)
                time.sleep(1)
                print('Airplane: Max...\n')                                                                        
                pwm.set_pwm(servo, 0, servo_max)
                time.sleep(1)

if __name__ == '__main__':
    traffic_signal_th  = TrafficSignalThread()
    police_light_th    = PoliceLightThread()
    airplane_servo_th  = AirplaneServoThread()    

    traffic_signal_th.start()
    police_light_th.start()
    airplane_servo_th.start()

    while True:
        time.sleep(60)

                                                           
