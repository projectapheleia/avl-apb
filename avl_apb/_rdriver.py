# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Driver

import asyncio
import random

import avl
import cocotb
from cocotb.triggers import First, NextTimeStep, RisingEdge

from ._driver import Driver
from ._item import SequenceItem


class ReqDriver(Driver):

    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize the Requester Driver for the AMBA agent.

        :param name: Name of the agent instance
        :type name: str
        :param parent: Parent component
        :type parent: Component
        """
        super().__init__(name, parent)

        # Pre and Post Wakeup
        if hasattr(self.i_f, "pwakeup"):
            self.pre_wakeup =  avl.Factory.get_variable(f"{self.get_full_name()}.pre_wakeup", lambda : 0.1)
            """Pre-wakeup delay - time to wait before driving the wakeup signal (0.0 - 1.0) (>= version 5)"""
            self.post_wakeup = avl.Factory.get_variable(f"{self.get_full_name()}.post_wakeup", lambda : 0.1)
            """Post-wakeup delay - time to wait after driving the wakeup signal (0.0 - 1.0) (>= version 5)"""

            if not callable(self.pre_wakeup) or not callable(self.post_wakeup):
                raise TypeError("pre_wakeup and post_wakeup must be callable (lambda functions) that return a float between 0.0 and 1.0")

    async def reset(self) -> None:
        """
        Reset the driver by setting all signals to their default values.
        This method is called when the driver is reset.

        By default 0's all signals - can be overridden in subclasses to add randomization or other behavior.
        """

        self.i_f.set("pwakeup", 0)
        self.i_f.set("paddr", 0)
        self.i_f.set("psel", 0)
        self.i_f.set("penable", 0)
        self.i_f.set("pwrite", 0)
        self.i_f.set("pwdata", 0)
        self.i_f.set("pstrb", 0)
        self.i_f.set("pprot", 0)
        self.i_f.set("pnse", 0)
        self.i_f.set("pwakeup", 0)
        self.i_f.set("pauser", 0)
        self.i_f.set("pwuser", 0)

    async def quiesce(self) -> None:
        """
        Quiesce the driver by setting the psel signal to 0.
        This method is called when the driver is quiesced.

        By default calls reset() to set all signals to their default values.
        Can be overridden in subclasses to add randomization or other behavior.
        """

        self.i_f.set("paddr", 0)
        self.i_f.set("psel", 0)
        self.i_f.set("penable", 0)
        self.i_f.set("pwrite", 0)
        self.i_f.set("pwdata", 0)
        self.i_f.set("pstrb", 0)
        self.i_f.set("pprot", 0)
        self.i_f.set("pnse", 0)
        self.i_f.set("pauser", 0)
        self.i_f.set("pwuser", 0)

    async def drive(self, item : SequenceItem) -> None:
        """
        Drive the signals based on the provided sequence item.
        This method is called to drive the signals of the AMBA interface.

        :param item: The sequence item containing the values to drive
        :type item: SequenceItem
        """
        awake = False
        try:
            self.i_f.set("penable", 0)

            # Rate Limiter
            rate = self.rate_limit()
            while random.random() > rate:
                await RisingEdge(self.i_f.pclk)

            if hasattr(self.i_f, "pwakeup") and not awake:
                self.i_f.set("pwakeup", 1)
                delay = self.pre_wakeup()
                while random.random() > delay:
                    await RisingEdge(self.i_f.pclk)


            self.i_f.set("psel",   item.get("psel"))
            self.i_f.set("paddr",  item.get("paddr"))
            self.i_f.set("pwrite", item.get("pwrite"))
            self.i_f.set("pwdata", item.get("pwdata"))
            self.i_f.set("pstrb",  item.get("pstrb"))
            self.i_f.set("pprot",  item.get("pprot"))
            self.i_f.set("pnse",   item.get("pnse"))
            self.i_f.set("pauser", item.get("pauser"))
            self.i_f.set("pwuser", item.get("pwuser"))

            await RisingEdge(self.i_f.pclk)
            self.i_f.set("penable", 1)

            while True:
                await RisingEdge(self.i_f.pclk)
                if self.i_f.get("pready", 1) and self.i_f.get("pwakeup", 1):
                    break

            item.set("prdata", self.i_f.get("prdata"))
            item.set("pruser", self.i_f.get("pruser"))
            item.set("pslverr", self.i_f.get("pslverr"))
            item.set("pbuser", self.i_f.get("pbuser"))

            # Clear the bus
            await self.quiesce()

            # Post wakeup
            if item.get("goto_sleep", False):
                delay = self.post_wakeup()
                while random.random() > delay:
                    await RisingEdge(self.i_f.pclk)
                self.i_f.set("pwakeup", 0)
                awake = False
            else:
                awake = True

            item.set_event("done")

        except asyncio.CancelledError:
            raise
        except Exception:
            self.warning(f"Requester drive task for item was cancelled by reset:\n{item}")

    async def get_next_item(self, item : SequenceItem = None) -> SequenceItem:
        """
        Get the next sequence item.

        This method retrieves the next sequence item from the sequencer or
        the previously reset interrupted item.

        The implementation ensures items are driven on the rising edge of pclk, when not in reset,
        while allowing for back-to-back requests if the sequencer provides them.

        :param item: The sequence item to retrieve, defaults to None
        :type item: SequenceItem, optional
        :return: The next sequence item
        :rtype: SequenceItem
        :raises NotImplementedError: If the method is not implemented in subclasses
        """

        async def next_time_step() -> None:
            await NextTimeStep()

        if item is not None:
            next_item = item
        else:
            a = cocotb.start_soon(self.seq_item_port.blocking_get())
            b = cocotb.start_soon(next_time_step())

            await First(a, b)
            if not a.done():
                await a
                await RisingEdge(self.i_f.pclk)
            next_item = a.result()

        while self.i_f.get("presetn") == 0:
            await RisingEdge(self.i_f.pclk)

        return next_item

__all__ = ["ReqDriver"]
