module example_hdl();


    logic clk, rst_n;

    apb_if#(.VERSION(4),
            .ADDR_WIDTH(32),
            .DATA_WIDTH(32),
            .Protection_Support(1),
            .Pstrb_Support(1))  apb_if();

    assign apb_if.pclk = clk;
    assign apb_if.presetn = rst_n;

endmodule : example_hdl
