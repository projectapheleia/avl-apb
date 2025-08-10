// Copyright 2025 Apheleia
//
// Description:
// Apheleia Verification Library APB Interface

interface apb_if #(parameter string CLASSIFICATION  = "APB",
                   parameter int    VERSION         = 2,
                   parameter int    PSEL_WIDTH      = 1,
                   parameter int    ADDR_WIDTH      = 32,
                   parameter int    DATA_WIDTH      = 32,
                   parameter int    PROTECTION      = 0,
                   parameter int    RME             = 0,
                   parameter int    WAKEUP          = 0,
                   parameter int    USER_REQ_WIDTH  = 0,
                   parameter int    USER_DATA_WIDTH = 0,
                   parameter int    USER_RESP_WIDTH = 0)();

    logic                  pclk;
    logic                  presetn;

    logic [ADDR_WIDTH-1:0] paddr;
    logic [PSEL_WIDTH-1:0] psel;
    logic                  penable;

    logic                  pwrite;
    logic [DATA_WIDTH-1:0] pwdata;
    logic [DATA_WIDTH-1:0] prdata;

    generate
        if (VERSION >= 3) begin : apb3
            logic pready;
            logic pslverr;
        end

        if (VERSION >= 4) begin : apb4
            logic [(DATA_WIDTH/8)-1:0] pstrb;
            logic [2:0]                pprot;

            if (PROTECTION == 0) begin
                always @(pprot) if ($time != 0) $fatal("Protection not supported");
            end
        end

        if (VERSION >= 5) begin : apb5
            logic pnse;
            logic pwakeup;
            logic [USER_REQ_WIDTH  > 0 ? USER_REQ_WIDTH-1  : 0 : 0] pauser;
            logic [USER_DATA_WIDTH > 0 ? USER_DATA_WIDTH-1 : 0 : 0] pwuser;
            logic [USER_DATA_WIDTH > 0 ? USER_DATA_WIDTH-1 : 0 : 0] pruser;
            logic [USER_RESP_WIDTH > 0 ? USER_RESP_WIDTH-1 : 0 : 0] pbuser;

            if ((PROTECTION == 0) || (RME == 0)) begin
                always @(pnse) if ($time != 0) $fatal("RME not supported");
            end

            if (WAKEUP == 0) begin
                always @(pwakeup) if ($time != 0) $fatal("Wakeup not supported");
            end

            if (USER_REQ_WIDTH == 0) begin : user_req
                always @(pauser) if ($time != 0) $fatal("User request not supported");
            end

            if (USER_DATA_WIDTH == 0) begin : user_data
                always @(pwuser) if ($time != 0) $fatal("User data not supported");
                always @(pruser) if ($time != 0) $fatal("User data not supported");
            end

            if (USER_RESP_WIDTH == 0) begin : user_resp
                always @(pbuser) if ($time != 0) $fatal("User resp not supported");
            end
        end

    endgenerate

endinterface : apb_if
