import sys
import subprocess
import argparse
import os
import re
import time as timestamp_timer
import requests

class UPSControl:

    @staticmethod
    def subprocess_cmd(command):
        try:
            with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True) as process:
                outs, errs = process.communicate()
                process.kill()
                return outs, errs
        except (subprocess.TimeoutExpired, ValueError, OSError) as e:
            process.kill()
            sys.exit(f"ERROR \t: (Subprocess) Error while executing cmd: {command}\nException msg: {e}".expandtabs(5))

    @staticmethod
    def setup():
        try:
            if os.path.isfile("data.txt"):
                print("INFO \t: (Setup) data.txt already exists.".expandtabs(5))
            else:
                try:
                     with open("data.txt", 'a', encoding='utf-8') as file:
                         file.close()
                except OSError as e:
                    sys.exit(f"ERROR \t: (Setup) Exception occurred when creating data.txt file. "
                             f"Exception msg: {e}".expandtabs(5))
                print("INFO \t: (Setup) data.txt created successfully.".expandtabs(5))
            sys.exit("INFO \t: (Setup) Setup finished.".expandtabs(5))
        except Exception as e:
            sys.exit(f"ERROR \t: (Setup) Some exception occurred. Exiting.\nException msg: {e}".expandtabs(5))

    def get_data(self, ups_n):
        timestamp_milliseconds = round(timestamp_timer.time() * 1000)
        command = f"upsc {ups_n}@localhost"
        out, _ = self.subprocess_cmd(command)
        if "not found" in out.decode("utf-8"):
            sys.exit("ERROR \t: (Get Data) There is no upsc command. Exiting.\n".expandtabs(5))

        load_r = r"(?<=ups.load: )(.*)(?=\n)"
        battery_runtime_r = r"(?<=battery.runtime: )(.*)(?=\n)"
        input_voltage_r = r"(?<=input.voltage: )(.*)(?=\n)"
        ups_status_r = r"(?<=ups.status: )(.*)(?=\n)"

        try:
            current_info = out.decode("utf-8")
            load_match = re.findall(load_r, current_info)[0]
            battery_runtime_match = re.findall(battery_runtime_r, current_info)[0]
            battery_runtime_match = int(battery_runtime_match) // 60
            input_voltage_match = re.findall(input_voltage_r, current_info)[0]
            ups_status_match = re.findall(ups_status_r, current_info)[0]
        except Warning as w:
            sys.exit(f"ERROR \t: (Get Data) Exception msg: {w}".expandtabs(5))

        print(f"INFO \t: (Get Data) {timestamp_milliseconds} timestamp milliseconds".expandtabs(5))
        print(f"INFO \t: (Get Data) {load_match}% UPS load".expandtabs(5))
        print(f"INFO \t: (Get Data) {battery_runtime_match}min battery remaining".expandtabs(5))
        print(f"INFO \t: (Get Data) {input_voltage_match}V input voltage".expandtabs(5))
        print(f"INFO \t: (Get Data) {ups_status_match} - UPS status".expandtabs(5))
        return timestamp_milliseconds, load_match, battery_runtime_match, input_voltage_match, ups_status_match

    @staticmethod
    def write_data(timestamp, battload, battery, voltage):
        try:
            with open("data.txt", "r+", encoding='utf-8') as file:
                lines = file.readlines()
                if len(lines) >= 1440:
                    file.seek(0)
                    file.truncate()
                    file.writelines(lines[1:])
                file.writelines(f"{timestamp} {battload} {battery} {voltage}\n")
        except OSError as e:
            sys.exit(f"ERROR \t: (Write Data) Exception occurred while writing data. Exception msg: {e}".expandtabs(5))

    @staticmethod
    def discord_notification_test(webhook):
        payload = {'username': 'UPS Bot', "content": "This is test message."}
        try:
            requests.post(webhook, data=payload)
            sys.exit("INFO \t: (Discord Test) Message sent correctly.".expandtabs(5))
        except Exception as e:
            sys.exit(f"ERROR \t: (Discord Test) Error while sending message. Exception: {e}".expandtabs(5))

    @staticmethod
    def discord_notification(battload, battery, status, webhook):
        if status != "OL":
            content = f"**POWER WENT DOWN!** \nStatus: {status} \nLoad: {battload}% \nBattery time: {battery}min"
            payload = {'username': 'UPS Bot', "content": {content}}
            print(payload)
            try:
                requests.post(webhook, data=payload)
                print("INFO \t: (Discord) Message sent correctly.".expandtabs(5))
            except Exception as e:
                sys.exit(f"ERROR \t: (Discord) Error while sending message. Exception: {e}".expandtabs(5))

    @staticmethod
    def getOpt(argv):
        parser = argparse.ArgumentParser \
            (usage='python3 ups.py [-i "ups name>" -n "webhook_url" -h -s -t "webhook_url"]',
             description="Simple python script, gathering data from UPS connected to Synology server with optional "
                         "Discord notification if UPS starts working on battery.",
             epilog="© 2022, wiktor.kobiela", prog="UPSControl", add_help=False,
             formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=120, width=250))

        available = parser.add_argument_group('Available (optional) arguments:')

        available.add_argument('-i', action='store', dest="ups_name", metavar='"ups name"',
                               help='Provide ups name for upsc command. Default is "ups".', default='ups')
        available.add_argument('-n', action='store', dest="notify", metavar='"webhook_url"',
                               help="Flag to send Discord notification if UPS is working on battery. "
                                    "Default is false.", default="false")
        available.add_argument('-s', action='store_true', dest="setup",
                               help="Boolean flag to setup files for data storage. After setup, script exits. "
                                    "Default is false.", default=False)
        available.add_argument('-t', action='store', dest="test", metavar='"webhook_url"',
                               help="Flag to send test Discord notification. After test, script exits. "
                                    "Default is false.", default="false")

        available.add_argument('-h', action='help', help='Show this help message and exit.')
        args = parser.parse_args()
        return args.ups_name, args.notify, args.setup, args.test


ups = UPSControl()
ups_name, notify, setup, test = ups.getOpt(sys.argv[1:])
if setup:
    ups.setup()
if test != "false":
    ups.discord_notification_test(webhook=test)
t, load, batt, volt, stat = ups.get_data(ups_n=ups_name)
ups.write_data(timestamp=t, battload=load, battery=batt, voltage=volt)
if notify != "false":
    ups.discord_notification(battload=load, battery=batt, status=stat, webhook=notify)
