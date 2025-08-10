.. _protocol:

Protocol Support
================

AVL-APB support APB2, APB3, APB4 and APB5 protocols including all optional signals.

For full details see `APB Documentation <https://developer.arm.com/documentation/ihi0024/latest/>`_.

.. list-table:: APB Signal List
   :header-rows: 1
   :widths: 8 20 55 17

   * - Version
     - Signal Name
     - Description
     - Driven By
   * - APB2
     - PCLK
     - APB clock signal; all APB transfers are synchronized to this clock.
     - Requester
   * - APB2
     - PRESETn
     - Asynchronous active-low reset for the APB interface.
     - Requester
   * - APB2
     - PADDR
     - Address bus; specifies the register address for the transfer.
     - Requester
   * - APB2
     - PSELx
     - Slave select; one per slave. High when the slave is selected.
     - Requester
   * - APB2
     - PENABLE
     - Indicates the second and subsequent cycles of an APB transfer.
     - Requester
   * - APB2
     - PWRITE
     - Write control signal; high for write, low for read.
     - Requester
   * - APB2
     - PWDATA
     - Write data bus from master to slave.
     - Requester
   * - APB2
     - PRDATA
     - Read data bus from slave to master.
     - Completer
   * - APB3
     - PREADY
     - Optional signal; indicates the slave is ready to complete the transfer.
     - Completer
   * - APB3
     - PSLVERR
     - Optional signal; indicates an error condition on the transfer.
     - Completer
   * - APB4
     - PPROT
     - Optional protection control signals for privilege, security, and instruction/data access.
     - Requester
   * - APB4
     - PSTRB
     - Optional byte lane strobe signals for write operations.
     - Requester
   * - APB5
     - PNSE
     - Optional signal; indicates whether the transfer is secure or non-secure.
     - Requester
   * - APB5
     - PWAKEUP
     - Optional wakeup signal from slave to master for low-power operation.
     - Completer
   * - APB5
     - PAUSER
     - Optional signal; specifies the user ID associated with the transfer for secure systems.
     - Requester
   * - APB5
     - PRUSER
     - Optional user-defined read data channel sideband signals.
     - Completer
   * - APB5
     - PWUSER
     - Optional user-defined write data channel sideband signals.
     - Requester
   * - APB5
     - PBUSER
     - Optional user-defined byte strobe channel sideband signals.
     - Requester
