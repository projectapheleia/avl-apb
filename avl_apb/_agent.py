# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Agent

import avl
from cocotb.handle import HierarchyObject
from cocotb.triggers import NextTimeStep, RisingEdge

from ._agent_cfg import AgentCfg
from ._bandwidth import Bandwidth
from ._cdriver import CplDriver
from ._coverage import Coverage
from ._interface import Interface
from ._monitor import Monitor
from ._rdriver import ReqDriver
from ._rsequence import ReqSequence


class Agent(avl.Agent):
    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize the avl-apb Agent

        :param name: Name of the agent instance
        :type name: str
        :param parent: Parent component
        :type parent: Component
        """
        super().__init__(name, parent)

        # Create configuration and export to children
        self.cfg = avl.Factory.get_variable(f"{self.get_full_name()}.cfg", AgentCfg("cfg", self))
        avl.Factory.set_variable(f"{self.get_full_name()}.*.cfg", self.cfg)

        # Bind HDL to establish parameters and configuration
        self._bind_(avl.Factory.get_variable(f"{self.get_full_name()}.hdl", None))

        # Create sequencer and driver if requester is enabled
        if self.cfg.has_requester:
            self.rsqr = avl.Sequencer("rsqr", self)
            self.rseq = ReqSequence("rseq",self.rsqr)
            self.rdrv = ReqDriver("rdrv", self)
            self.rsqr.seq_item_export.connect(self.rdrv.seq_item_port)

        if self.cfg.num_completer > 1:
            self.cdrv = []
            for i in range(self.cfg.num_completer):
                avl.Factory.set_variable(f"{self.get_full_name()}.cdrv_{i}.idx", i)
                self.cdrv.append(CplDriver(f"cdrv_{i}", self))
        elif self.cfg.num_completer == 1:
            self.cdrv = CplDriver("cdrv", self)

        # Create monitor if enabled
        if self.cfg.has_monitor:
            self.monitor = Monitor("monitor", self)

            if self.cfg.has_coverage:
                self.coverage = Coverage("coverage", self)
                self.monitor.item_export.connect(self.coverage.item_port)

            if self.cfg.has_bandwidth:
                self.bandwidth = Bandwidth("bandwidth", self)
                self.monitor.item_export.connect(self.bandwidth.item_port)

            if self.cfg.has_trace:
                self.trace = avl.Trace("trace", self)
                self.monitor.item_export.connect(self.trace.item_port)

    def _bind_(self, hdl) -> None:
        """
        Bind the agent to a hardware description language (HDL) interface.
        This method is used to associate the agent with a specific HDL interface,
        allowing it to interact with the hardware model.

        :param hdl: The HDL interface to bind to the agent
        :type hdl: HierarchyObject
        :raises TypeError: If `hdl` is not an instance of HierarchyObject
        """
        if not isinstance(hdl, HierarchyObject):
            raise TypeError(f"Expected HierarchyObject, got {type(hdl)}")

        # Assign Interface
        self.i_f = Interface(hdl)
        avl.Factory.set_variable(f"{self.get_full_name()}.*.i_f", self.i_f)

    async def run_phase(self) -> None:
        """
        Run the agent's phase. This method is called to start the agent's operation.
        It initializes the agent and starts the requester and completer if they are active.
        """

        self.raise_objection()
        await NextTimeStep()

        if self.cfg.has_requester:
            await self.rseq.start()

        # Run-off
        for _ in range(10):
            await RisingEdge(self.i_f.pclk)

        self.drop_objection()

__all__ = ["Agent"]
