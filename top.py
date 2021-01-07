from myhdl import *
import main

"""
yosys -l simple.log -p 'synth_ice40 -blif top.blif -json top.json' top.v
=== top ===

   Number of wires:                 43
   Number of wire bits:            157
   Number of public wires:          43
   Number of public wire bits:     157
   Number of memories:               0
   Number of memory bits:            0
   Number of processes:              0
   Number of cells:                 63
     SB_CARRY                       10
     SB_DFF                          2
     SB_DFFE                        18
     SB_DFFSS                        1
     SB_LUT4                        32


"""
 

@block
def top(clk,rx,tx):
	main_inst = main.main(clk,rx,tx)
	return instances()

def convert_top(hdl):
	
	top_0 = top(clk,rx,tx)
	top_0.convert(hdl=hdl)

clk=Signal(bool(0))
rx=Signal(bool(1))
tx=Signal(bool(0))
convert_top(hdl='Verilog')
