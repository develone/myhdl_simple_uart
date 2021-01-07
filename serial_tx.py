from myhdl import *

t_State = enum('ST_WAIT_START', 'ST_SEND_START_BIT', 'ST_SEND_DATA' , 'ST_SEND_STOP_BIT' )

@block
def serial_tx(clk, rst, start, data, n_stop_bits, baud_rate_tick, tx):

    """ Serial
    This module implements a transmitter serial interface

    Ports:
    -----
    clk: clk input
    rst: rst input
    baud_rate_tick: the baud rate
    start: start sending data
    data: the data to send
    n_stop_bits: number of stop bits
    tx: data output
    -----

    """
    END_OF_BYTE = 7

    state_reg = Signal(t_State.ST_WAIT_START)
    state = Signal(t_State.ST_WAIT_START)

    transmit_reg = Signal(bool(0))
    transmit = Signal(bool(0))

    count_8_bits_reg = Signal(intbv(0, min = 0, max = 8))
    count_8_bits = Signal(intbv(0, min = 0, max = 8))

    count_stop_bits_reg = Signal(intbv(0, min = 0, max = 8))
    count_stop_bits = Signal(intbv(0, min = 0, max = 8))

    @always_comb
    def outputs():
        tx.next = transmit_reg

    @always_seq(clk.posedge, reset = rst)
    def sequential_process():
        state_reg.next   = state
        transmit_reg.next  = transmit
        count_8_bits_reg.next = count_8_bits
        count_stop_bits_reg.next = count_stop_bits

    @always_comb
    def combinational_process():
        state.next  = state_reg
        transmit.next = transmit_reg
        count_8_bits.next = count_8_bits_reg
        count_stop_bits.next = count_stop_bits_reg

        if state_reg == t_State.ST_WAIT_START:
            transmit.next = True
            if start == True:
                state.next = t_State.ST_SEND_START_BIT

        elif state_reg == t_State.ST_SEND_START_BIT:
            transmit.next = False
            if baud_rate_tick == True:
                state.next = t_State.ST_SEND_DATA

        elif state_reg == t_State.ST_SEND_DATA:
            transmit.next = data[count_8_bits_reg]
            if baud_rate_tick == True:
                if count_8_bits_reg == END_OF_BYTE:
                    count_8_bits.next = 0
                    state.next = t_State.ST_SEND_STOP_BIT
                else:
                    count_8_bits.next = count_8_bits_reg + 1
                    state.next = t_State.ST_SEND_DATA


        elif state_reg == t_State.ST_SEND_STOP_BIT:
            transmit.next = True
            if baud_rate_tick == True:
                if count_stop_bits_reg == (n_stop_bits - 1):
                    count_stop_bits.next = 0
                    state.next = t_State.ST_WAIT_START
                else:
                    count_stop_bits.next = count_stop_bits_reg + 1
        else:
            raise ValueError("Undefined State")



    return outputs, sequential_process, combinational_process
