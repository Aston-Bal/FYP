import sys
import tkinter as tk
import requests
import json
import os


class Area:
    def __init__(self, name, menu, device):
        self.name = name
        self.menu = menu
        self.no_devices = device


class Device:
    def __init__(self, name, menu, type, vulnerability):
        self.name = name
        self.menu = menu
        self.type = type
        self.vulnerability = vulnerability


no_buttons: int = 0
buttons = []
global database


def initialize():
    url = "https://www.variotdbs.pl/api//vulns/?jsonld=false&since=2022-08-01&before=2099-01-01"  # Since Sep 2022
    # headers = {"curl -X GET 'https://www.variotdbs.pl/api/vulns/' -H 'Authorization: Token bdba526d34cb3ee6e3ca5c1673240e35c0c1a0b2'"}
    try:
        response = requests.get(url).json()
        with open('vulnerability.json', mode='w', encoding="UTF-8") as file:
            json.dump(response, file, ensure_ascii=False, indent=4)
    except requests.exceptions.RequestException as e:
        print("API connection failed!")
        if not os.path.exists("vulnerability.json"):
            raise SystemExit("Cannot connect to API and no local copy available, exiting!")

    with open('database.json', mode='r', encoding="UTF-8") as file:
        global database
        database = json.load(file)


def check_vulnerable():
    if stated_device.get() == "Sensor" and stated_area.get() == "Kitchen":
        tk.Label(window, text="Vulnerable", width=30).grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    elif stated_device.get() == "Camera" and stated_area.get() == "Bedroom":
        tk.Label(window, text="Vulnerable", width=30).grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    else:
        tk.Label(window, text="Not Vulnerable", width=30).grid(row=3, column=0, columnspan=2, padx=5, pady=5)


def add_new_area():
    area = tk.StringVar(window)
    area.set(location[0])  # Required to set default value
    area_optionmenu = tk.OptionMenu(window, area, *location)
    current_grid_size = window.grid_size()
    print(window.grid_size())
    tk.Label(window, text="Input area: ", width=10).grid(row=current_grid_size[1], column=0, padx=5, pady=5)
    area_optionmenu.grid(row=current_grid_size[1], column=1, padx=5, pady=5)
    global no_buttons
    area = Area(no_buttons, area_optionmenu, 0)
    buttons.append(area)
    no_buttons = no_buttons + 1
    add_devices = tk.Button(window, text="Add device", command=lambda: add_new_device(area))
    add_devices.grid(row=(current_grid_size[1] + 1), column=1, padx=5, pady=5)
    tk.Label(window, text="Input devices: ", bd=5).grid(row=(current_grid_size[1] + 1), column=0, padx=5, pady=5)


def add_new_device(area: Area):
    device = tk.StringVar(window)
    device.set(devices[0])
    device_menu = tk.OptionMenu(window, device, *devices)
    grid_location = area.menu.grid_info()
    area.no_devices = area.no_devices + 1
    device_menu.grid(row=(grid_location["row"] + 1), column=(grid_location["column"] + area.no_devices), padx=5, pady=5)


def toolbar():
    menu = tk.Menu(window)
    window.config(menu=menu)
    toolbar = tk.Menu(menu)
    menu.add_cascade(label='Options', menu=toolbar)
    toolbar.add_command(label='New')
    toolbar.add_command(label='Save')
    toolbar.add_separator()
    toolbar.add_command(label='Reqeust')
    toolbar.add_command(label='Report')
    toolbar.add_separator()
    toolbar.add_command(label='Exit', command=lambda: sys.exit())


initialize()
# Create window
window = tk.Tk()
toolbar()
window.geometry("1000x500")
window.title("IoT vulnerability scanner")
# State devices, currently as array
devices = ["Pi", "Camera", "Router", "Sensor"]
# state where devices is placed
location = ["Kitchen", "Living Room"]

# create buttons
calculate_vulnerability = tk.Button(window, text="Check vulnerable", command=lambda: check_vulnerable(), width=30)

# put buttons in window
temp_button = tk.Button(window, text="Add new area", command=lambda: add_new_area(), width=30)
temp_button.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
calculate_vulnerability.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
window.mainloop()
