# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Driver

import asyncio
import random

import avl
from cocotb.triggers import RisingEdge

from ._driver import Driver
from ._item import SequenceItem


class CplDriver(Driver):

    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize the Requester Driver for the AMBA agent.

        :param name: Name of the agent instance
        :type name: str
        :param parent: Parent component
        :type parent: Component
        """
        super().__init__(name, parent)

        self.idx = avl.Factory.get_variable(f"{self.get_full_name()}.idx", 0)
        """Index of the driver in the AMBA interface (psel), used to select the correct signals."""

    async def reset(self) -> None:
        """
        Reset the driver by setting all signals to their default values.
        This method is called when the driver is reset.

        By default 0's all signals - can be overridden in subclasses to add randomization or other behavior.
        """

        self.i_f.set("prdata", 0)
        self.i_f.set("pready", 0)
        self.i_f.set("pslverr", 0)
        self.i_f.set("pbuser", 0)
        self.i_f.set("pruser", 0)

    async def drive(self, item : SequenceItem) -> None:
        """
        Drive the signals based on the provided sequence item.
        This method is called to drive the signals of the AMBA interface.

        :param item: The sequence item containing the values to drive
        :type item: SequenceItem
        """
        try:

            if self.i_f.get("pready") is not None:
                self.i_f.set("pready", 0)
                # Rate Limiter
                rate = self.rate_limit()
                while random.random() > rate:
                    await RisingEdge(self.i_f.pclk)
                self.i_f.set("pready", 1)

            self.i_f.set("prdata", item.get("prdata"))
            self.i_f.set("pslverr", item.get("pslverr"))
            self.i_f.set("pruser", item.get("pruser"))
            self.i_f.set("pbuser", item.get("pbuser"))

            # Wait for the next clock edge to drive the item
            await RisingEdge(self.i_f.pclk)

            # Clear the bus
            await self.quiesce()

        except asyncio.CancelledError:
            raise
        except Exception:
            self.debug(f"Completer drive task for item was cancelled by reset:\n{item}")

    async def get_next_item(self, item : SequenceItem = None) -> SequenceItem:
        """
        Get the next sequence item.

        The implementation ensures items are driven on the rising edge of pclk, when not in reset,
        while allowing for back-to-back requests if the sequencer provides them.

        :param item: The sequence item to retrieve, defaults to None
        :type item: SequenceItem, optional
        :return: The next sequence item
        :rtype: SequenceItem
        :raises NotImplementedError: If the method is not implemented in subclasses
        """

        while True:
            await RisingEdge(self.i_f.pclk)
            if self.i_f.get("presetn") == 0:
                continue

            if bool(self.i_f.get("psel") & (1 << self.idx)) and bool(self.i_f.get("pwakeup", 1)):

                next_item = SequenceItem(f"from_{self.name}", self)
                next_item.set("paddr", self.i_f.get("paddr"))
                next_item.set("psel", self.i_f.get("psel"))
                next_item.set("pwrite", self.i_f.get("pwrite"))
                next_item.set("pwdata", self.i_f.get("pwdata"))
                next_item.set("prdata", 0)
                next_item.set("pslverr", 0)
                next_item.set("pstrb", self.i_f.get("pstrb"))
                next_item.set("pprot", self.i_f.get("pprot"))
                next_item.set("pnse", self.i_f.get("pnse"))
                next_item.set("pauser", self.i_f.get("pauser"))
                next_item.set("pwuser", self.i_f.get("pwuser"))
                next_item.set("pruser", 0)
                next_item.set("pbuser", 0)

                return next_item


class CplRandomDriver(CplDriver):
    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize the Random Driver for the APB agent.

        :param name: Name of the agent instance
        :type name: str
        :param parent: Parent component
        :type parent: Component
        """
        super().__init__(name, parent)

    async def get_next_item(self, item : SequenceItem = None) -> SequenceItem:
        """
        Get the next sequence item with randomization.

        In the random driver implementation, the item fields are randomized
        based on constraints from the sequence item.
        """
        item = await super().get_next_item(item)
        item.randomize_completion()

        return item

class CplMemoryDriver(CplDriver):
    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize the Memory Driver for the APB agent.

        This driver uses a memory model to simulate the behavior of the APB interface.

        It allows for reading and writing to a memory model, which is useful for
        simulating memory-mapped devices.

        By default accesses which miss the allocated range will return slverr (if supported)
        and randomize the item.

        :param name: Name of the agent instance
        :type name: str
        :param parent: Parent component
        :type parent: Component
        """
        super().__init__(name, parent)
        self.memory = avl.Memory(width=self.i_f.DATA_WIDTH)
        self.memory.miss = lambda address : None

        # Add ranges to the memory if specified in the configuration
        self.ranges = avl.Factory.get_variable(f"{self.get_full_name()}.ranges", None)
        if self.ranges is not None:
            for r in self.ranges:
                self.memory.add_range(r[0], r[1])

    async def get_next_item(self, item : SequenceItem = None) -> SequenceItem:
        """
        Get the next sequence item as if targeting a memory.

        In the memory driver implementation, the item memory is updated and
        returns data from the memory if the address is valid.

        In the event the address is not valid, the item is randomized and a plslverr
        signal is set to indicate an error (if present)
        """
        item = await super().get_next_item(item)

        if self.memory._check_address_(item.get("paddr")):
            if item.get("pwrite", False):
                self.memory.write(item.get("paddr"), item.get("pwdata"), strobe=item.get("pstrb", None))
            else:
                item.set("prdata", self.memory.read(item.get("paddr")))
        else:
            if hasattr(item, "pslverr"):
                item.add_constraint("_c_pslverr_", lambda x: x == 1, item.pslverr)
            item.randomize_completion()
        return item

__all__ = ["CplDriver", "CplRandomDriver", "CplMemoryDriver"]
