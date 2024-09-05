# ruff: noqa: F403,F405,E402,F541,E722
# import PVZ_asm
import PVZ_Hybrid as pvz
import PVZ_data as PVZ_data
from tkinter import filedialog
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
import tkinter as tk
from tkinter import (
    messagebox,
    # Toplevel,
    Listbox,
    Checkbutton,
    IntVar,
    # font,
    simpledialog,
)
import importlib.util
import requests
import keyboard
import json
import webbrowser

# import ctypes
import sys
import os

# import time
import re
import random
import psutil
import win32process
import win32gui
import queue
# from threading import Thread, Event
# import wmi
# import hashlib
# import pyperclip
# import struct

# from pyDes import *
# import binascii
from pymem import Pymem
from PIL import Image, ImageTk
# from Crypto import Random
# from typing import List, Dict
# from datetime import datetime, timedelta
# import base64
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_v1_5
# from urllib.parse import urlencode

Image.CUBIC = Image.BICUBIC
current_version = "0.38"
version_url = "https://gitee.com/EFrostBlade/PVZHybrid_Editor/raw/main/version.txt"
main_window = None
PVZ_data.update_PVZ_memory(1)
zombie_select = None
plant_select = None
item_select = None
plant_characteristic_type = None
shortcut_entries = []
shortcut_buttons = []
shortcut_comboboxs = []
action_values = []
action_list = [
    "fail",
    "setTheSun",
    "increaseSunlight",
    "freely",
    "freePlanting",
    "cancelTheCooling",
    "automaticallyCollect",
    "columnMode",
    "superShovel",
    "neverFail",
    "currentLevelVictory",
    "killAllZombies",
    "unlockAllPlants",
    "placedPlant",
    "ladder",
    "clearPlant",
    "zombies",
    "levelFailure",
    "archive",
    "readFile",
    "gamingAccelerate",
    "gameDeceleration",
    "randomCardSlot",
]
# Default configuration
default_config = {
    "shortcuts": {
        "key1": {"key": "ctrl+space", "action": 0},
        "key2": {"key": "Ctrl+f2", "action": 1},
        "key3": {"key": "Ctrl+f3", "action": 2},
        "key4": {"key": "Ctrl+f4", "action": 3},
        "key5": {"key": "Ctrl+f5", "action": 4},
        "key6": {"key": "Ctrl+f6", "action": 5},
        "key7": {"key": "Ctrl+f7", "action": 6},
        "key8": {"key": "Ctrl+f8", "action": 7},
        "key9": {"key": "Ctrl+f9", "action": 8},
        "key10": {"key": "Ctrl+f10", "action": 9},
        "key11": {"key": "Ctrl+f11", "action": 10},
        "key12": {"key": "Ctrl+f12", "action": 11},
    }
}
# Click to close and exit


def exit_editor(file_path, window, section="main_window_position"):
    config = load_config(file_path)
    config[section] = {"x": window.winfo_x(), "y": window.winfo_y()}
    save_config(config, file_path)
    os._exit(0)


def exit_with_delete_config(config_file_path):
    os.remove(config_file_path)
    os._exit(0)


def resource_path(relative_path):
    """The absolute path to obtain resources is suitable for the development environment and the Pyinstaller environment"""
    try:
        # The path of the temporary folder created by Pyinstaller is stored in _meipass
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Define the application name
app_name = "PVZHybrid_Editor"

# Get the current user's AppData directory path
appdata_path = os.getenv("APPDATA")

# Create a configuration folder for your application in the AppData directory
app_config_path = os.path.join(appdata_path, app_name)
if not os.path.exists(app_config_path):
    os.makedirs(app_config_path)

# Define the path of the configuration file
config_file_path = os.path.join(app_config_path, "config.json")

# Create a function of the configuration file


def create_config(file_path, default_config):
    with open(file_path, "w") as file:
        json.dump(default_config, file, indent=4, ensure_ascii=False)


# Read the function of the configuration file


def load_config(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return default_config
    except:
        delete_config()


# Modify the function of the configuration file


def modify_config(file_path, section, key, value):
    config = load_config(file_path)
    if section not in config:
        config[section] = {}
    config[section][key] = value
    save_config(config, file_path)


# Update the function of the configuration file
def save_config(config, file_path):
    with open(file_path, "w") as file:
        json.dump(config, file, indent=4)


# Create a queue for inter -thread communication
data_queue = queue.Queue()
result_queue = queue.Queue()


def get_intvar_value(intvar):
    # Put the request to get the Intvar value in the queue
    data_queue.put(("get", intvar))
    # Wait and get the value of intvar from the result queue
    return result_queue.get()


def set_intvar_value(intvar, value):
    # Put the request to set the Intvar value in the queue
    data_queue.put(("set", intvar, value))


def process_queue(root):
    while not data_queue.empty():
        request = data_queue.get()
        if request[0] == "get":
            # Get the value of intvar and put it in the results queue
            intvar = request[1]
            result_queue.put(intvar.get())
        elif request[0] == "set":
            # Set the value of Intvar
            intvar, value = request[1], request[2]
            intvar.set(value)
    # Call this function again every time
    root.after(100, process_queue, root)


def chooseGame():
    global main_window

    def openPVZ_memory(process1):
        try:
            window_name = re.search(r"\{\{(.+?)\}\}", process1).group(1)
            if "2.0" in window_name:
                PVZ_data.update_PVZ_version(2.0)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.1" in window_name:
                PVZ_data.update_PVZ_version(2.1)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.2" in window_name:
                PVZ_data.update_PVZ_version(2.2)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.3.5" in window_name:
                PVZ_data.update_PVZ_version(2.35)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.3.6" in window_name:
                PVZ_data.update_PVZ_version(2.36)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.3.7" in window_name:
                PVZ_data.update_PVZ_version(2.37)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.3" in window_name:
                PVZ_data.update_PVZ_version(2.3)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            PVZ_data.update_PVZ_memory(
                Pymem(int(re.search(r"(\d+)", process1).group(1)))
            )
            PVZ_data.update_PVZ_pid(int(re.search(r"(\d+)", process1).group(1)))
        except:
            Messagebox.show_error(
                "Without sufficient permissions, please make sure the game is not running as an administrator",
                title="Failure in the injection process",
                parent=choose_process_window,
            )
            choose_process_window.quit()
            choose_process_window.destroy()
        else:
            choose_process_window.quit()
            choose_process_window.destroy()

    def tryFindGame():
        try:
            hwnd = win32gui.FindWindow("MainWindow", None)
            pid = win32process.GetWindowThreadProcessId(hwnd)
            if "2.0" in win32gui.GetWindowText(hwnd):
                PVZ_data.update_PVZ_version(2.0)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.1" in win32gui.GetWindowText(hwnd):
                PVZ_data.update_PVZ_version(2.1)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.2" in win32gui.GetWindowText(hwnd):
                PVZ_data.update_PVZ_version(2.2)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.3.5" in win32gui.GetWindowText(hwnd):
                PVZ_data.update_PVZ_version(2.35)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.3.6" in win32gui.GetWindowText(hwnd):
                PVZ_data.update_PVZ_version(2.36)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.3.7" in win32gui.GetWindowText(hwnd):
                PVZ_data.update_PVZ_version(2.37)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.3" in win32gui.GetWindowText(hwnd):
                PVZ_data.update_PVZ_version(2.3)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            PVZ_data.update_PVZ_memory(Pymem(pid[1]))
            PVZ_data.update_PVZ_pid(pid[1])
            choose_process_window.quit()
            choose_process_window.destroy()
        except:
            Messagebox.show_error(
                "Please make sure the game has been opened and it is not running as an administrator\nIf you still can't inject the game, you can try to use the administrator to turn on the modifier",
                title="No game",
                parent=choose_process_window,
            )
            return

    # def retry():
    #     global PVZ_memory
    #     choose_process_window.quit()
    #     choose_process_window.destroy()
    #     data.update_PVZ_memory(1
    #     # choosegame()
    #     return PVZ_memory

    def close():
        choose_process_window.quit()
        choose_process_window.destroy()
        PVZ_data.update_PVZ_memory(0)
        PVZ_data.update_PVZ_pid(0)

    def getSelecthwnd():
        hwnd_title = dict()

        def get_all_hwnd(hwnd, mouse):
            if (
                win32gui.IsWindow(hwnd)
                and win32gui.IsWindowEnabled(hwnd)
                and win32gui.IsWindowVisible(hwnd)
            ):
                hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

        win32gui.EnumWindows(get_all_hwnd, 0)
        selecthwnd = list()
        for h, t in hwnd_title.items():
            if t != "":
                pid = win32process.GetWindowThreadProcessId((h))
                pn = psutil.Process(pid[1]).name()
                selecthwnd.append((pid[1], [t], [pn]))
        return selecthwnd

    choose_process_window = ttk.Toplevel(topmost=True)
    choose_process_window.title("Choose a process")
    choose_process_window.geometry("700x700")
    choose_process_window.iconphoto(
        False, ttk.PhotoImage(file=resource_path(r"res\icon\choose.png"))
    )
    choose_process_window.tk.call("tk", "scaling", 4 / 3)
    main_window_x = main_window.winfo_x()
    main_window_y = main_window.winfo_y()
    choose_process_window.geometry(f"+{main_window_x+50}+{main_window_y + 50}")
    label = ttk.Label(
        choose_process_window,
        text="If the game is not turned on, please click to find the game button after opening the game",
        bootstyle=WARNING,
        font=("Black body", 16),
    )
    label.pack(pady=20)
    frame1 = ttk.Frame(choose_process_window)
    frame1.pack()
    retry_button = ttk.Button(frame1, text="Find a game", command=lambda: tryFindGame())
    retry_button.pack(side=LEFT, padx=80)
    close_button = ttk.Button(
        frame1, text="closure", bootstyle=DANGER, command=lambda: close()
    )
    close_button.pack(side=RIGHT, padx=80)
    label = ttk.Label(
        choose_process_window,
        text="If necessary, you can manually select the game window below\nWindow name is generally plants vs. zombie hybrid version\nThe process name is generally plantsvszombies.exe\nThe display format is the PID window name process name",
        bootstyle=INFO,
        font=("Black body", 16),
    )
    label.pack(pady=(50, 10))
    frame2 = ttk.Frame(choose_process_window)
    frame2.pack()
    combobox = ttk.Combobox(frame2, bootstyle=PRIMARY, width=50)
    combobox.pack(side=LEFT)

    def refreshList():
        selecthwnd = getSelecthwnd()
        # Set the value in the drop -down menu
        combobox["state"] = NORMAL
        combobox["value"] = selecthwnd
        combobox["state"] = READONLY
        # Set the default value of the drop -down menu,The default value index starts from 0
        combobox.current(0)

    refreshList()
    refresh_button = ttk.Button(
        frame2, text="Refresh list", bootstyle=INFO, command=lambda: refreshList()
    )
    refresh_button.pack(side=LEFT, padx=(10, 0))
    comfrime_button = ttk.Button(
        choose_process_window,
        text="Sure",
        bootstyle=SUCCESS,
        command=lambda: openPVZ_memory(combobox.get()),
    )
    comfrime_button.pack(pady=(30, 0))
    choose_process_window.protocol("WM_DELETE_WINDOW", lambda: close())
    choose_process_window.mainloop()


def support():
    global main_window
    support_window = ttk.Toplevel(topmost=True)
    support_window.title("about")
    support_window.geometry("300x480")
    support_window.iconphoto(
        False, ttk.PhotoImage(file=resource_path((r"res\icon\info.png")))
    )
    support_window.tk.call("tk", "scaling", 4 / 3)
    main_window_x = main_window.winfo_x()
    main_window_y = main_window.winfo_y()
    support_window.geometry(f"+{main_window_x+100}+{main_window_y + 100}")
    ttk.Label(
        support_window, text="This software is completely free", font=("Black body", 18), bootstyle=SUCCESS
    ).pack(pady=10)

    def open_qq0():
        webbrowser.open_new(
            r"http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=jtpHFKp2U6UF-jQWoD6bFBGvOe8-nU33&authKey=xGtPLe9Hus9NLhJ%2FTZZdLU0uzPIAM2OGTGI%2B9K8D1Onyujzgmm5t1RPIGWpSrLaz&noverify=0&group_code=978991455"
        )

    qq0_frame = ttk.Frame(support_window)
    qq0_frame.pack()
    ttk.Label(qq0_frame, text="Communication group:", font=("Black body", 8), bootstyle=INFO).pack(
        side=LEFT
    )
    ttk.Button(
        qq0_frame,
        text="978991455",
        padding=0,
        bootstyle=(PRIMARY, LINK),
        cursor="hand2",
        command=open_qq0,
    ).pack(side=LEFT)
    ttk.Label(
        support_window, text="If you have any questions, you can add group feedback", font=("Black body", 8), bootstyle=INFO
    ).pack()
    text = ttk.Text(support_window, width=50, height=8)
    scroll = ttk.Scrollbar(support_window)
    # Put on the right side of the window, Fill in Y vertical direction
    scroll.place(x=0, y=155, relx=1, anchor=E, height=150)

    # Two control correlation
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)

    text.pack()
    str1 = (
        "b0.38\n"
        "Adaptation hybrid 2.3.7 16 card slot\n"
        "Only repair the stiff king's blood volume address\n"
        "b0.37\n"
        "Adaptation hybrid 2.3.6 16 card slot\n"
        "Only repair the stiff king's blood volume address\n"
        "Optimized the display effect of the plant selection interface\n"
        "b0.36\n"
        "Adaptation of hybrids 2.3.5 new plants, new zombies, new maps, new bullets\n"
        "Only repair the stiff king's blood volume address"
        "b0.35\n"
        'Adaptation to hybrid 2.3 new zombie blood volume, thank you for the group friends "." The hard -collected blood address address\n'
        "Fix the problem that there is no new card version of the win7 version, try to repair the problem of the WIN7 version that is not effective"
        "b0.34\n"
        "Adaptation of hybrid 2.3 New plants, new zombies, new maps, new bullets\n"
        "Only repair the stiff king's blood volume address"
        "b0.33\n"
        "Added hybrid 2.2 new bullets\n"
        "After repairing the modification of bullets and random bullets, now it will be modified before launch\n"
        "New Nuts Giant Flash Repair, Located on the Tab Page of Unthacoded Category\n"
        "Repair the abolition header to the free control failure failure\n"
        "Fixed the address of some zombie blood volume\n"
        "b0.32\n"
        "Adapted Hybrid 2.2 Version of New Maps, New Plants, New Zombies\n"
        "Add one -click to complete all mini game levels\n"
        "Fix a series of problems that have been modified\n"
        "Fixed the problem that the venue items may be loaded and failed to report an error.\n"
        "b0.31\n"
        "Fixed a problem of some new plant planting is bud\n"
        "Fix the problem of understanding all plants in the lock\n"
        "b0.30\n"
        "Added automatic recognition game version function, and currently supports 2.0 (including 2.088) and 2.1\n"
        "Fixed a series of 2.1 failure functions, including super shovel, unlock all cards, zombie beans charm, waste manuscript head control, blood repair, monster modification, gift box zombie, etc.\n"
        "Fix the modification of zombie blood volume, zombie card sun consumption modification\n"
        "Adapt to new maps, new version shortcut keys\n"
        "New features: Unlimited items, silver coins, gold coins, diamonds and store items are locked to 9999\n"
        "Temporarily shelves: Special circumstances of free placement and random bullets (planned)\n"
        "b0.29\n"
        "Newly added king drawing correction function to support the coexistence of multiple kings\n"
        "After rewriting the choice of plant, now when choosing a plant, you will pop up the illustration book for selection\n"
        "Fix the problem of disappearing the plants underneath when opening freely when opening freely.\n"
        "b0.28\n"
        "The logic of the shortcut keys is rewritten, and the problem of the shortcut key may cause the shortcut key when repairing the multi -threaded (such as loading plug -in).\n"
        "Freely placed newly added inspecting strong nut repairing surgery.Fix the problem of destruction and farm cannon to clear the previous plants, and repair the problem that the strong nuts and pumpkin categories in the pillar mode can only be stacked.\n"
        "b0.27\n"
        "Fixed the flickering of the random card slot, and the new random zombie card slot was added\n"
        "The plant attribute modification can modify the sunlight consumption of the zombie card \n"
        "Fix some problems that may cause shortcut keys to fail\n"
        "Fix the problem that the strange rate is too high and the type of strange strangeness may not take effect or flickering\n"
        "The new jumping function can enter the hidden level, located in the tabbed tabs without classification\n"
        "b0.26\n"
        "New blood repair can show the blood volume of dense fog, invisible zombies and roll kings\n"
        "Newly added special effects, located on the tab without classification\n"
        "Newly generated bullets, can be freely arranged for cool barrage, located on the tabs of no classification for the time being\n"
        "Added a monster modification function, you can modify the monster of the level\n"
        "b0.25\n"
        "Fix the charm of zombie beans failed\n"
        "The shortcut key planting adapts to the blood of 2.088 and moves to the first page\n"
        "The newly added waste manuscript helmet can be controlled, located in the tabs of unscolable categories for the time being\n"
        "New zombie blood volume modification function\n"
        "b0.24\n"
        "Remove the original high -level pause, please use the new version of the high -level pause\n"
        "The color of the high -level pause mask can be customized\n"
        "The new treasure devourer has no pits and skeleton zombies without pits, which is located in the tabs without classification\n"
        "New bullet size modification function (does not affect damage), which is effective for some plants\n"
        "New plant bullet type modification function is effective for some plants\n"
        "b0.23\n"
        "Fixed a bug that destroyed mushrooms without leaving a pit but still unable to grow\n"
        "Optimized the cancellation of cooling, and now it can be planted continuously when the advanced pause\n"
        "The visual effect reminder was added to the high -level suspension, and now the high -level suspension is changed to trigger from the shortcut key in the game\n"
        "The new archive modification function can quickly modify the level to pass or fail to pass\n"
        "CD -ROM and car replenishment increase all options, and increase automatic car replenishment function\n"
        "b0.22\n"
        "Fixed a bug that fell the zombie drop and caused the flashback\n"
        "Fixed the bug of potato thunder that was eliminated by the tombstone when turning on the super shovel.\n"
        "Optimized free placement and pillar mode\n"
        "Newly destroyed no pit, zombie beans produced charm zombies, no delayed, non -exhaustive rotation modification function, located in the current unsoliced ​​tab page\n"
    )

    text.insert(INSERT, str1)
    text.config(state=DISABLED)
    github_frame = ttk.Frame(support_window)
    github_frame.pack()
    ttk.Label(
        github_frame, text="All code opens from", font=("Black body", 12), bootstyle=SUCCESS
    ).pack(side=LEFT)

    def open_code():
        webbrowser.open_new("https://github.com/EFrostBlade/PVZHybrid_Editor")

    ttk.Button(
        github_frame,
        text="PVZHybrid_Editor(github.com)",
        padding=0,
        bootstyle=(PRIMARY, LINK),
        cursor="hand2",
        command=open_code,
    ).pack(side=LEFT)
    ttk.Label(
        support_window,
        text="If you think this software is helpful, welcome to sponsor support developers",
        font=("黑体", 8),
        bootstyle=WARNING,
    ).pack()

    def open_qq():
        webbrowser.open_new(
            r"https://ti.qq.com/open_qq/index2.html?url=mqqapi%3a%2f%2fuserprofile%2ffriend_profile_card%3fsrc_type%3dweb%26version%3d1.0%26source%3d2%26uin%3d3171264475"
        )

    qq_frame = ttk.Frame(support_window)
    ttk.Label(
        support_window,
        text="After sponsorship any amount, you can add the sponsorship group:",
        font=("黑体", 8),
        bootstyle=WARNING,
    ).pack()
    qq_frame.pack()
    ttk.Label(
        qq_frame,
        text="Add QQ",
        font=("Black body", 8),
        bootstyle=WARNING,
    ).pack(side=LEFT)
    ttk.Button(
        qq_frame,
        text="3171264475",
        padding=0,
        bootstyle=(PRIMARY, LINK),
        cursor="hand2",
        command=open_qq,
    ).pack(side=LEFT)
    ttk.Label(
        qq_frame,
        text="Pull into the group after sending the sponsorship screenshot",
        font=("Black body", 8),
        bootstyle=WARNING,
    ).pack(side=LEFT)
    ttk.Label(
        support_window,
        text="Entry groups can enjoy functions, priority adaptation, 1 to 1 problem solving and other services",
        font=("Black body", 8),
        bootstyle=WARNING,
    ).pack()
    ttk.Label(
        support_window,
        text=r"There are good things in the group, please enter the group after sponsorship\^o^/",
        font=("Black body", 8),
        bootstyle=WARNING,
    ).pack()
    image_frame = ttk.Frame(support_window)
    image_frame.pack()
    AliPay = ttk.PhotoImage(file=resource_path(r"res/support/AliPay.png"))
    WeChatPay = ttk.PhotoImage(file=resource_path(r"res/support/WeChatPay.png"))
    AliPay_image = ttk.Label(image_frame, image=AliPay)
    AliPay_image.grid(row=0, column=0, padx=10)
    WeChatPay_image = ttk.Label(image_frame, image=WeChatPay)
    WeChatPay_image.grid(row=0, column=1, padx=10)
    ttk.Label(image_frame, text="Alipay", bootstyle=PRIMARY, font=("Black body", 12)).grid(
        row=1, column=0, pady=5
    )
    ttk.Label(image_frame, text="WeChat payment", bootstyle=SUCCESS, font=("Black body", 12)).grid(
        row=1, column=1, pady=5
    )
    support_window.mainloop()


def delete_config():
    global main_window
    deete_config_window = ttk.Toplevel(topmost=True)
    deete_config_window.title("The configuration file is wrong!")
    deete_config_window.geometry("300x300")
    deete_config_window.tk.call("tk", "scaling", 4 / 3)
    main_window_x = main_window.winfo_x()
    main_window_y = main_window.winfo_y()
    deete_config_window.geometry(f"+{main_window_x+100}+{main_window_y + 100}")
    ttk.Label(
        deete_config_window,
        text="Error occurs when reading the configuration file\nDelete the configuration file and close the program\nPlease restart the program",
        font=("Black body", 18),
        bootstyle=DANGER,
    ).pack(pady=20)
    ttk.Button(
        deete_config_window,
        text="Sure",
        bootstyle=DANGER,
        command=lambda: exit_with_delete_config(config_file_path),
    ).pack()
    deete_config_window.protocol(
        "WM_DELETE_WINDOW", lambda: exit_with_delete_config(config_file_path)
    )
    deete_config_window.mainloop()


def on_card_image_click(event, window, combobox):
    index = int(event.widget.cget("text"))
    if 256 > index >= 60:
        index = index + 15
    combobox.current(index)
    window.destroy()


def open_card_select_window(combobox):
    global card_select_window
    card_select_window = tk.Toplevel()
    card_select_window.title("Choice card")
    main_window_x = main_window.winfo_x()
    main_window_y = main_window.winfo_y()
    card_select_window.geometry(f"+{main_window_x+50}+{main_window_y + 50}")

    notebook = ttk.Notebook(card_select_window)
    notebook.pack(fill="both", expand=True)

    # Create a tab for plants
    plant_tab = ttk.Frame(notebook)
    notebook.add(plant_tab, text="plant")

    plant_images = os.listdir(resource_path("res/cards/pvzhe_plants"))
    r = 0
    for i, image_file in enumerate(plant_images):
        image = Image.open(resource_path(f"res/cards/pvzhe_plants/{image_file}"))
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(plant_tab, image=photo, text=str(i))
        label.image = photo  # keep a reference to the image
        label.bind(
            "<Button-1>",
            lambda event: on_card_image_click(event, card_select_window, combobox),
        )
        label.grid(row=i // 18, column=i % 18)
        r = i // 18

    # Create a tab for zombies
    zombie_tab = ttk.Frame(notebook)
    notebook.add(zombie_tab, text="Zombie")

    zombie_images = os.listdir(resource_path("res/cards/pvzhe_zombies"))
    for i, image_file in enumerate(zombie_images):
        image = Image.open(resource_path(f"res/cards/pvzhe_zombies/{image_file}"))
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(zombie_tab, image=photo, text=str(i + 256))
        label.image = photo  # keep a reference to the image
        label.bind(
            "<Button-1>",
            lambda event: on_card_image_click(event, card_select_window, combobox),
        )
        label.grid(row=r + 1 + i // 18, column=i % 18)

    def closeCombobox(combobox):
        combobox.event_generate("<Escape>")

    card_select_window.after(100, lambda: closeCombobox(combobox))


def on_zombie_image_click(event, window, combobox):
    index = int(event.widget.cget("text"))
    combobox.current(index)
    window.destroy()


def open_zombie_select_window(combobox):
    global zombie_select_window
    zombie_select_window = tk.Toplevel()
    zombie_select_window.title("Choose a zombie")
    main_window_x = main_window.winfo_x()
    main_window_y = main_window.winfo_y()
    zombie_select_window.geometry(f"+{main_window_x+50}+{main_window_y + 50}")

    notebook = ttk.Notebook(zombie_select_window)
    notebook.pack(fill="both", expand=True)
    zombie_tab = ttk.Frame(notebook)
    notebook.add(zombie_tab, text="僵尸")

    zombie_images = os.listdir(resource_path("res/cards/pvzhe_zombies"))
    for i, image_file in enumerate(zombie_images):
        image = Image.open(resource_path(f"res/cards/pvzhe_zombies/{image_file}"))
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(zombie_tab, image=photo, text=i)
        label.image = photo  # keep a reference to the image
        label.bind(
            "<Button-1>",
            lambda event: on_zombie_image_click(event, zombie_select_window, combobox),
        )
        label.grid(row=i // 18, column=i % 18)

    def closeCombobox(combobox):
        combobox.event_generate("<Escape>")

    zombie_select_window.after(100, lambda: closeCombobox(combobox))


def mainWindow():
    global main_window
    main_window = ttk.Window()
    main_window.title(
        "Hybrid version of multi -function modifier  "
        + str(current_version)
        + "      Game version:"
        + str(PVZ_data.PVZ_version)
    )
    main_window.geometry("800x850")
    main_window.iconphoto(
        False, ttk.PhotoImage(file=resource_path(r"res\icon\editor.png"))
    )
    main_window.tk.call("tk", "scaling", 4 / 3)

    def apply_window_position(file_path, window, section="main_window_position"):
        config = load_config(file_path)
        try:
            position = config.get(section, {})
            x = position.get("x", 150)  # The default value is 100
            y = position.get("y", 150)  # The default value is 100
            window.geometry(f"+{x}+{y}")
        except:
            pass

    # Call after the main window is created
    apply_window_position(config_file_path, main_window)

    def open_update_window(latest_version):
        global main_window

        def close():
            update_window.quit()
            update_window.destroy()

        update_window = ttk.Toplevel(topmost=True)
        update_window.title("Have a new version")
        update_window.geometry("420x620")
        update_window.iconphoto(
            False, ttk.PhotoImage(file=resource_path((r"res\icon\info.png")))
        )
        update_window.tk.call("tk", "scaling", 4 / 3)
        main_window_x = main_window.winfo_x()
        main_window_y = main_window.winfo_y()
        update_window.geometry(f"+{main_window_x+150}+{main_window_y + 150}")
        ttk.Label(
            update_window,
            text="Detecting a new version{}".format(latest_version),
            font=("Black body", 18),
            bootstyle=INFO,
        ).pack()
        ttk.Label(
            update_window, text="This software is completely free", font=("Black body", 18), bootstyle=SUCCESS
        ).pack(pady=10)

        def open_qq0():
            webbrowser.open_new(
                r"http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=jtpHFKp2U6UF-jQWoD6bFBGvOe8-nU33&authKey=xGtPLe9Hus9NLhJ%2FTZZdLU0uzPIAM2OGTGI%2B9K8D1Onyujzgmm5t1RPIGWpSrLaz&noverify=0&group_code=978991455"
            )

        qq0_frame = ttk.Frame(update_window)
        qq0_frame.pack()
        ttk.Label(qq0_frame, text="Communication group:", font=("Black body", 8), bootstyle=INFO).pack(
            side=LEFT
        )
        ttk.Button(
            qq0_frame,
            text="978991455",
            padding=0,
            bootstyle=(PRIMARY, LINK),
            cursor="hand2",
            command=open_qq0,
        ).pack(side=LEFT)
        ttk.Label(
            update_window, text="If you have any questions, you can add group feedback", font=("Black body", 8), bootstyle=INFO
        ).pack()
        github_frame = ttk.Frame(update_window)
        github_frame.pack()
        ttk.Label(
            github_frame, text="Go to download the latest version", font=("Black body", 12), bootstyle=SUCCESS
        ).pack(side=LEFT)

        def open_code():
            webbrowser.open_new(
                "https://gitee.com/EFrostBlade/PVZHybrid_Editor/releases"
            )

        ttk.Button(
            github_frame,
            text="PVZHybrid_Editor(gitee.com)",
            padding=0,
            bootstyle=(PRIMARY, LINK),
            cursor="hand2",
            command=open_code,
        ).pack(side=LEFT)
        ttk.Label(
            update_window,
            text="If you think this software is helpful, welcome to sponsor support developers",
            font=("Black body", 8),
            bootstyle=WARNING,
        ).pack()

        def open_qq():
            webbrowser.open_new(
                r"https://ti.qq.com/open_qq/index2.html?url=mqqapi%3a%2f%2fuserprofile%2ffriend_profile_card%3fsrc_type%3dweb%26version%3d1.0%26source%3d2%26uin%3d3171264475"
            )

        qq_frame = ttk.Frame(update_window)
        ttk.Label(
            update_window,
            text="After sponsorship any amount, you can add the sponsorship group:",
            font=("Black body", 8),
            bootstyle=WARNING,
        ).pack()
        qq_frame.pack()
        ttk.Label(
            qq_frame,
            text="Add QQ",
            font=("Black body", 8),
            bootstyle=WARNING,
        ).pack(side=LEFT)
        ttk.Button(
            qq_frame,
            text="3171264475",
            padding=0,
            bootstyle=(PRIMARY, LINK),
            cursor="hand2",
            command=open_qq,
        ).pack(side=LEFT)
        ttk.Label(
            qq_frame,
            text="Pull into the group after sending the sponsorship screenshot",
            font=("Black body", 8),
            bootstyle=WARNING,
        ).pack(side=LEFT)
        ttk.Label(
            update_window,
            text="Entry groups can enjoy functions, priority adaptation, 1 to 1 problem solving and other services",
            font=("Black body", 8),
            bootstyle=WARNING,
        ).pack()
        ttk.Label(
            update_window,
            text=r"There are good things in the group, please enter the group after sponsorship\^o^/",
            font=("Black body", 8),
            bootstyle=WARNING,
        ).pack()
        image_frame = ttk.Frame(update_window)
        image_frame.pack()
        AliPay = ttk.PhotoImage(file=resource_path(r"res/support/AliPay.png"))
        WeChatPay = ttk.PhotoImage(file=resource_path(r"res/support/WeChatPay.png"))
        AliPay_image = ttk.Label(image_frame, image=AliPay)
        AliPay_image.grid(row=0, column=0, padx=10)
        WeChatPay_image = ttk.Label(image_frame, image=WeChatPay)
        WeChatPay_image.grid(row=0, column=1, padx=10)
        ttk.Label(
            image_frame, text="Alipay", bootstyle=PRIMARY, font=("黑体", 12)
        ).grid(row=1, column=0, pady=5)
        ttk.Label(
            image_frame, text="WeChat payment", bootstyle=SUCCESS, font=("黑体", 12)
        ).grid(row=1, column=1, pady=5)
        update_window.protocol("WM_DELETE_WINDOW", lambda: close())
        update_window.mainloop()

    try:
        # Get the latest version number from the server
        response = requests.get(version_url)
        latest_version = response.text.strip()
        print(latest_version)
        if latest_version == "The content may contain violation information":
            Messagebox.show_error(
                "The version number is blocked",
                title="Update test failure",
            )
        # 比较版本号
        elif latest_version > current_version:
            # If you find a new version, prompt the user
            open_update_window(latest_version)
    except Exception:
        Messagebox.show_error(
            "Can't check the update, please check your network connection.",
            title="Update test failure",
        )

    # style=ttk.Style()
    # style.configure('small.TButton',font=("黑体",8),padding=(0,0,0,0))
    process_frame = ttk.Frame(main_window)
    process_frame.place(x=0, y=0, relx=1, rely=1, anchor=SE)
    process_label = ttk.Label(process_frame, text="", font=("黑体", 8))
    process_label.pack(side=LEFT)

    def updateGame():
        chooseGame()
        if type(PVZ_data.PVZ_memory) != Pymem:  # noqa: E721
            process_label["text"] = "No game"
            process_label.config(bootstyle=DANGER)
        else:
            process_label["text"] = (
                "Find the process:"
                + str(PVZ_data.PVZ_memory.process_id)
                + str(psutil.Process(PVZ_data.PVZ_memory.process_id).name())
            )
            process_label.config(bootstyle=DANGER)

    def tryFindGame():
        try:
            hwnd = win32gui.FindWindow("MainWindow", None)
            pid = win32process.GetWindowThreadProcessId(hwnd)
            if "2.0" in win32gui.GetWindowText(hwnd):
                PVZ_data.update_PVZ_version(2.0)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.1" in win32gui.GetWindowText(hwnd):
                PVZ_data.update_PVZ_version(2.1)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.2" in win32gui.GetWindowText(hwnd):
                PVZ_data.update_PVZ_version(2.2)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.3.5" in win32gui.GetWindowText(hwnd):
                PVZ_data.update_PVZ_version(2.35)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.3.6" in win32gui.GetWindowText(hwnd):
                PVZ_data.update_PVZ_version(2.36)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.3.7" in win32gui.GetWindowText(hwnd):
                PVZ_data.update_PVZ_version(2.37)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            elif "2.3" in win32gui.GetWindowText(hwnd):
                PVZ_data.update_PVZ_version(2.3)
                main_window.title(
                    "Hybrid version of multi -function modifier  "
                    + str(current_version)
                    + "      Game version:"
                    + str(PVZ_data.PVZ_version)
                )
            PVZ_data.update_PVZ_memory(Pymem(pid[1]))
            PVZ_data.update_PVZ_pid(pid[1])
            process_label["text"] = (
                "Find the process:"
                + str(PVZ_data.PVZ_memory.process_id)
                + str(psutil.Process(PVZ_data.PVZ_memory.process_id).name())
            )
            process_label.config(bootstyle=DANGER)
        except:
            updateGame()

    tryFindGame()
    choose_process_button = ttk.Button(
        process_frame,
        text="Choose a game",
        padding=0,
        cursor="hand2",
        bootstyle=(PRIMARY, LINK),
        command=lambda: updateGame(),
    )
    choose_process_button.pack(side=LEFT)
    back_ground_status = ttk.IntVar(main_window)
    back_ground_check = ttk.Checkbutton(
        main_window,
        text="Background operation",
        variable=back_ground_status,
        bootstyle="round-toggle",
        command=lambda: pvz.backGround(back_ground_status.get()),
    )
    back_ground_check.place(x=3, y=-3, relx=0, rely=1, anchor=SW)

    page_tab = ttk.Notebook(main_window)
    page_tab.pack(padx=7, pady=(7, 25), fill=BOTH, expand=True)
    common_page = ttk.Frame(page_tab)
    common_page.pack()
    page_tab.add(common_page, text="Common function")
    resource_modify_frame = ttk.Labelframe(
        common_page, text="Resource modification", bootstyle=WARNING
    )
    resource_modify_frame.place(x=0, y=0, anchor=NW)
    upper_limit_status = ttk.BooleanVar(resource_modify_frame)
    upper_limit_check = ttk.Checkbutton(
        resource_modify_frame,
        text="Unlock resource limit",
        bootstyle="warning-round-toggle",
        variable=upper_limit_status,
        command=lambda: pvz.upperLimit(upper_limit_status.get()),
    )
    upper_limit_check.grid(row=0, column=0, columnspan=2, sticky=E)
    ttk.Label(
        resource_modify_frame, text="Current sunlight:", bootstyle=WARNING, font=("Song style", 9)
    ).grid(row=1, column=0, sticky=E)
    sun_value = ttk.IntVar(resource_modify_frame)
    sun_value_entry = ttk.Entry(
        resource_modify_frame, width=8, bootstyle=WARNING, textvariable=sun_value
    )
    sun_value_entry.grid(row=1, column=1)

    def setSun(event):
        pvz.setSun(sun_value.get())
        resource_modify_frame.focus_set()

    sun_value_entry.bind("<Return>", setSun)
    ttk.Label(
        resource_modify_frame, text="Increase sunlight:", bootstyle=WARNING, font=("Song style", 9)
    ).grid(row=2, column=0, sticky=E)
    sun_add_value = ttk.IntVar(resource_modify_frame)
    sun_add_entry = ttk.Entry(
        resource_modify_frame, width=8, bootstyle=WARNING, textvariable=sun_add_value
    )
    sun_add_entry.grid(row=2, column=1)
    config = load_config(config_file_path)
    try:
        sun_add_value.set(config["data"]["sunadd"])
    except:
        pass

    def addSun(event):
        pvz.addSun(sun_add_value.get())
        modify_config(config_file_path, "data", "sunadd", sun_add_value.get())
        resource_modify_frame.focus_set()

    sun_add_entry.bind("<Return>", addSun)

    ttk.Label(
        resource_modify_frame, text="Current silver coin:", bootstyle=SECONDARY, font=("Song style", 9)
    ).grid(row=3, column=0, sticky=E)
    silver_value = ttk.IntVar(resource_modify_frame)
    silver_value_entry = ttk.Entry(
        resource_modify_frame, width=8, bootstyle=WARNING, textvariable=silver_value
    )
    silver_value_entry.grid(row=3, column=1)

    def setSilver(event):
        pvz.setSilver(silver_value.get())
        resource_modify_frame.focus_set()

    silver_value_entry.bind("<Return>", setSilver)
    ttk.Label(
        resource_modify_frame, text="Increase silver coin:", bootstyle=SECONDARY, font=("Song style", 9)
    ).grid(row=4, column=0, sticky=E)
    silver_add_value = ttk.IntVar(resource_modify_frame)
    silver_add_entry = ttk.Entry(
        resource_modify_frame, width=8, bootstyle=WARNING, textvariable=silver_add_value
    )
    silver_add_entry.grid(row=4, column=1)
    config = load_config(config_file_path)
    try:
        silver_add_value.set(config["data"]["silveradd"])
    except:
        pass

    def addSilver(event):
        pvz.addSilver(silver_add_value.get())
        modify_config(config_file_path, "data", "silveradd", silver_add_value.get())
        resource_modify_frame.focus_set()

    silver_add_entry.bind("<Return>", addSilver)

    ttk.Label(
        resource_modify_frame, text="Current gold coin:", bootstyle=WARNING, font=("Song style", 9)
    ).grid(row=5, column=0, sticky=E)
    gold_value = ttk.IntVar(resource_modify_frame)
    gold_value_entry = ttk.Entry(
        resource_modify_frame, width=8, bootstyle=WARNING, textvariable=gold_value
    )
    gold_value_entry.grid(row=5, column=1)

    def setGold(event):
        pvz.setGold(gold_value.get())
        resource_modify_frame.focus_set()

    gold_value_entry.bind("<Return>", setGold)
    ttk.Label(
        resource_modify_frame, text="Increase gold coins:", bootstyle=WARNING, font=("Song style", 9)
    ).grid(row=6, column=0, sticky=E)
    gold_add_value = ttk.IntVar(resource_modify_frame)
    gold_add_entry = ttk.Entry(
        resource_modify_frame, width=8, bootstyle=WARNING, textvariable=gold_add_value
    )
    gold_add_entry.grid(row=6, column=1)
    config = load_config(config_file_path)
    try:
        gold_add_value.set(config["data"]["goldadd"])
    except:
        pass

    def addGold(event):
        pvz.addGold(gold_add_value.get())
        modify_config(config_file_path, "data", "goldadd", gold_add_value.get())
        resource_modify_frame.focus_set()

    gold_add_entry.bind("<Return>", addGold)

    ttk.Label(
        resource_modify_frame, text="Current diamond:", bootstyle=PRIMARY, font=("Song style", 9)
    ).grid(row=7, column=0, sticky=E)
    diamond_value = ttk.IntVar(resource_modify_frame)
    diamond_value_entry = ttk.Entry(
        resource_modify_frame, width=8, bootstyle=WARNING, textvariable=diamond_value
    )
    diamond_value_entry.grid(row=7, column=1)

    def setDiamond(event):
        pvz.setDiamond(diamond_value.get())
        resource_modify_frame.focus_set()

    diamond_value_entry.bind("<Return>", setDiamond)
    ttk.Label(
        resource_modify_frame, text="Increase diamond:", bootstyle=PRIMARY, font=("Song style", 9)
    ).grid(row=8, column=0, sticky=E)
    diamond_add_value = ttk.IntVar(resource_modify_frame)
    diamond_add_entry = ttk.Entry(
        resource_modify_frame,
        width=8,
        bootstyle=WARNING,
        textvariable=diamond_add_value,
    )
    diamond_add_entry.grid(row=8, column=1)
    config = load_config(config_file_path)
    try:
        diamond_add_value.set(config["data"]["diamondadd"])
    except:
        pass

    def addDiamond(event):
        pvz.addDiamond(diamond_add_value.get())
        modify_config(config_file_path, "data", "diamondadd", diamond_add_value.get())
        resource_modify_frame.focus_set()

    diamond_add_entry.bind("<Return>", addDiamond)

    quick_start_frame = ttk.LabelFrame(common_page, text="Use quickly", bootstyle=SUCCESS)
    quick_start_frame.place(x=0, y=0, relx=1, rely=0, anchor=NE)
    over_plant_status = ttk.BooleanVar(quick_start_frame)
    over_plant_check = ttk.Checkbutton(
        quick_start_frame,
        text="Freely",
        variable=over_plant_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.overPlant(over_plant_status.get()),
    )
    over_plant_check.grid(row=0, column=0, sticky=W)
    ToolTip(
        over_plant_check, text="Plants can overlap and place it and ignore the terrain", bootstyle=(INFO, INVERSE)
    )
    free_plant_status = ttk.BooleanVar(quick_start_frame)
    free_plant_check = ttk.Checkbutton(
        quick_start_frame,
        text="Free planting",
        variable=free_plant_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.ignoreSun(free_plant_status.get()),
    )
    free_plant_check.grid(row=1, column=0, sticky=W)
    ToolTip(free_plant_check, text="Plants can not consume sunlight planting", bootstyle=(INFO, INVERSE))
    cancel_cd_status = ttk.BooleanVar(quick_start_frame)
    cancel_cd_check = ttk.Checkbutton(
        quick_start_frame,
        text="Cancel the cooling",
        variable=cancel_cd_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.cancelCd(cancel_cd_status.get()),
    )
    cancel_cd_check.grid(row=2, column=0, sticky=W)
    ToolTip(cancel_cd_check, text="Do not enter the cooling time after planting", bootstyle=(INFO, INVERSE))
    auto_colect_status = ttk.BooleanVar(quick_start_frame)
    auto_colect_check = ttk.Checkbutton(
        quick_start_frame,
        text="Automatically collect",
        variable=auto_colect_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.autoCollect(auto_colect_status.get()),
    )
    auto_colect_check.grid(row=3, column=0, sticky=W)
    ToolTip(
        auto_colect_check,
        text="Automatically collect the natural drop of sunlight and the gold coins dropped by zombies",
        bootstyle=(INFO, INVERSE),
    )
    column_like_status = ttk.BooleanVar(quick_start_frame)
    column_like_check = ttk.Checkbutton(
        quick_start_frame,
        text="Column mode",
        variable=column_like_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.column(column_like_status.get()),
    )
    column_like_check.grid(row=4, column=0, sticky=W)
    ToolTip(
        column_like_check,
        text="After planting a plant, plant the same plants in other rows of the same column(可与自由放置配合使用)",
        bootstyle=(INFO, INVERSE),
    )
    shovel_pro_status = ttk.BooleanVar(quick_start_frame)
    shovel_pro_check = ttk.Checkbutton(
        quick_start_frame,
        text="Super shovel",
        variable=shovel_pro_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.shovelpro(shovel_pro_status.get()),
    )
    shovel_pro_check.grid(row=5, column=0, sticky=W)
    ToolTip(
        shovel_pro_check,
        text="Remove the plant and return its sunlight to consume and trigger the effect of dead language",
        bootstyle=(INFO, INVERSE),
    )
    never_fail_status = ttk.BooleanVar(quick_start_frame)
    never_fail_check = ttk.Checkbutton(
        quick_start_frame,
        text="Never fail",
        variable=never_fail_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.ignoreZombies(never_fail_status.get()),
    )
    never_fail_check.grid(row=6, column=0, sticky=W)
    ToolTip(never_fail_check, text="Zombies do not judge the failure of the game at home", bootstyle=(INFO, INVERSE))
    Infinite_Items_status = ttk.BooleanVar(quick_start_frame)
    Infinite_Items_check = ttk.Checkbutton(
        quick_start_frame,
        text="Unlimited item",
        variable=Infinite_Items_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.infiniteItems(Infinite_Items_status.get()),
    )
    Infinite_Items_check.grid(row=7, column=0, sticky=W)
    ToolTip(
        Infinite_Items_check,
        text="Silver coins, gold coins, diamonds and store items are locked to 9999",
        bootstyle=(INFO, INVERSE),
    )
    # pause_pro_status = ttk.BooleanVar(quick_start_frame)
    # pause_pro_check = ttk.Checkbutton(quick_start_frame, text="高级暂停", variable=pause_pro_status,
    #                                   bootstyle="success-round-toggle", command=lambda: pvz.pausePro(pause_pro_status.get()))
    # pause_pro_check.grid(row=7, column=0, sticky=W)
    # ToolTip(pause_pro_check, text="可以暂停种植植物", bootstyle=(INFO, INVERSE))
    win_button = ttk.Button(
        quick_start_frame,
        text="Current level victory",
        padding=0,
        bootstyle=(SUCCESS, OUTLINE),
        command=lambda: pvz.win(),
    )
    win_button.grid(row=8, column=0, sticky=W, pady=(2, 2))
    ToolTip(
        win_button, text="The current game level is directly settled", bootstyle=(INFO, INVERSE)
    )
    defeat_button = ttk.Button(
        quick_start_frame,
        text="The current level failed",
        padding=0,
        bootstyle=(SUCCESS, OUTLINE),
        command=lambda: pvz.defeat(),
    )
    defeat_button.grid(row=9, column=0, sticky=W, pady=(2, 2))
    ToolTip(
        defeat_button, text="The current game level fails to settle directly", bootstyle=(INFO, INVERSE)
    )
    kill_all_button = ttk.Button(
        quick_start_frame,
        text="Kill all zombies",
        padding=0,
        bootstyle=(SUCCESS, OUTLINE),
        command=lambda: pvz.killAllZombies(),
    )
    kill_all_button.grid(row=10, column=0, sticky=W, pady=(2, 2))
    ToolTip(kill_all_button, text="All the zombies on the current field", bootstyle=(INFO, INVERSE))
    unlock_button = ttk.Button(
        quick_start_frame,
        text="Unlock all plants",
        padding=0,
        bootstyle=(SUCCESS, OUTLINE),
        command=lambda: pvz.unlock(1),
    )
    unlock_button.grid(row=11, column=0, sticky=W, pady=(2, 2))
    ToolTip(
        unlock_button,
        text="All plants in the game in this game(Including hidden plants that cannot be obtained)",
        bootstyle=(INFO, INVERSE),
    )
    save_load_frame = ttk.Frame(quick_start_frame)
    save_load_frame.grid(row=12, column=0, sticky=W, pady=(2, 2))
    save_button = ttk.Button(
        save_load_frame,
        text="Archive",
        padding=0,
        bootstyle=(SUCCESS, OUTLINE),
        command=lambda: pvz.save(),
    )
    save_button.grid(row=0, column=0, sticky=W, padx=(5, 0), pady=(2, 2))
    load_button = ttk.Button(
        save_load_frame,
        text="Read file",
        padding=0,
        bootstyle=(SUCCESS, OUTLINE),
        command=lambda: pvz.load(),
    )
    load_button.grid(row=0, column=1, sticky=W, padx=(10, 0), pady=(2, 2))

    pause_pro_frame = ttk.LabelFrame(common_page, text="High -level pause", bootstyle=SUCCESS)
    pause_pro_frame.place(x=0, y=300, relx=1, rely=0, anchor=NE)
    pause_pro_status = ttk.BooleanVar(pause_pro_frame)
    pause_pro_check = ttk.Checkbutton(
        pause_pro_frame,
        text="Shortcut key advanced suspension",
        variable=pause_pro_status,
        bootstyle="success-round-toggle",
        command=lambda: setPauseKey(),
    )
    pause_pro_check.grid(row=0, column=0, sticky=W)
    slot_pause_key = ttk.Combobox(
        pause_pro_frame,
        width=5,
        values=PVZ_data.keyTpye,
        font=("Black body", 8),
        state=READONLY,
    )
    slot_pause_key.grid(row=1, column=0)
    slot_pause_key.current(0)
    pause_color_frame = ttk.Frame(pause_pro_frame)
    pause_color_frame.grid(row=2, column=0)
    ttk.Label(pause_color_frame, text="R:", font=("Black body", 12), bootstyle=DANGER).grid(
        row=0, column=0
    )
    pause_r_entry = ttk.Entry(
        pause_color_frame, width=3, font=("黑体", 12), bootstyle=SECONDARY
    )
    pause_r_entry.grid(row=0, column=1, sticky=W)
    ttk.Label(pause_color_frame, text="G:", font=("黑体", 12), bootstyle=SUCCESS).grid(
        row=0, column=2
    )
    pause_g_entry = ttk.Entry(
        pause_color_frame, width=3, font=("黑体", 12), bootstyle=SECONDARY
    )
    pause_g_entry.grid(row=0, column=3, sticky=W)
    ttk.Label(pause_color_frame, text="B:", font=("黑体", 12), bootstyle=PRIMARY).grid(
        row=1, column=0
    )
    pause_b_entry = ttk.Entry(
        pause_color_frame, width=3, font=("黑体", 12), bootstyle=SECONDARY
    )
    pause_b_entry.grid(row=1, column=1, sticky=W)
    ttk.Label(
        pause_color_frame, text="A:", font=("黑体", 12), bootstyle=SECONDARY
    ).grid(row=1, column=2)
    pause_a_entry = ttk.Entry(
        pause_color_frame, width=3, font=("黑体", 12), bootstyle=SECONDARY
    )
    pause_a_entry.grid(row=1, column=3, sticky=W)

    def get_pause_color():
        config = load_config(config_file_path)
        if "data" not in config or "pauseColor" not in config["data"]:
            pause_r_entry.insert(0, "66")
            pause_g_entry.insert(0, "CC")
            pause_b_entry.insert(0, "FF")
            pause_a_entry.insert(0, "AA")
        else:
            try:
                pause_r_entry.insert(0, config["data"]["pauseColor"]["R"])
            except:
                pause_r_entry.insert(0, "66")
            try:
                pause_g_entry.insert(0, config["data"]["pauseColor"]["G"])
            except:
                pause_g_entry.insert(0, "CC")
            try:
                pause_b_entry.insert(0, config["data"]["pauseColor"]["B"])
            except:
                pause_b_entry.insert(0, "FF")
            try:
                pause_a_entry.insert(0, config["data"]["pauseColor"]["A"])
            except:
                pause_a_entry.insert(0, "AA")

    get_pause_color()

    def loadPauseKey():
        config = load_config(config_file_path)
        try:
            slot_pause_key.current(config["slotKeys"]["pause"])
        except:
            pass

    loadPauseKey()

    def setPauseKey():
        if pause_pro_status.get():
            config = load_config(config_file_path)
            if "slotKeys" not in config:
                config["slotKeys"] = {}
            if slot_pause_key.current() != -1:
                config["slotKeys"]["pause"] = slot_pause_key.current()
            if "data" not in config:
                config["data"] = {}
            if "pauseColor" not in config["data"]:
                config["data"]["pauseColor"] = {}
            config["data"]["pauseColor"]["R"] = pause_r_entry.get()
            config["data"]["pauseColor"]["G"] = pause_g_entry.get()
            config["data"]["pauseColor"]["B"] = pause_b_entry.get()
            config["data"]["pauseColor"]["A"] = pause_a_entry.get()
            save_config(config, config_file_path)
            pvz.pauseProKey(
                slot_pause_key.current(),
                int(pause_r_entry.get(), 16),
                int(pause_g_entry.get(), 16),
                int(pause_b_entry.get(), 16),
                int(pause_a_entry.get(), 16),
            )
        else:
            pvz.pauseProKey(False, 0, 0, 0, 0)

    game_speed_frame = ttk.LabelFrame(common_page, text="Game speed", bootstyle=DARK)
    game_speed_frame.place(x=0, y=285, anchor=NW)
    game_speed_label = ttk.Label(game_speed_frame, text="1", bootstyle=DARK)
    game_speed_label.grid(row=0, column=0)
    game_speed_frame.columnconfigure(0, minsize=30)
    game_speed_value = ttk.DoubleVar(game_speed_frame)
    game_speed_value.set(2)

    def changeSpeedValue(value):
        step = 1
        adjusted_value = round(float(value) / step) * step
        game_speed_value.set(adjusted_value)
        if game_speed_value.get() == 0:
            game_speed_label.config(text="0.25")
        elif game_speed_value.get() == 1:
            game_speed_label.config(text="0.5")
        elif game_speed_value.get() == 2:
            game_speed_label.config(text="1")
        elif game_speed_value.get() == 3:
            game_speed_label.config(text="2")
        elif game_speed_value.get() == 4:
            game_speed_label.config(text="5")
        elif game_speed_value.get() == 5:
            game_speed_label.config(text="10")
        elif game_speed_value.get() == 6:
            game_speed_label.config(text="20")
        pvz.changeGameSpeed(game_speed_value.get())

    game_speed_scale = ttk.Scale(
        game_speed_frame,
        from_=0,
        to=6,
        orient=HORIZONTAL,
        variable=game_speed_value,
        command=changeSpeedValue,
    )
    game_speed_scale.grid(row=0, column=1)

    def on_mousewheel(event):
        # Calculate the rolling direction and distance of the roller
        increment = -1 if event.delta > 0 else 1
        # Get the value of the current scale
        value = game_speed_value.get() + increment
        # Set the new scale value
        step = 1
        adjusted_value = round(float(value) / step) * step
        game_speed_value.set(adjusted_value)
        if game_speed_value.get() == 0:
            game_speed_label.config(text="0.25")
        elif game_speed_value.get() == 1:
            game_speed_label.config(text="0.5")
        elif game_speed_value.get() == 2:
            game_speed_label.config(text="1")
        elif game_speed_value.get() == 3:
            game_speed_label.config(text="2")
        elif game_speed_value.get() == 4:
            game_speed_label.config(text="5")
        elif game_speed_value.get() == 5:
            game_speed_label.config(text="10")
        elif game_speed_value.get() == 6:
            game_speed_label.config(text="20")
        pvz.changeGameSpeed(game_speed_value.get())

    game_speed_scale.bind("<MouseWheel>", on_mousewheel)

    # game_difficult_frame = ttk.LabelFrame(common_page, text="游戏难度", bootstyle=DARK)
    # game_difficult_frame.place(x=0, y=320, anchor=NW)
    # gameDifficult = ttk.IntVar(game_difficult_frame)
    # ttk.Radiobutton(
    #     game_difficult_frame,
    #     text="简单",
    #     value=1,
    #     variable=gameDifficult,
    #     bootstyle=SUCCESS,
    #     command=lambda: pvz.setDifficult(gameDifficult.get()),
    # ).grid(row=0, column=0, padx=5)
    # ttk.Radiobutton(
    #     game_difficult_frame,
    #     text="普通",
    #     value=2,
    #     variable=gameDifficult,
    #     bootstyle=DARK,
    #     command=lambda: pvz.setDifficult(gameDifficult.get()),
    # ).grid(row=0, column=1, padx=5)
    # ttk.Radiobutton(
    #     game_difficult_frame,
    #     text="困难",
    #     value=3,
    #     variable=gameDifficult,
    #     bootstyle=DANGER,
    #     command=lambda: pvz.setDifficult(gameDifficult.get()),
    # ).grid(row=0, column=2, padx=5)

    game_save_frame = ttk.LabelFrame(common_page, text="存档修改", bootstyle=DARK)
    game_save_frame.place(x=0, y=325, anchor=NW)
    # ttk.Label(game_save_frame, text="冒险第").grid(row=0, column=0)
    # adventure_start_level_value = ttk.IntVar(game_save_frame)
    # adventure_start_level_combobox = ttk.Combobox(
    #     game_save_frame,
    #     textvariable=adventure_start_level_value,
    #     width=2,
    #     values=list(range(1, 67 + 1)),
    #     font=("黑体", 8),
    #     bootstyle=SECONDARY,
    #     state=READONLY,
    # )
    # adventure_start_level_combobox.grid(row=0, column=1)
    # adventure_start_level_value.set(1)
    # ttk.Label(game_save_frame, text="关至第").grid(row=0, column=2)
    # adventure_end_level_value = ttk.IntVar(game_save_frame)
    # adventure_end_level_combobox = ttk.Combobox(
    #     game_save_frame,
    #     textvariable=adventure_end_level_value,
    #     width=2,
    #     values=list(range(1, 67 + 1)),
    #     font=("黑体", 8),
    #     bootstyle=SECONDARY,
    #     state=READONLY,
    # )
    # adventure_end_level_combobox.grid(row=0, column=3)
    # adventure_end_level_value.set(67)
    # ttk.Label(game_save_frame, text="关").grid(row=0, column=4)

    def complete_advantures():
        # for i in range(
        #     adventure_start_level_value.get() - 1, adventure_end_level_value.get()
        # ):
        for i in range(0, 89):
            pvz.completeAdvanture(i)

    adventure_complete_button = ttk.Button(
        game_save_frame,
        text="Complete all adventures",
        bootstyle=(SUCCESS, OUTLINE),
        padding=0,
        command=lambda: complete_advantures(),
    )
    adventure_complete_button.grid(row=1, column=0, columnspan=2, padx=2)

    def lock_advantures():
        # for i in range(
        #     adventure_start_level_value.get() - 1, adventure_end_level_value.get()
        # ):
        for i in range(0, 89):
            pvz.lockAdvanture(i)

    adventure_lock_button = ttk.Button(
        game_save_frame,
        text="Lock all adventures",
        bootstyle=(DANGER, OUTLINE),
        padding=0,
        command=lambda: lock_advantures(),
    )
    adventure_lock_button.grid(row=1, column=2, columnspan=2, padx=2)
    # ttk.Label(game_save_frame, text="挑战第").grid(row=2, column=0)
    # challenge_start_level_value = ttk.IntVar(game_save_frame)
    # challenge_start_level_combobox = ttk.Combobox(
    #     game_save_frame,
    #     textvariable=challenge_start_level_value,
    #     width=2,
    #     values=list(range(1, 99 + 1)),
    #     font=("黑体", 8),
    #     bootstyle=SECONDARY,
    #     state=READONLY,
    # )
    # challenge_start_level_combobox.grid(row=2, column=1)
    # challenge_start_level_value.set(1)
    # ttk.Label(game_save_frame, text="关至第").grid(row=2, column=2)
    # challenge_end_level_value = ttk.IntVar(game_save_frame)
    # challenge_end_level_combobox = ttk.Combobox(
    #     game_save_frame,
    #     textvariable=challenge_end_level_value,
    #     width=2,
    #     values=list(range(1, 99 + 1)),
    #     font=("黑体", 8),
    #     bootstyle=SECONDARY,
    #     state=READONLY,
    # )
    # challenge_end_level_combobox.grid(row=2, column=3)
    # challenge_end_level_value.set(99)
    # ttk.Label(game_save_frame, text="关").grid(row=2, column=4)

    def complete_challenges():
        # for i in range(
        #     challenge_start_level_value.get() - 1, challenge_end_level_value.get()
        # ):
        for i in range(0, 132):
            pvz.completeChallenge(i)

    challenges_complete_button = ttk.Button(
        game_save_frame,
        text="Complete all challenges",
        bootstyle=(SUCCESS, OUTLINE),
        padding=0,
        command=lambda: complete_challenges(),
    )
    challenges_complete_button.grid(row=3, column=0, columnspan=2, padx=2)

    def lock_challenges():
        # for i in range(
        #     challenge_start_level_value.get() - 1, challenge_end_level_value.get()
        # ):
        for i in range(0, 132):
            pvz.lockChallenge(i)

    challenges_lock_button = ttk.Button(
        game_save_frame,
        text="Lock all challenges",
        bootstyle=(DANGER, OUTLINE),
        padding=0,
        command=lambda: lock_challenges(),
    )
    challenges_lock_button.grid(row=3, column=2, columnspan=2, padx=2)

    def complete_miniGame():
        # for i in range(
        #     challenge_start_level_value.get() - 1, challenge_end_level_value.get()
        # ):
        for i in range(0, 30):
            pvz.completeMiniGame(i)

    miniGame_complete_button = ttk.Button(
        game_save_frame,
        text="Complete mini games",
        bootstyle=(SUCCESS, OUTLINE),
        padding=0,
        command=lambda: complete_miniGame(),
    )
    miniGame_complete_button.grid(row=5, column=0, columnspan=2, padx=2)

    def lock_miniGame():
        # for i in range(
        #     challenge_start_level_value.get() - 1, challenge_end_level_value.get()
        # ):
        for i in range(0, 30):
            pvz.lockMiniGame(i)

    miniGame_lock_button = ttk.Button(
        game_save_frame,
        text="Lock mini game",
        bootstyle=(DANGER, OUTLINE),
        padding=0,
        command=lambda: lock_miniGame(),
    )
    miniGame_lock_button.grid(row=5, column=2, columnspan=2, padx=2)
    # Read the shortcut keys configuration

    def get_shortcuts():
        config = load_config(config_file_path)
        return config.get("shortcuts", {})

    # Remove all the current shortcut key monitoring
    def remove_all_hotkeys():
        for shortcut in get_shortcuts().values():
            keyboard.remove_hotkey(shortcut["key"])

    # Re -load shortcut keys and set up monitoring
    def reload_hotkeys():
        remove_all_hotkeys()
        shortcuts = get_shortcuts()
        for shortcut_id, shortcut_info in shortcuts.items():
            keyboard.add_hotkey(
                shortcut_info["key"],
                lambda action=shortcut_info["action"]: on_triggered(action),
            )

    # Modify the shortcut key configuration and reload the monitoring
    def modify_shortcut(shortcut_id, new_key, new_action):
        config = load_config(config_file_path)
        # Save the old shortcut key value
        old_key = config["shortcuts"].get(shortcut_id, {}).get("key")
        if "shortcuts" not in config:
            config["shortcuts"] = {}
        config["shortcuts"][shortcut_id] = {"key": new_key, "action": new_action}
        save_config(config, config_file_path)
        # If the old shortcut keys exist, remove the old shortcut keys to listen to
        if old_key:
            keyboard.remove_hotkey(old_key)
        # Add new shortcut key monitoring
        try:
            keyboard.add_hotkey(new_key, lambda: on_triggered(new_action))
        except:
            keyboard.add_hotkey(old_key, lambda: on_triggered(new_action))
            Messagebox.show_error("Please check whether the shortcut key input is correct", title="Shortcut key illegal")
            return

        # Update shortcut key display
        update_shortcut_display()

    def switch_status(status):
        if get_intvar_value(status) is True:
            set_intvar_value(status, False)
        elif get_intvar_value(status) is False:
            set_intvar_value(status, True)
        elif get_intvar_value(status) == 1:
            set_intvar_value(status, 0)
        elif get_intvar_value(status) == 0:
            set_intvar_value(status, 1)

    # Capture shortcut keys and output on the console
    def on_triggered(action):
        if action == 0:
            switch_status(pause_pro_status)
            pvz.pausePro(get_intvar_value(pause_pro_status))
        elif action == 1:
            pvz.setSun(get_intvar_value(sun_value))
        elif action == 2:
            sun = get_intvar_value(sun_add_value)
            pvz.addSun(sun)
        elif action == 3:
            switch_status(over_plant_status)
            pvz.overPlant(get_intvar_value(over_plant_status))
        elif action == 4:
            switch_status(free_plant_status)
            pvz.ignoreSun(get_intvar_value(free_plant_status))
        elif action == 5:
            switch_status(cancel_cd_status)
            pvz.cancelCd(get_intvar_value(cancel_cd_status))
        elif action == 6:
            switch_status(auto_colect_status)
            pvz.autoCollect(get_intvar_value(auto_colect_status))
        elif action == 7:
            switch_status(column_like_status)
            pvz.column(get_intvar_value(column_like_status))
        elif action == 8:
            switch_status(shovel_pro_status)
            pvz.shovelpro(get_intvar_value(shovel_pro_status))
        elif action == 9:
            switch_status(never_fail_status)
            pvz.ignoreZombies(get_intvar_value(never_fail_status))
        elif action == 10:
            pvz.win()
        elif action == 11:
            pvz.killAllZombies()
        elif action == 12:
            pvz.unlock()
        elif action == 13:
            putPlants(plantPut_type_combobox.current())
        elif action == 14:
            putLadders()
        elif action == 15:
            clearPlants()
        elif action == 16:
            putZombies(
                zombiePut_type_combobox.current(), get_intvar_value(zombiePut_num)
            )
        elif action == 17:
            pvz.defeat()
        elif action == 18:
            pvz.save()
        elif action == 19:
            pvz.load()
        elif action == 20:
            if get_intvar_value(game_speed_value) < 6:
                set_intvar_value(
                    game_speed_value, (get_intvar_value(game_speed_value) + 1)
                )
                pvz.changeGameSpeed(get_intvar_value(game_speed_value))
        elif action == 21:
            if get_intvar_value(game_speed_value) > 0:
                set_intvar_value(
                    game_speed_value, (get_intvar_value(game_speed_value) - 1)
                )
                pvz.changeGameSpeed(get_intvar_value(game_speed_value))
        elif action == 22:
            switch_status(random_slots_status)
            pvz.randomSlots(
                get_intvar_value(random_slots_status),
                get_intvar_value(random_slots_haszombie_status),
            )

    # Modify the window of the shortcut key

    def open_change_window(shortcut_id, current_key, current_action):
        global main_window
        new_shortcut = []

        def set_new_shortcut():
            if new_shortcut:
                new_key = "+".join(new_shortcut)
                modify_shortcut(shortcut_id, new_key, current_action)
                update_shortcut_display()
                change_shortcut_window.destroy()

        def record_key(event):
            key = event.keysym.lower() if event.keysym != "space" else "space"
            ctrl_pressed = event.state & 0x0004
            if "control" in key:
                key = "ctrl"
            elif "shift" in key:
                key = "shift"
            elif "alt" in key:
                key = "alt"
            elif "win" in key:
                key = "win"
            elif event.char == " " or (ctrl_pressed and key == "??"):
                key = "space"
            if key not in new_shortcut:
                new_shortcut.append(key)
                entry.delete(0, END)
                entry.insert(0, "+".join(new_shortcut))

        change_shortcut_window = ttk.Toplevel(topmost=True)
        change_shortcut_window.title("Modify shortcut keys")
        change_shortcut_window.geometry("200x100")
        change_shortcut_window.iconphoto(
            False, ttk.PhotoImage(file=resource_path(r"res\icon\change.png"))
        )
        change_shortcut_window.tk.call("tk", "scaling", 4 / 3)
        main_window_x = main_window.winfo_x()
        main_window_y = main_window.winfo_y()
        change_shortcut_window.geometry(f"+{main_window_x+200}+{main_window_y + 200}")

        label = ttk.Label(change_shortcut_window, text="Please press the new shortcut key")
        label.pack()

        entry = ttk.Entry(change_shortcut_window)
        entry.pack()
        entry.focus_set()

        # Record buttons
        change_shortcut_window.bind("<Key>", record_key)

        confirm_button = ttk.Button(
            change_shortcut_window,
            text="Sure",
            bootstyle=SUCCESS,
            command=set_new_shortcut,
        )
        confirm_button.place(x=20, y=-10, relx=0, rely=1, anchor=SW)

        cancel_button = ttk.Button(
            change_shortcut_window,
            text="Cancel",
            bootstyle=DANGER,
            command=change_shortcut_window.destroy,
        )
        cancel_button.place(x=-20, y=-10, relx=1, rely=1, anchor=SE)

    # Update shortcut key display
    def update_shortcut_display():
        shortcuts = get_shortcuts()
        for i, (shortcut_id, shortcut_info) in enumerate(shortcuts.items()):
            shortcut_entries[i].delete(0, END)
            shortcut_entries[i].insert(0, shortcut_info["key"])
            shortcut_buttons[i].config(
                command=lambda i=i,
                id=shortcut_id,
                info=shortcut_info: open_change_window(id, info["key"], info["action"])
            )

    shortcut_frame = ttk.LabelFrame(common_page, text="Fast buttons")
    shortcut_frame.place(x=280, y=0)
    # Create a shortcut key to display the text box and modify button
    shortcuts = get_shortcuts()
    for i, (shortcut_id, shortcut_info) in enumerate(shortcuts.items()):
        # Show the text box of shortcut keys
        entry = ttk.Entry(shortcut_frame, width=24, font=("黑体", 8))
        entry.insert(0, shortcut_info["key"])
        entry.grid(row=i, column=0, padx=2)
        shortcut_entries.append(entry)

        # The button to modify the shortcut key
        button = ttk.Button(
            shortcut_frame,
            text="Revise",
            padding=0,
            bootstyle=(OUTLINE),
            command=lambda i=i, id=shortcut_id, info=shortcut_info: open_change_window(
                id, info["key"], info["action"]
            ),
        )
        button.grid(row=i, column=1, padx=2)
        shortcut_buttons.append(button)

        combobox = ttk.Combobox(
            shortcut_frame, values=action_list, width=13, state=READONLY
        )
        combobox.grid(row=i, column=2, padx=2)
        combobox.current(shortcut_info["action"])
        shortcut_comboboxs.append(combobox)

        def modify_action(event, id=shortcut_id, i=i):
            print(id, i, shortcut_comboboxs[i].current())
            config = load_config(config_file_path)
            modify_shortcut(
                id, config["shortcuts"][id]["key"], shortcut_comboboxs[i].current()
            )

        combobox.bind("<<ComboboxSelected>>", modify_action)
    # Set shortcut key monitoring
    try:
        for shortcut_info in shortcuts.values():
            keyboard.add_hotkey(
                shortcut_info["key"],
                lambda action=shortcut_info["action"]: on_triggered(action),
            )
    except:
        delete_config()
    ttk.Label(
        shortcut_frame,
        text="If the shortcut keys cannot be used, try to use the administrator to run the modifier\nIt is still unavailable, please install version 3.12.2 Python and Keyboard libraries",
        font=("Song style", 8),
    ).grid(row=12, column=0, columnspan=3)

    global zombie_select
    zombie_page = ttk.Frame(page_tab)
    zombie_page.pack()
    page_tab.add(zombie_page, text="Zombie modification")
    zombie_list_frame = ttk.LabelFrame(zombie_page, text="Zombie list", bootstyle=DANGER)
    zombie_list_frame.place(x=0, y=0, anchor=NW, height=260, width=275)
    zombie_list_box_scrollbar = ttk.Scrollbar(zombie_list_frame, bootstyle=DANGER)
    zombie_list_box = ttk.Treeview(
        zombie_list_frame,
        show=TREE,
        selectmode=BROWSE,
        padding=0,
        columns=("zombie_list"),
        yscrollcommand=zombie_list_box_scrollbar.set,
        bootstyle=DANGER,
    )
    zombie_list_box_scrollbar.configure(command=zombie_list_box.yview)
    zombie_list_box.place(x=0, y=0, anchor=NW, height=240, width=50)
    zombie_list_box_scrollbar.place(x=45, y=0, height=240, anchor=NW)
    zombie_list = list()

    def refresh_zombie_list():
        zombie_list.clear()
        zombie_list_box.delete(*zombie_list_box.get_children())
        try:
            zombie_num = PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0xA0
            )
        except:
            return
        i = 0
        j = 0
        while i < zombie_num:
            zombie_addresss = (
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                    )
                    + 0x90
                )
                + 0x204 * j
            )
            zombie_exist = PVZ_data.PVZ_memory.read_bytes(zombie_addresss + 0xEC, 1)
            if zombie_exist == b"\x00":
                zombie_list.append(PVZ_data.zombie(zombie_addresss))
                i = i + 1
            j = j + 1
        n = 0
        for k in range(zombie_num):
            zombie_list_box.insert("", END, iid=n, text=str(zombie_list[k].no))
            if zombie_select is not None:
                if zombie_select.exist == 0:
                    if zombie_select.no == zombie_list[k].no:
                        zombie_list_box.selection_set((str(n),))
            n = n + 1

    refresh_zombie_list()
    zombie_attribute_frame = ttk.Frame(zombie_list_frame)
    zombie_attribute_frame.place(x=80, y=0, height=240, width=190)
    zombie_state_frame = ttk.Frame(zombie_attribute_frame)
    zombie_state_frame.grid(row=0, column=0, columnspan=12, sticky=W)
    ttk.Label(zombie_state_frame, text="Zombie type:").grid(
        row=0, column=0, columnspan=2, sticky=W
    )
    zombie_type_value = ttk.IntVar(zombie_state_frame)
    zombie_type_entry = ttk.Entry(
        zombie_state_frame,
        textvariable=zombie_type_value,
        width=18,
        font=("Black body", 8),
        state=READONLY,
        bootstyle=SECONDARY,
    )
    zombie_type_entry.grid(row=0, column=2, columnspan=5, sticky=W)
    ttk.Label(zombie_state_frame, text="state:").grid(row=1, column=0, sticky=W)
    zombie_state_value = ttk.IntVar(zombie_state_frame)
    zombie_state_entry = ttk.Entry(
        zombie_state_frame,
        textvariable=zombie_state_value,
        width=3,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    zombie_state_entry.grid(row=1, column=1, sticky=W)

    def setZombieState(event):
        zombie_select.setState(zombie_state_value.get())
        zombie_state_frame.focus_set()

    zombie_state_entry.bind("<Return>", setZombieState)
    ttk.Label(zombie_state_frame, text="size:").grid(row=1, column=3, sticky=W)
    zombie_size_value = ttk.DoubleVar(zombie_state_frame)
    zombie_size_entry = ttk.Entry(
        zombie_state_frame,
        textvariable=zombie_size_value,
        width=6,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    zombie_size_entry.grid(row=1, column=4, sticky=W)

    def setZombieSize(event):
        zombie_select.setSize(zombie_size_value.get())
        zombie_state_frame.focus_set()

    zombie_size_entry.bind("<Return>", setZombieSize)
    zombie_position_frame = ttk.LabelFrame(
        zombie_attribute_frame, text="Location", bootstyle=DANGER
    )
    zombie_position_frame.grid(row=2, column=0, columnspan=4, sticky=W)
    ttk.Label(zombie_position_frame, text="X coordinate:").grid(
        row=0, column=0, columnspan=3, sticky=W
    )
    zombie_x_value = ttk.DoubleVar(zombie_position_frame)
    zombie_x_entry = ttk.Entry(
        zombie_position_frame,
        textvariable=zombie_x_value,
        width=6,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    zombie_x_entry.grid(row=0, column=3, columnspan=3, sticky=W)

    def setZombieX(event):
        print(zombie_x_value.get())
        zombie_select.setX(zombie_x_value.get())
        zombie_position_frame.focus_set()

    zombie_x_entry.bind("<Return>", setZombieX)
    ttk.Label(zombie_position_frame, text="y coordinate:").grid(
        row=1, column=0, columnspan=3, sticky=W
    )
    zombie_y_value = ttk.DoubleVar(zombie_position_frame)
    zombie_y_entry = ttk.Entry(
        zombie_position_frame,
        textvariable=zombie_y_value,
        width=6,
        font=("Black body", 8),
        bootstyle=SECONDARY,
    )
    zombie_y_entry.grid(row=1, column=3, columnspan=3, sticky=W)

    def setZombieY(event):
        zombie_select.setY(zombie_y_value.get())
        zombie_position_frame.focus_set()

    zombie_y_entry.bind("<Return>", setZombieY)
    ttk.Label(zombie_position_frame, text="First").grid(row=2, column=0, sticky=W)
    zombie_row_value = ttk.IntVar(zombie_position_frame)
    zombie_row_combobox = ttk.Combobox(
        zombie_position_frame,
        textvariable=zombie_row_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6],
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    zombie_row_combobox.grid(row=2, column=1, columnspan=3, sticky=W)
    ttk.Label(zombie_position_frame, text="OK").grid(row=2, column=4, sticky=W)

    def setZombieRow(event):
        zombie_select.setRow(zombie_row_value.get())
        zombie_position_frame.focus_set()

    zombie_row_combobox.bind("<<ComboboxSelected>>", setZombieRow)
    zombie_hp_frame = ttk.LabelFrame(
        zombie_attribute_frame, text="Blood volume", bootstyle=DANGER
    )
    zombie_hp_frame.grid(row=2, column=4, columnspan=8, sticky=W)
    zombie_hp_frame.grid_columnconfigure(0, minsize=50)
    ttk.Label(zombie_hp_frame, text="Body:").grid(row=0, column=0)
    zombie_hp_value = ttk.IntVar(zombie_hp_frame)
    zombie_hp_entry = ttk.Entry(
        zombie_hp_frame,
        textvariable=zombie_hp_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    zombie_hp_entry.grid(row=0, column=1, ipady=0)

    def setZombieHP(event):
        zombie_select.setHP(zombie_hp_value.get())
        zombie_hp_frame.focus_set()

    zombie_hp_entry.bind("<Return>", setZombieHP)
    zombie_hatHP_label = ttk.Label(zombie_hp_frame, text="hat:")
    zombie_hatHP_label.grid(row=1, column=0)
    zombie_hatHP_value = ttk.IntVar(zombie_hp_frame)
    zombie_hatHP_entry = ttk.Entry(
        zombie_hp_frame,
        textvariable=zombie_hatHP_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    zombie_hatHP_entry.grid(row=1, column=1, ipady=0)

    def setZombieHatHP(event):
        zombie_select.setHatHP(zombie_hatHP_value.get())
        zombie_hp_frame.focus_set()

    zombie_hatHP_entry.bind("<Return>", setZombieHatHP)
    ttk.Label(zombie_hp_frame, text="iron gate:").grid(row=2, column=0, padx=(2, 0))
    zombie_doorHP_value = ttk.IntVar(zombie_hp_frame)
    zombie_doorHP_entry = ttk.Entry(
        zombie_hp_frame,
        textvariable=zombie_doorHP_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    zombie_doorHP_entry.grid(row=2, column=1, ipady=0)

    def setZombieDoorHP(event):
        zombie_select.setDoorHP(zombie_doorHP_value.get())
        zombie_hp_frame.focus_set()

    zombie_doorHP_entry.bind("<Return>", setZombieDoorHP)
    zombie_control_frame = ttk.LabelFrame(
        zombie_attribute_frame, text="Control time", bootstyle=DANGER
    )
    zombie_control_frame.grid(row=3, column=0, columnspan=3, sticky=W)
    ttk.Label(zombie_control_frame, text="减速:").grid(row=0, column=0)
    zombie_slow_value = ttk.IntVar(zombie_control_frame)
    zombie_slow_entry = ttk.Entry(
        zombie_control_frame,
        textvariable=zombie_slow_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    zombie_slow_entry.grid(row=0, column=1, ipady=0)

    def setZombieSlow(event):
        zombie_select.setSlow(zombie_slow_value.get())
        zombie_control_frame.focus_set()

    zombie_slow_entry.bind("<Return>", setZombieSlow)
    zombie_butter_label = ttk.Label(zombie_control_frame, text="butter:")
    zombie_butter_label.grid(row=1, column=0)
    zombie_butter_value = ttk.IntVar(zombie_control_frame)
    zombie_butter_entry = ttk.Entry(
        zombie_control_frame,
        textvariable=zombie_butter_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    zombie_butter_entry.grid(row=1, column=1, ipady=0)

    def setZombieButter(event):
        zombie_select.setButter(zombie_butter_value.get())
        zombie_control_frame.focus_set()

    zombie_butter_entry.bind("<Return>", setZombieButter)
    ttk.Label(zombie_control_frame, text="freeze:").grid(row=2, column=0, padx=(2, 0))
    zombie_frozen_value = ttk.IntVar(zombie_control_frame)
    zombie_frozen_entry = ttk.Entry(
        zombie_control_frame,
        textvariable=zombie_frozen_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    zombie_frozen_entry.grid(row=2, column=1, ipady=0)

    def setZombieFrozen(event):
        zombie_select.setFrozen(zombie_frozen_value.get())
        zombie_control_frame.focus_set()

    zombie_frozen_entry.bind("<Return>", setZombieFrozen)
    zombie_flag_frame = ttk.LabelFrame(
        zombie_attribute_frame, text="Status signs", bootstyle=DANGER
    )
    zombie_flag_frame.grid(row=3, column=3, columnspan=8, sticky=W)
    zombie_exist_flag = ttk.BooleanVar(zombie_flag_frame)

    def change_zombie_exist():
        if zombie_exist_flag.get() is False:
            zombie_select.setExist(2)

    ttk.Checkbutton(
        zombie_flag_frame,
        text="存在",
        bootstyle="danger-round-toggle",
        variable=zombie_exist_flag,
        command=lambda: change_zombie_exist(),
    ).grid(row=0, column=0)
    zombie_isVisible_flag = ttk.BooleanVar(zombie_flag_frame)

    def change_zombie_isVisible():
        zombie_select.setIsVisible(not zombie_isVisible_flag.get())

    ttk.Checkbutton(
        zombie_flag_frame,
        text="Invisible",
        bootstyle="danger-round-toggle",
        variable=zombie_isVisible_flag,
        command=lambda: change_zombie_isVisible(),
    ).grid(row=0, column=1)
    zombie_isEating_flag = ttk.BooleanVar(zombie_flag_frame)

    def change_zombie_isEating():
        zombie_select.setIsEating(zombie_isEating_flag.get())

    ttk.Checkbutton(
        zombie_flag_frame,
        text="Bite",
        bootstyle="danger-round-toggle",
        variable=zombie_isEating_flag,
        command=lambda: change_zombie_isEating(),
    ).grid(row=1, column=0)
    zombie_isHpynotized_flag = ttk.BooleanVar(zombie_flag_frame)

    def change_zombie_isHpynotized():
        zombie_select.setIsHPynotized(zombie_isHpynotized_flag.get())

    ttk.Checkbutton(
        zombie_flag_frame,
        text="Charm",
        bootstyle="danger-round-toggle",
        variable=zombie_isHpynotized_flag,
        command=lambda: change_zombie_isHpynotized(),
    ).grid(row=1, column=1)
    zombie_isBlow_flag = ttk.BooleanVar(zombie_flag_frame)

    def change_zombie_isBlow():
        zombie_select.setIsBlow(zombie_isBlow_flag.get())

    ttk.Checkbutton(
        zombie_flag_frame,
        text="Blew",
        bootstyle="danger-round-toggle",
        variable=zombie_isBlow_flag,
        command=lambda: change_zombie_isBlow(),
    ).grid(row=2, column=0)
    zombie_isDying_flag = ttk.BooleanVar(zombie_flag_frame)

    def change_zombie_isDying():
        zombie_select.setIsDying(not zombie_isDying_flag.get())

    ttk.Checkbutton(
        zombie_flag_frame,
        text="Dying",
        bootstyle="danger-round-toggle",
        variable=zombie_isDying_flag,
        command=lambda: change_zombie_isDying(),
    ).grid(row=2, column=1)

    zombie_put_frame = ttk.LabelFrame(zombie_page, text="Zombies", bootstyle=DANGER)
    zombie_put_frame.place(x=280, y=0, anchor=NW, height=120, width=130)
    ttk.Label(zombie_put_frame, text="第").grid(row=0, column=0)
    zombiePut_start_row_value = ttk.IntVar(zombie_put_frame)
    zombiePut_start_row_combobox = ttk.Combobox(
        zombie_put_frame,
        textvariable=zombiePut_start_row_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6],
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    zombiePut_start_row_combobox.grid(row=0, column=1)
    zombiePut_start_row_value.set(1)
    ttk.Label(zombie_put_frame, text="OK").grid(row=0, column=2)
    zombiePut_start_col_value = ttk.IntVar(zombie_put_frame)
    zombiePut_start_col_combobox = ttk.Combobox(
        zombie_put_frame,
        textvariable=zombiePut_start_col_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    zombiePut_start_col_combobox.grid(row=0, column=3)
    zombiePut_start_col_value.set(1)
    ttk.Label(zombie_put_frame, text="List").grid(row=0, column=4)
    ttk.Label(zombie_put_frame, text="to").grid(row=1, column=0)
    zombiePut_end_row_value = ttk.IntVar(zombie_put_frame)
    zombiePut_end_row_combobox = ttk.Combobox(
        zombie_put_frame,
        textvariable=zombiePut_end_row_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6],
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    zombiePut_end_row_combobox.grid(row=1, column=1)
    zombiePut_end_row_value.set(1)
    ttk.Label(zombie_put_frame, text="OK").grid(row=1, column=2)
    zombiePut_end_col_value = ttk.IntVar(zombie_put_frame)
    zombiePut_end_col_combobox = ttk.Combobox(
        zombie_put_frame,
        textvariable=zombiePut_end_col_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    zombiePut_end_col_combobox.grid(row=1, column=3)
    zombiePut_end_col_value.set(1)
    ttk.Label(zombie_put_frame, text="List").grid(row=1, column=4)
    zombiePut_type_combobox = ttk.Combobox(
        zombie_put_frame,
        width=15,
        values=PVZ_data.zombiesType,
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    zombiePut_type_combobox.grid(row=2, column=0, columnspan=4, sticky=W)
    zombiePut_type_combobox.current(0)
    zombiePut_type_combobox.bind(
        "<Button-1>", lambda event: open_zombie_select_window(zombiePut_type_combobox)
    )
    zombiePut_num = ttk.IntVar(zombie_put_frame)
    zombiePut_num_entry = ttk.Entry(
        zombie_put_frame, textvariable=zombiePut_num, font=("黑体", 8), width=7
    )
    zombiePut_num_entry.grid(row=3, column=0, columnspan=2, sticky=W)
    ttk.Label(zombie_put_frame, text="Only").grid(row=3, column=2)
    zombiePut_num.set(1)

    def putZombies(type, num):
        for _ in range(0, num):
            startRow = zombiePut_start_row_value.get() - 1
            startCol = zombiePut_start_col_value.get() - 1
            endRow = zombiePut_end_row_value.get() - 1
            endCol = zombiePut_end_col_value.get() - 1
            if type == 25:
                pvz.putBoss()
                print(type)
            else:
                print(startRow, startCol, endRow, endCol, type)
                if pvz.getMap is not False:
                    rows = pvz.getMap() - 1
                    if startRow > rows:
                        startRow = rows
                    if endRow > rows:
                        endRow = rows
                    if startRow > endRow or startCol > endCol:
                        Messagebox.show_error("The starting ranks are greater than the termination ranks", title="Enter an error")
                    else:
                        for i in range(startRow, endRow + 1):
                            for j in range(startCol, endCol + 1):
                                pvz.putZombie(i, j, type)

    ttk.Button(
        zombie_put_frame,
        text="Zombies",
        padding=0,
        bootstyle=(OUTLINE, DANGER),
        command=lambda: putZombies(
            zombiePut_type_combobox.current(), zombiePut_num.get()
        ),
    ).grid(row=3, column=0, columnspan=5, sticky=E)

    zombie_seed_frame = ttk.LabelFrame(zombie_page, text="Modify the strange", bootstyle=DANGER)
    zombie_seed_frame.place(x=280, y=130, anchor=NW, height=100, width=130)
    pausee_spawn_status = ttk.BooleanVar(zombie_seed_frame)
    pausee_spawn_check = ttk.Checkbutton(
        zombie_seed_frame,
        text="Parking the monster",
        variable=pausee_spawn_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.pauseSpawn(pausee_spawn_status.get()),
    )
    pausee_spawn_check.grid(row=0, column=0, sticky=W)

    # zombie_characteristic_frame=ttk.Labelframe(zombie_page,text="Basic attribute",bootstyle=DANGER)
    # zombie_characteristic_frame.place(x=280,y=210,anchor=NW,height=200,width=150)

    zombie_spoils_frame = ttk.LabelFrame(zombie_page, text="Kill", bootstyle=DANGER)
    zombie_spoils_frame.place(x=0, y=260, anchor=NW, height=200, width=275)
    spoil_1_percent = ttk.IntVar(zombie_spoils_frame)
    spoil_1_percent_spinbox = ttk.Spinbox(
        zombie_spoils_frame, from_=0, to=100, width=3, textvariable=spoil_1_percent
    )
    spoil_1_percent_spinbox.grid(row=1, column=0)
    ttk.Label(zombie_spoils_frame, text="%").grid(row=1, column=1)
    spoil_1_combobox = ttk.Combobox(
        zombie_spoils_frame,
        width=8,
        values=[
            "none",
            "silver",
            "gold",
            "diamond",
            "Sunshine",
            "Xiaoyuki",
            "Large sunshine",
            "Cup",
            "Note",
            "Plant card",
            "Submarine",
        ],
        state=READONLY,
    )
    spoil_1_combobox.grid(row=1, column=2)
    spoil_1_combobox.current(0)
    spoil_1_card = ttk.Combobox(
        zombie_spoils_frame, width=12, values=PVZ_data.plantsType
    )
    spoil_1_card.insert(0, "Chosen plant")
    spoil_1_card.configure(state=DISABLED)
    spoil_1_card.grid(row=1, column=3)
    spoil_1_card.bind("<Button-1>", lambda event: open_card_select_window(spoil_1_card))

    def setCard1(event):
        if spoil_1_combobox.current() == 9:
            spoil_1_card.configure(state=READONLY)
        else:
            spoil_1_card.configure(state=DISABLED)

    spoil_1_combobox.bind("<<ComboboxSelected>>", setCard1)
    spoil_2_percent = ttk.IntVar(zombie_spoils_frame)
    spoil_2_percent_spinbox = ttk.Spinbox(
        zombie_spoils_frame, from_=0, to=100, width=3, textvariable=spoil_2_percent
    )
    spoil_2_percent_spinbox.grid(row=2, column=0)
    ttk.Label(zombie_spoils_frame, text="%").grid(row=2, column=1)
    spoil_2_combobox = ttk.Combobox(
        zombie_spoils_frame,
        width=8,
        values=[
            "none",
            "silver",
            "gold",
            "diamond",
            "Sunshine",
            "Xiaoyuki",
            "Large sunshine",
            "Cup",
            "Note",
            "Plant card",
            "Submarine",
        ],
        state=READONLY,
    )
    spoil_2_combobox.grid(row=2, column=2)
    spoil_2_combobox.current(0)
    spoil_2_card = ttk.Combobox(
        zombie_spoils_frame, width=12, values=PVZ_data.plantsType
    )
    spoil_2_card.insert(0, "Chosen plant")
    spoil_2_card.configure(state=DISABLED)
    spoil_2_card.grid(row=2, column=3)
    spoil_2_card.bind("<Button-1>", lambda event: open_card_select_window(spoil_2_card))

    def setCard2(event):
        if spoil_2_combobox.current() == 9:
            spoil_2_card.configure(state=READONLY)
        else:
            spoil_2_card.configure(state=DISABLED)

    spoil_2_combobox.bind("<<ComboboxSelected>>", setCard2)
    spoil_3_percent = ttk.IntVar(zombie_spoils_frame)
    spoil_3_percent_spinbox = ttk.Spinbox(
        zombie_spoils_frame, from_=0, to=100, width=3, textvariable=spoil_3_percent
    )
    spoil_3_percent_spinbox.grid(row=3, column=0)
    ttk.Label(zombie_spoils_frame, text="%").grid(row=3, column=1)
    spoil_3_combobox = ttk.Combobox(
        zombie_spoils_frame,
        width=8,
        values=[
            "none",
            "silver",
            "gold",
            "diamond",
            "Sunshine",
            "Xiaoyuki",
            "Large sunshine",
            "Cup",
            "Note",
            "Plant card",
            "Submarine",
        ],
        state=READONLY,
    )
    spoil_3_combobox.grid(row=3, column=2)
    spoil_3_combobox.current(0)
    spoil_3_card = ttk.Combobox(
        zombie_spoils_frame, width=12, values=PVZ_data.plantsType
    )
    spoil_3_card.insert(0, "选择植物")
    spoil_3_card.configure(state=DISABLED)
    spoil_3_card.grid(row=3, column=3)
    spoil_3_card.bind("<Button-1>", lambda event: open_card_select_window(spoil_3_card))

    def setCard3(event):
        if spoil_3_combobox.current() == 9:
            spoil_3_card.configure(state=READONLY)
        else:
            spoil_3_card.configure(state=DISABLED)

    spoil_3_combobox.bind("<<ComboboxSelected>>", setCard3)
    spoil_4_percent = ttk.IntVar(zombie_spoils_frame)
    spoil_4_percent_spinbox = ttk.Spinbox(
        zombie_spoils_frame, from_=0, to=100, width=3, textvariable=spoil_4_percent
    )
    spoil_4_percent_spinbox.grid(row=4, column=0)
    ttk.Label(zombie_spoils_frame, text="%").grid(row=4, column=1)
    spoil_4_combobox = ttk.Combobox(
        zombie_spoils_frame,
        width=8,
        values=[
            "none",
            "silver",
            "gold",
            "diamond",
            "Sunshine",
            "Xiaoyuki",
            "Large sunshine",
            "Cup",
            "Note",
            "Plant card",
            "Submarine",
        ],
        state=READONLY,
    )
    spoil_4_combobox.grid(row=4, column=2)
    spoil_4_combobox.current(0)
    spoil_4_card = ttk.Combobox(
        zombie_spoils_frame, width=12, values=PVZ_data.plantsType
    )
    spoil_4_card.insert(0, "Chosen plant")
    spoil_4_card.configure(state=DISABLED)
    spoil_4_card.grid(row=4, column=3)
    spoil_4_card.bind("<Button-1>", lambda event: open_card_select_window(spoil_4_card))

    def setCard4(event):
        if spoil_4_combobox.current() == 9:
            spoil_4_card.configure(state=READONLY)
        else:
            spoil_4_card.configure(state=DISABLED)

    spoil_4_combobox.bind("<<ComboboxSelected>>", setCard4)
    spoils_card_frame = ttk.Frame(zombie_spoils_frame)
    spoils_card_frame.grid(row=5, column=0)

    def load_spoils_config():
        config = load_config(config_file_path)
        try:
            spoil_1_percent.set(config["spoils"]["spoil1"]["percent"])
        except:
            pass
        try:
            spoil_1_combobox.current(config["spoils"]["spoil1"]["type"])
        except:
            pass
        try:
            spoil_1_card.current(config["spoils"]["spoil1"]["card"])
        except:
            pass
        try:
            spoil_2_percent.set(config["spoils"]["spoil2"]["percent"])
        except:
            pass
        try:
            spoil_2_combobox.current(config["spoils"]["spoil2"]["type"])
        except:
            pass
        try:
            spoil_2_card.current(config["spoils"]["spoil2"]["card"])
        except:
            pass
        try:
            spoil_3_percent.set(config["spoils"]["spoil3"]["percent"])
        except:
            pass
        try:
            spoil_3_combobox.current(config["spoils"]["spoil3"]["type"])
        except:
            pass
        try:
            spoil_3_card.current(config["spoils"]["spoil3"]["card"])
        except:
            pass
        try:
            spoil_4_percent.set(config["spoils"]["spoil4"]["percent"])
        except:
            pass
        try:
            spoil_4_combobox.current(config["spoils"]["spoil4"]["type"])
        except:
            pass
        try:
            spoil_4_card.current(config["spoils"]["spoil4"]["card"])
        except:
            pass

    load_spoils_config()

    def setSpoils():
        if zombie_spoils_status.get():
            config = load_config(config_file_path)
            if "spoils" not in config:
                config["spoils"] = {}
            spoils_config = list()
            if "spoil1" not in config["spoils"]:
                config["spoils"]["spoil1"] = {}
            config["spoils"]["spoil1"]["percent"] = spoil_1_percent.get()
            config["spoils"]["spoil1"]["type"] = spoil_1_combobox.current()
            config["spoils"]["spoil1"]["card"] = spoil_1_card.current()
            if spoil_1_percent.get() != 0 and spoil_1_combobox.current() != 0:
                spoils_config.append(config["spoils"]["spoil1"])
            if "spoil2" not in config["spoils"]:
                config["spoils"]["spoil2"] = {}
            config["spoils"]["spoil2"]["percent"] = spoil_2_percent.get()
            config["spoils"]["spoil2"]["type"] = spoil_2_combobox.current()
            config["spoils"]["spoil2"]["card"] = spoil_2_card.current()
            if spoil_2_percent.get() != 0 and spoil_2_combobox.current() != 0:
                spoils_config.append(config["spoils"]["spoil2"])
            if "spoil3" not in config["spoils"]:
                config["spoils"]["spoil3"] = {}
            config["spoils"]["spoil3"]["percent"] = spoil_3_percent.get()
            config["spoils"]["spoil3"]["type"] = spoil_3_combobox.current()
            config["spoils"]["spoil3"]["card"] = spoil_3_card.current()
            if spoil_3_percent.get() != 0 and spoil_3_combobox.current() != 0:
                spoils_config.append(config["spoils"]["spoil3"])
            if "spoil4" not in config["spoils"]:
                config["spoils"]["spoil4"] = {}
            config["spoils"]["spoil4"]["percent"] = spoil_4_percent.get()
            config["spoils"]["spoil4"]["type"] = spoil_4_combobox.current()
            config["spoils"]["spoil4"]["card"] = spoil_4_card.current()
            if spoil_4_percent.get() != 0 and spoil_4_combobox.current() != 0:
                spoils_config.append(config["spoils"]["spoil4"])
            save_config(config, config_file_path)
            pvz.spoils(spoils_config)
        else:
            pvz.spoils(False)

    zombie_spoils_status = ttk.BooleanVar(zombie_spoils_frame)
    zombie_spoils_check = ttk.Checkbutton(
        zombie_spoils_frame,
        text="Open",
        variable=zombie_spoils_status,
        bootstyle="success-round-toggle",
        command=lambda: setSpoils(),
    )
    zombie_spoils_check.grid(row=5, column=0, columnspan=4, sticky=W)
    # ttk.Label(zombie_spoils_frame,text="卡片").grid(row=5,column=0)
    # spoil_card_combobox=ttk.Combobox(zombie_spoils_frame,width=8,values=data.plantsType,state=READONLY)
    # spoil_card_combobox.grid(row=5,column=1)
    # def setSpoilCard(event):
    #     data.PVZ_memory.write_int(0x0042FFB9,spoil_card_combobox.current())
    # spoil_card_combobox.bind("<<ComboboxSelected>>",setSpoilCard)

    def open_zombie_hp_window():
        zombie_hp_window = ttk.Toplevel()
        zombie_hp_window.title("Modify zombie blood volume")
        main_window_x = main_window.winfo_x()
        main_window_y = main_window.winfo_y()
        zombie_hp_window.geometry(f"+{main_window_x+50}+{main_window_y+50}")
        zombie_hp_values = {}
        row = None
        for i, (zombie_name, address) in enumerate(
            PVZ_data.zombies_HP_addresses.items()
        ):
            if i % 4 == 0:  # Every four data start a new line
                row = ttk.Frame(zombie_hp_window)
                row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            label = ttk.Label(row, text=zombie_name, width=15, anchor=E)
            value = ttk.IntVar(row)
            entry = ttk.Entry(row, textvariable=value, width=8)
            value.set(PVZ_data.PVZ_memory.read_int(address))  # Assume that reading the blood volume function
            label.pack(side=LEFT, anchor=E)
            entry.pack(side=LEFT, expand=YES, fill=X)
            zombie_hp_values[zombie_name] = value
        confirm_button = ttk.Button(
            zombie_hp_window, text="Confirm the modification", command=lambda: confirm_changes()
        )
        confirm_button.pack(side=BOTTOM, fill=X)

        def confirm_changes():
            for zombie_name, value in zombie_hp_values.items():
                new_hp = value.get()
                address = PVZ_data.zombies_HP_addresses[zombie_name]
                PVZ_data.PVZ_memory.write_int(address, new_hp)  # Assuming the blood volume function
            print("The blood volume of all zombies and accessories has been updated.")
            zombie_hp_window.destroy()

    zombie_HP_button = ttk.Button(
        zombie_page,
        text="Blood modification",
        bootstyle=DANGER,
        command=lambda: open_zombie_hp_window(),
    )
    zombie_HP_button.place(x=0, y=500, anchor=NW)

    def get_zombie_select(event):
        global zombie_select
        try:
            index = int(zombie_list_box.selection()[0])
            zombie_select = zombie_list[index]
        except:
            return

    def get_zombie_attribute():
        global zombie_select
        if zombie_select is not None:
            try:
                zombie_type_value.set(
                    str(zombie_select.type)
                    + ":"
                    + PVZ_data.zombiesType[zombie_select.type]
                )
                if zombie_attribute_frame.focus_get() != zombie_state_entry:
                    zombie_state_value.set(zombie_select.state)
                if zombie_attribute_frame.focus_get() != zombie_size_entry:
                    zombie_size_value.set(zombie_select.size)
                if zombie_attribute_frame.focus_get() != zombie_x_entry:
                    zombie_x_value.set(round(zombie_select.x, 2))
                if zombie_attribute_frame.focus_get() != zombie_y_entry:
                    zombie_y_value.set(round(zombie_select.y, 2))
                zombie_row_value.set(zombie_select.row)
                if zombie_attribute_frame.focus_get() != zombie_hp_entry:
                    zombie_hp_value.set(zombie_select.hp)
                if zombie_select.hatType == 0:
                    zombie_hatHP_label["text"] = "none:"
                elif zombie_select.hatType == 1:
                    zombie_hatHP_label["text"] = "Roadblock:"
                elif zombie_select.hatType == 2:
                    zombie_hatHP_label["text"] = "drum:"
                elif zombie_select.hatType == 3:
                    zombie_hatHP_label["text"] = "black olives:"
                elif zombie_select.hatType == 4:
                    zombie_hatHP_label["text"] = "Miner hat:"
                elif zombie_select.hatType == 7:
                    zombie_hatHP_label["text"] = "Sled car:"
                elif zombie_select.hatType == 8:
                    zombie_hatHP_label["text"] = "nut:"
                elif zombie_select.hatType == 9:
                    zombie_hatHP_label["text"] = "Gao Bingguo:"
                elif zombie_select.hatType == 10:
                    zombie_hatHP_label["text"] = "Steel helmet:"
                elif zombie_select.hatType == 11:
                    zombie_hatHP_label["text"] = "Green hat:"
                elif zombie_select.hatType == 12:
                    zombie_hatHP_label["text"] = "Sleeping cap:"
                elif zombie_select.hatType == 18:
                    zombie_hatHP_label["text"] = "Red olive:"
                elif zombie_select.hatType == 19:
                    zombie_hatHP_label["text"] = "Red olive:"
                elif zombie_select.hatType == 20:
                    zombie_hatHP_label["text"] = "Nut:"
                elif zombie_select.hatType == 21:
                    zombie_hatHP_label["text"] = "Gao Bingguo:"
                else:
                    zombie_hatHP_label["text"] = str(zombie_select.hatType) + "unknown:"
                if zombie_attribute_frame.focus_get() != zombie_hatHP_entry:
                    zombie_hatHP_value.set(zombie_select.hatHP)
                if zombie_attribute_frame.focus_get() != zombie_doorHP_entry:
                    zombie_doorHP_value.set(zombie_select.doorHP)
                if zombie_attribute_frame.focus_get() != zombie_slow_entry:
                    zombie_slow_value.set(zombie_select.slow)
                if zombie_attribute_frame.focus_get() != zombie_butter_entry:
                    zombie_butter_value.set(zombie_select.butter)
                if zombie_attribute_frame.focus_get() != zombie_frozen_entry:
                    zombie_frozen_value.set(zombie_select.frozen)
                if zombie_select.exist == 0:
                    zombie_exist_flag.set(True)
                else:
                    zombie_exist_flag.set(False)
            except:
                pass
            zombie_isVisible_flag.set(not zombie_select.isVisible)
            zombie_isEating_flag.set(zombie_select.isEating)
            zombie_isHpynotized_flag.set(zombie_select.isHpynotized)
            zombie_isBlow_flag.set(zombie_select.isBlow)
            zombie_isDying_flag.set(not zombie_select.isDying)

    zombie_list_box.bind("<<TreeviewSelect>>", get_zombie_select)

    plant_page = ttk.Frame(page_tab)
    plant_page.pack()
    page_tab.add(plant_page, text="Plant modification")
    plant_list_frame = ttk.LabelFrame(plant_page, text="Botanical list", bootstyle=SUCCESS)
    plant_list_frame.place(x=0, y=0, anchor=NW, height=390, width=235)
    plant_list_box_scrollbar = ttk.Scrollbar(plant_list_frame, bootstyle=SUCCESS)
    plant_list_box = ttk.Treeview(
        plant_list_frame,
        show=TREE,
        selectmode=BROWSE,
        padding=0,
        columns=("plant_list"),
        yscrollcommand=plant_list_box_scrollbar.set,
        bootstyle=SUCCESS,
    )
    plant_list_box_scrollbar.configure(command=plant_list_box.yview)
    plant_list_box.place(x=0, y=0, anchor=NW, height=370, width=50)
    plant_list_box_scrollbar.place(x=45, y=0, height=370, anchor=NW)
    plant_list = list()

    def refresh_plant_list():
        plant_list.clear()
        plant_list_box.delete(*plant_list_box.get_children())
        try:
            plant_num = PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0xBC
            )
        except:
            return
        i = 0
        j = 0
        while i < plant_num:
            plant_addresss = (
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                    )
                    + 0xAC
                )
                + 0x204 * j
            )
            plant_exist = PVZ_data.PVZ_memory.read_bytes(plant_addresss + 0x141, 1)
            if plant_exist == b"\x00":
                plant_list.append(PVZ_data.plant(plant_addresss))
                i = i + 1
            j = j + 1
        n = 0
        for k in range(plant_num):
            plant_list_box.insert("", END, iid=n, text=str(plant_list[k].no))
            if plant_select is not None:
                if plant_select.exist == 0:
                    if plant_select.no == plant_list[k].no:
                        plant_list_box.selection_set((str(n),))
            n = n + 1

    refresh_plant_list()
    plant_attribute_frame = ttk.Frame(plant_list_frame)
    plant_attribute_frame.place(x=80, y=0, height=370, width=150)
    plant_state_frame = ttk.Frame(plant_attribute_frame)
    plant_state_frame.grid(row=0, column=0, columnspan=12, sticky=W)
    ttk.Label(plant_state_frame, text="Plant:").grid(
        row=0, column=0, columnspan=2, sticky=W
    )
    plant_type_value = ttk.IntVar(plant_state_frame)
    plant_type_entry = ttk.Entry(
        plant_state_frame,
        textvariable=plant_type_value,
        width=12,
        font=("黑体", 8),
        state=READONLY,
        bootstyle=SECONDARY,
    )
    plant_type_entry.grid(row=0, column=2, columnspan=5, sticky=W)
    ttk.Label(plant_state_frame, text="state:").grid(row=1, column=0, sticky=W)
    plant_state_value = ttk.IntVar(plant_state_frame)
    plant_state_entry = ttk.Entry(
        plant_state_frame,
        textvariable=plant_state_value,
        width=3,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    plant_state_entry.grid(row=1, column=1, sticky=W)

    def setPlantState(event):
        plant_select.setState(plant_state_value.get())
        plant_state_frame.focus_set()

    plant_state_entry.bind("<Return>", setPlantState)
    plant_position_frame = ttk.LabelFrame(
        plant_attribute_frame, text="Location", bootstyle=SUCCESS
    )
    plant_position_frame.grid(row=2, column=0, columnspan=4, sticky=W)
    ttk.Label(plant_position_frame, text="X coordinate:").grid(
        row=0, column=0, columnspan=3, sticky=W
    )
    plant_x_value = ttk.IntVar(plant_position_frame)
    plant_x_entry = ttk.Entry(
        plant_position_frame,
        textvariable=plant_x_value,
        width=6,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    plant_x_entry.grid(row=0, column=3, columnspan=3, sticky=W)

    def setPlantX(event):
        print(plant_x_value.get())
        plant_select.setX(plant_x_value.get())
        plant_position_frame.focus_set()

    plant_x_entry.bind("<Return>", setPlantX)
    ttk.Label(plant_position_frame, text="y coordinate:").grid(
        row=1, column=0, columnspan=3, sticky=W
    )
    plant_y_value = ttk.IntVar(plant_position_frame)
    plant_y_entry = ttk.Entry(
        plant_position_frame,
        textvariable=plant_y_value,
        width=6,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    plant_y_entry.grid(row=1, column=3, columnspan=3, sticky=W)

    def setPlantY(event):
        plant_select.setY(plant_y_value.get())
        plant_position_frame.focus_set()

    plant_y_entry.bind("<Return>", setPlantY)
    plant_row_value = ttk.IntVar(plant_position_frame)
    plant_row_combobox = ttk.Combobox(
        plant_position_frame,
        textvariable=plant_row_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6],
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    plant_row_combobox.grid(row=2, column=1, columnspan=3, sticky=W)
    ttk.Label(plant_position_frame, text="OK").grid(row=2, column=4, sticky=W)

    def setPlantRow(event):
        plant_select.setRow(plant_row_value.get())
        plant_position_frame.focus_set()

    plant_row_combobox.bind("<<ComboboxSelected>>", setPlantRow)
    plant_col_value = ttk.IntVar(plant_position_frame)
    plant_col_combobox = ttk.Combobox(
        plant_position_frame,
        textvariable=plant_col_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    plant_col_combobox.grid(row=2, column=5, columnspan=3, sticky=W)
    ttk.Label(plant_position_frame, text="List").grid(row=2, column=8, sticky=W)

    def setPlantCol(event):
        plant_select.setCol(plant_col_value.get())
        plant_position_frame.focus_set()

    plant_col_combobox.bind("<<ComboboxSelected>>", setPlantCol)
    ttk.Label(plant_state_frame, text="血量:").grid(row=1, column=3)
    plant_hp_value = ttk.IntVar(plant_state_frame)
    plant_hp_entry = ttk.Entry(
        plant_state_frame,
        textvariable=plant_hp_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    plant_hp_entry.grid(row=1, column=4, ipady=0)

    def setPlantHP(event):
        plant_select.setHP(plant_hp_value.get())
        plant_state_frame.focus_set()

    plant_hp_entry.bind("<Return>", setPlantHP)
    plant_time_frame = ttk.LabelFrame(
        plant_attribute_frame, text="Countdown", bootstyle=SUCCESS
    )
    plant_time_frame.grid(row=3, column=0, columnspan=3, sticky=W)
    plant_dietime_label = ttk.Label(plant_time_frame, text="die:")
    plant_dietime_label.grid(row=0, column=0)
    ToolTip(
        plant_dietime_label,
        text="Part of the countdown of plant death",
        bootstyle=(INFO, INVERSE),
    )
    plant_dietime_value = ttk.IntVar(plant_time_frame)
    plant_dietime_entry = ttk.Entry(
        plant_time_frame,
        textvariable=plant_dietime_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    plant_dietime_entry.grid(row=0, column=1, ipady=0)

    def setPlantDieTime(event):
        plant_select.setDieTime(plant_dietime_value.get())
        plant_time_frame.focus_set()

    plant_dietime_entry.bind("<Return>", setPlantDieTime)
    plant_cindertime_label = ttk.Label(plant_time_frame, text="ash:")
    plant_cindertime_label.grid(row=1, column=0)
    ToolTip(
        plant_cindertime_label,
        text="Part of the ashes take effect, the female disappearing countdown",
        bootstyle=(INFO, INVERSE),
    )
    plant_cindertime_value = ttk.IntVar(plant_time_frame)
    plant_cindertime_entry = ttk.Entry(
        plant_time_frame,
        textvariable=plant_cindertime_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    plant_cindertime_entry.grid(row=1, column=1, ipady=0)

    def setPlantCinderTime(event):
        plant_select.setCinderTime(plant_cindertime_value.get())
        plant_time_frame.focus_set()

    plant_cindertime_entry.bind("<Return>", setPlantCinderTime)
    plant_effecttime_label = ttk.Label(plant_time_frame, text="效果:")
    plant_effecttime_label.grid(row=2, column=0, padx=(2, 0))
    ToolTip(
        plant_effecttime_label,
        text="Some plants become larger and produce countless results",
        bootstyle=(INFO, INVERSE),
    )
    plant_effecttime_value = ttk.IntVar(plant_time_frame)
    plant_effecttime_entry = ttk.Entry(
        plant_time_frame,
        textvariable=plant_effecttime_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    plant_effecttime_entry.grid(row=2, column=1, ipady=0)

    def setPlantEffectTime(event):
        plant_select.setEffectTime(plant_effecttime_value.get())
        plant_time_frame.focus_set()

    plant_effecttime_entry.bind("<Return>", setPlantEffectTime)
    plant_producttime_label = ttk.Label(plant_time_frame, text="attack:")
    plant_producttime_label.grid(row=3, column=0, padx=(2, 0))
    ToolTip(
        plant_producttime_label, text="Some plants attack countdown", bootstyle=(INFO, INVERSE)
    )
    plant_producttime_value = ttk.IntVar(plant_time_frame)
    plant_producttime_entry = ttk.Entry(
        plant_time_frame,
        textvariable=plant_producttime_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    plant_producttime_entry.grid(row=3, column=1, ipady=0)

    def setPlantProductTime(event):
        plant_select.setProductTime(plant_producttime_value.get())
        plant_time_frame.focus_set()

    plant_producttime_entry.bind("<Return>", setPlantProductTime)
    plant_productinterval_label = ttk.Label(plant_time_frame, text="interval:")
    plant_productinterval_label.grid(row=4, column=0, padx=(2, 0))
    ToolTip(
        plant_productinterval_label, text="The above plant attack interval", bootstyle=(INFO, INVERSE)
    )
    plant_productinterval_value = ttk.IntVar(plant_time_frame)
    plant_productinterval_entry = ttk.Entry(
        plant_time_frame,
        textvariable=plant_productinterval_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    plant_productinterval_entry.grid(row=4, column=1, ipady=0)

    def setPlantProductInterval(event):
        plant_select.setProductInterval(plant_productinterval_value.get())
        plant_time_frame.focus_set()

    plant_productinterval_entry.bind("<Return>", setPlantProductInterval)
    plant_attacktime_label = ttk.Label(plant_time_frame, text="shooting:")
    plant_attacktime_label.grid(row=5, column=0, padx=(2, 0))
    ToolTip(
        plant_attacktime_label, text="Some plants attack countdown", bootstyle=(INFO, INVERSE)
    )
    plant_attacktime_value = ttk.IntVar(plant_time_frame)
    plant_attacktime_entry = ttk.Entry(
        plant_time_frame,
        textvariable=plant_attacktime_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    plant_attacktime_entry.grid(row=5, column=1, ipady=0)

    def setPlantAttackTime(event):
        plant_select.setAttackTime(plant_attacktime_value.get())
        plant_time_frame.focus_set()

    plant_attacktime_entry.bind("<Return>", setPlantAttackTime)
    plant_suntime_label = ttk.Label(plant_time_frame, text="Sunlight:")
    plant_suntime_label.grid(row=6, column=0, padx=(2, 0))
    ToolTip(plant_suntime_label, text="Queen produces sunlight countdown", bootstyle=(INFO, INVERSE))
    plant_suntime_value = ttk.IntVar(plant_time_frame)
    plant_suntime_entry = ttk.Entry(
        plant_time_frame,
        textvariable=plant_suntime_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    plant_suntime_entry.grid(row=6, column=1, ipady=0)

    def setPlantSunTime(event):
        plant_select.setSunTime(plant_suntime_value.get())
        plant_time_frame.focus_set()

    plant_suntime_entry.bind("<Return>", setPlantSunTime)
    plant_humtime_label = ttk.Label(plant_time_frame, text="Sunlight:")
    plant_humtime_label.grid(row=7, column=0, padx=(2, 0))
    ToolTip(plant_humtime_label, text="Burger King produces sunlight countdown", bootstyle=(INFO, INVERSE))
    plant_humtime_value = ttk.IntVar(plant_time_frame)
    plant_humtime_entry = ttk.Entry(
        plant_time_frame,
        textvariable=plant_humtime_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    plant_humtime_entry.grid(row=7, column=1, ipady=0)

    def setPlantHumTime(event):
        plant_select.setHumTime(plant_humtime_value.get())
        plant_time_frame.focus_set()

    plant_humtime_entry.bind("<Return>", setPlantHumTime)
    plant_flag_frame = ttk.LabelFrame(
        plant_attribute_frame, text="Status signs", bootstyle=SUCCESS
    )
    plant_flag_frame.grid(row=3, column=3, columnspan=8, sticky=W)
    plant_exist_flag = ttk.BooleanVar(plant_flag_frame)

    def change_plant_exist():
        plant_select.setExist(not plant_exist_flag.get())

    ttk.Checkbutton(
        plant_flag_frame,
        text="exist",
        bootstyle="success-round-toggle",
        variable=plant_exist_flag,
        command=lambda: change_plant_exist(),
    ).grid(row=0, column=0)
    plant_isVisible_flag = ttk.BooleanVar(plant_flag_frame)

    def change_plant_isVisible():
        plant_select.setIsVisible(not plant_isVisible_flag.get())

    ttk.Checkbutton(
        plant_flag_frame,
        text="Invisible",
        bootstyle="success-round-toggle",
        variable=plant_isVisible_flag,
        command=lambda: change_plant_isVisible(),
    ).grid(row=1, column=0)
    plant_isAttack_flag = ttk.BooleanVar(plant_flag_frame)

    def change_plant_isAttack():
        plant_select.setIsAttack(plant_isAttack_flag.get())

    ttk.Checkbutton(
        plant_flag_frame,
        text="attack",
        bootstyle="success-round-toggle",
        variable=plant_isAttack_flag,
        command=lambda: change_plant_isAttack(),
    ).grid(row=2, column=0)
    plant_isSquash_flag = ttk.BooleanVar(plant_flag_frame)

    def change_plant_isSquash():
        plant_select.setIsSquash(plant_isSquash_flag.get())

    ttk.Checkbutton(
        plant_flag_frame,
        text="Flatte",
        bootstyle="success-round-toggle",
        variable=plant_isSquash_flag,
        command=lambda: change_plant_isSquash(),
    ).grid(row=3, column=0)
    plant_isSleep_flag = ttk.BooleanVar(plant_flag_frame)

    def change_plant_isSleep():
        plant_select.setIsSleep(plant_isSleep_flag.get())

    ttk.Checkbutton(
        plant_flag_frame,
        text="Sleep",
        bootstyle="success-round-toggle",
        variable=plant_isSleep_flag,
        command=lambda: change_plant_isSleep(),
    ).grid(row=4, column=0)

    plant_put_frame = ttk.LabelFrame(plant_page, text="种植", bootstyle=SUCCESS)
    plant_put_frame.place(x=240, y=0, anchor=NW, height=120, width=130)
    ttk.Label(plant_put_frame, text="第").grid(row=0, column=0)
    plantPut_start_row_value = ttk.IntVar(plant_put_frame)
    plantPut_start_row_combobox = ttk.Combobox(
        plant_put_frame,
        textvariable=plantPut_start_row_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6],
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    plantPut_start_row_combobox.grid(row=0, column=1)
    plantPut_start_row_value.set(1)
    ttk.Label(plant_put_frame, text="OK").grid(row=0, column=2)
    plantPut_start_col_value = ttk.IntVar(plant_put_frame)
    plantPut_start_col_combobox = ttk.Combobox(
        plant_put_frame,
        textvariable=plantPut_start_col_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    plantPut_start_col_combobox.grid(row=0, column=3)
    plantPut_start_col_value.set(1)
    ttk.Label(plant_put_frame, text="List").grid(row=0, column=4)
    ttk.Label(plant_put_frame, text="to").grid(row=1, column=0)
    plantPut_end_row_value = ttk.IntVar(plant_put_frame)
    plantPut_end_row_combobox = ttk.Combobox(
        plant_put_frame,
        textvariable=plantPut_end_row_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6],
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    plantPut_end_row_combobox.grid(row=1, column=1)
    plantPut_end_row_value.set(1)
    ttk.Label(plant_put_frame, text="OK").grid(row=1, column=2)
    plantPut_end_col_value = ttk.IntVar(plant_put_frame)
    plantPut_end_col_combobox = ttk.Combobox(
        plant_put_frame,
        textvariable=plantPut_end_col_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    plantPut_end_col_combobox.grid(row=1, column=3)
    plantPut_end_col_value.set(1)
    ttk.Label(plant_put_frame, text="List").grid(row=1, column=4)
    plantPut_type_combobox = ttk.Combobox(
        plant_put_frame,
        width=10,
        values=PVZ_data.plantsType,
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    plantPut_type_combobox.grid(row=2, column=0, columnspan=4, sticky=W)
    plantPut_type_combobox.current(0)
    plantPut_type_combobox.bind(
        "<Button-1>", lambda event: open_card_select_window(plantPut_type_combobox)
    )

    def putPlants(type):
        startRow = plantPut_start_row_value.get() - 1
        startCol = plantPut_start_col_value.get() - 1
        endRow = plantPut_end_row_value.get() - 1
        endCol = plantPut_end_col_value.get() - 1
        print(startRow, startCol, endRow, endCol, type)
        if pvz.getMap is not False:
            rows = pvz.getMap() - 1
            if startRow > rows:
                startRow = rows
            if endRow > rows:
                endRow = rows
            if startRow > endRow or startCol > endCol:
                Messagebox.show_error("The starting ranks are greater than the termination ranks", title="Enter an error")
            else:
                for i in range(startRow, endRow + 1):
                    for j in range(startCol, endCol + 1):
                        pvz.putPlant(i, j, type)

    ttk.Button(
        plant_put_frame,
        text="Plant",
        padding=0,
        bootstyle=(OUTLINE, SUCCESS),
        command=lambda: putPlants(plantPut_type_combobox.current()),
    ).grid(row=2, column=0, columnspan=5, sticky=E)

    def clearPlants():
        try:
            plant_num = PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0xBC
            )
        except:
            return
        i = 0
        j = 0
        while i < plant_num:
            plant_addresss = (
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                    )
                    + 0xAC
                )
                + 0x204 * j
            )
            plant_exist = PVZ_data.PVZ_memory.read_bytes(plant_addresss + 0x141, 1)
            if plant_exist == b"\x00":
                PVZ_data.PVZ_memory.write_bytes(plant_addresss + 0x141, b"\x01", 1)
                i = i + 1
            j = j + 1

    ttk.Button(
        plant_put_frame,
        text="All plants",
        padding=0,
        bootstyle=(OUTLINE, SUCCESS),
        command=lambda: clearPlants(),
    ).grid(row=3, column=0, columnspan=5, pady=(5, 0), sticky=W)

    plant_characteristic_frame = ttk.Labelframe(
        plant_page, text="Basic attribute", bootstyle=SUCCESS
    )
    plant_characteristic_frame.place(x=240, y=130, anchor=NW, height=140, width=130)
    plant_type_combobox = ttk.Combobox(
        plant_characteristic_frame,
        width=10,
        values=PVZ_data.plantsType,
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )

    def wait_select_plant_characteristic_card(event, plant_type_combobox):
        open_card_select_window(plant_type_combobox)
        card_select_window.wait_window()
        get_plant_type()

        def closeCombobox(plant_type_combobox):
            plant_type_combobox.event_generate("<Escape>")

        plant_type_combobox.after(100, lambda: closeCombobox(plant_type_combobox))

    plant_type_combobox.bind(
        "<Button-1>",
        lambda event: wait_select_plant_characteristic_card(event, plant_type_combobox),
    )
    plant_type_combobox.grid(row=0, column=0, columnspan=4, sticky=W)
    ttk.Label(plant_characteristic_frame, text="Sunlight:").grid(row=1, column=0)
    plant_characteristic_sun_value = ttk.IntVar(plant_characteristic_frame)
    plant_characteristic_sun_entry = ttk.Entry(
        plant_characteristic_frame,
        textvariable=plant_characteristic_sun_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    plant_characteristic_sun_entry.grid(row=1, column=1, ipady=0)

    def setPlantCharacteristicSun(event):
        plant_characteristic_type.setSun(plant_characteristic_sun_value.get())
        plant_characteristic_frame.focus_set()

    plant_characteristic_sun_entry.bind("<Return>", setPlantCharacteristicSun)
    plant_characteristic_cd_label = ttk.Label(plant_characteristic_frame, text="冷却:")
    plant_characteristic_cd_label.grid(row=2, column=0)
    plant_characteristic_cd_value = ttk.IntVar(plant_characteristic_frame)
    plant_characteristic_cd_entry = ttk.Entry(
        plant_characteristic_frame,
        textvariable=plant_characteristic_cd_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    plant_characteristic_cd_entry.grid(row=2, column=1, ipady=0)

    def setPlantCharacteristicCd(event):
        plant_characteristic_type.setCd(plant_characteristic_cd_value.get())
        plant_characteristic_frame.focus_set()

    plant_characteristic_cd_entry.bind("<Return>", setPlantCharacteristicCd)
    plant_characteristic_canAttack_flag = ttk.BooleanVar(plant_flag_frame)

    def change_plant_characteristic_canAttack():
        plant_characteristic_type.setCanAttack(
            plant_characteristic_canAttack_flag.get()
        )

    ttk.Checkbutton(
        plant_characteristic_frame,
        text="Attack",
        bootstyle="success-round-toggle",
        variable=plant_characteristic_canAttack_flag,
        command=lambda: change_plant_characteristic_canAttack(),
    ).grid(row=3, column=0, columnspan=4)
    ttk.Label(plant_characteristic_frame, text="Attack interval:").grid(row=4, column=0)
    plant_characteristic_attackinterval_value = ttk.IntVar(plant_characteristic_frame)
    plant_characteristic_attackinterval_entry = ttk.Entry(
        plant_characteristic_frame,
        textvariable=plant_characteristic_attackinterval_value,
        width=5,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    plant_characteristic_attackinterval_entry.grid(row=4, column=1, ipady=0)

    def setPlantCharacteristicAttackInterval(event):
        plant_characteristic_type.setAttackInterval(
            plant_characteristic_attackinterval_value.get()
        )
        plant_characteristic_frame.focus_set()

    plant_characteristic_attackinterval_entry.bind(
        "<Return>", setPlantCharacteristicAttackInterval
    )

    def get_plant_type():
        global plant_characteristic_type
        plant_characteristic_type = PVZ_data.plantCharacteristic(
            plant_type_combobox.current()
        )
        plant_characteristic_sun_value.set(plant_characteristic_type.sun)
        plant_characteristic_cd_value.set(plant_characteristic_type.cd)
        plant_characteristic_attackinterval_value.set(
            plant_characteristic_type.attackInterval
        )
        plant_characteristic_canAttack_flag.set(plant_characteristic_type.canAttack)
        plant_characteristic_frame.focus_set()

    bullet_frame = ttk.Labelframe(plant_page, text="Bullet modification", bootstyle=SUCCESS)
    bullet_frame.place(x=0, y=390, anchor=NW, height=120, width=300)
    all_bullet_frame = ttk.Frame(bullet_frame)
    all_bullet_frame.pack(anchor=W)
    all_bullet_status = ttk.BooleanVar(all_bullet_frame)
    bullet_type_modify_combobox = ttk.Combobox(
        all_bullet_frame,
        width=10,
        values=PVZ_data.bulletType,
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    bullet_type_modify_combobox.pack(side=RIGHT)
    bullet_type_modify_combobox.current(0)
    ttk.Checkbutton(
        all_bullet_frame,
        variable=all_bullet_status,
        text="Modify all bullets as",
        bootstyle="success-round-toggle",
        command=lambda: pvz.setAllBullet(
            all_bullet_status.get(), bullet_type_modify_combobox.current()
        ),
    ).pack(side=RIGHT)
    random_bullet_frame = ttk.Frame(bullet_frame)
    random_bullet_frame.pack(anchor=W)
    random_bullet_hasPepper = ttk.BooleanVar(random_bullet_frame)
    ttk.Checkbutton(
        random_bullet_frame, text="chili", variable=random_bullet_hasPepper
    ).pack(side=RIGHT)
    random_bullet_hasMine = ttk.BooleanVar(random_bullet_frame)
    ttk.Checkbutton(
        random_bullet_frame, text="Torine", variable=random_bullet_hasMine
    ).pack(side=RIGHT)
    random_bullet_hasDoom = ttk.BooleanVar(random_bullet_frame)
    ttk.Checkbutton(
        random_bullet_frame, text="Mushroom", variable=random_bullet_hasDoom
    ).pack(side=RIGHT)
    ttk.Label(random_bullet_frame, text="Include").pack(side=RIGHT)
    random_bullet_status = ttk.BooleanVar(random_bullet_frame)
    ttk.Checkbutton(
        random_bullet_frame,
        variable=random_bullet_status,
        text="All bullets",
        bootstyle="success-round-toggle",
        command=lambda: pvz.randomBullet(
            random_bullet_status.get(),
            random_bullet_hasDoom.get(),
            random_bullet_hasMine.get(),
            random_bullet_hasPepper.get(),
        ),
    ).pack(side=RIGHT)
    attack_speed_frame = ttk.Frame(bullet_frame)
    attack_speed_frame.pack(anchor=W)
    attack_speed_label = ttk.Label(attack_speed_frame, text="Plant attack speed multiplied:")
    attack_speed_label.pack(side=LEFT)
    ToolTip(
        attack_speed_label, text="Excessive high will cause plants to be unable to attack", bootstyle=(INFO, INVERSE)
    )
    attack_speed_multiple = ttk.IntVar(attack_speed_frame)
    attack_speed_multiple.set(1)
    attack_speed_entry = ttk.Entry(
        attack_speed_frame,
        font=("Black body", 8),
        width=3,
        textvariable=attack_speed_multiple,
    )
    attack_speed_entry.pack(side=LEFT)
    attack_animation_status = ttk.BooleanVar(attack_speed_frame)
    attack_animation_check = ttk.Checkbutton(
        attack_speed_frame,
        variable=attack_animation_status,
        text="Attack ignoring animation",
        bootstyle="success-round-toggle",
        command=lambda: pvz.cancelAttackAnimation(attack_animation_status.get()),
    )
    attack_animation_check.pack(side=LEFT)
    ToolTip(
        attack_animation_check,
        text="Some plants are effective, and they can ignore the animation to attack and increase the upper limit of the attack speed",
        bootstyle=(INFO, INVERSE),
    )
    bullet_size_frame = ttk.Frame(bullet_frame)
    bullet_size_frame.pack(anchor=W)
    bullet_size = ttk.IntVar(bullet_size_frame)
    bullet_size_entry = ttk.Entry(
        bullet_size_frame,
        width=3,
        textvariable=bullet_size,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    bullet_size_entry.pack(side=RIGHT)
    bullet_size.set(1)
    bullet_size_status = ttk.BooleanVar(bullet_size_frame)
    ttk.Checkbutton(
        bullet_size_frame,
        variable=bullet_size_status,
        text="Modify bullet size multiple(Positive integer)",
        bootstyle="success-round-toggle",
        command=lambda: pvz.setBulletSize(bullet_size_status.get(), bullet_size.get()),
    ).pack(side=RIGHT)

    def setAttackSpeed(event):
        pvz.setAttackSpeed(attack_speed_multiple.get())
        attack_speed_frame.focus_set()

    attack_speed_entry.bind("<Return>", setAttackSpeed)

    plant_bullet_frame = ttk.Labelframe(
        plant_page, text="Plant bullet modification", bootstyle=SUCCESS
    )
    plant_bullet_frame.place(x=370, y=0, anchor=NW, height=130, width=100)
    plant_type_bullet_combobox = ttk.Combobox(
        plant_bullet_frame,
        width=10,
        values=PVZ_data.plantsType,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    plant_type_bullet_combobox.pack()
    plant_type_bullet_combobox.bind(
        "<Button-1>", lambda event: open_card_select_window(plant_type_bullet_combobox)
    )
    plant_type_bullet_combobox.insert(0, "Chosen plant")
    plant_type_bullet_combobox.config(state=READONLY)
    plant_bullet_status = ttk.BooleanVar(plant_bullet_frame)
    plantBulletMode = ttk.IntVar(plant_bullet_frame)
    ttk.Checkbutton(
        plant_bullet_frame,
        variable=plant_bullet_status,
        text="Modify the bullet to",
        bootstyle="success-round-toggle",
        command=lambda: pvz.setPlantBullet(
            plant_bullet_status.get(),
            plant_type_bullet_combobox.current(),
            plant_bullet_type_combobox.current(),
            plantBulletMode.get(),
        ),
    ).pack()
    plant_bullet_type_combobox = ttk.Combobox(
        plant_bullet_frame,
        width=10,
        values=PVZ_data.bulletType,
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    plant_bullet_type_combobox.pack()
    plant_bullet_type_combobox.current(0)
    plant_bullet_mode_frame = ttk.Frame(plant_bullet_frame)
    plant_bullet_mode_frame.pack()
    ttk.Radiobutton(
        plant_bullet_mode_frame,
        text="usually",
        value=0,
        variable=plantBulletMode,
        bootstyle=PRIMARY,
    ).grid(row=0, column=0, padx=2)
    ttk.Radiobutton(
        plant_bullet_mode_frame,
        text="Slow",
        value=8,
        variable=plantBulletMode,
        bootstyle=PRIMARY,
    ).grid(row=0, column=1, padx=2)
    ttk.Radiobutton(
        plant_bullet_mode_frame,
        text="track",
        value=9,
        variable=plantBulletMode,
        bootstyle=PRIMARY,
    ).grid(row=1, column=0, padx=2)
    ttk.Radiobutton(
        plant_bullet_mode_frame,
        text="Reverse",
        value=6,
        variable=plantBulletMode,
        bootstyle=PRIMARY,
    ).grid(row=1, column=1, padx=2)
    plantBulletMode.set(0)

    # bullet_damage_frame = ttk.Labelframe(
    #     plant_page, text="简易子弹伤害修改", bootstyle=SUCCESS
    # )
    # bullet_damage_frame.place(x=370, y=140, anchor=NW, height=100, width=100)
    # bullet_type_damage_combobox = ttk.Combobox(
    #     bullet_damage_frame,
    #     width=10,
    #     values=data.bulletType,
    #     font=("黑体", 8),
    #     bootstyle=SECONDARY,
    # )
    # bullet_type_damage_combobox.pack()
    # bullet_type_damage_combobox.insert(0, "选择子弹")
    # bullet_type_damage_combobox.config(state=READONLY)
    # bullet_damage_status = ttk.BooleanVar(bullet_damage_frame)
    # bullet_type_damage_value = ttk.IntVar(bullet_damage_frame)
    # ttk.Checkbutton(
    #     bullet_damage_frame,
    #     variable=bullet_damage_status,
    #     text="修改伤害为",
    #     bootstyle="success-round-toggle",
    #     command=lambda: pvz.setBulletDamage(
    #         bullet_damage_status.get(),
    #         bullet_type_damage_combobox.current(),
    #         bullet_type_damage_value.get(),
    #     ),
    # ).pack()
    # bullet_type_damage_entry = ttk.Entry(
    #     bullet_damage_frame, textvariable=bullet_type_damage_value, width=8
    # )
    # bullet_type_damage_entry.pack()

    def get_plant_select(event):
        global plant_select
        try:
            index = int(plant_list_box.selection()[0])
            plant_select = plant_list[index]
        except:
            return

    def get_plant_attribute():
        global plant_select
        if plant_select is not None:
            try:
                plant_type_value.set(
                    str(plant_select.type)
                    + ":"
                    + PVZ_data.plantsType[plant_select.type]
                )
                if plant_attribute_frame.focus_get() != plant_state_entry:
                    plant_state_value.set(plant_select.state)
                if plant_attribute_frame.focus_get() != plant_x_entry:
                    plant_x_value.set(plant_select.x)
                if plant_attribute_frame.focus_get() != plant_y_entry:
                    plant_y_value.set(plant_select.y)
                plant_row_value.set(plant_select.row)
                plant_col_value.set(plant_select.col)
                if plant_attribute_frame.focus_get() != plant_hp_entry:
                    plant_hp_value.set(plant_select.hp)
                if plant_attribute_frame.focus_get() != plant_dietime_entry:
                    plant_dietime_value.set(plant_select.dieTime)
                if plant_attribute_frame.focus_get() != plant_cindertime_entry:
                    plant_cindertime_value.set(plant_select.cinderTime)
                if plant_attribute_frame.focus_get() != plant_effecttime_entry:
                    plant_effecttime_value.set(plant_select.effectTime)
                if plant_attribute_frame.focus_get() != plant_producttime_entry:
                    plant_producttime_value.set(plant_select.productTime)
                if plant_attribute_frame.focus_get() != plant_attacktime_entry:
                    plant_attacktime_value.set(plant_select.attackTime)
                if plant_attribute_frame.focus_get() != plant_productinterval_entry:
                    plant_productinterval_value.set(plant_select.productInterval)
                if plant_attribute_frame.focus_get() != plant_suntime_entry:
                    plant_suntime_value.set(plant_select.sunTime)
                if plant_attribute_frame.focus_get() != plant_humtime_entry:
                    plant_humtime_value.set(plant_select.humTime)
            except:
                pass
            plant_isVisible_flag.set(not plant_select.isVisible)
            plant_exist_flag.set(not plant_select.exist)
            plant_isAttack_flag.set(plant_select.isAttack)
            plant_isSquash_flag.set(plant_select.isSquash)
            plant_isSleep_flag.set(plant_select.isSleep)

    plant_list_box.bind("<<TreeviewSelect>>", get_plant_select)

    grid_page = ttk.Frame(page_tab)
    grid_page.pack()
    page_tab.add(grid_page, text="Venue modification")
    item_list_frame = ttk.LabelFrame(grid_page, text="Item list", bootstyle=DARK)
    item_list_frame.place(x=0, y=0, anchor=NW, height=140, width=200)
    item_list_box_scrollbar = ttk.Scrollbar(item_list_frame, bootstyle=DARK)
    item_list_box = ttk.Treeview(
        item_list_frame,
        show=TREE,
        selectmode=BROWSE,
        padding=0,
        columns=("item_list"),
        yscrollcommand=item_list_box_scrollbar.set,
        bootstyle=DARK,
    )
    item_list_box_scrollbar.configure(command=item_list_box.yview)
    item_list_box.place(x=0, y=0, anchor=NW, height=120, width=70)
    item_list_box_scrollbar.place(x=65, y=0, height=120, anchor=NW)
    item_list = list()

    def refresh_item_list():
        item_list.clear()
        item_list_box.delete(*item_list_box.get_children())
        try:
            item_num = PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0x12C
            )
        except:
            return
        i = 0
        j = 0
        while i < item_num:
            item_addresss = (
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                    )
                    + 0x11C
                )
                + 0x1EC * j
            )
            item_exist = PVZ_data.PVZ_memory.read_bytes(item_addresss + 0x20, 1)
            if item_exist == b"\x00":
                item_list.append(PVZ_data.item(item_addresss))
                i = i + 1
            j = j + 1
        n = 0
        for k in range(item_num):
            item_list_box.insert(
                "",
                END,
                iid=n,
                text=str(item_list[k].no) + PVZ_data.itemType[item_list[k].type],
            )
            if item_select is not None:
                if item_select.exist == 0:
                    if item_select.no == item_list[k].no:
                        item_list_box.selection_set((str(n),))
            n = n + 1

    refresh_item_list()
    item_attribute_frame = ttk.Frame(item_list_frame)
    item_attribute_frame.place(x=80, y=0, height=120, width=115)
    item_exist_flag = ttk.BooleanVar(item_attribute_frame)

    def change_item_exist():
        item_select.setExist(not item_exist_flag.get())

    ttk.Checkbutton(
        item_attribute_frame,
        text="exist",
        bootstyle="dark-round-toggle",
        variable=item_exist_flag,
        command=lambda: change_item_exist(),
    ).grid(row=0, column=0, columnspan=4, sticky=W)
    item_row_value = ttk.IntVar(item_attribute_frame)
    item_row_combobox = ttk.Combobox(
        item_attribute_frame,
        textvariable=item_row_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6],
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    item_row_combobox.grid(row=1, column=0)
    ttk.Label(item_attribute_frame, text="OK").grid(row=1, column=1)

    def setItemRow(event):
        item_select.setRow(item_row_value.get())
        item_attribute_frame.focus_set()

    item_row_combobox.bind("<<ComboboxSelected>>", setItemRow)
    item_col_value = ttk.IntVar(item_attribute_frame)
    item_col_combobox = ttk.Combobox(
        item_attribute_frame,
        textvariable=item_col_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    item_col_combobox.grid(row=1, column=2)
    ttk.Label(item_attribute_frame, text="List").grid(row=1, column=3)

    def setItemCol(event):
        item_select.setCol(item_col_value.get())
        item_attribute_frame.focus_set()

    item_col_combobox.bind("<<ComboboxSelected>>", setItemCol)
    item_time_value = ttk.IntVar(item_attribute_frame)

    def setItemTime(event):
        item_select.setTime(item_time_meter.amountusedvar.get())
        item_attribute_frame.focus_set()

    item_time_meter = ttk.Meter(
        item_attribute_frame,
        metersize=80,
        bootstyle=DARK,
        amounttotal=18000,
        showtext=True,
        metertype="semi",
        interactive=True,
        textfont="-size 7",
        subtext="time left",
        subtextfont="-size 7",
        subtextstyle="dark",
    )

    def setItemTimeMeterFocus(event):
        item_time_meter.focus_set()

    item_time_meter.indicator.bind("<Button-1>", setItemTimeMeterFocus)
    item_time_meter.indicator.bind("<ButtonRelease-1>", setItemTime)

    def clearLadders():
        try:
            item_num = PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0x12C
            )
        except:
            return
        i = 0
        j = 0
        while i < item_num:
            item_addresss = (
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                    )
                    + 0x11C
                )
                + 0x1EC * j
            )
            item_exist = PVZ_data.PVZ_memory.read_bytes(item_addresss + 0x20, 1)
            if item_exist == b"\x00":
                PVZ_data.PVZ_memory.write_bytes(item_addresss + 0x20, b"\x01", 1)
                i = i + 1
            j = j + 1

    ladder_put_frame = ttk.LabelFrame(grid_page, text="搭梯", bootstyle=DARK)
    ladder_put_frame.place(x=200, y=0, anchor=NW, height=90, width=130)
    ttk.Label(ladder_put_frame, text="第").grid(row=0, column=0)
    ladder_start_row_value = ttk.IntVar(ladder_put_frame)
    item_start_row_combobox = ttk.Combobox(
        ladder_put_frame,
        textvariable=ladder_start_row_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6],
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    item_start_row_combobox.grid(row=0, column=1)
    ladder_start_row_value.set(1)
    ttk.Label(ladder_put_frame, text="行").grid(row=0, column=2)
    ladder_start_col_value = ttk.IntVar(ladder_put_frame)
    item_start_col_combobox = ttk.Combobox(
        ladder_put_frame,
        textvariable=ladder_start_col_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    item_start_col_combobox.grid(row=0, column=3)
    ladder_start_col_value.set(1)
    ttk.Label(ladder_put_frame, text="List").grid(row=0, column=4)
    ttk.Label(ladder_put_frame, text="to").grid(row=1, column=0)
    ladder_end_row_value = ttk.IntVar(ladder_put_frame)
    item_end_row_combobox = ttk.Combobox(
        ladder_put_frame,
        textvariable=ladder_end_row_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6],
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    item_end_row_combobox.grid(row=1, column=1)
    ladder_end_row_value.set(1)
    ttk.Label(ladder_put_frame, text="OK").grid(row=1, column=2)
    ladder_end_col_value = ttk.IntVar(ladder_put_frame)
    item_end_col_combobox = ttk.Combobox(
        ladder_put_frame,
        textvariable=ladder_end_col_value,
        width=2,
        values=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    item_end_col_combobox.grid(row=1, column=3)
    ladder_end_col_value.set(1)
    ttk.Label(ladder_put_frame, text="List").grid(row=1, column=4)

    def putLadders():
        startRow = ladder_start_row_value.get() - 1
        startCol = ladder_start_col_value.get() - 1
        endRow = ladder_end_row_value.get() - 1
        endCol = ladder_end_col_value.get() - 1
        print(startRow, startCol, endRow, endCol)
        if pvz.getMap is not False:
            rows = pvz.getMap() - 1
            if startRow > rows:
                startRow = rows
            if endRow > rows:
                endRow = rows
            if startRow > endRow or startCol > endCol:
                Messagebox.show_error("The starting ranks are greater than the termination ranks", title="Enter an error")
            else:
                for i in range(startRow, endRow + 1):
                    for j in range(startCol, endCol + 1):
                        pvz.putLadder(i, j)

    ttk.Button(
        ladder_put_frame,
        text="Ladder",
        padding=0,
        bootstyle=(OUTLINE, DARK),
        command=lambda: putLadders(),
    ).grid(row=2, column=0, columnspan=5, sticky=E)

    car_frame = ttk.LabelFrame(grid_page, text="Car", bootstyle=DANGER)
    car_frame.place(x=330, y=0, anchor=NW, height=120, width=160)
    start_car_value = ttk.IntVar(ladder_put_frame)
    start_car_combobox = ttk.Combobox(
        car_frame,
        textvariable=start_car_value,
        width=5,
        values=[1, 2, 3, 4, 5, 6, "all"],
        font=("Black body", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    start_car_combobox.grid(row=0, column=0)
    start_car_combobox.current(6)

    def startCar():
        rows = pvz.getMap()
        if rows is False:
            return
        else:
            if start_car_combobox.current() == 6:
                try:
                    car_num = PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(
                            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                        )
                        + 0x110
                    )
                except:
                    return
                i = 0
                j = 0
                start_car_list = [0] * rows
                while i < car_num:
                    car_addresss = (
                        PVZ_data.PVZ_memory.read_int(
                            PVZ_data.PVZ_memory.read_int(
                                PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress)
                                + 0x768
                            )
                            + 0x100
                        )
                        + 0x48 * j
                    )
                    car_exist = PVZ_data.PVZ_memory.read_bytes(car_addresss + 0x30, 1)
                    if car_exist == b"\x00":
                        try:
                            c = PVZ_data.car(car_addresss)
                            if start_car_list[c.row] == 0:
                                pvz.startCar(car_addresss)
                                start_car_list[c.row] = 1
                        except:
                            pass
                        i = i + 1
                    j = j + 1

            elif start_car_combobox.current() > rows - 1:
                return
            else:
                try:
                    car_num = PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(
                            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                        )
                        + 0x110
                    )
                except:
                    return
                i = 0
                j = 0
                while i < car_num:
                    car_addresss = (
                        PVZ_data.PVZ_memory.read_int(
                            PVZ_data.PVZ_memory.read_int(
                                PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress)
                                + 0x768
                            )
                            + 0x100
                        )
                        + 0x48 * j
                    )
                    car_exist = PVZ_data.PVZ_memory.read_bytes(car_addresss + 0x30, 1)
                    if car_exist == b"\x00":
                        c = PVZ_data.car(car_addresss)
                        if c.row == start_car_combobox.current():
                            pvz.startCar(car_addresss)
                            return
                        i = i + 1
                    j = j + 1

    ttk.Button(
        car_frame,
        text="Start a small car",
        padding=0,
        bootstyle=(OUTLINE, DANGER),
        command=lambda: startCar(),
    ).grid(row=0, column=1)
    recover_car_value = ttk.IntVar(ladder_put_frame)
    recover_car_combobox = ttk.Combobox(
        car_frame,
        textvariable=recover_car_value,
        width=5,
        values=[1, 2, 3, 4, 5, 6, "all"],
        font=("Black body", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    recover_car_combobox.grid(row=1, column=0)
    recover_car_combobox.current(6)

    def recoveryCar():
        rows = pvz.getMap()
        if rows is False:
            return
        else:
            if recover_car_combobox.current() == 6:
                pass
            elif recover_car_combobox.current() > rows - 1:
                return
            pvz.recoveryCars()
            try:
                car_num = PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                    )
                    + 0x110
                )
            except:
                return
            if recover_car_combobox.current() < 6:
                i = 0
                j = 0
                delete_car_list = [0] * rows
                print(delete_car_list)
                delete_car_list[recover_car_combobox.current()] = 1
                while i < car_num:
                    car_addresss = (
                        PVZ_data.PVZ_memory.read_int(
                            PVZ_data.PVZ_memory.read_int(
                                PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress)
                                + 0x768
                            )
                            + 0x100
                        )
                        + 0x48 * j
                    )
                    car_exist = PVZ_data.PVZ_memory.read_bytes(car_addresss + 0x30, 1)
                    if car_exist == b"\x00":
                        c = PVZ_data.car(car_addresss)
                        try:
                            if (
                                c.row != recover_car_combobox.current()
                                and delete_car_list[c.row] == 0
                            ):
                                print(c.row)
                                print(delete_car_list)
                                c.setExist(True)
                                delete_car_list[c.row] = 1
                        except:
                            pass
                        i = i + 1
                    j = j + 1

    ttk.Button(
        car_frame,
        text="Restore a small car",
        padding=0,
        bootstyle=(OUTLINE, DANGER),
        command=lambda: recoveryCar(),
    ).grid(row=1, column=1)
    endless_car_status = ttk.BooleanVar()
    ttk.Checkbutton(
        car_frame,
        text="Endless car",
        variable=endless_car_status,
        padding=0,
        bootstyle="danger-round-toggle",
        command=lambda: pvz.endlessCar(endless_car_status.get()),
    ).grid(row=2, column=1)
    init_car_status = ttk.BooleanVar()
    ttk.Checkbutton(
        car_frame,
        text="Initial car",
        variable=init_car_status,
        padding=0,
        bootstyle="danger-round-toggle",
        command=lambda: pvz.initCar(init_car_status.get()),
    ).grid(row=3, column=0)
    auto_car_status = ttk.BooleanVar()
    ttk.Checkbutton(
        car_frame,
        text="Automatic car replenishment",
        variable=auto_car_status,
        padding=0,
        bootstyle="danger-round-toggle",
        command=lambda: pvz.autoCar(auto_car_status.get()),
    ).grid(row=3, column=1)

    def get_item_select(event):
        global item_select
        try:
            index = int(item_list_box.selection()[0])
            item_select = item_list[index]
        except:
            return

    def get_item_attribute():
        global item_select
        if item_select is not None:
            item_exist_flag.set(not item_select.exist)
            item_row_value.set(item_select.row)
            item_col_value.set(item_select.col)
            if item_select.type == 2:
                try:
                    if item_attribute_frame.focus_get() != item_time_meter:
                        item_time_value.set(item_select.time)
                        item_time_meter.grid(row=2, column=0, columnspan=4)
                        item_time_meter.configure(amountused=item_time_value.get())
                except:
                    pass
            else:
                item_time_meter.grid_forget()

    item_list_box.bind("<<TreeviewSelect>>", get_item_select)

    formation_frame = ttk.LabelFrame(grid_page, text="Array", bootstyle=SUCCESS)
    formation_frame.place(x=0, y=140)
    # Set font
    small_font = ("黑体", 8)

    # Venue data and ladder attributes
    plants_data = [[[] for _ in range(9)] for _ in range(6)]
    ladders_data = [[0 for _ in range(9)] for _ in range(6)]

    # Update plant types displayed by venue grid

    def update_field():
        for i, row in enumerate(plants_data):
            for j, indices in enumerate(row):
                text = (
                    "\n".join([PVZ_data.plantsType[index] for index in indices])
                    if indices
                    else ""
                )
                buttons[i][j].config(
                    text=text, bg="gray" if ladders_data[i][j] else "#90ee90"
                )

    # Management of plant types

    def manage_plants(i, j):
        formation_plant_window = ttk.Toplevel(formation_frame)
        formation_plant_window.title("Managed plant")
        formation_plant_window.geometry("200x300")

        main_window_x = main_window.winfo_x()
        main_window_y = main_window.winfo_y()
        formation_plant_window.geometry(f"+{main_window_x+150}+{main_window_y + 150}")
        # List box
        listbox = Listbox(formation_plant_window, height=10, font=small_font)
        listbox.pack()

        # Add the existing plant type to the list box
        for index in plants_data[i][j]:
            listbox.insert(tk.END, PVZ_data.plantsType[index])

        # Combobox
        combobox = ttk.Combobox(
            formation_plant_window, values=PVZ_data.plantsType, font=small_font
        )
        combobox.pack()
        combobox.bind("<Button-1>", lambda event: open_card_select_window(combobox))

        # Ladder attribute check box
        ladder_check = IntVar(value=ladders_data[i][j])
        ladder_checkbox = Checkbutton(
            formation_plant_window, text="Is there a ladder", variable=ladder_check
        )
        ladder_checkbox.pack()

        # Add plant type
        def add_plant():
            selected_plant = combobox.get()
            if selected_plant in PVZ_data.plantsType:
                index = PVZ_data.plantsType.index(selected_plant)
                plants_data[i][j].append(index)
                listbox.insert(tk.END, selected_plant)

        # Delete the selected plant type
        def delete_plant():
            selections = listbox.curselection()
            if selections:
                for index in selections[::-1]:
                    del plants_data[i][j][listbox.index(index)]
                    listbox.delete(index)

        button_frame = ttk.Frame(formation_plant_window)
        button_frame.pack()
        # Add button
        add_button = ttk.Button(button_frame, text="Add to", command=add_plant)
        add_button.pack(side=LEFT, padx=10, pady=5)

        # Delete button
        delete_button = ttk.Button(
            button_frame, text="delete", command=delete_plant, bootstyle=DANGER
        )
        delete_button.pack(side=LEFT, padx=10, pady=5)

        # Update and close the window
        def close_and_update():
            # Update ladder attributes
            ladders_data[i][j] = ladder_check.get()
            update_field()
            formation_plant_window.destroy()

        # Complete button
        done_button = ttk.Button(
            formation_plant_window,
            text="Finish",
            command=close_and_update,
            bootstyle=SUCCESS,
        )
        done_button.pack()

    # Create the venue grid button
    buttons = [
        [
            tk.Label(
                formation_frame,
                text="",
                width=9,
                height=4,
                font=small_font,
                borderwidth=2,
                relief="groove",
                bg="#90ee90",
            )
            for j in range(9)
        ]
        for i in range(6)
    ]
    for i in range(6):
        for j in range(9):
            buttons[i][j].grid(row=i, column=j, padx=1, pady=1, sticky="nsew")
            buttons[i][j].bind("<Button-1>", lambda e, i=i, j=j: manage_plants(i, j))
    update_field()

    # Save the venue data JSON document

    def creat_formation_config(plants_data, ladders_data):
        if new_formation_config_entry.get() == "":
            Messagebox.show_error("Please enter the formation name", title="Failure to create formation")
        else:
            config = load_config(config_file_path)
            if "formation" not in config:
                config["formation"] = {}
            if new_formation_config_entry.get() not in config["formation"]:
                config["formation"][new_formation_config_entry.get()] = {}
            config["formation"][new_formation_config_entry.get()]["plants"] = (
                plants_data
            )
            config["formation"][new_formation_config_entry.get()]["ladders"] = (
                ladders_data
            )
            save_config(config, config_file_path)
            Messagebox.show_info(
                "Formation”" + new_formation_config_entry.get() + "”Have created",
                title="Successful creation formation",
            )
            update_formation_config_combobox()
            formation_config_combobox.set(new_formation_config_entry.get())

    def save_formation_config(plants_data, ladders_data):
        config = load_config(config_file_path)
        if "formation" not in config:
            config["formation"] = {}
        if formation_config_combobox.get() not in config["formation"]:
            Messagebox.show_error("The formation name does not exist, please build a new formation first", title="Save formation failed")
        config["formation"][formation_config_combobox.get()]["plants"] = plants_data
        config["formation"][formation_config_combobox.get()]["ladders"] = ladders_data
        save_config(config, config_file_path)
        Messagebox.show_info(
            "Formation" + formation_config_combobox.get() + "Modify successfully", title="Modify the formation successfully"
        )

    # Create saving and reading button
    formation_config_frame = ttk.Frame(formation_frame)
    formation_config_frame.grid(row=6, column=0, columnspan=9, pady=(10, 0))
    new_formation_config_entry = ttk.Entry(
        formation_config_frame, width=10, font=("宋体", 8)
    )
    new_formation_config_entry.pack(side=LEFT, padx=2)
    new_formation_config_button = ttk.Button(
        formation_config_frame,
        text="New formation",
        bootstyle=SUCCESS,
        padding=0,
        command=lambda: creat_formation_config(plants_data, ladders_data),
    )
    new_formation_config_button.pack(side=LEFT, padx=2)
    formation_config_combobox = ttk.Combobox(
        formation_config_frame, width=12, bootstyle="secondary", font=("宋体", 8)
    )
    formation_config_combobox.pack(side=LEFT, padx=2)
    formation_config_combobox.insert(0, "Choice formation")
    formation_config_combobox.configure(state=READONLY)

    def update_formation_config_combobox():
        config = load_config(config_file_path)
        if "formation" not in config:
            return
        formation_config_combobox.configure(values=list(config["formation"].keys()))

    update_formation_config_combobox()

    def load_formation_config(event, plants_data, ladders_data):
        config = load_config(config_file_path)
        loaded_data = config["formation"][formation_config_combobox.get()]
        for i in range(6):
            for j in range(9):
                plants_data[i][j] = loaded_data["plants"][i][j]
                ladders_data[i][j] = loaded_data["ladders"][i][j]
        update_field()

    formation_config_combobox.bind(
        "<<ComboboxSelected>>",
        lambda event, plants=plants_data, ladders=ladders_data: load_formation_config(
            event, plants, ladders
        ),
    )
    load_formation_config_button = ttk.Button(
        formation_config_frame,
        text="Modify configuration",
        bootstyle=WARNING,
        padding=0,
        command=lambda: save_formation_config(plants_data, ladders_data),
    )
    load_formation_config_button.pack(side=LEFT, padx=2)

    def delete_formation_config():
        config = load_config(config_file_path)
        if "formation" not in config:
            config["formation"] = {}
        if formation_config_combobox.get() not in config["formation"]:
            Messagebox.show_error("The formation name does not exist", title="Delete the formation failed")
        del config["formation"][formation_config_combobox.get()]
        save_config(config, config_file_path)
        Messagebox.show_info(
            "Formation" + formation_config_combobox.get() + "Deleted", title="Delete the formation successfully"
        )
        update_formation_config_combobox()

    delete_formation_button = ttk.Button(
        formation_config_frame,
        text="Delete formation",
        bootstyle=DANGER,
        padding=0,
        command=lambda: delete_formation_config(),
    )
    delete_formation_button.pack(side=LEFT, padx=2)

    def clear_grid():
        clearPlants()
        clearLadders()

    clear_game_grid = ttk.Button(
        formation_config_frame,
        text="Clear the game venue",
        bootstyle=DARK,
        padding=0,
        command=lambda: clear_grid(),
    )
    clear_game_grid.pack(side=LEFT, padx=2)

    def get_game_formation(plants_data, ladders_data):
        for r in range(0, 6):
            for c in range(0, 9):
                plants_data[r][c].clear()
                ladders_data[r][c] = 0
        try:
            plant_num = PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0xBC
            )
        except:
            return
        i = 0
        j = 0
        while i < plant_num:
            plant_addresss = (
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                    )
                    + 0xAC
                )
                + 0x204 * j
            )
            plant_exist = PVZ_data.PVZ_memory.read_bytes(plant_addresss + 0x141, 1)
            if plant_exist == b"\x00":
                p = PVZ_data.plant(plant_addresss)
                if p.row > 5 or p.col > 8:
                    continue
                plants_data[p.row][p.col].append(p.type)
                i = i + 1
            j = j + 1
        try:
            item_num = PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0x12C
            )
        except:
            return
        i = 0
        j = 0
        while i < item_num:
            item_addresss = (
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                    )
                    + 0x11C
                )
                + 0x1EC * j
            )
            item_exist = PVZ_data.PVZ_memory.read_bytes(item_addresss + 0x20, 1)
            if item_exist == b"\x00":
                it = PVZ_data.item(item_addresss)
                if it.type == 3:
                    ladders_data[it.row - 1][it.col - 1] = 1
                i = i + 1
            j = j + 1
        update_field()

    get_game_formation_button = ttk.Button(
        formation_config_frame,
        text="Load from the game",
        bootstyle=INFO,
        padding=0,
        command=lambda: get_game_formation(plants_data, ladders_data),
    )
    get_game_formation_button.pack(side=LEFT, padx=2)

    def set_game_formation(plants_data, ladders_data):
        rols = pvz.getMap()
        if rols is False:
            Messagebox.show_error("Please use it in the level", title="Application formation failure")
            return
        for r in range(0, rols):
            for c in range(0, 9):
                for p in plants_data[r][c]:
                    print(p)
                    print(PVZ_data.plantsType[p])
                    pvz.putPlant(r, c, p)
                if ladders_data[r][c] == 1:
                    pvz.putLadder(r, c)

    set_game_formation_button = ttk.Button(
        formation_config_frame,
        text="Apply to the game",
        bootstyle=PRIMARY,
        padding=0,
        command=lambda: set_game_formation(plants_data, ladders_data),
    )
    set_game_formation_button.pack(side=LEFT, padx=2)

    slot_page = ttk.Frame(page_tab)
    slot_page.pack()
    page_tab.add(slot_page, text="Slot modification")
    slots_configuration_mode = ttk.BooleanVar(slot_page)
    slots_configuration_mode.set(False)
    slots_frame = ttk.LabelFrame(slot_page, text="Monitoring mode", bootstyle=SUCCESS)
    slots_frame.place(x=0, y=0)
    slot_list = list()

    def refresh_slot_list():
        slot_list.clear()
        try:
            slot_num = PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                    )
                    + 0x144
                )
                + 0x24
            )
        except:
            return
        i = 0
        while i < slot_num:
            slot_addresss = (
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                    )
                    + 0x144
                )
                + 0x28
                + 0x50 * i
            )
            slot_list.append(PVZ_data.slot(slot_addresss))
            i = i + 1

    slot_type_comboboxes = []
    slot_elapsed_values = []
    slot_elapsed_entrys = []
    slot_cooldown_values = []
    slot_cooldown_entrys = []
    slot_cd_progressBars = []
    slot_isVisible_flags = []
    # slot_canUse_flags = []

    def create_slot_ui(slot_number):
        ttk.Label(slots_frame, text=f"{slot_number}").grid(
            row=slot_number - 1, column=0, sticky=W
        )
        ttk.Label(slots_frame, text="plant:").grid(
            row=slot_number - 1, column=1, sticky=W
        )

        slot_type_combobox = ttk.Combobox(
            slots_frame,
            width=12,
            values=PVZ_data.plantsType,
            state="readonly",
            bootstyle="secondary",
        )
        slot_type_combobox.grid(row=slot_number - 1, column=2, sticky=W)

        def wait_select_slot_plant(event, slot_type_combobox):
            open_card_select_window(slot_type_combobox)
            card_select_window.wait_window()
            set_slot_type()

            def closeCombobox(slot_type_combobox):
                slot_type_combobox.event_generate("<Escape>")

            slot_type_combobox.after(100, lambda: closeCombobox(slot_type_combobox))

        slot_type_combobox.bind(
            "<Button-1>",
            lambda event: wait_select_slot_plant(event, slot_type_combobox),
        )
        slot_type_comboboxes.append(slot_type_combobox)

        def set_slot_type(index=slot_number - 1):
            if slots_configuration_mode.get() is False:
                slot_list[index].setType(slot_type_combobox.current())
                slots_frame.focus_set()

        slot_elapsed_value = ttk.IntVar()
        slot_elapsed_values.append(slot_elapsed_value)
        slot_elapsed_entry = ttk.Entry(
            slots_frame,
            textvariable=slot_elapsed_value,
            width=5,
            font=("黑体", 8),
            bootstyle="secondary",
        )
        slot_elapsed_entrys.append(slot_elapsed_entry)

        def set_slot_elapsed(event, index=slot_number - 1):
            if slots_configuration_mode.get() is False:
                slot_list[index].setElapsed(slot_elapsed_value.get())
                slots_frame.focus_set()

        slot_elapsed_entry.bind("<Return>", set_slot_elapsed)

        slot_cooldown_value = ttk.IntVar()
        slot_cooldown_values.append(slot_cooldown_value)
        slot_cooldown_entry = ttk.Entry(
            slots_frame,
            textvariable=slot_cooldown_value,
            width=5,
            font=("黑体", 8),
            bootstyle="secondary",
        )
        slot_cooldown_entrys.append(slot_cooldown_entry)

        def set_slot_cooldown(event, index=slot_number - 1):
            if slots_configuration_mode.get() is False:
                slot_list[index].setCooldown(slot_cooldown_value.get())
                slots_frame.focus_set()

        slot_cooldown_entry.bind("<Return>", set_slot_cooldown)

        slot_cooldown_label = ttk.Label(slots_frame, text="Cooling progress")
        slot_cooldown_label.grid(row=slot_number - 1, column=3, padx=(2, 0))
        slot_cd_progressBar = ttk.Progressbar(
            slots_frame,
            length=80,
            mode=DETERMINATE,
            maximum=slot_cooldown_value.get(),
            variable=slot_elapsed_value,
            bootstyle="success-striped",
        )
        slot_cd_progressBar.grid(row=slot_number - 1, column=4, ipady=0)
        slot_cd_progressBars.append(slot_cd_progressBar)

        def set_cd_progressBar_focus(event):
            if slots_configuration_mode.get() is False:
                slot_cd_progressBar.focus_set()

        def set_cd_value(event, index=slot_number - 1):
            if slots_configuration_mode.get() is False:
                fraction = event.x / slot_cd_progressBar.winfo_width()
                new_value = int(fraction * slot_cd_progressBar["maximum"])
                slot_elapsed_value.set(new_value)
                slot_list[index].setElapsed(slot_elapsed_value.get())

        slot_cd_progressBar.bind("<Button-1>", set_cd_progressBar_focus)
        slot_cd_progressBar.bind("<ButtonRelease-1>", set_cd_value)

        slot_isVisible_flag = ttk.BooleanVar(slots_frame)
        slot_isVisible_flags.append(slot_isVisible_flag)

        def change_slot_isVisible(index=slot_number - 1):
            if slots_configuration_mode.get() is False:
                slot_list[index].setIsVisible(not slot_isVisible_flag.get())

        ttk.Checkbutton(
            slots_frame,
            text="Invisible",
            bootstyle="danger-round-toggle",
            variable=slot_isVisible_flag,
            command=lambda: change_slot_isVisible(),
        ).grid(row=slot_number - 1, column=5)
        # slot_canUse_flag=ttk.BooleanVar(slots_frame)
        # slot_canUse_flags.append(slot_canUse_flag)
        # def change_slot_canUse(index=slot_number-1):
        #     slot_list[index].setCanUse(slot_canUse_flag.get())
        # ttk.Checkbutton(slots_frame,text="可用",bootstyle="danger-round-toggle",variable=slot_canUse_flag,command=lambda:change_slot_canUse()).grid(row=slot_number-1,column=6)

    # 为slots 1至14创建UI组件
    for slot_number in range(1, 17):
        create_slot_ui(slot_number)

    slots_config_frame = ttk.LabelFrame(slot_page, text="Card slot settings", bootstyle=SUCCESS)
    slots_config_frame.place(x=0, y=0, relx=1, anchor=NE)
    slot_num_frame = ttk.Frame(slots_config_frame)
    slot_num_frame.pack()
    ttk.Label(slot_num_frame, text="Number of card slots:").pack(side=LEFT)
    slots_num_value = ttk.IntVar()
    slots_num_combobox = ttk.Combobox(
        slot_num_frame,
        textvariable=slots_num_value,
        width=2,
        values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        font=("黑体", 8),
        bootstyle=SECONDARY,
        state=READONLY,
    )
    slots_num_combobox.pack(side=LEFT)

    def setSlotsNum(event):
        PVZ_data.PVZ_memory.write_int(
            PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                )
                + 0x144
            )
            + 0x24,
            slots_num_value.get(),
        )
        slot_num_frame.focus_set()

    slots_num_combobox.bind("<<ComboboxSelected>>", setSlotsNum)
    no_slot_status = ttk.BooleanVar(slots_config_frame)
    no_slot_check = ttk.Checkbutton(
        slots_config_frame,
        text="No need to choose a card",
        variable=no_slot_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.noSolt(no_slot_status.get()),
    )
    no_slot_check.pack(pady=5, anchor=W)
    ToolTip(no_slot_check, text="You can start the game without choosing a card", bootstyle=(INFO, INVERSE))
    change_all_frame = ttk.Frame(slots_config_frame)
    change_all_frame.pack(pady=(0, 10))
    ttk.Label(change_all_frame, text="Modify all card slots:").pack(anchor=W)
    change_all_combobox = ttk.Combobox(
        change_all_frame,
        width=12,
        values=PVZ_data.plantsType,
        state="readonly",
        bootstyle="secondary",
    )
    change_all_combobox.pack()

    def wait_select_all_slot_plant(event, change_all_combobox):
        open_card_select_window(change_all_combobox)
        card_select_window.wait_window()
        for slot in slot_list:
            slot.setType(change_all_combobox.current())

        def closeCombobox(change_all_combobox):
            change_all_combobox.event_generate("<Escape>")

        change_all_combobox.after(100, lambda: closeCombobox(change_all_combobox))

    change_all_combobox.bind(
        "<Button-1>",
        lambda event: wait_select_all_slot_plant(event, change_all_combobox),
    )
    random_slots_status = ttk.BooleanVar(slots_config_frame)
    random_slots_haszombie_status = ttk.BooleanVar(slots_config_frame)
    random_slots_check = ttk.Checkbutton(
        slots_config_frame,
        text="Random changes in card slot",
        variable=random_slots_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.randomSlots(
            random_slots_status.get(), random_slots_haszombie_status.get()
        ),
    )
    random_slots_check.pack(pady=5, anchor=W)
    random_slots_haszombie_check = ttk.Checkbutton(
        slots_config_frame,
        text="Zombie card slot",
        variable=random_slots_haszombie_status,
    )
    random_slots_haszombie_check.pack()

    card_select_frame = ttk.LabelFrame(slot_page, text="Card selection configuration", bootstyle=DARK)
    card_select_frame.place(x=0, y=180, relx=1, anchor=NE)

    def changeSlotsConfiguration():
        if slots_configuration_mode.get() is True:
            slots_frame.configure(text="Configuration mode", bootstyle=DARK)
        else:
            slots_frame.configure(text="Monitoring mode", bootstyle=SUCCESS)

    slots_configuration_change = ttk.Checkbutton(
        card_select_frame,
        text="Configuration mode",
        variable=slots_configuration_mode,
        bootstyle="dark-round-toggle",
        command=lambda: changeSlotsConfiguration(),
    )
    slots_configuration_change.pack()
    ToolTip(
        slots_configuration_change,
        text="After turning on the left side card slot into the configuration mode, you can configure the card selection scheme",
        bootstyle=(INFO, INVERSE),
    )
    # card_select_combobox = ttk.Combobox(card_select_frame, width=12, values=data.plantsType, state='readonly', bootstyle='secondary')
    # card_select_combobox.pack()
    # ttk.Button(card_select_frame,text="选卡",command=lambda:pvz.selectCard(card_select_combobox.current())).pack()
    # ttk.Button(card_select_frame,text="退卡",command=lambda:pvz.deselectCard(card_select_combobox.current())).pack()
    new_solts_config_frame = ttk.Frame(card_select_frame)
    new_solts_config_frame.pack()
    new_solts_config_entry = ttk.Entry(
        new_solts_config_frame, width=8, font=("宋体", 8)
    )
    new_solts_config_entry.pack(side=LEFT)

    def create_slots_config():
        if slots_configuration_mode.get() is True:
            if new_solts_config_entry.get() == "":
                Messagebox.show_error("Please enter the configuration name", title="Create configuration failure")
            else:
                config = load_config(config_file_path)
                if "slots" not in config:
                    config["slots"] = {}
                if new_solts_config_entry.get() not in config["slots"]:
                    config["slots"][new_solts_config_entry.get()] = {}
                plants = []
                for c in slot_type_comboboxes:
                    plants.append(c.current())
                config["slots"][new_solts_config_entry.get()]["plants"] = plants
                save_config(config, config_file_path)
                Messagebox.show_info(
                    "Configuration "" + new_solts_config_entry.get() + """,
                    title="Create configuration successfully",
                )
                update_slots_config_combobox()
                slots_config_combobox.set(new_solts_config_entry.get())
        else:
            Messagebox.show_error("Please modify the card slot configuration in the configuration mode", title="Create configuration failure")

    new_solts_config_button = ttk.Button(
        new_solts_config_frame,
        text="Newly built",
        padding=0,
        bootstyle=(DARK, OUTLINE),
        command=lambda: create_slots_config(),
    )
    new_solts_config_button.pack(side=LEFT)
    slots_config_combobox = ttk.Combobox(
        card_select_frame, width=12, bootstyle="secondary"
    )
    slots_config_combobox.pack()
    slots_config_combobox.insert(0, "Select configuration")
    slots_config_combobox.configure(state=READONLY)

    def update_slots_config_combobox():
        config = load_config(config_file_path)
        if "slots" not in config:
            return
        slots_config_combobox.configure(values=list(config["slots"].keys()))

    update_slots_config_combobox()

    def set_config_slots(event):
        if slots_configuration_mode.get() is False:
            slots_configuration_mode.set(True)
            changeSlotsConfiguration()
        config = load_config(config_file_path)
        n = 0
        for i in config["slots"][slots_config_combobox.get()]["plants"]:
            slot_type_comboboxes[n].current(i)
            n = n + 1

    slots_config_combobox.bind("<<ComboboxSelected>>", set_config_slots)
    card_select_button_frame = ttk.Frame(card_select_frame)
    card_select_button_frame.pack()

    def save_slots_config():
        if slots_configuration_mode.get() is True:
            config = load_config(config_file_path)
            if "slots" not in config:
                config["slots"] = {}
            if slots_config_combobox.get() not in config["slots"]:
                Messagebox.show_error(
                    "The configuration name does not exist, please create a new configuration first", title="Save the configuration failure"
                )
            plants = []
            for c in slot_type_comboboxes:
                plants.append(c.current())
            config["slots"][slots_config_combobox.get()]["plants"] = plants
            save_config(config, config_file_path)
            Messagebox.show_info(
                "Configuration "" + slots_config_combobox.get() + """, title="Save the configuration successfully"
            )
            update_slots_config_combobox()
        else:
            Messagebox.show_error("Please modify the card slot configuration in the configuration mode", title="Save the configuration failure")

    def delete_slots_config():
        if slots_configuration_mode.get() is True:
            config = load_config(config_file_path)
            if "slots" not in config:
                config["slots"] = {}
            if slots_config_combobox.get() not in config["slots"]:
                Messagebox.show_error("The configuration name does not exist", title="Delete configuration failure")
            del config["slots"][slots_config_combobox.get()]
            save_config(config, config_file_path)
            Messagebox.show_info(
                "Configuration" + slots_config_combobox.get() + "”Deleted", title="Delete the configuration successfully"
            )
            update_slots_config_combobox()
        else:
            Messagebox.show_error("Please modify the card slot configuration in the configuration mode", title="Delete configuration failure")

    def select_slots_config():
        card_list = [999] * 14
        try:
            selected_num = PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x774
                )
                + 0xD24
            )
        except:
            Messagebox.show_error(
                "Please use the card selection card on the card selection interface\nPlease click on the application in the level", title="Card selection failed"
            )
            return
        if selected_num != 0:
            i = 0
            j = 0
            while j < selected_num:
                if i == 48:
                    i = i + 27
                if (
                    PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(
                            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x774
                        )
                        + 0xC8
                        + 0x3C * i
                    )
                    == 1
                ):
                    n = int(
                        (
                            PVZ_data.PVZ_memory.read_int(
                                PVZ_data.PVZ_memory.read_int(
                                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress)
                                    + 0x774
                                )
                                + 0xA4
                                + 0x3C * i
                            )
                            - 79
                        )
                        / 51
                    )
                    print("Card slot" + str(n) + "Tensor" + PVZ_data.plantsType[i])
                    card_list[n] = i
                    j = j + 1
                i = i + 1
        for c in slot_type_comboboxes:
            selected_num = PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x774
                )
                + 0xD24
            )
            limit_num = PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                    )
                    + 0x144
                )
                + 0x24
            )
            print(selected_num, limit_num)
            if selected_num < limit_num:
                if c.current() > 47 and c.current() < 75:
                    Messagebox.show_error(
                        "Can't choose a special card\nIf you need to use a special card, please click on the application after starting the game",
                        title="Card selection failed",
                    )
                    for c in reversed(card_list):
                        if c != 999:
                            print(c)
                            pvz.deselectCard(c)
                    return
                if c.current() not in card_list:
                    pvz.selectCard(c.current())
                    print(c.current())
                    card_list[selected_num] = c.current()
                else:
                    print("------")
                    Messagebox.show_error(
                        "Can't choose duplicate cards\nIf you need to use the same card, please click on the application after starting the game",
                        title="Card selection failed",
                    )
                    for c in reversed(card_list):
                        if c != 999:
                            print(c)
                            pvz.deselectCard(c)
                    return

    def clear_slots():
        card_list = [999] * 14
        try:
            selected_num = PVZ_data.PVZ_memory.read_int(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x774
                )
                + 0xD24
            )
        except:
            Messagebox.show_error("Please use it on the card selection interface", title="Clear card selection failed")
            return
        if selected_num != 0:
            i = 0
            j = 0
            while j < selected_num:
                if i == 48:
                    i = i + 27
                if (
                    PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(
                            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x774
                        )
                        + 0xC8
                        + 0x3C * i
                    )
                    == 1
                    or PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(
                            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x774
                        )
                        + 0xC8
                        + 0x3C * i
                    )
                    == 0
                ):
                    n = int(
                        (
                            PVZ_data.PVZ_memory.read_int(
                                PVZ_data.PVZ_memory.read_int(
                                    PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress)
                                    + 0x774
                                )
                                + 0xA4
                                + 0x3C * i
                            )
                            - 79
                        )
                        / 51
                    )
                    print("Card slot" + str(n) + "Tensor" + PVZ_data.plantsType[i])
                    card_list[n] = i
                    j = j + 1
                i = i + 1
        for c in reversed(card_list):
            if c != 999:
                print(c)
                pvz.deselectCard(c)

    def apply_slots_config():
        if slots_configuration_mode.get() is True:
            i = 0
            for c in slot_type_comboboxes:
                slot_list[i].setType(c.current())
                i = i + 1
            slots_configuration_mode.set(False)
            changeSlotsConfiguration()
        else:
            Messagebox.show_error("Please apply card slot configuration in configuration mode", title="Application configuration failed")

    ttk.Button(
        card_select_button_frame,
        text="keep",
        padding=0,
        bootstyle=(DARK, OUTLINE),
        command=lambda: save_slots_config(),
    ).grid(row=0, column=0)
    ttk.Button(
        card_select_button_frame,
        text="delete",
        padding=0,
        bootstyle=(DARK, OUTLINE),
        command=lambda: delete_slots_config(),
    ).grid(row=0, column=1)
    ttk.Button(
        card_select_button_frame,
        text="Choose a card",
        padding=0,
        bootstyle=(DARK, OUTLINE),
        command=lambda: select_slots_config(),
    ).grid(row=1, column=0)
    ttk.Button(
        card_select_button_frame,
        text="Clear Card",
        padding=0,
        bootstyle=(DARK, OUTLINE),
        command=lambda: clear_slots(),
    ).grid(row=1, column=1)
    ttk.Button(
        card_select_button_frame,
        text="application",
        padding=0,
        bootstyle=(DARK, OUTLINE),
        command=lambda: apply_slots_config(),
    ).grid(row=1, column=2)

    card_select_frame = ttk.LabelFrame(common_page, text="Fast planting", bootstyle=PRIMARY)
    card_select_frame.place(x=0, y=540, relx=0, anchor=NW)
    ttk.Label(card_select_frame, text="1:").grid(row=0, column=0)
    slot_1_key = ttk.Combobox(
        card_select_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_1_key.grid(row=0, column=1)
    slot_1_key.current(2)
    ttk.Label(card_select_frame, text="2:").grid(row=0, column=2)
    slot_2_key = ttk.Combobox(
        card_select_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_2_key.grid(row=0, column=3)
    slot_2_key.current(3)
    ttk.Label(card_select_frame, text="3:").grid(row=0, column=4)
    slot_3_key = ttk.Combobox(
        card_select_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_3_key.grid(row=0, column=5)
    slot_3_key.current(4)
    ttk.Label(card_select_frame, text="4:").grid(row=0, column=6)
    slot_4_key = ttk.Combobox(
        card_select_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_4_key.grid(row=0, column=7)
    slot_4_key.current(5)
    ttk.Label(card_select_frame, text="5:").grid(row=0, column=8)
    slot_5_key = ttk.Combobox(
        card_select_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_5_key.grid(row=0, column=9)
    slot_5_key.current(6)
    ttk.Label(card_select_frame, text="6:").grid(row=0, column=10)
    slot_6_key = ttk.Combobox(
        card_select_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_6_key.grid(row=0, column=11)
    slot_6_key.current(7)
    ttk.Label(card_select_frame, text="7:").grid(row=0, column=12)
    slot_7_key = ttk.Combobox(
        card_select_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_7_key.grid(row=0, column=13)
    slot_7_key.current(8)
    ttk.Label(card_select_frame, text="8:").grid(row=1, column=0)
    slot_8_key = ttk.Combobox(
        card_select_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_8_key.grid(row=1, column=1)
    slot_8_key.current(9)
    ttk.Label(card_select_frame, text="9:").grid(row=1, column=2)
    slot_9_key = ttk.Combobox(
        card_select_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_9_key.grid(row=1, column=3)
    slot_9_key.current(10)
    ttk.Label(card_select_frame, text="10:").grid(row=1, column=4)
    slot_10_key = ttk.Combobox(
        card_select_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_10_key.grid(row=1, column=5)
    slot_10_key.current(1)
    ttk.Label(card_select_frame, text="11:").grid(row=1, column=6)
    slot_11_key = ttk.Combobox(
        card_select_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_11_key.grid(row=1, column=7)
    slot_11_key.current(27)
    ttk.Label(card_select_frame, text="12:").grid(row=1, column=8)
    slot_12_key = ttk.Combobox(
        card_select_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_12_key.grid(row=1, column=9)
    slot_12_key.current(33)
    ttk.Label(card_select_frame, text="13:").grid(row=1, column=10)
    slot_13_key = ttk.Combobox(
        card_select_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_13_key.grid(row=1, column=11)
    slot_13_key.current(15)
    ttk.Label(card_select_frame, text="14:").grid(row=1, column=12)
    slot_14_key = ttk.Combobox(
        card_select_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_14_key.grid(row=1, column=13)
    slot_14_key.current(28)
    function_key_frame = ttk.Frame(card_select_frame)
    function_key_frame.grid(row=2, column=0, columnspan=14)
    shovel_key_label = ttk.Label(function_key_frame, text="Shovel:")
    shovel_key_label.grid(row=0, column=0)
    slot_shovel_key = ttk.Combobox(
        function_key_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_shovel_key.grid(row=0, column=1)
    slot_shovel_key.current(36)
    # ToolTip(shovel_key_label, text="Shovel", bootstyle=(INFO, INVERSE))
    zombie_hp_key_label = ttk.Label(function_key_frame, text="Zombies show blood:")
    zombie_hp_key_label.grid(row=0, column=2)
    slot_zombie_hp_key = ttk.Combobox(
        function_key_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_zombie_hp_key.grid(row=0, column=3)
    slot_zombie_hp_key.current(34)
    # ToolTip(zombie_hp_key_label, text="显示僵尸血量", bootstyle=(INFO, INVERSE))
    plant_hp_key_label = ttk.Label(function_key_frame, text="Bleeding:")
    plant_hp_key_label.grid(row=0, column=4)
    slot_plant_hp_key = ttk.Combobox(
        function_key_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_plant_hp_key.grid(row=0, column=5)
    slot_plant_hp_key.current(13)
    # ToolTip(plant_hp_key_label, text="显示僵尸血量", bootstyle=(INFO, INVERSE))
    top_key_label = ttk.Label(function_key_frame, text="Stuck:")
    top_key_label.grid(row=0, column=6)
    slot_top_key = ttk.Combobox(
        function_key_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_top_key.grid(row=0, column=7)
    slot_top_key.current(32)
    # ToolTip(top_key_label, text="卡槽置顶", bootstyle=(INFO, INVERSE))
    speed_key_label = ttk.Label(function_key_frame, text="Gaming accelerate:")
    speed_key_label.grid(row=0, column=8)
    slot_speed_key = ttk.Combobox(
        function_key_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_speed_key.grid(row=0, column=9)
    slot_speed_key.current(24)
    bag_key_label = ttk.Label(function_key_frame, text="Use item:")
    bag_key_label.grid(row=1, column=0)
    slot_bag_key = ttk.Combobox(
        function_key_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_bag_key.grid(row=1, column=1)
    slot_bag_key.current(12)
    slot_15_key_label = ttk.Label(function_key_frame, text="15:")
    slot_15_key_label.grid(row=1, column=2)
    slot_15_key = ttk.Combobox(
        function_key_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_15_key.grid(row=1, column=3)
    slot_15_key.current(PVZ_data.keyTpye.index("T"))
    slot_16_key_label = ttk.Label(function_key_frame, text="16:")
    slot_16_key_label.grid(row=1, column=4)
    slot_16_key = ttk.Combobox(
        function_key_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_16_key.grid(row=1, column=5)
    slot_16_key.current(PVZ_data.keyTpye.index("Y"))
    reserved3_key_label = ttk.Label(function_key_frame, text="Reserved fast:")
    reserved3_key_label.grid(row=1, column=6)
    slot_reserved3_key = ttk.Combobox(
        function_key_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_reserved3_key.grid(row=1, column=7)
    slot_reserved3_key.current(0)
    reserved4_key_label = ttk.Label(function_key_frame, text="Reserved fast:")
    reserved4_key_label.grid(row=1, column=8)
    slot_reserved4_key = ttk.Combobox(
        function_key_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_reserved4_key.grid(row=1, column=9)
    slot_reserved4_key.current(0)
    reserved5_key_label = ttk.Label(function_key_frame, text="Reserved fast:")
    reserved5_key_label.grid(row=2, column=0)
    slot_reserved5_key = ttk.Combobox(
        function_key_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_reserved5_key.grid(row=2, column=1)
    slot_reserved5_key.current(0)
    reserved6_key_label = ttk.Label(function_key_frame, text="Reserved fast:")
    reserved6_key_label.grid(row=2, column=2)
    slot_reserved6_key = ttk.Combobox(
        function_key_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_reserved6_key.grid(row=2, column=3)
    slot_reserved6_key.current(0)
    reserved7_key_label = ttk.Label(function_key_frame, text="Reserved fast:")
    reserved7_key_label.grid(row=2, column=4)
    slot_reserved7_key = ttk.Combobox(
        function_key_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_reserved7_key.grid(row=2, column=5)
    slot_reserved7_key.current(0)
    reserved8_key_label = ttk.Label(function_key_frame, text="Reserved fast:")
    reserved8_key_label.grid(row=2, column=6)
    slot_reserved8_key = ttk.Combobox(
        function_key_frame,
        width=3,
        values=PVZ_data.keyTpye,
        font=("黑体", 8),
        state=READONLY,
    )
    slot_reserved8_key.grid(row=2, column=7)
    slot_reserved8_key.current(0)

    def loadSlotKey():
        config = load_config(config_file_path)
        try:
            slot_1_key.current(config["slotKeys"]["1"])
        except:
            pass
        try:
            slot_2_key.current(config["slotKeys"]["2"])
        except:
            pass
        try:
            slot_3_key.current(config["slotKeys"]["3"])
        except:
            pass
        try:
            slot_4_key.current(config["slotKeys"]["4"])
        except:
            pass
        try:
            slot_5_key.current(config["slotKeys"]["5"])
        except:
            pass
        try:
            slot_6_key.current(config["slotKeys"]["6"])
        except:
            pass
        try:
            slot_7_key.current(config["slotKeys"]["7"])
        except:
            pass
        try:
            slot_8_key.current(config["slotKeys"]["8"])
        except:
            pass
        try:
            slot_9_key.current(config["slotKeys"]["9"])
        except:
            pass
        try:
            slot_10_key.current(config["slotKeys"]["10"])
        except:
            pass
        try:
            slot_11_key.current(config["slotKeys"]["11"])
        except:
            pass
        try:
            slot_12_key.current(config["slotKeys"]["12"])
        except:
            pass
        try:
            slot_13_key.current(config["slotKeys"]["13"])
        except:
            pass
        try:
            slot_14_key.current(config["slotKeys"]["14"])
        except:
            pass
        try:
            slot_shovel_key.current(config["slotKeys"]["shovel"])
        except:
            pass
        try:
            slot_zombie_hp_key.current(config["slotKeys"]["zombie_hp"])
        except:
            pass
        try:
            slot_plant_hp_key.current(config["slotKeys"]["plant_hp"])
        except:
            pass
        try:
            slot_top_key.current(config["slotKeys"]["top"])
        except:
            pass
        try:
            slot_speed_key.current(config["slotKeys"]["speed"])
        except:
            pass
        try:
            slot_bag_key.current(config["slotKeys"]["bag"])
        except:
            pass
        try:
            slot_15_key.current(config["slotKeys"]["15"])
        except:
            pass
        try:
            slot_16_key.current(config["slotKeys"]["16"])
        except:
            pass

    loadSlotKey()

    def setSlotKey():
        if slot_key_status.get():
            config = load_config(config_file_path)
            if "slotKeys" not in config:
                config["slotKeys"] = {}
            slot_key_list = list()
            if slot_1_key.current() != -1:
                config["slotKeys"]["1"] = slot_1_key.current()
                slot_key_list.append(slot_1_key.current())
            if slot_2_key.current() != -1:
                if (
                    slot_2_key.current() not in slot_key_list
                    or slot_2_key.current() == 0
                ):
                    config["slotKeys"]["2"] = slot_2_key.current()
                    slot_key_list.append(slot_2_key.current())
                else:
                    Messagebox.show_error("Shortcut key 2 repeat", title="Do not set the same shortcut keys")
                    slot_key_status.set(False)
                    return ()
            if slot_3_key.current() != -1:
                if (
                    slot_3_key.current() not in slot_key_list
                    or slot_3_key.current() == 0
                ):
                    config["slotKeys"]["3"] = slot_3_key.current()
                    slot_key_list.append(slot_3_key.current())
                else:
                    Messagebox.show_error("Shortcut key 3 repeat", title="Do not set the same shortcut keys")
                    slot_key_status.set(False)
                    return ()

            if slot_4_key.current() != -1:
                if (
                    slot_4_key.current() not in slot_key_list
                    or slot_4_key.current() == 0
                ):
                    config["slotKeys"]["4"] = slot_4_key.current()
                    slot_key_list.append(slot_4_key.current())
                else:
                    Messagebox.show_error("Shortcut key 4 repeat", title="Do not set the same shortcut keys")
                    slot_key_status.set(False)
                    return ()

            if slot_5_key.current() != -1:
                if (
                    slot_5_key.current() not in slot_key_list
                    or slot_5_key.current() == 0
                ):
                    config["slotKeys"]["5"] = slot_5_key.current()
                    slot_key_list.append(slot_5_key.current())
                else:
                    Messagebox.show_error("Shortcut key 5 repeat", title="Do not set the same shortcut keys")
                    slot_key_status.set(False)
                    return ()

            if slot_6_key.current() != -1:
                if (
                    slot_6_key.current() not in slot_key_list
                    or slot_6_key.current() == 0
                ):
                    config["slotKeys"]["6"] = slot_6_key.current()
                    slot_key_list.append(slot_6_key.current())
                else:
                    Messagebox.show_error("Shortcut key 6 repeat", title="Do not set the same shortcut keys")
                    slot_key_status.set(False)
                    return ()

            if slot_7_key.current() != -1:
                if (
                    slot_7_key.current() not in slot_key_list
                    or slot_7_key.current() == 0
                ):
                    config["slotKeys"]["7"] = slot_7_key.current()
                    slot_key_list.append(slot_7_key.current())
                else:
                    Messagebox.show_error("Shortcut keys 7 repeat", title="Do not set the same shortcut keys")
                    slot_key_status.set(False)
                    return ()

            if slot_8_key.current() != -1:
                if (
                    slot_8_key.current() not in slot_key_list
                    or slot_8_key.current() == 0
                ):
                    config["slotKeys"]["8"] = slot_8_key.current()
                    slot_key_list.append(slot_8_key.current())
                else:
                    Messagebox.show_error("Shortcut keys 8 repeat", title="Do not set the same shortcut keys")
                    slot_key_status.set(False)
                    return ()

            if slot_9_key.current() != -1:
                if (
                    slot_9_key.current() not in slot_key_list
                    or slot_9_key.current() == 0
                ):
                    config["slotKeys"]["9"] = slot_9_key.current()
                    slot_key_list.append(slot_9_key.current())
                else:
                    Messagebox.show_error("Shortcut keys 9 repeat", title="Do not set the same shortcut keys")
                    slot_key_status.set(False)
                    return ()

            if slot_10_key.current() != -1:
                if (
                    slot_10_key.current() not in slot_key_list
                    or slot_10_key.current() == 0
                ):
                    config["slotKeys"]["10"] = slot_10_key.current()
                    slot_key_list.append(slot_10_key.current())
                else:
                    Messagebox.show_error("Shortcut keys 10 repeat", title="Do not set the same shortcut keys")
                    slot_key_status.set(False)
                    return ()

            if slot_11_key.current() != -1:
                if (
                    slot_11_key.current() not in slot_key_list
                    or slot_11_key.current() == 0
                ):
                    config["slotKeys"]["11"] = slot_11_key.current()
                    slot_key_list.append(slot_11_key.current())
                else:
                    Messagebox.show_error("Shortcut keys 11 repeat", title="Do not set the same shortcut keys")
                    slot_key_status.set(False)
                    return ()

            if slot_12_key.current() != -1:
                if (
                    slot_12_key.current() not in slot_key_list
                    or slot_12_key.current() == 0
                ):
                    config["slotKeys"]["12"] = slot_12_key.current()
                    slot_key_list.append(slot_12_key.current())
                else:
                    Messagebox.show_error("Shortcut key 12 repeat", title="Do not set the same shortcut keys")
                    slot_key_status.set(False)
                    return ()

            if slot_13_key.current() != -1:
                if (
                    slot_13_key.current() not in slot_key_list
                    or slot_13_key.current() == 0
                ):
                    config["slotKeys"]["13"] = slot_13_key.current()
                    slot_key_list.append(slot_13_key.current())
                else:
                    Messagebox.show_error("Shortcut key 13 repeat", title="Do not set the same shortcut keys")
                    slot_key_status.set(False)
                    return ()

            if slot_14_key.current() != -1:
                if (
                    slot_14_key.current() not in slot_key_list
                    or slot_14_key.current() == 0
                ):
                    config["slotKeys"]["14"] = slot_14_key.current()
                    slot_key_list.append(slot_14_key.current())
                else:
                    Messagebox.show_error("Shortcut key 14 repeat", title="Do not set the same shortcut keys")
                    slot_key_status.set(False)
                    return ()
            if slot_15_key.current() != -1:
                if (
                    slot_15_key.current() not in slot_key_list
                    or slot_15_key.current() == 0
                ):
                    config["slotKeys"]["15"] = slot_15_key.current()
                    slot_key_list.append(slot_15_key.current())
                else:
                    Messagebox.show_error("Shortcut key 15 repeat", title="Do not set the same shortcut keys")
                    slot_key_status.set(False)
                    return ()
            if slot_16_key.current() != -1:
                if (
                    slot_16_key.current() not in slot_key_list
                    or slot_16_key.current() == 0
                ):
                    config["slotKeys"]["16"] = slot_16_key.current()
                    slot_key_list.append(slot_16_key.current())
                else:
                    Messagebox.show_error("Shortcut key 16 repeat", title="Do not set the same shortcut keys")
                    slot_key_status.set(False)
                    return ()
            if slot_shovel_key.current() != -1:
                if (
                    slot_shovel_key.current() not in slot_key_list
                    or slot_shovel_key.current() == 0
                ):
                    config["slotKeys"]["shovel"] = slot_shovel_key.current()
                    slot_key_list.append(slot_shovel_key.current())
                else:
                    Messagebox.show_error("Repeat the shovel shortcut key", title="Do not set the same shortcut keys")
                    slot_key_status.set(False)
                    return ()
            if slot_zombie_hp_key.current() != -1:
                if (
                    slot_zombie_hp_key.current() not in slot_key_list
                    or slot_zombie_hp_key.current() == 0
                ):
                    config["slotKeys"]["zombie_hp"] = slot_zombie_hp_key.current()
                    slot_key_list.append(slot_zombie_hp_key.current())
                else:
                    Messagebox.show_error(
                        "Zombies show blood shortcut keys repeated", title="Do not set the same shortcut keys"
                    )
                    slot_key_status.set(False)
                    return ()
            if slot_plant_hp_key.current() != -1:
                if (
                    slot_plant_hp_key.current() not in slot_key_list
                    or slot_plant_hp_key.current() == 0
                ):
                    config["slotKeys"]["plant_hp"] = slot_plant_hp_key.current()
                    slot_key_list.append(slot_plant_hp_key.current())
                else:
                    Messagebox.show_error(
                        "Plant blood shortcut keys repeated", title="Do not set the same shortcut keys"
                    )
                    slot_key_status.set(False)
                    return ()
            if slot_top_key.current() != -1:
                if (
                    slot_top_key.current() not in slot_key_list
                    or slot_top_key.current() == 0
                ):
                    config["slotKeys"]["top"] = slot_top_key.current()
                    slot_key_list.append(slot_top_key.current())
                else:
                    Messagebox.show_error(
                        "Card slot top shortcut key repeat", title="Do not set the same shortcut keys"
                    )
                    slot_key_status.set(False)
                    return ()
            if slot_speed_key.current() != -1:
                if (
                    slot_speed_key.current() not in slot_key_list
                    or slot_speed_key.current() == 0
                ):
                    config["slotKeys"]["speed"] = slot_speed_key.current()
                    slot_key_list.append(slot_speed_key.current())
                else:
                    Messagebox.show_error(
                        "Game acceleration shortcut key repeat", title="Do not set the same shortcut keys"
                    )
                    slot_key_status.set(False)
                    return ()
            if slot_bag_key.current() != -1:
                if (
                    slot_bag_key.current() not in slot_key_list
                    or slot_bag_key.current() == 0
                ):
                    config["slotKeys"]["bag"] = slot_bag_key.current()
                    slot_key_list.append(slot_bag_key.current())
                else:
                    Messagebox.show_error(
                        "Use item shortcut keys to repeat", title="Do not set the same shortcut keys"
                    )
                    slot_key_status.set(False)
                    return ()

            save_config(config, config_file_path)
            slot_key_list = config["slotKeys"]
            pvz.slotKey(slot_key_list)
        else:
            pvz.slotKey(False)

    slot_key_status = ttk.BooleanVar(function_key_frame)
    slot_key_check = ttk.Checkbutton(
        function_key_frame,
        text="开启",
        variable=slot_key_status,
        bootstyle="primary-round-toggle",
        command=lambda: setSlotKey(),
    )
    slot_key_check.grid(row=2, column=8, columnspan=4)

    hp_show_frame = ttk.LabelFrame(common_page, text="Renovation of blood", bootstyle=DANGER)
    hp_show_frame.place(x=505, y=440, relx=0, anchor=NW)
    fog_hp_status = ttk.BooleanVar(hp_show_frame)
    fog_hp_check = ttk.Checkbutton(
        hp_show_frame,
        text="Dense fog show blood",
        variable=fog_hp_status,
        bootstyle="danger-round-toggle",
        command=lambda: pvz.fogDraw(fog_hp_status.get()),
    )
    fog_hp_check.pack()
    invisible_hp_status = ttk.BooleanVar(hp_show_frame)
    invisible_hp_check = ttk.Checkbutton(
        hp_show_frame,
        text="Invisible blood",
        variable=invisible_hp_status,
        bootstyle="danger-round-toggle",
        command=lambda: pvz.invisibleDraw(invisible_hp_status.get()),
    )
    invisible_hp_check.pack()
    boss_hp_status = ttk.BooleanVar(hp_show_frame)
    boss_hp_check = ttk.Checkbutton(
        hp_show_frame,
        text="Ritual king showed blood",
        variable=boss_hp_status,
        bootstyle="danger-round-toggle",
        command=lambda: pvz.bossHPDraw(boss_hp_status.get()),
    )
    boss_hp_check.pack()

    boss_correct_status = ttk.BooleanVar(common_page)
    boss_correct_check = ttk.Checkbutton(
        common_page,
        text="King\nCorrection",
        variable=boss_correct_status,
        bootstyle="danger-round-toggle",
        command=lambda: pvz.bossCorrect(boss_correct_status.get()),
    )
    boss_correct_check.place(x=505, y=525, relx=0, anchor=NW)

    # 定义一个函数来更新slot的属性
    def get_slot_attribute():
        for index, slot in enumerate(slot_list):
            try:
                slot_type_comboboxes[index].current(slot.type)
                if (
                    slot_page.focus_get() != slot_cooldown_entrys[index]
                    and slot_page.focus_get() != slot_cd_progressBars[index]
                ):
                    slot_cooldown_values[index].set(slot.cooldown)
                    slot_cd_progressBars[index].configure(
                        maximum=slot_cooldown_values[index].get()
                    )
                if (
                    slot_page.focus_get() != slot_elapsed_entrys[index]
                    and slot_page.focus_get() != slot_cd_progressBars[index]
                ):
                    slot_elapsed_values[index].set(slot.elapsed)
                slot_isVisible_flags[index].set(not slot.isViible)
                # slot_canUse_flags[index].set(slot.canUse)
            except:
                pass
        try:
            slots_num_value.set(
                PVZ_data.PVZ_memory.read_int(
                    PVZ_data.PVZ_memory.read_int(
                        PVZ_data.PVZ_memory.read_int(
                            PVZ_data.PVZ_memory.read_int(PVZ_data.baseAddress) + 0x768
                        )
                        + 0x144
                    )
                    + 0x24
                )
            )
        except:
            pass

    other_page = ttk.Frame(page_tab)
    other_page.pack()
    page_tab.add(other_page, text="Non -category")
    other_toggle_frame = ttk.LabelFrame(other_page, text="Uncategal switch")
    other_toggle_frame.pack(anchor=W)

    doom_no_hole_status = ttk.BooleanVar(other_toggle_frame)
    bone_no_hole_status = ttk.BooleanVar(other_toggle_frame)
    treasure_no_hole_status = ttk.BooleanVar(other_toggle_frame)
    doom_no_hole_check = ttk.Checkbutton(
        other_toggle_frame,
        text="Destroy",
        variable=doom_no_hole_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.noHole(
            doom_no_hole_status.get(),
            bone_no_hole_status.get(),
            treasure_no_hole_status.get(),
        ),
    )
    doom_no_hole_check.pack()
    bone_no_hole_check = ttk.Checkbutton(
        other_toggle_frame,
        text="Skeleton does not leave a pit",
        variable=bone_no_hole_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.noHole(
            doom_no_hole_status.get(),
            bone_no_hole_status.get(),
            treasure_no_hole_status.get(),
        ),
    )
    bone_no_hole_check.pack()
    treasure_no_hole_check = ttk.Checkbutton(
        other_toggle_frame,
        text="Treasure does not leave a pit",
        variable=treasure_no_hole_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.noHole(
            doom_no_hole_status.get(),
            bone_no_hole_status.get(),
            treasure_no_hole_status.get(),
        ),
    )
    treasure_no_hole_check.pack()
    zombiebean_hpynotized_status = ttk.BooleanVar(other_toggle_frame)
    zombiebean_hpynotized_check = ttk.Checkbutton(
        other_toggle_frame,
        text="Zombie Bean Charm",
        variable=zombiebean_hpynotized_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.zombiebeanHpynotized(zombiebean_hpynotized_status.get()),
    )
    zombiebean_hpynotized_check.pack()
    conveyor_belt_full_status = ttk.BooleanVar(other_toggle_frame)
    conveyor_belt_full_check = ttk.Checkbutton(
        other_toggle_frame,
        text="The conveyor belt is full",
        variable=conveyor_belt_full_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.conveyorBeltFull(conveyor_belt_full_status.get()),
    )
    conveyor_belt_full_check.pack()
    scrap_helmet_controlled_status = ttk.BooleanVar(other_toggle_frame)
    scrap_helmet_controlled_check = ttk.Checkbutton(
        other_toggle_frame,
        text="The abandoned manuscript is controlled",
        variable=scrap_helmet_controlled_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.scrapHelmetControlled(scrap_helmet_controlled_status.get()),
    )
    scrap_helmet_controlled_check.pack()
    fix_nut_gargantuar_status = ttk.BooleanVar(other_toggle_frame)
    fix_nut_gargantuar_check = ttk.Checkbutton(
        other_toggle_frame,
        text="Nut Giant Fix",
        variable=fix_nut_gargantuar_status,
        bootstyle="success-round-toggle",
        command=lambda: pvz.fix_nut_gargantuar(fix_nut_gargantuar_status.get()),
    )
    fix_nut_gargantuar_check.pack()
    endless_frame = ttk.Frame(other_page)
    endless_frame.pack(anchor=W)
    ttk.Label(endless_frame, text="Endless wheel").pack(side=LEFT)
    endless_round = ttk.IntVar(endless_frame)
    endless_round_entry = ttk.Entry(endless_frame, width=5, textvariable=endless_round)
    endless_round_entry.pack(side=LEFT)

    def setEndlessRound(event):
        pvz.setEndlessRound(endless_round.get())
        endless_frame.focus_set()

    endless_round_entry.bind("<Return>", setEndlessRound)

    jump_level_frame = ttk.Frame(other_page)
    jump_level_frame.pack(anchor=W)
    jump_level_value = ttk.IntVar(jump_level_frame)
    jump_level_status = ttk.BooleanVar(jump_level_frame)
    jump_level_entry = ttk.Entry(
        jump_level_frame, width=5, textvariable=jump_level_value
    )
    jump_level_entry.pack(side=LEFT)
    ttk.Checkbutton(
        jump_level_frame,
        text="Jump",
        bootstyle="success-round-toggle",
        variable=jump_level_status,
        command=lambda: pvz.lockLevel(jump_level_status.get(), jump_level_value.get()),
    ).pack(side=LEFT)

    effect_frame = ttk.LabelFrame(other_page, text="Special effect")
    effect_frame.pack(anchor=W)
    ttk.Label(effect_frame, text="x").grid(row=0, column=0)
    effect_x_value = ttk.IntVar(effect_frame)
    effect_x_combobox = ttk.Entry(
        effect_frame,
        textvariable=effect_x_value,
        width=4,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    effect_x_combobox.grid(row=0, column=1)
    effect_x_value.set(300)
    ttk.Label(effect_frame, text="y").grid(row=0, column=2)
    effect_y_value = ttk.IntVar(effect_frame)
    effect_y_combobox = ttk.Entry(
        effect_frame,
        textvariable=effect_y_value,
        width=4,
        font=("黑体", 8),
        bootstyle=SECONDARY,
    )
    effect_y_combobox.grid(row=0, column=3)
    effect_y_value.set(150)
    ttk.Label(effect_frame, text="Special effect ID").grid(row=1, column=0, columnspan=2)
    effect_id = ttk.IntVar(effect_frame)
    effect_id_entry = ttk.Spinbox(
        effect_frame,
        textvariable=effect_id,
        font=("黑体", 8),
        width=7,
        from_=0,
        to=100,
    )
    effect_id_entry.grid(row=1, column=2, columnspan=2, sticky=W)
    effect_id.set(1)

    ttk.Button(
        effect_frame,
        text="generate",
        padding=0,
        bootstyle=(OUTLINE, DANGER),
        command=lambda: pvz.creatSpecialEffects(
            effect_id.get(), effect_x_value.get(), effect_y_value.get()
        ),
    ).grid(row=1, column=4, sticky=E)

    bullet_creat_frame = ttk.LabelFrame(other_page, text="Generate bullet")
    bullet_creat_frame.pack(anchor=W)

    # Add bullet to the text box function
    def add_bullet():
        bullet_type = bullet_type_combobox.get()
        x = x_entry.get()
        y = y_entry.get()
        v_x = vx_entry.get()
        v_y = vy_entry.get()
        bullet_list.insert(tk.END, f"{bullet_type}, {x}, {y}, {v_x}, {v_y}\n")

    # The function of generating all bullets from the text box
    def generate_bullets():
        bullets_list = []
        bullets = bullet_list.get("1.0", tk.END).strip().split("\n")
        for bullet in bullets:
            bullet_type, x, y, v_x, v_y = bullet.split(", ")
            try:
                bullet_index = PVZ_data.bulletType.index(bullet_type)
                bullets_list.append(
                    (bullet_index, int(x), int(y), float(v_x), float(v_y))
                )
                print(bullets_list)
            except ValueError:
                print(f"{bullet_type} Not in the list.")
        pvz.creatBullet(bullets_list)

    # Create a drop -down box
    bullet_type_combobox = ttk.Combobox(
        bullet_creat_frame, values=PVZ_data.bulletType, width=8
    )
    bullet_type_combobox.grid(row=0, column=0, columnspan=2)

    # Create an input box
    ttk.Label(bullet_creat_frame, text="X coordinate").grid(row=1, column=0)
    x_entry = ttk.Entry(bullet_creat_frame, width=5)
    x_entry.grid(row=1, column=1)
    ttk.Label(bullet_creat_frame, text="y coordinate").grid(row=2, column=0)
    y_entry = ttk.Entry(bullet_creat_frame, width=5)
    y_entry.grid(row=2, column=1)
    ttk.Label(bullet_creat_frame, text="X speed").grid(row=3, column=0)
    vx_entry = ttk.Entry(bullet_creat_frame, width=5)
    vx_entry.grid(row=3, column=1)
    ttk.Label(bullet_creat_frame, text="Y speed").grid(row=4, column=0)
    vy_entry = ttk.Entry(bullet_creat_frame, width=5)
    vy_entry.grid(row=4, column=1)

    # Create the addition button
    add_button = ttk.Button(bullet_creat_frame, text="Add bullet", command=add_bullet)
    add_button.grid(row=5, column=0, columnspan=2)

    # Create a text box
    bullet_list = ttk.Text(bullet_creat_frame, height=10, width=20)
    bullet_list.grid(row=0, column=2, rowspan=5, padx=10)

    # Create a generating button
    generate_button = ttk.Button(
        bullet_creat_frame, text="Generate bullet", command=generate_bullets
    )
    generate_button.grid(row=5, column=2)

    zombie_spaw_page = ttk.Frame(page_tab)
    zombie_spaw_page.pack()
    page_tab.add(zombie_spaw_page, text="Modify")
    spaw_multiplier_frame = ttk.Frame(zombie_spaw_page)
    spaw_multiplier_frame.pack(anchor=W)
    spaw_multiplier_status = ttk.BooleanVar(spaw_multiplier_frame)
    spaw_multiplier_value = ttk.IntVar(spaw_multiplier_frame)
    ttk.Label(spaw_multiplier_frame, text="Blame", font=("黑体", 12)).pack(side=LEFT)
    ttk.Spinbox(
        spaw_multiplier_frame,
        from_=0,
        to=36,
        textvariable=spaw_multiplier_value,
        width=4,
    ).pack(side=LEFT, padx=5)
    ttk.Checkbutton(
        spaw_multiplier_frame,
        text="Modify",
        variable=spaw_multiplier_status,
        bootstyle="danger-round-toggle",
        command=lambda: pvz.modifySpawMultiplier(
            spaw_multiplier_status.get(), spaw_multiplier_value.get()
        ),
    ).pack(side=LEFT)
    spaw_num_value = ttk.IntVar(spaw_multiplier_frame)
    spaw_num_status = ttk.BooleanVar(spaw_multiplier_frame)
    ttk.Label(spaw_multiplier_frame, text="Strange waves", font=("黑体", 12)).pack(side=LEFT)
    ttk.Spinbox(
        spaw_multiplier_frame,
        from_=0,
        to=10,
        textvariable=spaw_num_value,
        width=4,
    ).pack(side=LEFT, padx=5)
    ttk.Checkbutton(
        spaw_multiplier_frame,
        text="Modify the waves",
        variable=spaw_num_status,
        bootstyle="danger-round-toggle",
        command=lambda: pvz.modifySpawNum(spaw_num_status.get(), spaw_num_value.get()),
    ).pack(side=LEFT)
    spaw_type_frame = ttk.LabelFrame(zombie_spaw_page, text="Modify")
    spaw_type_frame.pack(anchor=W)

    # Dictionary of storing re -election frame status
    checkboxes = {}
    # The dictionary of the INTVAR object binding with weight
    weight_vars = {}
    # Dictionary of storing zombie type objects
    zombies = {}

    def update_weights():
        for zombie_name in PVZ_data.zombieSpaw:
            if checkboxes[zombie_name].get():
                weight_var = weight_vars[zombie_name]
                weight = weight_var.get()
                try:
                    weight = int(weight)
                    zombies[zombie_name].setWeight(weight)
                except ValueError:
                    messagebox.showerror("mistake", f"Invalid weight: {weight}")
        selected_ids = [
            str(idx)
            for idx, zombie_name in enumerate(PVZ_data.zombieSpaw)
            if checkboxes[zombie_name].get()
        ]
        print(selected_ids)
        pvz.globalSpawModify(1, selected_ids)
        messagebox.showinfo("success", "Successful configuration application")

    try:
        # Create interface elements
        for idx, zombie_name in enumerate(PVZ_data.zombieSpaw):
            row = idx // 4
            col = idx % 4
            var = ttk.IntVar()
            chk = ttk.Checkbutton(spaw_type_frame, text=zombie_name + ":", variable=var)
            chk.grid(row=row, column=col * 2, sticky=W)
            checkboxes[zombie_name] = var

            zombie = PVZ_data.zombieType(idx)
            zombies[zombie_name] = zombie
            weight_var = ttk.IntVar(value=zombie.weight)
            weight_vars[zombie_name] = weight_var
            entry = ttk.Entry(spaw_type_frame, textvariable=weight_var, width=5)
            entry.grid(row=row, column=col * 2 + 1, padx=(0, 10))
    except Exception as e:
        print(zombie_name)
        messagebox.showerror("mistake", f"Error occurs when creating interface elements: {e}")

    # Read the configuration scheme
    def load_configurations():
        try:
            with open(resource_path("configurations.json"), "r") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            return {}

    # Save the configuration scheme
    def save_configurations(configurations):
        with open(resource_path("configurations.json"), "w") as json_file:
            json.dump(configurations, json_file, indent=4)
        messagebox.showinfo("success", "Configuration update")

    # Update the drop -down box option
    def update_combobox_options():
        configurations = load_configurations()
        combobox["values"] = list(configurations.keys())

    # Create a new configuration scheme and save the current data
    def create_new_configuration():
        name = simpledialog.askstring("New configuration", "Please enter the configuration name")
        if name:
            configurations = load_configurations()
            current_data = {"selected": {}, "weights": {}}
            for zombie_name in PVZ_data.zombieSpaw:
                current_data["selected"][zombie_name] = checkboxes[zombie_name].get()
                current_data["weights"][zombie_name] = weight_vars[zombie_name].get()
            configurations[name] = current_data
            save_configurations(configurations)
            update_combobox_options()
            combobox.set(name)  # Set the drop -down box as the new configuration name

    # Modify the current configuration scheme
    def modify_current_configuration():
        name = combobox.get()
        if name:
            configurations = load_configurations()
            for zombie_name in PVZ_data.zombieSpaw:
                configurations[name]["selected"][zombie_name] = checkboxes[
                    zombie_name
                ].get()
                configurations[name]["weights"][zombie_name] = weight_vars[
                    zombie_name
                ].get()
            save_configurations(configurations)

    # The selected configuration scheme
    def apply_configuration(name):
        configurations = load_configurations()
        if name in configurations:
            for zombie_name in PVZ_data.zombieSpaw:
                checkboxes[zombie_name].set(
                    configurations[name]["selected"].get(zombie_name, False)
                )
                weight_vars[zombie_name].set(
                    configurations[name]["weights"].get(zombie_name, 0)
                )

    # Add button
    update_btn = ttk.Button(spaw_type_frame, text="Application configuration", command=update_weights)
    update_btn.grid(row=(len(PVZ_data.zombieSpaw) - 1) // 4 + 1, column=4)

    # Create the drop -down box and button
    combobox = ttk.Combobox(spaw_type_frame, width=12)
    combobox.grid(row=(len(PVZ_data.zombieSpaw) - 1) // 4 + 1, column=0, columnspan=2)
    combobox.bind(
        "<<ComboboxSelected>>", lambda event: apply_configuration(combobox.get())
    )

    create_btn = ttk.Button(
        spaw_type_frame, text="New configuration", command=create_new_configuration
    )
    create_btn.grid(row=(len(PVZ_data.zombieSpaw) - 1) // 4 + 1, column=2)

    modify_btn = ttk.Button(
        spaw_type_frame, text="Preservation and placement", command=modify_current_configuration
    )
    modify_btn.grid(row=(len(PVZ_data.zombieSpaw) - 1) // 4 + 1, column=3)

    # Initialize the drop box option
    update_combobox_options()

    def refreshData():
        if page_tab.index("current") == 0:
            # gameDifficult.set(pvz.getDifficult())
            if pvz.getMap() is not False:
                try:
                    if main_window.focus_get() != sun_value_entry:
                        sun_value.set(pvz.getSun())
                    if main_window.focus_get() != silver_value_entry:
                        silver_value.set(pvz.getSilver())
                    if main_window.focus_get() != gold_value_entry:
                        gold_value.set(pvz.getGold())
                    if main_window.focus_get() != diamond_value_entry:
                        diamond_value.set(pvz.getDiamond())
                except:
                    pass
        if page_tab.index("current") == 1:
            if pvz.getMap() is not False:
                refresh_zombie_list()
                get_zombie_attribute()
        if page_tab.index("current") == 2:
            if pvz.getMap() is not False:
                refresh_plant_list()
                get_plant_attribute()
        if page_tab.index("current") == 3:
            if pvz.getMap() is not False:
                refresh_item_list()
                get_item_attribute()
        if page_tab.index("current") == 4:
            if slots_configuration_mode.get() is False:
                refresh_slot_list()
                get_slot_attribute()
        if page_tab.index("current") == 5:
            try:
                if main_window.focus_get() != endless_round_entry:
                    endless_round.set(pvz.getEndlessRound())
            except:
                pass
        recruit_button.configure(
            bootstyle=random.choice(["danger", "success", "warning", "primary"])
        )
        main_window.after(100, refreshData)

    def load_plugin(main_window):
        plugin_name = filedialog.askopenfilename(
            title="Select plug -in file",
            filetypes=[("PVZHybrid_Editor插件文件", "*.pyc *.pyd")],
        )
        if plugin_name:
            global plugin
            print(f"选中的文件: {plugin_name}")
            # Determine the module loading method according to the expansion name of the file
            if plugin_name.endswith(".pyc"):
                spec = importlib.util.spec_from_file_location(
                    "plugin_module", plugin_name
                )
                plugin = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(plugin)
                # 假设插件有一个名为open_plugin_window的函数
                plugin.open_plugin_window(main_window)
            elif plugin_name.endswith(".pyd"):
                print(plugin_name)
                filename_with_extension = os.path.basename(plugin_name)
                directory_path = os.path.dirname(plugin_name)
                filename_without_extension = os.path.splitext(filename_with_extension)[
                    0
                ]
                # # 生成导入语句
                # import_statement = f"import {ilename_without_extension} as plugin"
                # print(ilename_without_extension)
                # 在全局作用域内执行导入语句
                print(directory_path)
                sys.path.append(directory_path)
                globals()[filename_without_extension] = __import__(
                    filename_without_extension
                )
                globals()["plugin"] = globals()[filename_without_extension]
                plugin.open_plugin_window(main_window)

            else:
                print("Unwilling file type")
                return
        else:
            print("No choice file")

    # 创建一个按钮，用于加载插件
    plugin_button = ttk.Button(
        main_window,
        text="Load plug -in",
        padding=0,
        bootstyle="primary",
        cursor="hand2",
        command=lambda: load_plugin(main_window),
    )
    plugin_button.place(x=100, y=0, relx=0, rely=1, anchor="sw")

    def recruit():
        global main_window
        recruit_window = ttk.Toplevel(topmost=True)
        recruit_window.title("Anchor recruitment")
        recruit_window.geometry("300x460")
        recruit_window.iconphoto(
            False, ttk.PhotoImage(file=resource_path((r"res\icon\info.png")))
        )
        recruit_window.tk.call("tk", "scaling", 4 / 3)
        main_window_x = main_window.winfo_x()
        main_window_y = main_window.winfo_y()
        recruit_window.geometry(f"+{main_window_x+100}+{main_window_y + 100}")
        ttk.Label(
            recruit_window,
            text="Douyin the strongest plant union, 0 draws\nOne -on -one teaching set up number\nThe anchor is operating 24 hours\nReceive five digits per month during the anchor of the anchor\nWelcome everyone to join",
            font=("黑体", 14),
            bootstyle=PRIMARY,
        ).pack(pady=10)

        WeChat = ttk.PhotoImage(file=resource_path(r"res/support/WeChat.png"))
        AliPay_image = ttk.Label(recruit_window, image=WeChat)
        AliPay_image.pack(pady=10)
        recruit_window.mainloop()

    recruit_button = ttk.Button(
        main_window,
        text="Want to be anchor here",
        padding=0,
        bootstyle="danger",
        cursor="hand2",
        command=lambda: recruit(),
    )
    recruit_button.place(x=180, y=0, relx=0, rely=1, anchor="sw")

    support_button = ttk.Button(
        main_window,
        text="Update announcement",
        padding=0,
        bootstyle=(PRIMARY, LINK),
        cursor="hand2",
        command=lambda: support(),
    )
    support_button.place(x=0, y=0, relx=1, anchor=NE)
    main_window.after(100, process_queue, main_window)
    main_window.after(100, refreshData)

    main_window.protocol(
        "WM_DELETE_WINDOW", lambda: exit_editor(config_file_path, main_window)
    )
    main_window.mainloop()


if __name__ == "__main__":
    mainWindow()
