import tkinter as tk
import csv
import requests
import json
import os


def initialize():
    url = "https://www.variotdbs.pl/api/vuln/VAR-202303-0357/?jsonld=false"
    # headers = {"Authorization: Token bdba526d34cb3ee6e3ca5c1673240e35c0c1a0b2"}
    response = requests.get(url).json()
    print(json.dumps(response, sort_keys=True, indent=4))
    # y = json.loads(response.json()) #Confusion
    with open('vulnerability.json', mode='w') as file:
        json.dump(response, file, ensure_ascii=False, indent=4)
    # open the list of devices in csv
    # if not os.path.exists("devices.csv"):
    with open('devices.csv', mode='r') as file:
        # read csv
        csvfile = csv.reader(file)
        # add to local array (remove)
        for line in csvfile:
            global devices
            devices = line
    # open the list of area's in csv
    with open('area.csv', mode='r') as file:
        # read csv
        csvfile = csv.reader(file)
        # add to local array (remove)
        for line in csvfile:
            global area
            area = line


def check_vulnerable():
    if stated_device.get() == "Sensor" and stated_area.get() == "Kitchen":
        tk.Label(window, text="Vulnerable", width=30).grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    elif stated_device.get() == "Camera" and stated_area.get() == "Bedroom":
        tk.Label(window, text="Vulnerable", width=30).grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    else:
        tk.Label(window, text="Not Vulnerable", width=30).grid(row=3, column=0, columnspan=2, padx=5, pady=5)


initialize()
# Create window
window = tk.Tk()
window.geometry("500x500")
window.title("IoT vulnerability scanner")

# State devices, currently as array
# devices = ["Pi", "Camera", "Router", "Sensor"]

# state where devices is placed
# area = ["Kitchen", "Living Room"]

# set selected devices to device zero and make it a string
stated_device = tk.StringVar(window)
stated_device.set(devices[0])
# same for area
stated_area = tk.StringVar(window)
stated_area.set(area[0])

# create buttons
device_input = tk.OptionMenu(window, stated_device, *devices)
area_input = tk.OptionMenu(window, stated_area, *area)
save_button = tk.Button(window, text="Check vulnerable", command=lambda: check_vulnerable(), width=30)

# put buttons in window
tk.Label(window, text="Input devices: ", width=10).grid(row=0, column=0, padx=5, pady=5)
device_input.grid(row=0, column=1, padx=5, pady=5)
tk.Label(window, text="Input area: ", width=10).grid(row=1, column=0, padx=5, pady=5)
area_input.grid(row=1, column=1, padx=5, pady=5)
save_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

window.mainloop()
