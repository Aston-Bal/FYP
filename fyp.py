import tkinter as tk
import csv
import requests
import json
import pandas as pd
import os


def initialize():
    url = "https://www.variotdbs.pl/api//vulns/?jsonld=false&since=2022-08-01&before=2099-01-01"  # Since Sep 2022
    connect_failure = False
    # headers = {"curl -X GET 'https://www.variotdbs.pl/api/vulns/' -H 'Authorization: Token bdba526d34cb3ee6e3ca5c1673240e35c0c1a0b2'"}
    try:
        response = requests.get(url).json()
    except requests.exceptions.RequestException as e:
        connect_failure = True
        print("API connection failed!")

    if not connect_failure:
        with open('vulnerability.json', mode='w', encoding="UTF-8") as file:
            json.dump(response, file, ensure_ascii=False, indent=4)

    if not os.path.exists("vulnerability.json") and connect_failure:
        raise SystemExit("Cannot connect to API and no local copy available, exiting!")
    dataframe = pd.read_json("vulnerability.json")
    print(dataframe.loc[00]["results"]["affected_products"]["data"][00]["model"])
   # print(dataframe.head(5))
    # df = str(response_dataframe.loc["data", "affected_products"]).replace("\'", "\"")  # seems wrong
    # obj = json.loads(df)
    #    print(obj[00]["vendor"])
    # print(response["affected_products"]["data"][00])
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
