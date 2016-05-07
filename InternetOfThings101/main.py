import dweepy
import paho.mqtt.client as paho
import psutil
import pywapi
import signal
import sys
import time

from threading import Thread

import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout, Figure


import pyupm_grove as grove

# Create the relay switch object using GPIO pin 2 (D2)
relay = grove.GroveRelay(2)

username = 'TheIoTLearningInitiative'
api_key = 'twr0hlw78c'
stream_token = '2v04m1lk1x'

def interruptHandler(signal, frame):
    sys.exit(0)

def on_publish(mosq, obj, msg):
    pass

def dataNetwork():
    netdata = psutil.net_io_counters()
    return netdata.packets_sent + netdata.packets_recv

def actuador(key):
    if key == 'on':
        relay.on()
    elif key == 'off':
        relay.off()
    time.sleep(1)

def GetMACAddress(ifname):
    import fcntl, socket, struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', 
ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])

def dataNetworkHandler():
    idDevice = str(GetMACAddress('wlan0'))
    mqttclient = paho.Client()
    mqttclient.on_publish = on_publish
    mqttclient.connect("test.mosquitto.org", 1883, 60)
    while True:
        packets = dataNetwork()
        message = idDevice + " " + str(packets)
        print "MQTT dataNetworkHandler " + message
        mqttclient.publish("IoT101/" + idDevice + "/Network", message)
        time.sleep(1)

def on_message(mosq, obj, msg):
    print "MQTT dataMessageHandler %s %s" % (msg.topic, msg.payload)
    actuador(str(msg.payload))

def dataMessageHandler():
    mqttclient = paho.Client()
    mqttclient.on_message = on_message
    mqttclient.connect("test.mosquitto.org", 1883, 60)
    mqttclient.subscribe("IoT101/" + GetMACAddress('wlan0') + 
"/Message", 0)
    while mqttclient.loop() == 0:
        pass

def dataPlotly():
    return dataNetwork()

def dataPlotlyHandler():

    py.sign_in(username, api_key)

    trace1 = Scatter(
        x=[],
        y=[],
        stream=dict(
            token=stream_token,
            maxpoints=200
        )
    )

    layout = Layout(
        title='Hello Internet of Things 101 Data'
    )

    fig = Figure(data=[trace1], layout=layout)

    print py.plot(fig, filename='Hello Internet of Things 101 Plotly')

    i = 0
    stream = py.Stream(stream_token)
    stream.open()

    while True:
        stream_data = dataPlotly()
        stream.write({'x': i, 'y': stream_data})
        i += 1
        time.sleep(0.25)

if __name__ == '__main__':

    signal.signal(signal.SIGINT, interruptHandler)

    threadx = Thread(target=dataNetworkHandler)
    threadx.start()

    thready = Thread(target=dataMessageHandler)
    thready.start()

    threadz = Thread(target=dataPlotlyHandler)
    threadz.start()

    while True:
        print "Hello Internet of Things 101"
        time.sleep(5)
        json= {"Packet":dataNetwork()}
        dweepy.dweet_for("lesparza90_test_1", json)
