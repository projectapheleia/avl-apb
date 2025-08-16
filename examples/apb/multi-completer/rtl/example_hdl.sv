module example_hdl();


    logic clk, rst_n;

    apb_if#(.VERSION(3),
            .PSEL_WIDTH(3),
            .ADDR_WIDTH(12),
            .DATA_WIDTH(16))  apb_if();

    assign apb_if.pclk = clk;
    assign apb_if.presetn = rst_n;

endmodule : example_hdl
