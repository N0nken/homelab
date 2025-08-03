import psutil
import os
import time

while True:
    #os.system('cls' if os.name == 'nt' else 'clear')
    thermals = psutil.sensors_temperatures()
    cpu_temp = thermals["cpu_thermal"]
    nvme_temp = thermals["nvme"]
    print(f"CPU: {cpu_temp[0].current} °C\nNVMe: {nvme_temp[0].current} °C")
    time.sleep(10)  # Refresh every 10 seconds