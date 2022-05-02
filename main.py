import re
import subprocess
import time as another
import random

# output = b'battery.charge: 100\nbattery.charge.low: 10\nbattery.charge.warning: 20\nbattery.mfr.date: CPS\nbattery.runtime: 2610\nbattery.runtime.low: 300\nbattery.type: PbAcid\nbattery.voltage: 8.9\nbattery.voltage.nominal: 12\ndevice.mfr: CPS\ndevice.model: VP700ELCD\ndevice.type: ups\ndriver.name: usbhid-ups\ndriver.parameter.pollfreq: 30\ndriver.parameter.pollinterval: 5\ndriver.parameter.port: auto\ndriver.version: DSM6-2-25510-201118\ndriver.version.data: CyberPower HID 0.3\ndriver.version.internal: 0.38\ninput.transfer.high: 295\ninput.transfer.low: 167\ninput.voltage: 238.0\ninput.voltage.nominal: 230\noutput.voltage: 238.0\nups.beeper.status: enabled\nups.delay.shutdown: 20\nups.delay.start: 30\nups.load: 20\nups.mfr: CPS\nups.model: VP700ELCD\nups.productid: 0501\nups.realpower.nominal: 390\nups.status: OL\nups.test.result: No test initiated\nups.timer.shutdown: -60\nups.timer.start: -60\nups.vendorid: 0764\n'


class UPSControl:

    @staticmethod
    def subprocess_cmd(command):
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            outs, errs = process.communicate()
            process.kill()
            return outs, errs
        except (subprocess.TimeoutExpired, ValueError, OSError) as e:
            process.kill()
            print(f"Error while executing cmd: {command}\nException msg: {e}")

    def get_data(self):

        timestamp_milliseconds = round(another.time() * 1000)
        command = "upsc ups@localhost"
        out, _ = self.subprocess_cmd(command)

        load_r = r"(?<=ups.load: )(.*)(?=\n)"
        battery_runtime_r = r"(?<=battery.runtime: )(.*)(?=\n)"

        # current_info = output.decode("utf-8")
        current_info = out.decode("utf-8")

        load_match = re.findall(load_r, current_info)[0]
        battery_runtime_match = re.findall(battery_runtime_r, current_info)[0]
        battery_runtime_match = int(battery_runtime_match)//60
        print(f"{timestamp_milliseconds} timestamp milliseconds")
        print(f"{load_match}% ups load")
        print(f"{battery_runtime_match}min battery remaining")

        #
        # load_match = random.randint(0, 100)
        # battery_runtime_match = random.randint(5, 360)
        return timestamp_milliseconds, load_match, battery_runtime_match

    @staticmethod
    def write_data(timestamp, load, battery):
        with open("data.txt", "r+") as file:
            lines = file.readlines()
            # print(len(lines))
            if len(lines) >= 1440:
                file.seek(0)
                file.truncate()
                file.writelines(lines[1:])
            file.writelines(f"{timestamp} {load} {battery}\n")


ups = UPSControl()
t, load, batt = ups.get_data()
ups.write_data(t, load, batt)


# timer = 0
# while timer < 1500:
#     timer += 1
#     t, load, batt = ups.get_data()
#     ups.write_data(t, load, batt)


