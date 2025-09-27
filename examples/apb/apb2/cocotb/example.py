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

        cocotb.start_soon(self.timeout(1, units="ms"))
        cocotb.start_soon(self.clock(self.clk, 100))
        await self.async_reset(self.rst_n, duration=100, units="ns", active_high=False)

        self.drop_objection()

@cocotb.test
async def test(dut):
    """
    Example APB2 interface
        - No pready
        - No pslverr
        - Single psel
        - 100 items in the request sequence with a rate limit of 0.1
        - random data

    :param dut: The DUT instance
    :return: None
    """
    avl.Factory.set_variable("*.clk", dut.clk)
    avl.Factory.set_variable("*.rst_n", dut.rst_n)
    avl.Factory.set_variable("*.hdl", dut.apb_if)
    avl.Factory.set_variable("*.agent.cfg.has_requester", True)
    avl.Factory.set_variable("*.agent.cfg.num_completer", 1)
    avl.Factory.set_variable("*.agent.cfg.has_monitor", True)
    avl.Factory.set_variable("*.agent.rsqr.rseq.n_items", 100)
    avl.Factory.set_variable("*.agent.rdrv.rate_limit", lambda: 0.1)

    avl.Factory.set_override_by_type(avl_apb.CplDriver, avl_apb.CplRandomDriver)

    e = example_env("env", None)
    await e.start()

