import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GObject


class Caption(Gtk.Label):

    def __init__(self, *args, **kwds):
        super(Caption, self).__init__(*args, **kwds)
        self.modify_font(Pango.FontDescription("sans 12"))
