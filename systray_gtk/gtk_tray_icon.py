"""
gtk-systray-ttkbootstrap-threaded-template:
    A program to demonstrate use of GTK systray and ttkbootstrap using threads,
    using the Mediator design pattern.

    Copyright (C) 2023 serverlinkdev@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""
import gi
from mediator.base_component import BaseComponent
import threading

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3


class Systray(BaseComponent):
    """
    A class using the Mediator design pattern.

    User's of this class should only:
    - Instantiate
    - Set mediator
    - Call in to this class using 'notify' method.
    """
    _indicator = None
    _mediator = None
    _menu = None
    _menu_item_quit = None
    _menu_item_image_show = None
    _menu_item_show = None
    _tray_image = None

    def __init__(self, tray_image, show_menu_item_image="test.png"):
        """
        Args:
        tray_image (str): the icon you want to see in your new tray
        show_menu_item_image (str): the path to the image you want to use for
                                    the "Show" tray menu entry
        """
        super().__init__()

        self._menu_item_image_show = show_menu_item_image
        self._tray_image = tray_image

        # For dev purposes, we are hard coding "dialog-information"
        # for the tray icon.
        #
        # It should be present on a GNU/Linux system.
        #
        # Note we do NOT put a file extension next to the file's name!
        #
        # main.py of this app passes the file name with extension, you
        # need to remove that.
        #
        # In time you will want to replace that with "self._tray_image"!
        #
        # The AppIndicator actually requires an entire icon theme for your
        # icon.  I have examples of how to achieve this at bottom of this file.
        #
        # You will need to distribute this with your application at release time.
        #
        self._indicator = AppIndicator3.Indicator.new(
            "example-system-tray",
            "dialog-information",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self._indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self._indicator.set_title("My Application Tooltip")

        self._create_tray()

    def notify(self, sender, event):
        if sender == "ConcreteMediator":
            if event == "START":
                self._start_systray()
            else:
                print(f"Unhandled command in Systray notify method.")

    def _build_menu_item_with_icon(self):  # Show menu item
        # Build "Print Hello" menu image and label and put into an Gtk.Box Hbox:
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        menu_item_image_show = Gtk.Image.new_from_file(self._menu_item_image_show)
        hbox.pack_start(menu_item_image_show, False, False, 0)
        menu_item_label_show = Gtk.Label(label="Show")
        hbox.pack_start(menu_item_label_show, False, False, 0)

        # Build "Print Hello" menu item:
        menu_item_show = Gtk.MenuItem()
        menu_item_show.add(hbox)
        menu_item_show.connect("activate", self._show_main_window)

        return menu_item_show

    def _build_menu_item_without_icon(self):  # Quit menu item
        menu_item_quit = Gtk.MenuItem(label="Quit")
        menu_item_quit.connect("activate", self._quit_main_window)

        return menu_item_quit

    def _create_tray(self):
        """
        Build the Systray
        """

        self._menu = Gtk.Menu()

        self._menu_item_show = self._build_menu_item_with_icon()
        self._menu.append(self._menu_item_show)

        self._menu_item_quit = self._build_menu_item_without_icon()
        self._menu.append(self._menu_item_quit)

        self._menu.show_all()

        self._indicator.set_menu(self._menu)

    def _quit_main_window(self, _):
        """
        Tell's ConcreteMediator that we need to quit the MainWindow.
        Stop's the Systray from running.
        """
        print(f"Quit menu item was clicked!")
        self.mediator.notify(self, "QUIT")
        Gtk.main_quit()

    def _show_main_window(self, _):
        """
        Tell's ConcreteMediator to show the MainWindow
        """
        print(f"Show menu item was clicked!")
        self.mediator.notify(self, "SHOW")

    def _start_systray(self):
        """
        Create a thread to run the Systray in

        Note: Both Tkinter and Gtk have their own mainloop.  By putting
        the tray into its own thread, the two can coincide.
        """
        self._worker_thread = threading.Thread(
            daemon=True,
            target=lambda: Gtk.main()
        )
        self._worker_thread.start()


#
# As a courtesy I'm putting these commands here.
# Use at your own risk, as I accept no responsibility implied or otherwise.
#
# App indicator requires icons in theme dirs, we cannot hard code a path.
# On GNU/Linux systems global themes are in /usr/local/share/icons/hicolor
# For dev purposes, one can use the following:
#
# mkdir -p ~/.local/share/icons/hicolor/16x16/apps;
# mkdir -p ~/.local/share/icons/hicolor/24x24/apps;
# mkdir -p ~/.local/share/icons/hicolor/32x32/apps;
# mkdir -p ~/.local/share/icons/hicolor/48x48/apps;
# mkdir -p ~/.local/share/icons/hicolor/64x64/apps;
# mkdir -p ~/.local/share/icons/hicolor/96x96/apps;
# mkdir -p ~/.local/share/icons/hicolor/128x128/apps;
# mkdir -p ~/.local/share/icons/hicolor/256x256/apps;
# mkdir -p ~/.local/share/icons/hicolor/512x512/apps;
#
# Example of what I did when making this application:
# cp icons/smile16.png ~/.local/share/icons/hicolor/16x16/apps/smile.png;
# cp icons/smile24.png ~/.local/share/icons/hicolor/24x24/apps/smile.png;
# cp icons/smile32.png ~/.local/share/icons/hicolor/32x32/apps/smile.png;
# cp icons/smile48.png ~/.local/share/icons/hicolor/48x48/apps/smile.png;
# cp icons/smile64.png ~/.local/share/icons/hicolor/64x64/apps/smile.png;
# cp icons/smile96.png ~/.local/share/icons/hicolor/96x96/apps/smile.png;
# cp icons/smile128.png ~/.local/share/icons/hicolor/128x128/apps/smile.png;
# cp icons/smile256.png ~/.local/share/icons/hicolor/256x256/apps/smile.png;
# cp icons/smile512.png ~/.local/share/icons/hicolor/512x512/apps/smile.png;
#
# If you want to remove the icon from above:
# rm ~/.local/share/icons/hicolor/16x16/apps/smile.png;
# rm ~/.local/share/icons/hicolor/24x24/apps/smile.png;
# rm ~/.local/share/icons/hicolor/32x32/apps/smile.png;
# rm ~/.local/share/icons/hicolor/48x48/apps/smile.png;
# rm ~/.local/share/icons/hicolor/64x64/apps/smile.png;
# rm ~/.local/share/icons/hicolor/96x96/apps/smile.png;
# rm ~/.local/share/icons/hicolor/128x128/apps/smile.png;
# rm ~/.local/share/icons/hicolor/256x256/apps/smile.png;
# rm ~/.local/share/icons/hicolor/512x512/apps/smile.png;
#
# Don't forget to update the icon cache there with:
# gtk-update-icon-cache ~/.local/share/icons/hicolor/
