import os
import shutil
from pathlib import Path

import darkdetect
from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

# Create QApplication
app = QApplication([])
app.setQuitOnLastWindowClosed(False)

TRASH_PATH = str(Path.home() / ".local/share/Trash/files/")
ICON_DARK_EMPTY = QIcon("icons/EmptyBinLight.png")
ICON_DARK = QIcon("icons/BinLight.png")
ICON_LIGHT_EMPTY = QIcon("icons/EmptyBinDark.png")
ICON_LIGHT = QIcon("icons/BinDark.png")


# Empty trash function
def empty_trash():
    for root_dir_path, dirs, files in os.walk(TRASH_PATH, True):
        for file in files:
            file_path = os.path.join(root_dir_path, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root_dir_path, dir)
            shutil.rmtree(dir_path)


# Create the menu
systray_menu = QMenu()

# Add amount of items
systray_menu_items = QAction("Items:")
systray_menu_items.setDisabled(True)
systray_menu.addAction(systray_menu_items)

# Add size of items
systray_menu_size = QAction("Size:")
systray_menu_size.setDisabled(True)
systray_menu.addAction(systray_menu_size)

# Add empty trash option
systray_menu_empty = QAction("Empty")
systray_menu_empty.triggered.connect(empty_trash)
systray_menu.addAction(systray_menu_empty)

# Add quit option
systray_menu_quit = QAction("Quit")
systray_menu_quit.triggered.connect(app.quit)
systray_menu.addAction(systray_menu_quit)

# Create the system tray
systray = QSystemTrayIcon()
if darkdetect.theme() == "Light":
    systray.setIcon(ICON_LIGHT_EMPTY)
else:
    systray.setIcon(ICON_DARK_EMPTY)
systray.setVisible(True)
systray.setContextMenu(systray_menu)


# Function that checks the trash directory periodically (to handle icon change and other stuff)
def check_trash():
    if os.path.exists(TRASH_PATH) and os.listdir(TRASH_PATH):
        if darkdetect.theme() == "Light":
            systray.setIcon(ICON_LIGHT)
        else:
            systray.setIcon(ICON_DARK)
    else:
        if darkdetect.theme() == "Light":
            systray.setIcon(ICON_LIGHT_EMPTY)
        else:
            systray.setIcon(ICON_DARK_EMPTY)

    file_list = []
    for root_dir_path, dirs, files in os.walk(TRASH_PATH, True):
        for file in files:
            file_list.append(os.path.join(root_dir_path, file))
        for dir in dirs:
            file_list.append(os.path.join(root_dir_path, dir))

    size = 0
    for file in os.scandir(TRASH_PATH):
        size += os.path.getsize(file)

    calculated_size = int(size / 1048576)
    systray_menu_items.setText("Items: " + str(len(file_list)))
    systray_menu_size.setText("Size: " + str(calculated_size) + " MB")


# Checks each 50ms
systimer = QTimer()
systimer.timeout.connect(check_trash)
systimer.start(50)

# Run the app
app.exec()
