# mygame/commands/combat.py

from evennia import CmdSet
from evennia import default_cmds

class CombatCmdSet(CmdSet):
    key = "combat_cmdset"
    mergetype = "Replace"
    priority = 10
    no_exits = True

    def at_cmdset_creation(self):
        self.add(CmdHit())
        self.add(CmdParry())
        self.add(CmdFeint())
        self.add(CmdDefend())
        self.add(CmdDisengage())
        self.add(CmdHelp())
        self.add(default_cmds.CmdPose())
        self.add(default_cmds.CmdSay())