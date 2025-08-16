// Copyright 2025 Apheleia
//
// Description:
// Apheleia Verification Library APB Interface
// As defined in https://developer.arm.com/documentation/ihi0024/latest/

`define AVL_APB_IMPL_CHECK(cond, signal) \
if (``cond`` == 1) begin : ``signal``_cond \
    initial begin \
        #0.1; \
        @(``signal``) $fatal("%m: ``signal`` not supported in configuration");\
    end \
end : ``signal``_cond

interface apb_if #(parameter string CLASSIFICATION      = "APB",
                   parameter int    VERSION             = 2,
                   parameter int    PSEL_WIDTH          = 1,
                   parameter int    ADDR_WIDTH          = 32,
                   parameter int    DATA_WIDTH          = 32,
                   parameter bit    Protection_Support  = 0,
                   parameter bit    RME_Support         = 0,
                   parameter bit    Pstrb_Support       = 0,
                   parameter bit    Wakeup_Signal       = 0,
                   parameter int    USER_REQ_WIDTH      = 0,
                   parameter int    USER_DATA_WIDTH     = 0,
                   parameter int    USER_RESP_WIDTH     = 0)();

    localparam PSTRB_WIDTH = int'(DATA_WIDTH/8);

    logic                                                   pclk;
    logic                                                   presetn;
    logic [ADDR_WIDTH-1:0]                                  paddr;
    logic [2:0]                                             pprot;
    logic                                                   pnse;
    logic [PSEL_WIDTH-1:0]                                  psel;
    logic                                                   penable;
    logic                                                   pwrite;
    logic [DATA_WIDTH-1:0]                                  pwdata;
    logic [PSTRB_WIDTH-1:0]                                 pstrb;
    logic                                                   pready;
    logic [DATA_WIDTH-1:0]                                  prdata;
    logic                                                   pslverr;
    logic                                                   pwakeup;
    logic [USER_REQ_WIDTH  > 0 ? USER_REQ_WIDTH-1  : 0 : 0] pauser;
    logic [USER_DATA_WIDTH > 0 ? USER_DATA_WIDTH-1 : 0 : 0] pwuser;
    logic [USER_DATA_WIDTH > 0 ? USER_DATA_WIDTH-1 : 0 : 0] pruser;
    logic [USER_RESP_WIDTH > 0 ? USER_RESP_WIDTH-1 : 0 : 0] pbuser;

    generate

        `AVL_APB_IMPL_CHECK((VERSION < 3), pready)

        `AVL_APB_IMPL_CHECK((VERSION < 3), pslverr)

        `AVL_APB_IMPL_CHECK(((VERSION < 4) || (Protection_Support == 0)), pprot)

        `AVL_APB_IMPL_CHECK(((VERSION < 4) || (Pstrb_Support == 0)), pstrb)

        `AVL_APB_IMPL_CHECK(((VERSION < 5) || (RME_Support == 0)), pnse)

        `AVL_APB_IMPL_CHECK(((VERSION < 5) || (Wakeup_Signal == 0)), pwakeup)

        `AVL_APB_IMPL_CHECK(((VERSION < 5) || (USER_REQ_WIDTH == 0)), pauser)

        `AVL_APB_IMPL_CHECK(((VERSION < 5) || (USER_DATA_WIDTH == 0)), pwuser)

        `AVL_APB_IMPL_CHECK(((VERSION < 5) || (USER_DATA_WIDTH == 0)), pruser)

        `AVL_APB_IMPL_CHECK(((VERSION < 5) || (USER_RESP_WIDTH == 0)), pbuser)

    endgenerate

endinterface : apb_if

`undef AVL_APB_IMPL_CHECK
