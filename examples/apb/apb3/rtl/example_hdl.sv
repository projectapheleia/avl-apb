module example_hdl();


    logic clk, rst_n;

    apb_if#(.ADDR_WIDTH(12),.DATA_WIDTH(16),.VERSION(3))  apb_if();

    assign apb_if.pclk = clk;
    assign apb_if.presetn = rst_n;

endmodule : example_hdl
