from math import *
from myhdl import *

from serial_tx import serial_tx
from serial_rx import serial_rx
from baudrate_gen import baudrate_gen

new_header = """\
-----------------------------------------------------------------------------
-- Title :
-- Project :
-----------------------------------------------------------------------------
-- File : $filename
-- Author :
-- Company :
-- Created : $date
-- Last update : $date
-- Target Device : Cyclone V
-- Standard : VHDL'93
------------------------------------------------------------------------------
-- Description :
------------------------------------------------------------------------------
-- Generated with MyHDL Version $version
------------------------------------------------------------------------------
-- Copyright : (c) 2014
------------------------------------------------------------------------------
-- Revisions :
-- Date     Version     Author    Description
------------------------------------------------------------------------------

-- Libraries and use clauses
"""

@block
def bench():

    CLK_PERIOD = 10
    clk_freq = 100000000
    baud_const = int(floor(clk_freq / 115200))
    clk = Signal(bool(0))
    rst = ResetSignal(0, active=0, isasync=True)
    start = Signal(False)
    rx_rdy = Signal(False)
    tx_data = Signal(intbv(0, min = 0, max = 256))
    rx_data = Signal(intbv(0, min = 0, max = 256))
    n_stop_bits = 1
    baudrate_tick = Signal(bool(0))
    half_baudrate_tick = Signal(bool(0))
    tx = Signal(bool(0))
    rx = Signal(bool(0))


    # design under test

    baud_gen_inst = baudrate_gen(clk, rst, baud_const, half_baudrate_tick, \
        baudrate_tick)
    serial_tx_inst   = serial_tx(clk, rst, start, tx_data, n_stop_bits, \
        baudrate_tick, tx)
    serial_rx_inst   = serial_rx(clk, rst, n_stop_bits, half_baudrate_tick, \
        baudrate_tick, tx, rx_data, rx_rdy)


    # clock generator
    @always(delay(CLK_PERIOD/2))
    def clockgen():
        clk.next = not clk

    @instance
    def stimulus():
        tx_data.next = 65
        rst.next = 0
        for i in range(1):
            yield clk.negedge
        rst.next = 1
        for i in range(10):
            yield clk.negedge
        start.next = 1
        yield clk.negedge
        start.next = 0
        yield rx_rdy
        assert (rx_data == tx_data)
        raise StopSimulation

    #return baud_gen_inst, serial_tx_inst, serial_rx_inst, clockgen, stimulus
    return instances()

tb = bench()
tb.config_sim(trace=True)
tb.run_sim()
