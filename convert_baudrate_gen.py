from math import *

from myhdl import Signal, ResetSignal, intbv

from baudrate_gen import baudrate_gen

def convert_baudrate_gen(hdl):
    """Convert baudrate_gen block to Verilog or VHDL."""
    clk_freq = 100000000
    baud_const = int(floor(clk_freq / 115200))
    clk = Signal(bool(0))
    rst = ResetSignal(0, active=0, isasync=True)
    baudrate_tick = Signal(bool(0))
    half_baud_rate_tick = Signal(bool(0))     
    rx_data = Signal(intbv(0, min = 0, max = 256))
    tx = Signal(bool(0))
    n_stop_bits = 1
    rx_rdy = Signal(False)
    start = Signal(False)
    tx_data = Signal(intbv(0, min = 0, max = 256))
    tx = Signal(bool(0))
        



    baudrate_gen_1 = baudrate_gen(clk, rst, baud_const, half_baud_rate_tick, baudrate_tick)

    baudrate_gen_1.convert(hdl=hdl)


convert_baudrate_gen(hdl='Verilog')
convert_baudrate_gen(hdl='VHDL')
