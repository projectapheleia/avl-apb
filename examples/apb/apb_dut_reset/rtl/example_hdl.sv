module example_hdl ();

  timeunit 1ns;
  timeprecision 1ps;

  logic clk;
  logic rst_n;

  apb_if #(.ADDR_WIDTH(12), .DATA_WIDTH(32), .VERSION(3)) u_apb ();

  assign u_apb.pclk    = clk;
  assign u_apb.presetn = rst_n;

  // Icarus only creates VPI handles for interface members referenced by RTL.
  // These signals are driven solely from Python, so without a reference here
  // the VIP cannot bind to them (example_hdl.u_apb contains no child object named paddr).
  initial begin : keep_vpi
    logic unused;
    unused = ^{u_apb.paddr, u_apb.psel, u_apb.penable, u_apb.pwrite,
               u_apb.pwdata, u_apb.pready, u_apb.prdata, u_apb.pslverr};
  end

  initial begin
    clk = 1'b0;
    forever #5 clk = ~clk;
  end

  initial begin
    rst_n = 1'b0;     // X -> 0 in time step 0: the monitor's FallingEdge(presetn) fires here
    #100;
    rst_n = 1'b1;
  end

endmodule : example_hdl
