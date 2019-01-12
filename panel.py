import dbus
import dbus.bus
import dbus.service
import dbus.mainloop.glib

from clock import *
from notifications import *
from window import *
from vagrant import *
from caption import *
from usage import *

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import Pango, GObject
from gi.repository.GdkPixbuf import Pixbuf

DBUS_NAME = "com.grocid.panel"


class DBusDaemon(dbus.service.Object):

    def __init__(self, bus, path, name):
        dbus.service.Object.__init__(self, bus, path, name)
        self.running = False
        self.icon_theme = Gtk.IconTheme.get_default()

        self.notifications = ScrolledListbox()
        self.clock = Clock()
        self.vagrant = Vagrant()
        self.usage = ComputerUsage()
        vagrant_caption = Caption()
        vagrant_caption.set_text("Virtuellt")
        notifications_caption = Caption()
        notifications_caption.set_text("Notifikationer")

        # Create a vertical layout
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.box.pack_start(self.clock, False, False, 30)
        self.box.pack_start(self.usage, False, False, 0)
        self.box.pack_start(vagrant_caption, False, False, 30)
        self.box.pack_start(vagrant_caption, False, False, 30)
        self.box.pack_start(self.vagrant.view.view, False, False, 0)
        self.box.pack_start(notifications_caption, False, False, 30)
        self.box.pack_start(self.notifications.view, True, True, 0)
        self.vagrant.update()

        # Setup window
        self.main_window = TransparentWindow(alpha=0.3)
        self.main_window.add(self.box)
        self.main_window.connect('destroy', Gtk.main_quit)
        self.main_window.set_border_width(0)
        self.main_window.connect("enter-notify-event", self.undim)
        self.main_window.connect("leave-notify-event", self.dim)
        self.notifications.view.connect("enter-notify-event", self.undim)
        self.vagrant.view.view.connect("enter-notify-event", self.undim)
        self.main_window.show_all()

    def dim(self, a, b):
        self.main_window.fadeout()

    def undim(self, a, b):
        self.main_window.fadein()

    @dbus.service.method(DBUS_NAME, in_signature='', out_signature='b')
    def is_running(self):
        return self.running

    @dbus.service.method(DBUS_NAME, in_signature='a{sv}i', out_signature='')
    def start(self, options, timestamp):
        if self.is_running():
            self.main_window.present_with_time(timestamp)
        else:
            self.running = True
            Gtk.main()
            self.running = False

    def notification(self, bus, message):

        def shorten(msg):
            if len(msg) > 32:
                msg = msg[:29] + "..."
            return msg

        keys = [
            "app_name",
            "replaces_id",
            "app_icon",
            "summary",
            "body",
            "actions",
            "hints",
            "expire_timeout"
        ]

        name_map = {
            "networkmanager": "network-manager",
            "telegram": "telegram-desktop",
            "terminal": "utilities-terminal"
        }

        args = message.get_args_list()

        if len(args) == 8:
            dbus_notification = dict([(keys[i], args[i]) for i in range(8)])
            try:
                name = dbus_notification["app_name"].lower()
                summary = shorten(dbus_notification["summary"].encode('utf-8'))
                body = shorten(dbus_notification["body"].encode('utf-8'))
                if name in name_map:
                    name = name_map[name]
                item = ListBoxRow()
                item.set_content(summary, body)
                if self.icon_theme.has_icon(name):
                    item.set_symbol(self.icon_theme.load_icon(name, 24, 0))
                elif self.icon_theme.has_icon("utilities-terminal"):
                    item.set_symbol(
                        self.icon_theme.load_icon("utilities-terminal", 24, 0)
                    )
                self.notifications.add(item)
            except Exception:
                pass


dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
request = bus.request_name(DBUS_NAME, dbus.bus.NAME_FLAG_DO_NOT_QUEUE)
app = DBusDaemon(bus, '/', DBUS_NAME)

bus.add_match_string_non_blocking(
    "eavesdrop=true," +
    "interface='org.freedesktop.Notifications'," +
    "member='Notify'"
)
bus.add_message_filter(app.notification)

app.start({}, int(time.time()))
if app.is_running():
    Gdk.notify_startup_complete()
