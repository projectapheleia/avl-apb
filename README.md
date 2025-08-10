# AVL-APB - Apheleia Verification Library AMBA APB Verification Component

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)


AVL-APB has been developed by experienced, industry professional verification engineers to provide a simple, \
extensible verification component for the [AMBA APB Bus](https://developer.arm.com/documentation/ihi0024/latest/) \
developed in [Python](https://www.python.org/) and the [AVL](https://avl-core.readthedocs.io/en/latest/index.html) library.

AVL is built on the [CocoTB](https://docs.cocotb.org/en/stable/) framework, but aims to combine the best elements of \
[UVM](https://accellera.org/community/uvm) in a more engineer friendly and efficient way.


## Protocol Features

| Version | Signal Name | Description | Driven By |
|---------|-------------|-------------|-----------|
| APB2    | PCLK        | APB clock signal; all APB transfers are synchronized to this clock. | Requester |
| APB2    | PRESETn     | Asynchronous active-low reset for the APB interface. | Requester |
| APB2    | PADDR       | Address bus; specifies the register address for the transfer. | Requester |
| APB2    | PSELx       | Slave select; one per slave. High when the slave is selected. | Requester |
| APB2    | PENABLE     | Indicates the second and subsequent cycles of an APB transfer. | Requester |
| APB2    | PWRITE      | Write control signal; high for write, low for read. | Requester |
| APB2    | PWDATA      | Write data bus from master to slave. | Requester |
| APB2    | PRDATA      | Read data bus from slave to master. | Completer |
| APB3    | PREADY      | Optional signal; indicates the slave is ready to complete the transfer. | Completer |
| APB3    | PSLVERR     | Optional signal; indicates an error condition on the transfer. | Completer |
| APB4    | PPROT       | Optional protection control signals for privilege, security, and instruction/data access. | Requester |
| APB4    | PSTRB       | Optional byte lane strobe signals for write operations. | Requester |
| APB5    | PNSE        | Optional signal; indicates whether the transfer is secure or non-secure. | Requester |
| APB5    | PWAKEUP     | Optional wakeup signal from slave to master for low-power operation. | Completer |
| APB5    | PAUSER      | Optional signal; specifies the user ID associated with the transfer for secure systems. | Requester |
| APB5    | PRUSER      | Optional user-defined read data channel sideband signals. | Completer |
| APB5    | PWUSER      | Optional user-defined write data channel sideband signals. | Requester |
| APB5    | PBUSER      | Optional user-defined byte strobe channel sideband signals. | Requester |

## Component Features

- All protocol features supported
- Simple RTL interface to interact with HDL and define parameter and configuration options
- Requester sequence, sequencer and driver with easy to control rate limiter and wakeup control
- Completer driver with vanilla, random and memory response patterns
- Monitor
- Bandwidth monitor generating bus activity plots over user defined windows during simulation
- Functional coverage including performance measurements
- Searchable trace file generation

---

## 📦 Installation

### Using `pip`
```sh
# Standard build
pip install avl-core

# Development build
pip install avl-core[dev]
```

### Install from Source
```sh
git clone https://github.com/projectapheleia/avl.git
cd avl

# Standard build
pip install .

# Development build
pip install .[dev]
```

Alternatively if you want to create a [virtual environment](https://docs.python.org/3/library/venv.html) rather than install globally a script is provided. This will install, with edit privileges to local virtual environment.

This script assumes you have [Graphviz](https://graphviz.org/download/) and appropriate simulator installed, so all examples and documentation will build out of the box.


```sh
git clone https://github.com/projectapheleia/avl-apb.git
cd avl-apb
source avl-apb.sh
```

## 📖 Documentation

In order to build the documentation you must have installed the development build.

### Build from Source
```sh
cd docs
make html
<browser> build/html/index.html
```
## 🏃 Examples

In order to run all the examples you must have installed the development build.

To run all examples:

```sh
cd examples

# To run
make -j 8 sim

# To clean
make -j 8 clean
```

To run an individual example:

```sh
cd examples/THE EXAMPLE YOU WANT

# To run
make sim

# To clean
make clean
```

The examples use the [CocoTB Makefile](https://docs.cocotb.org/en/stable/building.html) and default to [Verilator](https://www.veripool.org/verilator/) with all waveforms generated. This can be modified using the standard CocoTB build system.

---


## 🧹 Code Style & Linting

This project uses [**Ruff**](https://docs.astral.sh/ruff/) for linting and formatting.

Check code for issues:

```sh
ruff check .
```

Automatically fix common issues:

```sh
ruff check . --fix
```



## 📧 Contact

- Email: avl@projectapheleia.net
- GitHub: [projectapheleia](https://github.com/projectapheleia)
