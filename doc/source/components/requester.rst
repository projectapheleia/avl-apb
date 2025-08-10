.. _requester:

AVL-APB Requester
=================


The requester side of the AVL-APB agent follow the standard AVL / UVM structure of sequence, sequencer and driver.

Request Sequence
-----------------

.. inheritance-diagram:: avl_apb._rsequence
    :parts: 1

A very simple sequence is provided that generates a stream of :any:`SequenceItem` items.

The length of the sequence is defined by the n_items variable, which defaults to 1, but is expected to be override by the factory.

In addition a list of ranges can be provided to define the address space for the sequence. If not provided, the sequence will randomize \
the address along with all other variables of the item.

As the item is parameterized, only the request side attributes present will be randomized.

The user is expected to extend the sequence for custom behavior.

Request driver
--------------

.. inheritance-diagram:: avl_apb._rdriver
    :parts: 2

The request driver implements the legal protocol for the bus via 3 user defined tasks:

- :any:`ReqDriver.reset` Action to be taken on bus reset. By default all request signals are set to 0.
- :any:`ReqDriver.quiesce` Action to be taken between transactions. By default all request signals are set to 0.
- :any:`ReqDriver.drive` Action of driving the transaction on the bus.


Rate Control
~~~~~~~~~~~~

The request driver is responsible for rate control. By setting the rate_limit variable in the :any:`ReqDriver` class, \
using a lambda function that returns a value between 0.0 and 1.0 the user can control the rate of driving the request signals. i.e. the inter-transaction gap.

.. code-block:: python

    avl.Factory.set_variable("*.agent.rdrv.rate_limit", lambda: 0.1)

Wakeup Control (ABP5)
~~~~~~~~~~~~~~~~~~~~~

In ABP5, the requester driver can control the wakeup signal. The pre_wakeup and post_wakeup variables are used to define the \
pre-wakeup and post-wakeup delays, respectively. These are defined as lambda functions that return a value between 0.0 and 1.0.

This feature ensures the wakeup signals are driven correctly according to the ABP5 protocol, while providing randomization of the assertion and \
de-assertion timing.

.. code-block:: python

    avl.Factory.set_variable("*.agent.rdrv.pre_wakeup", lambda: 0.1) # Early assertion of wakeup sign before driving the request
    avl.Factory.set_variable("*.agent.rdrv.post_wakeup", lambda: 0.9) # Quick de-assertion of wakeup signal after driving the request
