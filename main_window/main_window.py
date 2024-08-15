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
import logging
import signal
import ttkbootstrap as ttk
import tkinter.font as tkFont

from ttkbootstrap import Style
from ttkbootstrap.constants import *
from mediator.base_component import BaseComponent
from PIL import Image, ImageTk


class MainWindow(BaseComponent):
    """
    A MainWindow class using ttkbootstrap using the Mediator design pattern.

    User's of this class should only:
    - Instantiate
    - Set mediator
    - Call in to this class using 'notify' method.
    """

    _app_name = None
    _global_font = None
    mediator = None
    _style = None
    _theme = None
    _window = None

    def __init__(self, app_name, theme):
        """
        Args:
            app_name (str): the name of the app to be used by the OS
            theme (str): the ttkbootstrap theme for the application
        """
        super().__init__()
        self._app_name = app_name
        self._theme = theme
        signal.signal(signal.SIGINT, self._quit)

    def notify(self, sender, event):
        if sender == "ConcreteMediator":  # guard! but it should always be CM
            if event == "QUIT":
                self._quit()
            if event == "SHOW":
                self._show_window()
            if event == "START":
                self._create_ui()
                self._window.after(1000, self._dummy_function)
                self._window.mainloop()

    def _create_start_button(self):
        """
        Build and add a button to the MainWindow
        """
        start_button = ttk.Button(self._window, text="Start Task",
                                  command=self._start_task,
                                  style=SUCCESS)
        start_button.pack()

    def _create_ui(self):
        """
        Build the MainWindow
        """
        self._window = ttk.Window(themename=self._theme)
        self._window.title(self._app_name)
        # While having a handle to the current Style isn't really used in this
        # app, having this is variable in our template helps, so that if we
        # change things for events in a _real_app_ we can revert with:
        #       self._style.theme_use(themename=self._theme)
        # Some things might need tweaking, but saves a lot of work.
        self._style = Style()
        self._create_window_icon()
        self._set_global_font_defaults()
        self._create_start_button()
        # override the def behavior of clicking close window button to hide it!
        self._window.protocol("WM_DELETE_WINDOW", self._hide_window)

    def _create_window_icon(self):
        """
        Create a transparent icon and use that instead of Tk's default icon.

        The use of transparent is optional, you can use a real icon or the TK
        default if you like.
        """
        # Create a transparent icon image in memory, to get rid of ugly Tk icon.
        app_icon = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        icon_photo = ImageTk.PhotoImage(app_icon)
        self._window.iconphoto(True, icon_photo)

    def _dummy_function(self):
        """
        https://stackoverflow.com/questions/9998274/tkinter-keyboard-interrupt-isnt-handled-until-tkinter-frame-is-raised
        What you're seeing is caused by the way signal handlers are
        handled. You're stuck in the Tcl/Tk main loop, and signal handlers
        are only handled by the Python interpreter. A quick workaround
        is to use after() to schedule a dummy function to be called once a
        second or so -- this will make it appear that your signal is handled
        in a timely manner.

        --Guido van Rossum

        This function is used to yield control back to Python so we can catch
        SIGINT when the app is not in focus.
        """
        self._window.after(2000, self._dummy_function)

    def _hide_window(self):
        """
        Hide's the MainWindow
        """
        if self._window:
            self._window.withdraw()

    def _quit(self, signum=None, frame=None):
        """
        Closes the MainWindow
        """
        if self._window:
            self._window.quit()
            logging.info("Goodbye from MainWindow!")

    def _set_global_font_defaults(self):
        """
        Set the global default font and size for all widgets created after
        this is function has been called.
        """
        self._global_font = tkFont.nametofont("TkDefaultFont")
        self._global_font.configure(size=16)

    def _show_window(self):
        """
        Shows the main window of our application and brings it to focus.
        """
        self._window.after(0, self._window.deiconify)
        # get the window to come to foreground on GNU/Linux
        self._window.lift()
        self._window.attributes("-topmost", True)
        self._window.focus_force()

    def _start_task(self):
        """
        Simulate some work
        """
        logging.info("Hello world!")
