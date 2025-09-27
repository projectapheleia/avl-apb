# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Bandwidth Monitor

import avl
import cocotb
import matplotlib.pyplot as plt
import numpy as np
from cocotb.triggers import Timer
from cocotb.utils import get_sim_time


class Bandwidth(avl.Component):

    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize Bandwidth Monitor

        Class contains variable window_ns which defines the time window in nanoseconds. This
        is configurable via the factory.

        :param name: Name of the bandwidth monitor.
        :type name: str
        :param parent: Parent component.
        :type parent: Component
        """
        super().__init__(name, parent)
        self.i_f = avl.Factory.get_variable(f"{self.get_full_name()}.i_f", None)

        self.window_ns = avl.Factory.get_variable(f"{self.get_full_name()}.window_ns", 1000)
        """ Rolling ime window in nanoseconds for bandwidth calculation. Default is 1000 ns. """

        self.item_port = avl.List()
        self.bandwidth = {}

    async def run_phase(self) -> None:
        """
        Run phase for the coverage component.

        """
        async def counter():
            while True:
                self.item = await self.item_port.blocking_get()

                incr = self.i_f.PSTRB_WIDTH
                if self.item.get("pwrite"):
                    pstrb = self.item.get("pstrb", None)
                    if pstrb is not None:
                        incr = bin(pstrb).count("1")
                self.bandwidth[t] += incr

        cocotb.start_soon(counter())

        while True:
            t = get_sim_time(unit="ns")
            self.bandwidth[t] = 0

            self.raise_objection()
            await Timer(self.window_ns, unit="ns")
            self.drop_objection()

    async def report_phase(self) -> None:
        """
        Report phase for the bandwidth component.

        Generate plot of bytes on bus over time windows

        """
        times = list(self.bandwidth.keys())
        counts = list(self.bandwidth.values())

        if len(times) > 1:
            # For unevenly spaced data, calculate individual widths
            # This uses the minimum spacing to avoid overlapping bars
            spacings = np.diff(times)
            bar_width = np.min(spacings)
        else:
            # For single bar, use a default width
            bar_width = 1

        # Create plot
        plt.figure(figsize=(8, 4))
        plt.bar(times, counts, width=bar_width, align='center')
        plt.title("Bus Bandwidth (Bytes over Time)")
        plt.xlabel("Time (ns)")
        plt.ylabel("Byte Count")
        plt.grid(True)

        # Export to PNG
        plt.savefig(f"{self.get_full_name()}.png")
        plt.close()

__all__ = ["Bandwidth"]
