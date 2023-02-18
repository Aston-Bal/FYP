import tkinter as tk
import csv


def get_db():
    # open csv
    with open('devices.csv', mode='r') as file:
        # read csv
        csvfile = csv.reader(file)
        # add to local array (remove)
        for line in csvfile:
            global devices
            devices = line

    with open('area.csv', mode='r') as file:
        # read csv
        csvfile = csv.reader(file)
        # add to local array (remove)
        for line in csvfile:
            global area
            area = line


def check_vuln():
    if stated_device.get() == "Pi" and stated_area.get() == "Kitchen":
        print('Vuln')
    else:
        print('Not vuln')


get_db()
# Create window
window = tk.Tk()
window.geometry('500x500')
window.title("")

# State devices, currently as array
# devices = ["Pi", "Camera", "Router", "Sensor"]

# state where devices is placed
#area = ["Kitchen", "Living Room"]

# set selected devices to device zero and make it a string
stated_device = tk.StringVar(window)
stated_device.set(devices[0])
# same for area
stated_area = tk.StringVar(window)
stated_area.set(area[0])

# create buttons
device_input = tk.OptionMenu(window, stated_device, *devices)
area_input = tk.OptionMenu(window, stated_area, *area)
save_button = tk.Button(window, text="Check vuln", command=check_vuln(), width=20)

# put buttons in window
tk.Label(window, text="input devices: ", width=10).pack(pady=1, padx=1)
device_input.pack(pady=10, padx=10)
tk.Label(window, text="input area: ", width=10).pack(pady=1, padx=1)
area_input.pack(pady=10, padx=10)
save_button.pack(pady=10, padx=10)

window.mainloop()
