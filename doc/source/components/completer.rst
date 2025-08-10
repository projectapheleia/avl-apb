.. _completer:

AVL-APB Completer
=================

.. inheritance-diagram:: avl_apb._cdriver
    :parts: 2

The completer side of the AVL-APB agent does not follow the standard AVL / UVM structure of sequence, sequencer and driver.

As the completer is inheritably responsive the complication of interacting between a monitor, sequence and driver is overly complicated \
and not required.

Instead the completer is implemented as a single driver that implements the legal protocol for the bus via 3 user defined tasks:

- :any:`CplDriver.reset` Action to be taken on bus reset. By default all completion signals are set to 0.
- :any:`Driver.quiesce` Action to be taken between transactions. By default all completion signals are set to 0.
- :any:`CplDriver.drive` Action of driving.

A single function is used to decide how to complete the request:

- :any:`CplDriver.get_next_item`

This function is called with the an argument of the item to be completed, the request side of the protocol has already \
populated the item in order to make a decision.

Each :any:`CplDriver` must be configured with and index :any:`CplDriver.idx` that corresponds to the psel signal of the AMBA interface.
This index is assiged atomatically by the :any:`avl_apb._cdriver.CplDriver` class based on the number of completers in the agent.

3 drivers are provided:

- :any:`CplDriver` - The default driver that completes the request by driving the response signals.
- :any:`CplRandomDriver` - Fully randomize the completion based on the :any:`SequenceItem` attributes.
- :any:`CplMemoryDriver` - Completes the request behaving as a memory device.

Rate Control
~~~~~~~~~~~~

The request driver is responsible for rate control. By setting the rate_limit variable in the :any:`CplDriver` class, \
using a lambda function that returns a value between 0.0 and 1.0 the user can control the rate of driving the pready signal, if supported.

.. code-block:: python

    avl.Factory.set_variable("*.agent.cdrv.rate_limit", lambda: 0.1)

Memory Completion Driver
------------------------

The memory completion driver must be configured to support one or more address ranges. \
This is done by setting the ranges variable to a list of address ranges. \
The ranges are defined as tuples of (start, end) addresses.

.. code-block:: python

    avl.Factory.set_variable("*.agent.cdrv.ranges", [(0x0000, 0xFFFF), (0x1000, 0x1FFF)])

If the requests is accessing a region supported by the memory driver:

- Writes will update the memory. Strobes are taken into account, if supported.
- Reads will return the value stored in the memory.

If the request is accessing a region not supported by the memory driver, the driver will:

- Ignore writes.
- Randomize completion read data.
- Return pslverr if supported.

The is easy to override in the :any:`CplMemoryDriver.get_next_item` method.

Example
~~~~~~~

.. literalinclude:: ../../../examples/apb/apb4/cocotb/example.py
    :language: python
