import os
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
            os.rmdir(dir_path)


# Create the menu
systray_menu = QMenu()

# Add a empty trash option
systray_menu_empty = QAction("Empty")
systray_menu_empty.triggered.connect(empty_trash)
systray_menu.addAction(systray_menu_empty)

# Add a quit option
systray_menu_quit = QAction("Quit")
systray_menu_quit.triggered.connect(app.quit)
systray_menu.addAction(systray_menu_quit)

# Create the system tray
systray = QSystemTrayIcon()
if darkdetect.theme() == "light":
    systray.setIcon(ICON_LIGHT_EMPTY)
else:
    systray.setIcon(ICON_DARK_EMPTY)
systray.setVisible(True)
systray.setContextMenu(systray_menu)


# Function that checks the trash directory periodically (to handle icon change)
def check_trash():
    if os.path.exists(TRASH_PATH) and os.listdir(TRASH_PATH):
        if darkdetect.theme() == "light":
            systray.setIcon(ICON_LIGHT)
        else:
            systray.setIcon(ICON_DARK)
    else:
        if darkdetect.theme() == "light":
            systray.setIcon(ICON_LIGHT_EMPTY)
        else:
            systray.setIcon(ICON_DARK_EMPTY)


# Checks each 100ms
systimer = QTimer()
systimer.timeout.connect(check_trash)
systimer.start(100)

# Run the app
app.exec()
