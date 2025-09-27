# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Base Driver


import asyncio

import avl
import cocotb
from cocotb.triggers import FallingEdge, First

from ._item import SequenceItem


class Driver(avl.Driver):

    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize the Driver for the APB agent.

        :param name: Name of the agent instance
        :type name: str
        :param parent: Parent component
        :type parent: Component
        """
        super().__init__(name, parent)

        self.i_f = avl.Factory.get_variable(f"{self.get_full_name()}.i_f", None)
        self.rate_limit = avl.Factory.get_variable(f"{self.get_full_name()}.rate_limit", lambda : 1.0)
        """Rate limit for driving signals. lambda function (0.0 - 1.0)"""

        if not callable(self.rate_limit):
            raise TypeError("rate_limit must be a callable (lambda function) that returns a float between 0.0 and 1.0")

    async def reset(self) -> None:
        """
        Reset the driver by setting all signals to their default values.
        This method is called when the driver is reset.

        By default 0's all signals - can be overridden in subclasses to add randomization or other behavior.
        """

        raise NotImplementedError("Reset method must be implemented in subclasses")

    async def wait_on_reset(self) -> None:
        """
        Wait for the reset signal to go low and then call the reset method.
        This method is called to ensure that the driver is reset before driving any signals.
        It waits for the presetn signal to go low, indicating that the reset is active,
        and then calls the reset method to set all signals to their default values.
        """

        try:
            await FallingEdge(self.i_f.presetn)
            await self.reset()
        except asyncio.CancelledError:
            raise
        except Exception:
            pass

    async def quiesce(self) -> None:
        """
        Quiesce the driver by setting the psel signal to 0.
        This method is called when the driver is quiesced.

        By default calls reset() to set all signals to their default values.
        Can be overridden in subclasses to add randomization or other behavior.
        """

        await self.reset()

    async def drive(self, item : SequenceItem) -> None:
        """
        Drive the signals based on the provided sequence item.
        This method is called to drive the signals of the APB interface.

        :param item: The sequence item containing the values to drive
        :type item: SequenceItem
        """
        raise NotImplementedError("Drive method must be implemented in subclasses")

    async def get_next_item(self, item : SequenceItem = None) -> SequenceItem:
        """
        Get the next sequence item.

        For the Request driver this method retrieves the next sequence item from the sequencer or
        the previously reset interrupted item.

        The implementation ensures items are driven on the rising edge of pclk, when not in reset,
        while allowing for back-to-back requests if the sequencer provides them.

        For the completion driver this method adjusts the completion side of the observed request.

        :param item: The sequence item to retrieve, defaults to None
        :type item: SequenceItem, optional
        :return: The next sequence item
        :rtype: SequenceItem
        :raises NotImplementedError: If the method is not implemented in subclasses
        """

        raise NotImplementedError("get_next_item method must be implemented in subclasses")

    async def run_phase(self):
        """
        Run phase for the Requester Driver.
        This method is called during the run phase of the simulation.
        It is responsible for driving the request signals based on the sequencer's items.

        :raises NotImplementedError: If the run phase is not implemented.
        """
        item = None

        # Start from reset state
        await self.reset()

        while True:
            item = await self.get_next_item(item)

            drive_task = cocotb.start_soon(self.drive(item))
            reset_task = cocotb.start_soon(self.wait_on_reset())

            await First(drive_task, reset_task)

            if drive_task.done():
                item = None

            for t in [drive_task, reset_task]:
                if not t.done():
                    t.cancel()

__all__ = ["Driver"]
