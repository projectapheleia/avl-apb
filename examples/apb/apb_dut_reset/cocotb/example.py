import avl
import avl_apb
import cocotb
from cocotb.triggers import RisingEdge


class example_env(avl.Env):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.rst_n = avl.Factory.get_variable(f"{self.get_full_name()}.rst_n", None)
        self.agent = avl_apb.Agent("agent", self)

    async def run_phase(self):
        self.raise_objection()
        


        # Only bound the run. A hang at 0 ns never reaches this timer because the simulator
        # never regains control.
        cocotb.start_soon(self.timeout(100, units="us"))
        await RisingEdge(self.rst_n)

        self.drop_objection()


@cocotb.test
async def test(dut):
    """APB3, reset from the HDL in time step 0, 20 random items answered by a random completer."""
    avl.Factory.set_variable("*.rst_n", dut.rst_n)
    avl.Factory.set_variable("*.hdl", dut.u_apb)
    avl.Factory.set_variable("*.agent.cfg.has_requester", True)
    avl.Factory.set_variable("*.agent.cfg.num_completer", 1)
    avl.Factory.set_variable("*.agent.cfg.has_monitor", True)
    avl.Factory.set_variable("*.agent.cfg.has_coverage", False)
    avl.Factory.set_variable("*.agent.cfg.has_bandwidth", False)
    avl.Factory.set_variable("*.agent.cfg.has_trace", True)
    avl.Factory.set_variable("*.agent.rsqr.rseq.n_items", 20)

    avl.Factory.set_override_by_type(avl_apb.CplDriver, avl_apb.CplRandomDriver)
    e = example_env("env", None)
    # rpdb = RemotePdb("0.0.0.0", 4444)
    # rpdb.set_trace()  # place where needed
    await e.start()
