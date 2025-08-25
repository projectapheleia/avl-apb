.. _monitor:

AVL-APB Monitor
===============

.. inheritance-diagram:: avl_apb._monitor
    :parts: 2


The :any:`Monitor <avl_apb._monitor.Monitor>` module is a passive component that observes the bus transactions and provides a way to collect and analyze the data.

It's behavior is as you would expect for any AVL or UVM monitor. It observes the bus signals and generates transactions based on the observed activity, \
passing it to the item_export for further processing.

.. code-block:: python

    avl.Factory.set_variable("*.agent_cfg.has_monitor", True)

Wait Cycles
-----------

In addition to constructing the :any:`SequenceItem` from the observed bus activity, the monitor also calculates the wait cycles.

Wait cycles are defined as the number of clock cycles between the request (penable) and the response (pready) signals and can be used \
for coverage or latency analysis.

In APB2 where the pready signal is not present wait cycles will be excluded.
