from math import *

from myhdl import Signal, ResetSignal, intbv

from serial_tx import serial_tx

def convert_serial_tx(hdl):
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

    serial_tx_inst   = serial_tx(clk, rst, start, tx_data, n_stop_bits, \
        baudrate_tick, tx)

    serial_tx_inst.convert(hdl=hdl)


convert_serial_tx(hdl='Verilog')
convert_serial_tx(hdl='VHDL')
