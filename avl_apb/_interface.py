# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Interface

from cocotb.handle import HierarchyObject

from typing import Any

class Interface:
    def __init__(self, hdl : HierarchyObject) -> None:
        """
        Create an interface
        Work around simulator specific issues with accessing signals inside generates.
        """
        # Parameters
        self.classification = str(hdl.CLASSIFICATION.value.decode("utf-8"))
        self.version = int(hdl.VERSION.value)
        self.psel_width = int(hdl.PSEL_WIDTH.value)
        self.address_width = int(hdl.ADDR_WIDTH.value)
        self.data_width = int(hdl.DATA_WIDTH.value)
        self.protection = bool(hdl.PROTECTION.value)
        self.rme = bool(hdl.RME.value)
        self.wakeup = bool(hdl.WAKEUP.value)
        self.user_req_width = int(hdl.USER_REQ_WIDTH.value)
        self.user_data_width = int(hdl.USER_DATA_WIDTH.value)
        self.user_resp_width = int(hdl.USER_RESP_WIDTH.value)

        # Base Signals
        self.pclk = hdl._id("pclk", extended=False)
        self.presetn = hdl._id("presetn", extended=False)
        self.paddr  = hdl._id("paddr", extended=False)
        self.psel = hdl._id("psel", extended=False)
        self.penable = hdl._id("penable", extended=False)
        self.pwrite = hdl._id("pwrite", extended=False)
        self.pwdata = hdl._id("pwdata", extended=False)
        self.prdata = hdl._id("prdata", extended=False)

        # APB3
        if self.version >= 3:
            self.pready = hdl._id("apb3.pready", extended=False)
            self.pslverr = hdl._id("apb3.pslverr", extended=False)

        # APB4
        if self.version >= 4 :
            self.pstrb = hdl._id("apb4.pstrb", extended=False)
            if self.protection:
                self.pprot = hdl._id("apb4.pprot", extended=False)

        # APB5
        if self.version >= 5:
            if self.protection and self.rme:
                self.pnse = hdl._id("apb5.pnse", extended=False)
            if self.wakeup:
                self.pwakeup = hdl._id("apb5.pwakeup", extended=False)
            if self.user_req_width > 0:
                self.pauser = hdl._id("apb5.pauser", extended=False)
            if self.user_data_width > 0:
                self.pwuser = hdl._id("apb5.pwuser", extended=False)
                self.pruser = hdl._id("apb5.pruser", extended=False)
            if self.user_resp_width > 0:
                self.pbuser = hdl._id("apb5.pbuser", extended=False)

    def set(self, name : str, value : int) -> None:
        signal = getattr(self, name, None)
        if signal is not None:
            signal.value = value

    def get(self, name : str, default : Any = None) -> int:
        signal = getattr(self, name, None)
        if signal is not None:
            return signal.value
        return default

__all__ = ["Interface"]
