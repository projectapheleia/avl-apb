# Copyright 2025 Apheleia
#
# Description:
# Apheleia Verification Library Requester Sequence

import random

import avl
from z3 import And

from ._item import SequenceItem


class ReqSequence(avl.Sequence):

    def __init__(self, name: str, parent: avl.Component) -> None:
        """
        Initialize the sequence item

        :param name: Name of the sequence item
        :param parent: Parent component of the sequence item
        """
        super().__init__(name, parent)

        self.i_f = avl.Factory.get_variable(f"{self.get_full_name()}.i_f", None)
        """Handle to interface - defines capabilities and parameters"""

        self.n_items = avl.Factory.get_variable(f"{self.get_full_name()}.n_items", 1)
        """Number of items in the sequence (default 1)"""

        self.ranges = avl.Factory.get_variable(f"{self.get_full_name()}.ranges", None)
        """List of ranges for the address space (optional, default None)"""

    async def body(self) -> None:
        """
        Body of the sequence
        """

        self.info(f"Starting sequence {self.get_full_name()} with {self.n_items} items")
        for _ in range(self.n_items):
            item = SequenceItem(f"from_{self.name}", self)
            await self.start_item(item)
            if self.ranges is not None:
                (psel, lo, hi) = random.choices(list(self.ranges.keys()), weights=list(self.ranges.values()), k=1)[0]

                item.add_constraint("_c_psel_", lambda x,y=psel: x == int(1 << y), item.psel)
                item.add_constraint("_c_paddr_", lambda x,y=lo,z=(hi-self.i_f.PSTRB_WIDTH): And(x >= y, x <= z), item.paddr)

            item.randomize_request()
            await self.finish_item(item)

__all__ = ["ReqSequence"]
