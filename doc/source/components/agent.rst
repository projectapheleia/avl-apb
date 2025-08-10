.. _agent:

AVL-APB Agent
=============

.. inheritance-diagram:: avl_apb._agent_cfg
    :parts: 1

.. inheritance-diagram:: avl_apb._agent
    :parts: 1

Unlike many VIPs AVL-APB does not contain an environment.

The AVL-APB verification components is designed to be integrated easily into existing AVL environments, and \
as such an agent can be individually configured without a wider global environment.

The agent is composed of a requester and responder side, which can be used independently or together, and \
and number of non-directional passive components. To configure the agents, the user must override the :doc:`avl_apb.AgentCfg </modules/avl_apb._agent_cfg>` class. \
The best way to do this is via the facory:

.. code-block:: python

    avl.Factory.set_variable("*.agent.cfg.has_requester", True)
    avl.Factory.set_variable("*.agent.cfg.num_completer", 1)
    avl.Factory.set_variable("*.agent.cfg.has_monitor", True)

.. note::

    The :doc:`avl_apb.AgentCfg </modules/avl_apb._agent_cfg>` does not configure the APB bus itself, only the agent. \
    The bus configuration is done via RTL interface (see :ref:`configuration` for more details.)

Sub-Components
--------------

.. toctree::
   :maxdepth: 1

   requester
   completer
   monitor
   bandwidth
   coverage
   trace

