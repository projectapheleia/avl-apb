.. _configuration:

AVL-APB Configuration
=====================

AVL-APB is configured via the provided RTL interface.

The default interface does not contain any modports or clocking blocs to remain compatible with \
the majority of simulators.

If the user wishes to add directionality or timing to the interface, they can do so by \
modifying the avl_apb.sv file.

Connection the interface to the APB bus should be done with standard assign statements.

All signals are included, however, optional signals are disabled by default. \
To enable optional signals, the user must set the appropriate parameters in the interface. \
Where defined the same configuration naming conventions used in the AMBA specification have been followed.

Assertion checks for optional signals that are not included ensure they remain unchanged during simulation and therefore can \
be ignored the the user.

These assertion checks are deliberately implemented as initial blocks with $fatals in order to be supported on \
the widest range of simulators.


.. literalinclude:: ../../../avl_apb/rtl/avl_apb.sv
    :language: verilog


Integrating with a Build Environment
------------------------------------

AVL-APB comes with a tools utility :func:`avl_apb._tools.get_verilog` to help integrate the library into your build environment.

This is exposed to the environment as the command line tool `avl_apb_get_verilog` which returns a list of all RTL files required \
for AVL_APB.

An example of integrating with the verilator build environment is shown below:

.. code-block:: makefile

    # HDL source files
    VERILOG_SOURCES      += $(shell avl-apb-get-verilog)

    # include cocotb's make rules to take care of the simulator setup
    include $(shell cocotb-config --makefiles)/Makefile.sim


Connecting to the AVL Environment
---------------------------------

The recommended way to connect to the AVL environment is via the factory.

.. code-block:: python

    avl.Factory.set_variable("*.hdl", dut.apb_if)

When the agent is created it will automatically use this factory setting to connect to the APB interface.

Parameterization
----------------

The AVL environment automatically picks up the parameters (version, features and width) from the RTL interface. \
This ensures the AVL environment and HDL environment are always in sync.

Once connected the agent creates and internal :doc:`avl_apb.Interface </modules/avl_apb._interface>` object which is used to \
act as the physical interface to the APB bus and share the parameters with the rest of the environment.

This internal interface in generated to serve 2 purposes:

    1. It abstracts the simulator specific behaviour of the generate blocks. Some simulators flatten the generate blocks, while others do not.
    2. It provides :any:`Interface.get` and :any:`Interface.set` methods to access the HDL with knowledge of which signals are present based on the configuration of the bus.
