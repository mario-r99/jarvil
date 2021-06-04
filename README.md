# J.A.R.V.I.L. - Just A Rather Very Intelligent Library

## Introduction

J.A.R.V.I.L. is a project of the "Smart Cities & IoT" course at the University of Stuttgart. It's main goal is to simplify and automate various tasks in a modern library to make daily work easier for students.

## Services Configuration & Run

### Arduino Configuration

StandartFirmata_Bluetooth allows building arduino code from remote devices via Bluetooth connection, using pyFirmata. 
StandartFirmata building arduino code from remote devices via USB, using pyFirmata.

To configure a new arduino device, please build the StandartFirmata_Bluetooth.ino or StandartFirmata.ino via Arduino IDE USB connection

### System Setup Instructions

To setup the system one needs to start the containers in each pi folder, under jarvil\docker, on their respective Raspberry Pi's. In order to run a container one must run "docker-compose up -d" in its directory. Each container contains the following:

1. The development container contains all services for live development.

2. The pi-1 container contains time slot booking services.

3. The pi-2 container contains mqtt broker and analysis services.

4. The pi-3 container contains mqtt endpoint services.

### MQTT Broker - Mosquitto 

The system uses Mosquitto, a mqtt broker, to communicate between system components ensuring indirect communication.

### Database - Influxdb

The system uses Influxdb as a database to store all data aquired by the system and that is then used by the system to make decisions. Influxdb is a time series database.

### Time Slot Booking Service

In order to visit the library one must book a time slot on the booking interface. The booking interface is accessible at http://localhost:5000/. When booking a slot one must select at least one 6 hour slot and fill your first name, last name and email adress and submit your reservation. First and last names have a minimum of 2 characters.

The time slot on the booking interface's data is cached on Redis. Redis can be accessed on http://localhost:6379/ and the cache can be viewed there.

## Full Documentation

See the [Wiki](https://github.com/mario-r99/smart-office/wiki/) for full documentation and other information.
