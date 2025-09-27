# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Monitor

import asyncio

import avl
import cocotb
from cocotb.triggers import FallingEdge, First, RisingEdge
from cocotb.utils import get_sim_time

from ._item import SequenceItem


class Monitor(avl.Monitor):
    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize the AMBA Monitor for the APB agent.

        :param name: Name of the agent instance
        :type name: str
        :param parent: Parent component
        :type parent: Component
        """
        super().__init__(name, parent)

        self.i_f = avl.Factory.get_variable(f"{self.get_full_name()}.i_f", None)

        self.wakeup = 0

    async def monitor(self) -> None:
        """
        Monitor the APB bus signals and create sequence items based on the activity.
        This method is called to monitor the bus signals and create sequence items
        when there is activity on the bus.
        """
        try:
            item = SequenceItem(f"from_{self.name}", self)
            item.wait_cycles = 0

            while bool(self.i_f.get("penable")):
                await RisingEdge(self.i_f.pclk)

            item.time_since_wakeup = get_sim_time("ns") - self.wakeup

            item.set("psel",   self.i_f.get("psel"))
            item.set("paddr",  self.i_f.get("paddr"))
            item.set("pwrite", self.i_f.get("pwrite"))
            item.set("pwdata", self.i_f.get("pwdata"))
            item.set("pstrb" , self.i_f.get("pstrb"))
            item.set("pprot",  self.i_f.get("pprot"))
            item.set("pnse",   self.i_f.get("pnse"))
            item.set("pauser", self.i_f.get("pauser"))
            item.set("pwuser", self.i_f.get("pwuser"))

            while True:
                await RisingEdge(self.i_f.pclk)
                if bool(self.i_f.get("pready", 1)):
                    break
                item.wait_cycles += 1

            item.set("prdata", self.i_f.get("prdata"))
            item.set("pslverr", self.i_f.get("pslverr"))
            item.set("prdata", self.i_f.get("prdata"))
            item.set("pbuser", self.i_f.get("pbuser"))

            # Send to export
            self.item_export.write(item)

        except asyncio.CancelledError:
            raise
        except Exception:
            self.debug(f"Drive task for item {item} was cancelled by reset")
            item.set_event("done")

    async def run_phase(self):
        """
        Run phase for the Requester Driver.
        This method is called during the run phase of the simulation.
        It is responsible for driving the request signals based on the sequencer's items.

        :raises NotImplementedError: If the run phase is not implemented.
        """

        async def wait_on_wakeup() -> None:
            while True:
                await RisingEdge(self.i_f.pwakeup)
                self.wakeup = get_sim_time("ns")

        async def wait_on_reset() -> None:
            try:
                await FallingEdge(self.i_f.presetn)
                await self.reset()
            except asyncio.CancelledError:
                raise
            except Exception:
                pass

        # Start Wakeup Monitor
        if hasattr(self.i_f, "pwakeup"):
            cocotb.start_soon(wait_on_wakeup())

        while True:
            if self.i_f.presetn == 0 or self.i_f.psel == 0 or self.i_f.get("pwakeup", 1) == 0:
                await RisingEdge(self.i_f.pclk)
                continue

            monitor_task = cocotb.start_soon(self.monitor())
            reset_task = cocotb.start_soon(wait_on_reset())

            await First(monitor_task, reset_task)
            for t in [monitor_task, reset_task]:
                if not t.done():
                    t.cancel()

__all__ = ["Monitor"]
