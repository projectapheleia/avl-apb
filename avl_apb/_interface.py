# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Interface

from typing import Any

from cocotb.handle import HierarchyObject

parameters = [
    "CLASSIFICATION",
    "VERSION",
    "PSEL_WIDTH",
    "ADDR_WIDTH",
    "DATA_WIDTH",
    "Protection_Support",
    "RME_Support",
    "Pstrb_Support",
    "Wakeup_Signal",
    "USER_REQ_WIDTH",
    "USER_DATA_WIDTH",
    "USER_RESP_WIDTH",
    "PSTRB_WIDTH",
]

class Interface:
    def __init__(self, hdl : HierarchyObject) -> None:
        """
        Create an interface
        Work around simulator specific issues with accessing signals inside generates.
        """
        # Parameters
        for p in parameters:
            # Parameters not exposed by list() in some simulators - look up explicitly
            v = getattr(hdl, p)
            if isinstance(v.value, bytes):
                setattr(self, p, str(v.value.decode("utf-8")))
            else:
                setattr(self, p, int(v.value))

        # Signals
        for child in list(hdl):
            # Signals start with a lowercase letter
            if not child._name[0].isupper():
                setattr(self, child._name, child)

        if self.CLASSIFICATION != "APB":
            raise TypeError(f"Expected APB classification, got {self.CLASSIFICATION}")

        if self.VERSION not in [2, 3, 4, 5]:
            raise ValueError(f"Unsupported APB version: {self.VERSION}")

        if self.PSEL_WIDTH < 1:
            raise ValueError(f"Invalid PSEL_WIDTH: {self.PSEL_WIDTH}")

        # Remove un-configured signals
        if self.VERSION < 3:
            delattr(self, "pready")
            delattr(self, "pslverr")

        if self.VERSION < 4 or self.Protection_Support == 0:
            delattr(self, "pprot")

        if self.VERSION < 4 or self.Pstrb_Support == 0:
            delattr(self, "pstrb")

        if self.VERSION < 5 or self.RME_Support == 0:
            delattr(self, "pnse")

        if self.VERSION < 5 or self.Wakeup_Signal == 0:
            delattr(self, "pwakeup")

        if self.VERSION < 5 or self.USER_REQ_WIDTH == 0:
            delattr(self, "pauser")

        if self.VERSION < 5 or self.USER_DATA_WIDTH == 0:
            delattr(self, "pwuser")
            delattr(self, "pruser")

        if self.VERSION < 5 or self.USER_RESP_WIDTH == 0:
            delattr(self, "pbuser")

    def set(self, name : str, value : int) -> None:
        """
        Set the value of a signal (if signal exists)

        :param name: The name of the signal
        :type name: str
        :param value: The value to set
        :type value: int
        :return: None
        """
        signal = getattr(self, name, None)
        if signal is not None:
            signal.value = value

    def get(self, name : str, default : Any = None) -> int:
        """
        Get the value of a signal (if signal exists)

        :param name: The name of the signal
        :type name: str
        :param default: The default value to return if signal does not exist
        :type default: Any
        :return: The value of the signal or the default value
        :rtype: int
        """
        signal = getattr(self, name, None)
        if signal is not None:
            return int(signal.value)
        return default

__all__ = ["Interface"]
