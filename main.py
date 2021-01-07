from math import *
from myhdl import *

from serial_tx import serial_tx
from serial_rx import serial_rx
from baudrate_gen import baudrate_gen

@block
def main(clk,rx,tx):

    clk_freq = 100000000
    baud_const = int(floor(clk_freq / 115200))
    #clk = Signal(bool(0))
    rst = ResetSignal(0, active=0, isasync=True)
    baudrate_tick = Signal(bool(0))
    half_baud_rate_tick = Signal(bool(0))     
    rx_data = Signal(intbv(0, min = 0, max = 256))
    #tx = Signal(bool(0))
    n_stop_bits = 1
    rx_rdy = Signal(False)
    start = Signal(False)
    tx_data = Signal(intbv(0, min = 0, max = 256))
    #tx = Signal(bool(0))

    baud_gen_inst = baudrate_gen(clk, rst, baud_const, half_baud_rate_tick, \
        baudrate_tick)
    serial_tx_inst   = serial_tx(clk, rst, start, tx_data, n_stop_bits, \
        baudrate_tick, tx)
    serial_rx_inst   = serial_rx(clk, rst, n_stop_bits, half_baud_rate_tick, \
        baudrate_tick, tx, rx_data, rx_rdy)
	
    @always_comb
    def outputs():
    	tx_data.next = rx_data
    
    return instances()

def convert_main(hdl):
	
    main_0 = main(clk,rx,tx)
    main_0.convert(hdl=hdl)

clk=Signal(bool(0))
rx=Signal(bool(1))
tx=Signal(bool(0))
convert_main(hdl='Verilog')
