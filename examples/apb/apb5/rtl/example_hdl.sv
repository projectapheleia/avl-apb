module example_hdl();


    logic clk, rst_n;

    apb_if#(.ADDR_WIDTH(12),
            .DATA_WIDTH(32),
            .VERSION(5),
            .PROTECTION(1),
            .RME(1),
            .WAKEUP(1),
            .USER_REQ_WIDTH(4),
            .USER_DATA_WIDTH(8),
            .USER_RESP_WIDTH(2))  apb_if();

    assign apb_if.pclk = clk;
    assign apb_if.presetn = rst_n;

endmodule : example_hdl
