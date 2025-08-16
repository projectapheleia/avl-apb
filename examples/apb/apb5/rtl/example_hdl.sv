module example_hdl();


    logic clk, rst_n;

    apb_if#(.VERSION(5),
            .ADDR_WIDTH(12),
            .DATA_WIDTH(32),
            .Protection_Support(1),
            .Pstrb_Support(1),
            .RME_Support(1),
            .Wakeup_Signal(1),
            .USER_REQ_WIDTH(4),
            .USER_DATA_WIDTH(8),
            .USER_RESP_WIDTH(2))  apb_if();

    assign apb_if.pclk = clk;
    assign apb_if.presetn = rst_n;

endmodule : example_hdl
