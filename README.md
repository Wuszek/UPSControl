# UPSControl

Python script combined with simple web page (canvasjs + jquery) to utilize information 
about UPS system connected to Synology server.

## Purpose

UPSControl gather information about UPS load and available battery runtime in last 24h
and plots it on one chart. Second chart is input voltage value in time. 

It is possible to configure script to send Discord notification, when 
UPS change status from OL (online) to another (eg. OB (on battery)).

## Help 

```bash
usage: python3 ups.py [-i "ups name>" -n "webhook_url" -h -s -t]

Simple python script, gathering data from UPS connected to Synology server with optional Discord notification if UPS starts working on battery.

Available (optional) arguments::
  -i "ups name"     Provide ups name for upsc command. Default is "ups".
  -n "webhook_url"  Flag to send Discord notification if UPS is working on battery. Default is false.
  -s                Boolean flag to setup files for data storage and discord notifications. Default is false.
  -t "webhook_url"  Flag to send test discord notification. Default is false.
  -h                Show this help message and exit.

© 2022, wiktor.kobiela
```

## How does it work?

Script uses Synology `upsc` command with given `-i ups_name` or default UPS name.
Full command invoked:
```bash 
user@Synology:~$ upsc ups@localhost
```

Output of this command consists of several useful information, that can't be obtained other from 
UPS physical screen (if it has one) or using SSH connection:

Fragment of sample output:
```bash 
battery.charge: 100
battery.charge.low: 10
battery.charge.warning: 20
battery.mfr.date: CPS
battery.runtime: 2370
battery.runtime.low: 300
input.transfer.high: 295
input.transfer.low: 167
input.voltage: 242.0
input.voltage.nominal: 230
ups.load: 27
ups.status: OL
```

Script is saving info about `battery.runtime`, `ups.load` and `input.voltage`. It is also checking UPS status.

## How to use 

Help
```bash
python3 ups.py -h
```

Setup - create data file with load/time/status.
```bash
python3 ups.py -s
```

Test - send test Discord message to test notifications
```bash 
python3 ups.py -t "webhook_url"
```

Run with optional ups_name argument and optional Discord notification.
```bash 
python3 ups.py -i "ups_name" -n "webhook_url"
```

It is preferred to run script using built in Synology scheduler, preferable every 1 minute to gather data.
Also, there will be 1minute threshold for getting info about power failure and UPS running on battery.

## Screenshot
![Test run and Discord notification screenshot](/media/screenshot.png)

![Webpage with charts gif](/media/preview.gif)

