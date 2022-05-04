import re
import subprocess
import time as timestamp_timer


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
            print(f"ERROR \t: Error while executing cmd: {command}\nException msg: {e}".expandtabs(5))

    def get_data(self):
        timestamp_milliseconds = round(timestamp_timer.time() * 1000)
        command = "upsc ups@localhost"
        out, _ = self.subprocess_cmd(command)

        load_r = r"(?<=ups.load: )(.*)(?=\n)"
        battery_runtime_r = r"(?<=battery.runtime: )(.*)(?=\n)"
        input_voltage_r = r"(?<=input.voltage: )(.*)(?=\n)"
        ups_status_r = r"(?<=ups.status: )(.*)(?=\n)"

        current_info = out.decode("utf-8")

        load_match = re.findall(load_r, current_info)[0]
        battery_runtime_match = re.findall(battery_runtime_r, current_info)[0]
        battery_runtime_match = int(battery_runtime_match)//60
        input_voltage_match = re.findall(input_voltage_r, current_info)[0]
        ups_status_match = re.findall(ups_status_r, current_info)[0]
        print(f"INFO \t: {timestamp_milliseconds} timestamp milliseconds".expandtabs(5))
        print(f"INFO \t: {load_match}% ups load".expandtabs(5))
        print(f"INFO \t: {battery_runtime_match}min battery remaining".expandtabs(5))
        print(f"INFO \t: {input_voltage_match}V input voltage".expandtabs(5))
        print(f"INFO \t: {ups_status_match} - UPS status".expandtabs(5))

        return timestamp_milliseconds, load_match, battery_runtime_match, input_voltage_match, ups_status_match

    @staticmethod
    def write_data(timestamp, battload, battery, voltage):
        with open("data.txt", "w+") as file:
            lines = file.readlines()
            if len(lines) >= 1440:
                file.seek(0)
                file.truncate()
                file.writelines(lines[1:])
            file.writelines(f"{timestamp} {battload} {battery} {voltage}\n")

    def discord_notification(self, load, battery, status):
        if status != "OL":
            command = f'./discord.sh \
                        --username "UPS_bot" \
                        --avatar "https://avatarlink.com/logo.png" \
                        --text "POWER WENT DOWN!\n UPS STATUS IS {status}"'
            #self.subprocess_cmd(command)
            print(f"POWER DOWN!\nStatus: {status}\nLoad: {load}% \nBatt_time: {battery}min")


ups = UPSControl()
# t, load, batt, volt, stat = ups.get_data()
ups.discord_notification("10", "20", "BT")
# ups.write_data(t, load, batt, volt)



