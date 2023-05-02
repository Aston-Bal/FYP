import sys
import tkinter as tk
import requests
import json
import os


class Area:
    def __init__(self, name, menu, number_of_devices):
        self.devices = []
        self.name = name
        self.menu = menu
        self.number_of_devices = number_of_devices

    def add_device(self, devices):
        self.devices.append(devices)


class Device:
    def __init__(self, name, tag, vulnerability):
        self.name = name
        self.tag = tag
        self.vulnerability = vulnerability

    def __str__(self):
        return self.name


class Organisation:

    def __init__(self, name, devices):
        self.name = name
        self.devices = devices


number_of_buttons: int = 0
buttons_list = []
devices_list = []
locations = ["Kitchen", "Living Room", "Entrance  Hall", "Dining Room", "Bedroom", "Guest Room", "Kid's Bedroom",
             "Office",
             "Loft (Attic)", "Basement", "Garage"]
global database


def initialize():
    """" url = "https://www.variotdbs.pl/api//vulns/?jsonld=false&since=2022-08-01&before=2099-01-01"  # Since Sep 2022
    # headers = {"curl -X GET 'https://www.variotdbs.pl/api/vulns/' -H 'Authorization: Token bdba526d34cb3ee6e3ca5c1673240e35c0c1a0b2'"}
    try:
        response = requests.get(url).json()
        with open('vulnerability.json', mode='w', encoding="UTF-8") as file:
            json.dump(response, file, ensure_ascii=False, indent=4)
    except requests.exceptions.RequestException as e:
        print("API connection failed!")
        if not os.path.exists("vulnerability.json"):
            raise SystemExit("Cannot connect to API and no local copy available, exiting!")
    """
    with open('database.json', mode='r', encoding="UTF-8") as file:
        global database
        database = json.load(file)
        database = database["vendors"]
        for vendors in database:
            current_vendor = list(vendors.values())[0]  # Increment into the actual vendor
            for devices in current_vendor:
                if len(devices) == 3:  # Database has 3 values when if the device is vulnerable
                    new_device = Device(devices["model"], devices["tag"], devices["vulnerability"])
                else:
                    new_device = Device(devices["model"], devices["tag"], None)
                devices_list.append(new_device)


def check_vulnerable():
    if buttons_list:
        if buttons_list[0].devices:
            vulnerabilities_list: list = []
            tags_of_devices: list = []
            report: list = ["We will always recommend to update your devices, as this can easily prevent countless "
                            "vulnerabilities"]
            for areas in buttons_list:
                for devices_in_area in areas.devices:
                    for devices in devices_list:
                        if str(devices_in_area.get()) == str(devices.name) and devices.vulnerability is not None:
                            device_vulnerabilities = devices.vulnerability
                            for vulnerabilities in device_vulnerabilities:
                                if vulnerabilities not in vulnerabilities_list:
                                    vulnerabilities_list.append(vulnerabilities)
                        if devices_in_area.get() == devices.name:
                            tags_of_devices.append(devices.tag)
            for tags in tags_of_devices:
                for location in locations:
                    if tags == "Smart Camera" or "Smart Assistant" and location == "Kid's Bedroom":
                        message = "Devices located in Kid's bedroom, we extremely recommend to limit the device capabilities using parental controls, or removing the device due to safety concerns."
                        if message not in report:
                            report.append(message)
                    if tags == "Smart Camera" and location == "Bedroom":
                        message = "Camera's in bedrooms are target's for attackers, typically for blackmail, we recommend removing the device, or oriented it in way that only shows Entry/Exit doors"
                        if message not in report:
                            report.append(message)
            new_window = tk.Toplevel(window)
            new_window.title("Report")
            new_window.geometry("1000x500")
            if vulnerabilities_list:
                tk.Label(new_window, text="Vulnerabilities: ", wraplength=500, justify="left").pack()
            for vulnerabilities in vulnerabilities_list:
                tk.Label(new_window, text=("Name: " + vulnerabilities["name"]), wraplength=500, justify="left").pack()
                tk.Label(new_window, text=("Description: \n" + vulnerabilities["description"]), wraplength=500,
                         justify="left").pack()
            tk.Label(new_window, text="Report: ", wraplength=500,
                     justify="left").pack()
            for items in report:
                tk.Label(new_window, text=items, wraplength=500,
                         justify="left").pack()


def add_new_area():
    area = tk.StringVar(window)
    area.set(locations[0])  # Required to set default value
    area_menu = tk.OptionMenu(window, area, *locations)
    current_grid_size = window.grid_size()
    tk.Label(window, text="Input area: ").grid(row=current_grid_size[1], column=0, padx=5, pady=5)
    area_menu.grid(row=current_grid_size[1], column=1, padx=5, pady=5)
    global number_of_buttons
    area = Area(number_of_buttons, area, 0)
    buttons_list.append(area)
    number_of_buttons = number_of_buttons + 1
    add_devices = tk.Button(window, text="Add device",
                            command=lambda: add_new_device(area, (current_grid_size[1]), current_grid_size[0]))
    add_devices.grid(row=(current_grid_size[1] + 1), column=1, padx=5, pady=5)
    tk.Label(window, text="Input devices: ").grid(row=(current_grid_size[1] + 1), column=0, padx=5, pady=5)


def add_new_device(area: Area, row: int, col: int):
    device = tk.StringVar(window)
    device.set(devices_list[0])
    device_menu = tk.OptionMenu(window, device, *devices_list)
    area.number_of_devices = area.number_of_devices + 1
    area.add_device(device)
    device_menu.grid(row=(row + 1), column=(col + area.number_of_devices), padx=5,
                     pady=5)


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

# main buttons
calculate_vulnerability = tk.Button(window, text="Check vulnerable", command=lambda: check_vulnerable(), width=30)
temp_button = tk.Button(window, text="Add new area", command=lambda: add_new_area(), width=30)
temp_button.grid(row=0, column=0, columnspan=5, padx=5, pady=5)
calculate_vulnerability.grid(row=1, column=0, columnspan=5, padx=5, pady=5)
window.mainloop()
