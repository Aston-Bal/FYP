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


def check_vulnerable():
    if stated_device.get() == "Sensor" and stated_area.get() == "Kitchen":
        print('Vulnerable')
    elif stated_device.get() == "Camera" and stated_area.get() == "Bedroom":
        print('Vulnerable')
    else:
        print('Not vulnerable')



get_db()
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
save_button = tk.Button(window, text="Check vulnerable", command=lambda: check_vulnerable(), width=20)

# put buttons in window
tk.Label(window, text="input devices: ", width=10).grid(row=0, column=0)
device_input.grid(row=0, column=1)
tk.Label(window, text="input area: ", width=10).grid(row=1, column=0)
area_input.grid(row=1, column=1)
save_button.grid(row=2, column=0)

window.mainloop()
