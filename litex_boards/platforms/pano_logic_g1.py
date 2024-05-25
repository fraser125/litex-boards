#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2019 Tom Keddie <git@bronwenandtom.com>
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# Copyright (c) 2020 Florent Kermarrec <florent@enjoy-digital.fr>
# Copyright (c) 2024 Fraser.MIPS <fraser dot MIPS at gmail dot com>
# SPDX-License-Identifier: BSD-2-Clause

# The Pano Logic Zero Client G1 is a thin commercial client from Pano Logic that can be repurposed
# as a generic development board thanks to reverse engineering efforts than can be found at:
# https://github.com/tomverbeure/panologic

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform
from litex.build.openocd import OpenOCD

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("clk100",    0, Pins("U10"),  IOStandard("LVCMOS33")),
    ("rst_n",     0, Pins("K3"), IOStandard("LVCMOS33")),

    # Leds
    ("user_led", 0, Pins("H1"),  IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("L1"),  IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("L3"),  IOStandard("LVCMOS33")),

    # Buttons
    ("user_btn_n", 0, Pins("R7"), IOStandard("LVCMOS33")),

    # Serial - Not available
    #("serial", 0, # hdmi
    #    Subsignal("tx", Pins("AB19")),
    #    Subsignal("rx", Pins("AA21")),
    #    IOStandard("LVCMOS33")
    #),

    # Serial - Not available
    #("serial", 1, # dvi
    #    Subsignal("tx", Pins("C14")),
    #    Subsignal("rx", Pins("C17")),
    #    IOStandard("LVCMOS33")
    #),

    # SPIFlash
    ("spiflash", 0,
        Subsignal("cs_n", Pins("U3"),   IOStandard("LVCMOS33")),
        Subsignal("clk",  Pins("U16"),  IOStandard("LVCMOS33")),
        Subsignal("mosi", Pins("T4"), IOStandard("LVCMOS33")), # Could be swapped
        Subsignal("miso", Pins("N10"), IOStandard("LVCMOS33")) # Could be swapped
    ),

    # DDR2 SDRAM
    ("ddram_clock_a", 0,
        Subsignal("p", Pins("J17")),
        Subsignal("n", Pins("J16")),
        IOStandard("LVCMOS18"), Misc("IN_TERM=NONE")
    ),
    ("ddram_a", 0,
        Subsignal("a", 
                  Pins(
            "F11 D13 E13 E11 B16 A16 A12 A11 D14 A14 B14 A13"),
            IOStandard("LVCMOS18")),
        Subsignal("ba",    Pins("F12 E12"), IOStandard("LVCMOS18")),
        Subsignal("ras_n", Pins("H14"), IOStandard("LVCMOS18")),
        Subsignal("cas_n", Pins("M14"), IOStandard("LVCMOS18")),
        Subsignal("we_n",  Pins("P16"), IOStandard("LVCMOS18")),
        Subsignal("dm",    Pins("K12 K13 J14 H15"), IOStandard("LVCMOS18")),
        Subsignal("dq",    Pins(
            "T17 U18 T18 R18 N14 N15 P18 P17",
            "M16 M15 M18 N18 L15 L16 K14 K15",
            "J13 J12 H17 H16 G16 G15 G13 G14",
            "F17 F18 F14 F15 D16 D17 C17 C18"),
            IOStandard("LVCMOS18")),
        Subsignal("dqs",   Pins("R15 L18 J15 E16"), IOStandard("LVCMOS18")),
        #Subsignal("dqs_n", Pins("T22 L22"), IOStandard("LVCMOS18")),
        Subsignal("cke", Pins("E15"), IOStandard("LVCMOS18")),
        #Subsignal("odt", Pins("G22"), IOStandard("LVCMOS18")),
    ),    

    # GMII Ethernet
    ("eth_rst_n",  0, Pins("K3"), IOStandard("LVCMOS33")),
    ("eth_clocks", 0,
        Subsignal("tx",  Pins("K5")),
        Subsignal("gtx", Pins("AA12")),
        Subsignal("rx",  Pins("K4")),
        IOStandard("LVCMOS33")
    ),
    ("eth", 0,
        Subsignal("rst_n",   Pins("K3")),
        Subsignal("int_n",   Pins("T1")),
        Subsignal("mdio",    Pins("M5")),
        Subsignal("mdc",     Pins("T2")),
        Subsignal("rx_dv",   Pins("R1")),
        Subsignal("rx_er",   Pins("U1")),
        Subsignal("rx_data", Pins("N2 N1 M1 K7")),
        Subsignal("tx_en",   Pins("R3")),
        Subsignal("tx_er",   Pins("R2")),
        Subsignal("tx_data", Pins("P4 P1 P2 P3")),
        Subsignal("col",     Pins("N5")),
        Subsignal("crs",     Pins("N4")),
        IOStandard("LVCMOS33")
    ),
]

# Platform -----------------------------------------------------------------------------------------

class Platform(XilinxSpartan6Platform):
    default_clk_name   = "clk100"
    default_clk_period = 1e9/125e6

    def __init__(self, revision="c", toolchain="ise"):
        assert revision in ["b", "c"]
        device = {"b": "xc6slx150-2-fgg484", "c": "xc6slx100-2-fgg484"}[revision]
        XilinxSpartan6Platform.__init__(self, device, _io, toolchain=toolchain)
        self.add_platform_command("""CONFIG VCCAUX="2.5";""")
        self.add_period_constraint(self.lookup_request("clk100", loose=True), 1e9/125e6)

    def create_programmer(self):
        return OpenOCD("openocd_xc6_ft232.cfg")
