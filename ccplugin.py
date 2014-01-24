__author__ = 'Sebastian Haenisch'

from robotide.pluginapi import Plugin
from robotide.pluginapi import ActionInfo
from robotide.pluginapi import RideLogMessage
from robotide.widgets.popupmenu import PopupMenuItem
import subprocess
import os


class ClearCasePlugin(Plugin):
    """
    This plugin for RIDE implements Check Out and Check In Cleartool operations.
    """

    def __init__(self, application):
        Plugin.__init__(self, application, name=None, doc=None, metadata=None,
                        default_settings=None, initially_enabled=True)

        self.menu = [
            ActionInfo("ClearCase", "Check &Out", self.OnCheckOut, position=0),
            ActionInfo("ClearCase", "&Undo Check out", self.OnUndoCheckOut, position=1),
            ActionInfo("ClearCase", "Check &In", self.OnCheckIn, position=2),
        ]

        self.treemenuitems = [
            PopupMenuItem("---"),
            PopupMenuItem("Check Out", self.OnCheckOut, self),
            PopupMenuItem("Undo Check Out", self.OnUndoCheckOut, self),
            PopupMenuItem("Check In", self.OnCheckIn, self)
        ]

    def _treeMenuHook(self, data):
        return self.treemenuitems

    def enable(self):
        self.register_actions(self.menu)
        self.tree.register_context_menu_hook(self._treeMenuHook)
        mess = RideLogMessage(message="ClearCasePlugin enabled")
        mess.publish()

    def disable(self):
        self.unregister_actions()
        self.tree.unregister_context_menu_hook(self._treeMenuHook)
        mess = RideLogMessage(message="ClearCasePlugin disabled")
        mess.publish()

    def _getPath(self):
        file = self.get_selected_datafile()
        if file is not None:
            path = os.path.join(file.directory, file.source)
            return path
        return None

    def OnCheckOut(self, event):
        subprocess.call("cleartool checkout -nc %s" % self._getPath(), shell=True)

    def OnCheckIn(self, event):
        subprocess.call("cleartool checkin %s" % self._getPath(), shell=True)

    def OnUndoCheckOut(self, event):
        subprocess.call("cleartool uncheckout -rm %s" % self._getPath(), shell=True)
        pass