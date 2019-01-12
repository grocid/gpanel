import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject

WINDOW_WIDTH = 335


class TransparentWindow(Gtk.Window):
    def __init__(self, alpha=0.3):
        Gtk.Window.__init__(self)
        self.connect('draw', self.draw)
        self.set_resizable(True)
        #self.set_keep_below(True)
        self.set_keep_above(True)
        self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)
        self.set_wmclass ("gPanel", "gPanel")
        self.set_title ("gPanel")
        self.alpha = alpha

        screen = self.get_screen()
        self.set_size_request(WINDOW_WIDTH, screen.get_height() - 25)
        self.set_gravity(Gdk.Gravity.NORTH_WEST)
        self.move(screen.get_width() - WINDOW_WIDTH, 0)

        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)

        self.set_app_paintable(True)
        self.set_decorated(False)
        self.show_all()

    def draw(self, widget, context):
        context.set_source_rgba(0, 0, 0, self.alpha)
        context.paint()

    def fadein(self):
        self.set_opacity(1)

    def fadeout(self):
        self.set_opacity(0)
