# UPSControl

Python script combined with simple web page (canvasjs + jquery) to utilize information 
about UPS system connected to Synology server.

## Purpose

UPSControl gather information about UPS load and available battery runtime in last 24h
and plots it on one chart. 

Second chart is input voltage value in time. 

## How does it work?

Script uses Synology `upsc` command with default UPS name. This can be easily changed in code.
Full command invoked:
```bash 
user@Synology:~$ upsc ups@localhost
```

Output of this command consists of several useful information, that can't be obtained other from 
UPS physical screen (if it has one) or using SSH connection:

Sample output:
```bash 
battery.charge: 100
battery.charge.low: 10
battery.charge.warning: 20
battery.mfr.date: CPS
battery.runtime: 2370
battery.runtime.low: 300
battery.type: PbAcid
battery.voltage: 8.9
battery.voltage.nominal: 12
device.mfr: CPS
device.model: VP700ELCD
device.type: ups
driver.name: usbhid-ups
driver.parameter.pollfreq: 30
driver.parameter.pollinterval: 5
driver.parameter.port: auto
driver.version: DSM6-2-25510-201118
driver.version.data: CyberPower HID 0.3
driver.version.internal: 0.38
input.transfer.high: 295
input.transfer.low: 167
input.voltage: 242.0
input.voltage.nominal: 230
output.voltage: 242.0
ups.beeper.status: enabled
ups.delay.shutdown: 20
ups.delay.start: 30
ups.load: 27
ups.mfr: CPS
ups.model: VP700ELCD
ups.productid: 0501
ups.realpower.nominal: 390
ups.status: OL
ups.test.result: No test initiated
ups.timer.shutdown: -60
ups.timer.start: -60
ups.vendorid: 0764 
```

Script is saving info about `battery.runtime`, `ups.load` and `input.voltage`.

## How to use 
```python
python3 main.py
```
Run script using built in Synology scheduler, preferable every 1 minute to gather data.

## Screenshot

![alt text](/media/preview.gif)