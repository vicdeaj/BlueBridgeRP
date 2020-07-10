# BlueBridgeRP
Raspberry pi side of the bluebridge
# Requirements
PyBluez: You'll need to run the bluetooth service in compatibility mode as state here https://github.com/pybluez/pybluez/issues/161
Moreover, the user running the bluebridge applications need read/write access to /var/run/sdp

# How to use it
1. Run main.py, it will forward connection received through bluetooth to por 8022, so you'll have to change the port in the program or run the desired service on this port
2. The program will wait for connections with the uuid f331dead-1234-4321-9999-785340612afe at wich the BlueBridge app is configured to connect so if you want to multiply the number of services you'll have to asign diferents uuid to them.

# Bluebridge
The other part is in https://github.com/vik0t0r/BlueBridge.git
