import gi
import os
import subprocess

from notifications import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository.GdkPixbuf import Pixbuf


class Vagrant():

    def __init__(self):
        self.view = ScrolledListbox()
        self.icon_theme = Gtk.IconTheme.get_default()
        self.icon = self.icon_theme.load_icon(
            "network-transmit-receive-symbolic", 24, 0
        )
        self.virtual_machines = []
        self.view.content.connect('row-activated', self.on_row_activated)
        #self.startclocktimer()

    def update(self):
        self.virtual_machines = self.get_vms()
        for vm in self.virtual_machines:
            item = ListBoxRow()
            vm_id = vm[0]
            vm_name = vm[1]
            vm_provider = vm[2]
            vm_state = vm[3]
            item.set_content(
                "Vagrant (%s)" % vm_provider,
                "%s (%s)" % (vm_name, vm_id),
                data=vm_id
            )
            item.set_symbol(self.icon)
            item.time.set_text(vm_state)
            self.view.add(item)
        return True

    def startclocktimer(self):
        GObject.timeout_add(1000, self.update)

    def get_vms(self):
        virtual_machines = []
        result = subprocess.check_output([
            "vagrant", "global-status"
        ]).split("\n")
        for row in result[2:]:
            row = row.strip()
            vm = row.split()
            if len(vm) != 5:
                continue
            virtual_machines.append(vm)
        return virtual_machines

    def on_row_activated(self, widget, row):
        if row.data is not None:
            os.system(
                "mate-terminal -e 'bash -c " +
                "\"vagrant ssh %s; exec bash\"'" % row.data
            )
        self.view.content.unselect_all()

