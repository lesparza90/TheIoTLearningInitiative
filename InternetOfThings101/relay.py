import time
import pyupm_grove as grove

# Create the relay switch object using GPIO pin 2 (D2)
relay = grove.GroveRelay(2)


# Import Adafruit IO REST client.
from Adafruit_IO import Client

# Set to your Adafruit IO key.
ADAFRUIT_IO_KEY = '8a32de2fc1854d8ca4af204696e5dd24'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_KEY)

# Now read the most recent value from the feed 'Test'.  Notice that it comes
# back as a string and should be converted to an int if performing calculations
# on it.

#data = aio.receive('relay')
#print('>>>> value attributes: {0}'.format(data))
#print('<<<< value: {0}'.format(data.value))


while True:
    print 'ready...'
    if relay.isOn():
        print 'relay is on'
        aio.send('clientstatus', 1)
    elif relay.isOff():
        print 'relay is off'
        aio.send('clientstatus', 0)
    data = aio.receive('relay')
    if str(data.value) == 'ON':
        relay.on()
    elif str(data.value) == 'OFF':
        relay.off()
    time.sleep(1)
