import gi
import time

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GObject


class Clock(Gtk.Label):

    def __init__(self, *args, **kwds):
        super(Clock, self).__init__(*args, **kwds)
        self.modify_font(Pango.FontDescription("sans 32"))
        self.update()
        self.startclocktimer()

    def startclocktimer(self):
        GObject.timeout_add(1000, self.update)

    def update(self):
        self.set_text(
            time.strftime("%H:%M", time.localtime())
        )
        return True
