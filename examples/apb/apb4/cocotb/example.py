# Copyright 2024 Apheleia
#
# Description:
# Apheleia attributes example


import avl
import avl_apb
import cocotb


class example_env(avl.Env):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.hdl = avl.Factory.get_variable(f"{self.get_full_name()}.hdl", None)
        self.clk = avl.Factory.get_variable(f"{self.get_full_name()}.clk", None)
        self.rst_n = avl.Factory.get_variable(f"{self.get_full_name()}.rst_n", None)
        self.agent = avl_apb.Agent("agent", self)

    async def run_phase(self):
        self.raise_objection()

        await cocotb.start(self.timeout(1, units="ms"))
        await cocotb.start(self.clock(self.clk, 100))
        await self.async_reset(self.rst_n, duration=100, units="ns", active_high=False)

        self.drop_objection()

@cocotb.test
async def test(dut):
    """
    Example APB4 interface
        - Single psel
        - 1000 items in the request sequence with a rate limit of 0.1
            - 2 memory ranges (0x0000, 0x00FF) and (0xFF00, 0xFFFF)
        - pready with rate limit of 0.8
        - pslverr for paddr not in (0x0000, 0x00FF)
        - random wdata
        - memory based rdata
        - random pstrb
        - random pprot

    :param dut: The DUT instance
    :return: None
    """
    avl.Factory.set_variable("*.clk", dut.clk)
    avl.Factory.set_variable("*.rst_n", dut.rst_n)
    avl.Factory.set_variable("*.hdl", dut.apb_if)
    avl.Factory.set_variable("*.agent.cfg.has_requester", True)
    avl.Factory.set_variable("*.agent.cfg.num_completer", 1)
    avl.Factory.set_variable("*.agent.cfg.has_monitor", True)
    avl.Factory.set_variable("*.agent.cfg.has_coverage", True)
    avl.Factory.set_variable("*.agent.cfg.has_bandwidth", True)
    avl.Factory.set_variable("*.agent.cfg.has_trace", True)
    avl.Factory.set_variable("*.agent.rsqr.rseq.n_items", 100)
    avl.Factory.set_variable("*.agent.rdrv.rate_limit", lambda : 0.1)
    avl.Factory.set_variable("*.agent.cdrv.rate_limit", lambda : 0.8)

    # Set the ranges for the request sequence
    req_ranges = {
        (0, 0x0000, 0x00FF): 0.9,
        (0, 0xFF00, 0xFFFF): 0.1,
    }
    avl.Factory.set_variable("*.agent.rsqr.rseq.ranges", req_ranges)

    # Set the range for the completer driver
    avl.Factory.set_variable("*.agent.cdrv.ranges", [(0x0000, 0x00FF)])

    avl.Factory.set_override_by_type(avl_apb.CplDriver, avl_apb.CplMemoryDriver)
    e = example_env("env", None)
    await e.start()

