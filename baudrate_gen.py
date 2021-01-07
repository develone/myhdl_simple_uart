from myhdl import *

@block
def baudrate_gen(clk, rst, baud_rate, half_baud_rate_tick, baud_rate_tick):

    """ Serial
    This module implements a baudrate generator

    Ports:
    -----
    clk: clk input
    rst: rst input
    baud_rate: the baut rate to generate
    baud_rate_tick: the baud rate enable
    -----

    """
    baud_gen_count_reg = Signal(intbv(0, min = 0, max = 900))
    half_baud_const = baud_rate//2

    @always_seq(clk.posedge, reset = rst)
    def sequential_process():
        baud_gen_count_reg.next = baud_gen_count_reg + 1
        baud_rate_tick.next = 0
        half_baud_rate_tick.next = 0
        if baud_gen_count_reg == baud_rate:
            baud_gen_count_reg.next = 0
            baud_rate_tick.next = 1
        if baud_gen_count_reg == half_baud_const:
            half_baud_rate_tick.next = 1


    return sequential_process
