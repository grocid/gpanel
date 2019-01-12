import gi
import psutil

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GObject


class ComputerUsage(Gtk.Box):

    def __init__(self, *args, **kwds):
        super(ComputerUsage, self).__init__(*args, **kwds)

        self.spacing = 10

        self.cpu = Gtk.ProgressBar()
        self.cpu.set_text("Processor\n")
        self.cpu.set_show_text(True)

        self.mem = Gtk.ProgressBar()
        self.mem.set_text("Minne\n")
        self.mem.set_show_text(True)

        self.pack_start(self.cpu, False, False, 10)
        self.pack_start(self.mem, False, False, 10)

        self.update()
        self.startclocktimer()

    def startclocktimer(self):
        GObject.timeout_add(1000, self.update)

    def update(self):
        self.cpu.set_fraction(psutil.cpu_percent() / 100)
        self.mem.set_fraction(psutil.virtual_memory().percent / 100)
        return True
