import math
import sys
import json
import socketio
import time
from grove.adc import ADC

__all__ = ["GroveMoistureSensor"]

class GroveMoistureSensor:
    '''
    Grove Moisture Sensor class

    Args:
        pin(int): number of analog pin/channel the sensor connected.
    '''
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def moisture(self):
        '''
        Get the moisture strength value/voltage

        Returns:
            (int): voltage, in mV
        '''
        value = self.adc.read_voltage(self.channel)
        return value

Grove = GroveMoistureSensor

sio = socketio.Client()

#Socket io info


@sio.event
def disconnect():
    print('disconnected from server')

@sio.event
def connect():
    print('connection established')

sio.connect('https://calm-river-80577.herokuapp.com/')

def main():
    from grove.helper import SlotHelper
    sh = SlotHelper(SlotHelper.ADC)
    pin = sh.argv2pin()

    sensor = GroveMoistureSensor(pin)

    print('Detecting moisture...')
    while True:
        m = sensor.moisture
        if 0 <= m and m < 300:
            print(m)
            result = 'Dry'
        elif 300 <= m and m < 600:
            print(m)
            result = 'Moist'
        else:
            print(m)
            result = 'Wet'
        print('Moisture value: {0}, {1}'.format(m, result))
        
        sio.emit('moisture-data', json.dumps({'val' : '%d' % m , 'category' : '%s' % result}))


        time.sleep(1)

if __name__ == '__main__':
    main()