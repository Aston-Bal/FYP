import sys
import tkinter as tk
import requests
import json
import os


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
# Removable?
    with open('vulnerability.json', mode='r', encoding="UTF-8") as file:
        dataframe = json.load(file)

    with open('devices.json', mode='w+', encoding="UTF-8") as file:
        file_data = []
        for i in dataframe["results"]:
            for d in i["affected_products"]["data"]:
                print(d["model"], d["version"], d["vendor"])
                device_info = {"model": str(d["model"]), "version": str(d["version"]), "vendor": str(d["vendor"])}
                file_data.append(device_info)
        json.dump(file_data, file, ensure_ascii=False, indent=4)


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
menu = tk.Menu(window)
window.config(menu=menu)
filemenu = tk.Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New')
filemenu.add_command(label='Save')
filemenu.add_command(label='Reqeust')
filemenu.add_command(label='Report')
filemenu.add_command(label='Exit', command=lambda:sys.exit())
window.geometry("500x500")
window.title("IoT vulnerability scanner")


# State devices, currently as array
devices = ["Pi", "Camera", "Router", "Sensor"]

# state where devices is placed
location = ["Kitchen", "Living Room"]

# set selected devices to device zero and make it a string
stated_device = tk.StringVar(window)
stated_device.set(devices[0])
# same for area
stated_area = tk.StringVar(window)
stated_area.set(location[0])

# create buttons
vendor_input = tk.OptionMenu(window, stated_device, *devices)
model_input = tk.OptionMenu(window, stated_device, *devices)
version_input = tk.OptionMenu(window, stated_device, *devices)
area_input = tk.OptionMenu(window, stated_area, *location)
calculate_vulnerability = tk.Button(window, text="Check vulnerable", command=lambda: check_vulnerable(), width=30)

# put buttons in window
tk.Label(window, text="Input devices: ", bd=5).grid(row=0, column=0, padx=5, pady=5)
vendor_input.grid(row=0, column=1, padx=5, pady=5)
model_input.grid(row=0, column=2, padx=5, pady=5)
version_input.grid(row=0, column=3, padx=5, pady=5)
tk.Label(window, text="Input area: ", width=10).grid(row=1, column=0, padx=5, pady=5)
area_input.grid(row=1, column=1, padx=5, pady=5)
calculate_vulnerability.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

window.mainloop()
