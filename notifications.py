import gi
import time

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import Pango, GObject
from gi.repository.GdkPixbuf import Pixbuf


class ListBoxRow(Gtk.ListBoxRow):

    __gtype_name__ = 'ChannelWidget'

    def __init__(self, *args, **kwds):
        super(ListBoxRow, self).__init__(*args, **kwds)
        # Create elements
        self.symbol = Gtk.Image()
        self.caption = Gtk.Label()
        self.caption.set_justify(Gtk.Justification.LEFT)
        self.text = Gtk.Label()
        self.text.set_justify(Gtk.Justification.LEFT)
        self.text.set_line_wrap(True)
        self.time = Gtk.Label()
        self.time.set_justify(Gtk.Justification.RIGHT)

        innermost = Gtk.VBox()
        tmp = Gtk.HBox()
        tmp.pack_start(self.caption, False, False, 0)
        innermost.pack_start(tmp, True, True, 0)

        tmp = Gtk.HBox()
        tmp.pack_start(self.text, False, False, 0)
        innermost.pack_start(tmp, True, True, 0)

        inner = Gtk.HBox()
        inner.pack_start(self.symbol, False, False, 15)
        inner.pack_start(innermost, True, True, 0)
        inner.pack_start(self.time, False, True, 15)

        outer = Gtk.VBox()
        outer.pack_start(inner, False, False, 9)

        # Add to layout
        self.add(outer)

    def set_symbol(self, symbol):
        self.symbol.set_from_pixbuf(symbol)

    def set_content(self, title, message, data=None):
        self.caption.modify_font(Pango.FontDescription("sans bold 8"))
        self.caption.set_text(title)
        self.text.set_text(message)
        self.text.modify_font(Pango.FontDescription("sans 8"))
        self.time.set_text(
            time.strftime("%H:%M", time.gmtime())
        )
        self.time.modify_font(Pango.FontDescription("sans 8"))
        self.data = data

    def get_data(self):
        return self.data


class ScrolledListbox():

    def __init__(self):
        self.content = Gtk.ListBox()
        self.content.connect('row-activated', self.on_row_activated)
        self.content.override_background_color(
            0, Gdk.RGBA(0, 0, 0, 0)
        )

        self.view = Gtk.ScrolledWindow()
        self.view.get_vscrollbar().set_visible(False)
        self.view.get_hscrollbar().set_visible(False)
        self.view.add(self.content)
        self.view.set_propagate_natural_height(True)

    def add(self, element):
        self.content.insert(element, 0)
        self.content.show_all()

    def on_row_activated(self, widget, row):
        self.content.unselect_all()
