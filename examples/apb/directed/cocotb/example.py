# Copyright 2024 Apheleia
#
# Description:
# Apheleia attributes example


import avl
import avl_apb
import cocotb

class DirectedSequence(avl_apb.ReqSequence):
    async def body(self) -> None:
        self.info(f"Starting Requester Manager sequence {self.get_full_name()}")

        # Aligned write and read back
        await self.write(psel=1, paddr=0x100, pwdata=0xdeadbeef, pstrb=0xf)
        cpl = await self.read(psel=1, paddr=0x100)
        assert cpl.prdata == 0xdeadbeef

        # Partial aligned write
        await self.write(psel=1, paddr=0x100, pwdata=0xcafebabe, pstrb=0x3)
        cpl = await self.read(psel=1, paddr=0x100)
        assert cpl.prdata == 0xdeadbabe

        # Offset writes
        await self.write(psel=1, paddr=0x201, pwdata=0x76543210, pstrb=0xe)
        cpl = await self.read(psel=1, paddr=0x200)
        assert cpl.prdata == 0x76543200
        cpl = await self.read(psel=1, paddr=0x204)
        assert cpl.prdata == 0x00000000

        # Offset reads
        await self.write(psel=1, paddr=0x300, pwdata=0x76543210, pstrb=0xf)
        await self.write(psel=1, paddr=0x304, pwdata=0xfedcba98, pstrb=0xf)
        cpl = await self.read(psel=1, paddr=0x302)
        assert cpl.prdata == 0x7654ba98


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
    avl.Factory.set_variable("*.agent.rdrv.rate_limit", lambda : 0.5)
    avl.Factory.set_variable("*.agent.cdrv.rate_limit", lambda : 0.5)

    # Set the ranges for the request sequence
    req_ranges = {
        (0, 0x0000, 0x4000): 1.9,
    }
    avl.Factory.set_variable("*.agent.rsqr.rseq.ranges", req_ranges)

    # Set the range for the completer driver
    avl.Factory.set_variable("*.agent.cdrv.ranges", [(0x0000, 0x4000)])

    avl.Factory.set_override_by_type(avl_apb.CplDriver, avl_apb.CplMemoryDriver)
    avl.Factory.set_override_by_type(avl_apb.ReqSequence, DirectedSequence)
    e = example_env("env", None)
    await e.start()

