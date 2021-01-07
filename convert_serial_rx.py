from math import *

from myhdl import Signal, ResetSignal, intbv

from serial_rx import serial_rx

def convert_serial_rx(hdl):
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

    serial_rx_inst   = serial_rx(clk, rst, n_stop_bits, half_baud_rate_tick, \
        baudrate_tick, tx, rx_data, rx_rdy)

    serial_rx_inst.convert(hdl=hdl)


convert_serial_rx(hdl='Verilog')
convert_serial_rx(hdl='VHDL')
