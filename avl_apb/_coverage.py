# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Coverage

import avl

from ._item import SequenceItem


class Coverage(avl.Component):

    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize Coverage

        :param name: Name of the coverage class.
        :type name: str
        :param parent: Parent component.
        :type parent: Component
        """
        super().__init__(name, parent)

        self.item_port = avl.List()
        self.item = SequenceItem("for_coverage", self)

        # Define coverage
        self.cg = avl.Covergroup("apb", self)
        self.cg.set_comment("APB Coverage")

        # PSEL
        self.cp_psel = self.cg.add_coverpoint("psel", lambda: self.item.psel)
        self.cp_psel.set_comment("PSEL (1-hot select)")
        for i in range(self.item.psel.width):
            self.cp_psel.add_bin(f"{i}", lambda x, y=i : x & (1<<y))

        # PADDR
        self.cp_paddr_bits = self.cg.add_coverpoint("paddr_bits", lambda: self.item.paddr)
        self.cg.set_comment("PADDR (address bits)")
        for i in range(self.item.paddr.width):
            self.cp_paddr_bits.add_bin(f"[{i}] == 0", lambda x, y=i : 0 == (x & (1<<y)))
            self.cp_paddr_bits.add_bin(f"[{i}] == 1", lambda x, y=i : 0 != (x & (1<<y)))

        # PWRITE
        self.cp_pwrite = self.cg.add_coverpoint("pwrite", lambda: self.item.pwrite)
        self.cp_pwrite.set_comment("PWRITE (write enable)")
        for i in range(2):
            self.cp_pwrite.add_bin(f"{i}", i)

        # PWDATA
        self.cp_pwdata = self.cg.add_coverpoint("pwdata", lambda: self.item.pwdata if self.item.pwrite == 1 else 0)
        self.cp_pwdata.set_comment("PWDATA (write data)")
        for i in range(self.item.pwdata.width):
            self.cp_pwdata.add_bin(f"[{i}] == 0", lambda x ,y=i: 0 == (x & (1<<y)))
            self.cp_pwdata.add_bin(f"[{i}] == 1", lambda x ,y=i: 0 != (x & (1<<y)))

        # PRDATA
        self.cp_prdata = self.cg.add_coverpoint("prdata", lambda: self.item.prdata if self.item.pwrite == 0 else 0)
        self.cp_prdata.set_comment("PRDATA (read data)")
        for i in range(self.item.prdata.width):
            self.cp_prdata.add_bin(f"[{i}] == 0", lambda x ,y=i: 0 == (x & (1<<y)))
            self.cp_prdata.add_bin(f"[{i}] == 1", lambda x ,y=i: 0 != (x & (1<<y)))

        if hasattr(self.item, "wait_cycles"):
            # PREADY
            self.cp_wait_cycles = self.cg.add_coverpoint("wait_cycles", lambda: self.item.wait_cycles)
            self.cp_wait_cycles.set_comment("Wait cycles (number of cycles before PREADY after PENABLE)")
            for i in range(3):
                self.cp_wait_cycles.add_bin(f"{i}", i)
            self.cp_wait_cycles.add_bin("wait_cycles", range(0,1024), stats=True)

        if hasattr(self.item, "pslverr"):
            # PSLVERR
            self.cp_psvlverr = self.cg.add_coverpoint("pslverr", lambda: self.item.pslverr)
            for i in range(2):
                self.cp_psvlverr.add_bin(f"{i}", i)

            self.cc_pslverrXpwrite = self.cg.add_covercross("pslverrXpwrite", self.cp_psvlverr, self.cp_pwrite)
            self.cc_pslverrXpwrite.set_comment("Cross PSLVERR and PWRITE")

        if hasattr(self.item, "pstrb"):
            # PSTRB
            self.cp_pstrb = self.cg.add_coverpoint("pstrb", lambda: self.item.pstrb if self.item.pwrite == 1 else 0)
            self.cp_pstrb.set_comment("PSTRB (write strobe)")
            for i in range(self.item.pstrb.width):
                self.cp_pstrb.add_bin(f"[{i}] == 0", lambda x, y=i : 0 == (x & (1<<y)))
                self.cp_pstrb.add_bin(f"[{i}] == 1", lambda x, y=i : 0 != (x & (1<<y)))

            self.cp_pstrb_size = self.cg.add_coverpoint("pstrb_size", lambda: int(self.item.pstrb).bit_count() if self.item.pwrite == 1 else 0)
            self.cp_pstrb_size.set_comment("PSTRB (write strobe size)")
            for i in range(1, self.item.pstrb.width+1):
                self.cp_pstrb_size.add_bin(f"{i}", i)

        if hasattr(self.item, "pprot"):
            # PPROT
            self.cp_pprot = self.cg.add_coverpoint("pprot", lambda: self.item.pprot)
            self.cp_pprot.set_comment("PPROT (protection)")
            for i in range(8):
                self.cp_pprot.add_bin(f"{i}", i)

            self.cc_pprotXpwrite = self.cg.add_covercross("pprotXpwrite", self.cp_pprot, self.cp_pwrite)
            self.cc_pprotXpwrite.set_comment("Cross PPROT and PWRITE")

        if hasattr(self.item, "pnse"):
            # PNSE
            self.cp_pnse = self.cg.add_coverpoint("pnse", lambda: self.item.pnse)
            self.cp_pnse.set_comment("PNSE (non-secure enable)")
            for i in range(2):
                self.cp_pnse.add_bin(f"{i}", i)

            self.cc_pprotXpnse = self.cg.add_covercross("pprotXpnse", self.cp_pprot, self.cp_pnse)
            self.cc_pprotXpnse.set_comment("Cross PPROT and PNSE")

            self.cc_pnseXpwrite = self.cg.add_covercross("pnseXpwrite", self.cp_pnse, self.cp_pwrite)
            self.cc_pnseXpwrite.set_comment("Cross PNSE and PWRITE")

        if hasattr(self.item, "time_since_wakeup"):
            # PWAKEUP
            self.cp_pwakeup = self.cg.add_coverpoint("pwakeup", lambda: self.item.time_since_wakeup)
            self.cp_pwakeup.set_comment("PWAKEUP (wakeup indication - time in ns since wakeup was raised)")
            self.cp_pwakeup.add_bin("ns", range(0, 1000), stats=True)

        if hasattr(self.item, "pauser"):
            # PAUSER
            self.cp_pauser = self.cg.add_coverpoint("pauser", lambda: self.item.pauser)
            self.cp_pauser.set_comment("PAUSER (user request sideband)")
            for i in range(self.item.pauser.width):
                self.cp_pauser.add_bin(f"[{i}] == 0", lambda x, y=i : 0 == (x & (1<<y)))
                self.cp_pauser.add_bin(f"[{i}] == 1", lambda x, y=i : 0 != (x & (1<<y)))

        if hasattr(self.item, "pwuser"):
            # PWUSER
            self.cp_pwuser = self.cg.add_coverpoint("pwuser", lambda: self.item.pwuser)
            self.cp_pwuser.set_comment("PWUSER (user write sideband)")
            for i in range(self.item.pwuser.width):
                self.cp_pwuser.add_bin(f"[{i}] == 0", lambda x, y=i : 0 == (x & (1<<y)))
                self.cp_pwuser.add_bin(f"[{i}] == 1", lambda x, y=i : 0 != (x & (1<<y)))

        if hasattr(self.item, "pruser"):
            # PRUSER
            self.cp_pruser = self.cg.add_coverpoint("pruser", lambda: self.item.pruser)
            self.cp_pruser.set_comment("PRUSER (user read sideband)")
            for i in range(self.item.pruser.width):
                self.cp_pruser.add_bin(f"[{i}] == 0", lambda x, y=i : 0 == (x & (1<<y)))
                self.cp_pruser.add_bin(f"[{i}] == 1", lambda x, y=i : 0 != (x & (1<<y)))

        if hasattr(self.item, "pbuser"):
            # PBUSER
            self.cp_pbuser = self.cg.add_coverpoint("pbuser", lambda: self.item.pbuser)
            self.cp_pbuser.set_comment("PBUSER (user response sideband)")
            for i in range(self.item.pbuser.width):
                self.cp_pbuser.add_bin(f"[{i}] == 0", lambda x, y=i : 0 == (x & (1<<y)))
                self.cp_pbuser.add_bin(f"[{i}] == 1", lambda x, y=i : 0 != (x & (1<<y)))

    async def run_phase(self) -> None:
        """
        Run phase for the coverage component.

        """

        while True:
            # Wait for an item to be available
            self.item = await self.item_port.blocking_get()

            # Sample
            self.cg.sample()

__all__ = ["Coverage"]
