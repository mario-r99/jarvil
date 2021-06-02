# J.A.R.V.I.L. - Just A Rather Very Intelligent Library

## Introduction

J.A.R.V.I.L. is a project of the "Smart Cities & IoT" course at the University of Stuttgart. It's main goal is to simplify and automate various tasks in a modern library to make daily work easier for students.

## Services Configuration & Run

### Arduino Configuration

StandartFirmata_Bluetooth allows building arduino code from remote devices via Bluetooth connection, using pyFirmata. 
StandartFirmata building arduino code from remote devices via USB, using pyFirmata.

To configure a new arduino device, please build the StandartFirmata_Bluetooth.ino or StandartFirmata.ino via Arduino IDE USB connection

### Run Configuration Options

There are four configurations in which the system can be run. These are:

1. The configuration under jarvil\docker\development has the following services: mqtt-broker, time-slot-booking, redis and redisinsight. In order to run this configuration one can run "docker-compose up -d" in this directory.

2. The configuration under jarvil\docker\pi-1 has the following services: time-slot-booking and redis. In order to run this configuration one can run "docker-compose up -d" in this directory.

3. The configuration under jarvil\docker\pi-2 has the following services: mqtt-broker. In order to run this configuration one can run "docker-compose up -d" in this directory.

4. The configuration under jarvil\docker\pi-3 has the following services: none. In order to run this configuration one can run "docker-compose up -d" in this directory.

### Time Slot Booking Service

In order to visit the library one must book a time slot on the booking interface. The booking interface is accessible at http://localhost:5000/. When booking a slot one must select at least one 6 hour slot and fill your first name, last name and email adress and submit your reservation. First and last names have a minimum of 2 characters.

## Full Documentation

See the [Wiki](https://github.com/mario-r99/smart-office/wiki/) for full documentation and other information.
