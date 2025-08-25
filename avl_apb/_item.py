# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Sequence Item

from typing import Any

import avl
from z3 import BoolRef, Implies


class SequenceItem(avl.SequenceItem):
    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize the sequence item

        :param name: Name of the sequence item
        :param parent: Parent component of the sequence item
        """
        super().__init__(name, parent)

        # Handle to interface - defines capabilities and parameters
        i_f = avl.Factory.get_variable(f"{self.get_full_name()}.i_f", None)

        self.paddr = avl.Logic(0, width=len(i_f.paddr), fmt=hex)
        """Address"""

        self.psel = avl.Logic(0, width=len(i_f.psel), fmt=hex)
        """Select (1-hot)"""

        self.pwrite = avl.Logic(0, width=len(i_f.pwrite), fmt=str)
        """Write enable"""

        self.pwdata = avl.Logic(0, width=len(i_f.pwdata), fmt=hex)
        """Write data"""

        self.prdata = avl.Logic(0, width=len(i_f.prdata), fmt=hex)
        """Read data"""

        if hasattr(i_f, "pslverr"):
            self.pslverr = avl.Logic(0, width=len(i_f.pslverr), fmt=str)
            """Slave error (>= version 3)"""

        if hasattr(i_f, "pstrb"):
            self.pstrb = avl.Logic(0, width=len(i_f.pstrb), fmt=hex)
            """Write strobe (byte enable) (>= version 4)"""

        if hasattr(i_f, "pprot"):
            self.pprot = avl.Logic(0, width=len(i_f.pprot), fmt=hex)
            """Protection bits (optional >= version 4)"""

        if hasattr(i_f, "pnse"):
            self.pnse = avl.Logic(0, width=len(i_f.pnse), fmt=str)
            """Non-secure enable (optional >= version 5)"""

        if hasattr(i_f, "pwakeup"):
            self.goto_sleep = avl.Logic(0, width=len(i_f.pwakeup), fmt=str)
            """Wakeup indication (optional >= version 5)"""

        if hasattr(i_f, "pauser"):
            self.pauser = avl.Logic(0, width=len(i_f.pauser), fmt=hex)
            """User Request Sideband (optional >= version 5)"""

        if hasattr(i_f, "pwuser"):
            self.pwuser = avl.Logic(0, width=len(i_f.pwuser), fmt=hex)
            """User Write Sideband (optional >= version 5)"""

        if hasattr(i_f, "pruser"):
            self.pruser = avl.Logic(0, width=len(i_f.pruser), fmt=hex)
            """User Read Sideband (optional >= version 5)"""

        if hasattr(i_f, "pbuser"):
            self.pbuser = avl.Logic(0, width=len(i_f.pbuser), fmt=hex)
            """User Response Sideband (optional >= version 5)"""

        # Constraints
        self.add_constraint("c_psel_valid", lambda x : x != 0, self.psel)
        self.add_constraint("c_psel_1hot", lambda x : (x & (x-1) == 0), self.psel)

        if hasattr(self, "pstrb"):
            self.add_constraint("c_pstrb", lambda x, y : Implies(x == 0, y == 0), self.pwrite, self.pstrb)

        # Monitor only attributes used for debug and coverage
        if hasattr(i_f, "pready"):
            self.wait_cycles = 0
            """Wait cycles - cycles from enable to ready (monitor only)"""
            self.set_field_attributes("wait_cycles", compare=False)


        if hasattr(i_f, "pwakeup"):
            self.time_since_wakeup = 0
            """Time since last wakeup - used for debug and coverage (monitor only)"""
            self.set_field_attributes("time_since_wakeup", compare=False)

        # By default transpose to make more readable
        self.set_table_fmt(transpose=True)

    def set(self, name : str, value : int) -> None:
        """
        Set the value of a field in the sequence item - if it exists.

        :param name: Name of the field to set
        :param value: Value to set for the field
        """
        signal = getattr(self, name, None)
        if signal is not None:
            signal.value = value

    def get(self, name : str, default : Any = None) -> int:
        """
        Get the value of a field in the sequence item - if it exists.

        :param name: Name of the field to get
        :param default: Default value to return if the field does not exist
        :return: Value of the field or default value
        """
        signal = getattr(self, name, None)
        if signal is not None:
            return signal.value
        return default

    def randomize_request(self, hard: list[BoolRef] = None, soft: list[BoolRef] = None) -> None:
        """
        Randomize the request fields of the sequence item.
        """
        for f in ["prdata", "pslverr", "pruser", "pbuser"]:
            if hasattr(self, f):
                getattr(self, f)._auto_random_ = False

        self.randomize(hard=hard, soft=soft)

        for f in ["prdata", "pslverr", "pruser", "pbuser"]:
            if hasattr(self, f):
                getattr(self, f)._auto_random_ = True

    def randomize_completion(self, hard: list[BoolRef] = None, soft: list[BoolRef] = None) -> None:
        """
        Randomize the completion fields of the sequence item.
        """

        for f in ["paddr", "psel", "pwrite", "pwdata", "pstrb", "pprot", "pnse", "pauser", "pwuser", "goto_sleep"]:
            if hasattr(self, f):
                getattr(self, f)._auto_random_ = False

        self.randomize(hard=hard, soft=soft)

        for f in ["paddr", "psel", "pwrite", "pwdata", "pstrb", "pprot", "pnse", "pauser", "pwuser", "goto_sleep"]:
            if hasattr(self, f):
                getattr(self, f)._auto_random_ = True

__all__ = ["SequenceItem"]
