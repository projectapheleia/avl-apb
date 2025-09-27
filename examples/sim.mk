#Copyright 2024 Apheleia
#
#Description:
# Apheleia Verification Library (AVL) Example

# Makefile

# HDL source files
VERILOG_SOURCES      += $(shell avl-apb-get-verilog) $(PWD)/rtl/example_hdl.sv
VERILOG_INCLUDE_DIRS +=
COMPILE_ARGS         +=

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL             := example_hdl
PYTHONPATH           := $(PWD)/cocotb

# COCOTB_TEST_MODULES is the basename of the Python test file(s)
COCOTB_TEST_MODULES  ?= example

# Questa / ModelSim workaround
VSIM_ARGS            += -lib work

# Enable VCD trace from Verilator
ifeq ($(SIM), verilator)
EXTRA_ARGS           += --trace --trace-structs --timing
endif

# Default seed
COCOTB_RANDOM_SEED	   		 ?= 1
export COCOTB_RANDOM_SEED

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim

clean::
	rm -rf cocotb/__pycache__/
	rm -rf *.txt *.xml *.json *.csv *.yaml *.vcd *.png sim.log html transcript modelsim.ini ucli.key
