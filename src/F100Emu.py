## ============================================================================
## F100Emu.py - Emulator for the Ferranti F100-L CPU
##
## COPYRIGHT 2016 Richard Evans, Ed Spittles
##
## This file is part of f100l - an set of utilities for programming and
## emulation of the Ferranti F100-L CPU and peripheral components.
##
## f100l is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## f100l is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## See  <http://www.gnu.org/licenses/> for a copy of the GNU Lesser General
## Public License
##
## ============================================================================
'''
USAGE:

  F100Emu is a very simple emulator for the Ferranti F100-L CPU.

REQUIRED SWITCHES ::

  -f --filename  <filename>      specify the assembled object file

  -g --format    <bin|ihex|hex>  set the file format for the assembled code


OPTIONAL SWITCHES ::

  -a --adsel      <0|1>          specify the state of the AdSel pin
                                 - defaults to 1 if not specified

  -e --endianness <little|big>   set endianness of byte oriented input file
                                 - default is little-endian

  -t --traceon                   print all memory transactions to stdout

  -h --help                      print this help message

EXAMPLES ::

  python3.5 F100Emu.py -f test.hex -g hex

'''

banner =\
'''
# -------------------------------------------------------------------------------------------
#    _____________  ____        __       ______                __      __
#   / ____<  / __ \/ __ \      / /      / ____/___ ___  __  __/ /___ _/ /_____  _____
#  / /_   / / / / / / / /_____/ /      / __/ / __ `__ \/ / / / / __ `/ __/ __ \/ ___/
# / __/  / / /_/ / /_/ /_____/ /___   / /___/ / / / / / /_/ / / /_/ / /_/ /_/ / /
#/_/    /_/\____/\____/     /_____/  /_____/_/ /_/ /_/\__,_/_/\__,_/\__/\____/_/
#
#
# F 1 0 0 - L * E M U L A T O R (c) 2016 Revaldinho & BigEd
# -------------------------------------------------------------------------------------------'''

from F100_Opcodes.F100_Opcode import F100HaltException
from F100CPU import F100CPU
from hex2bin import Hex2Bin
import getopt
import sys

def print_header():
    print(banner)
    print("#                                   Condition Reg.")
    print("# PC   : Memory         : Acc. OR.  I Z V S C M F  : Instruction ")
    print("# -------------------------------------------------------------------------------------------")

class F100Emu:
    def __init__ (self, ramsize=32768, adsel=1, traceon=False):
        self.CPU = F100CPU(adsel=adsel, memory_read=self.memory_read, memory_write=self.memory_write)
        self.RAM = [0xDEAD]*ramsize
        self.MEMTOP = ramsize-1
        self.traceon = traceon

    def memory_read(self, address):
        if self.traceon == True:
            print ("READ 0x%04X 0x%04X" % ( address & 0xFFFF, self.RAM[address] & 0xFFFF))

        if 0 <= address <= self.MEMTOP:
            return self.RAM[address]
        else:
            raise UserWarning("Memory out of range error for address 0x%04X" % address )

    def memory_write(self, address, data):
        if self.traceon == True:
            print ("STORE 0x%04X 0x%04X" % ( address & 0xFFFF, data & 0xFFFF))
        if 0 <= address <= self.MEMTOP:
            self.RAM[address] = data & 0xFFFF
        else:
            raise UserWarning("Memory out of range error for address 0x%04X" % address )

    def single_step(self):
        return self.CPU.single_step()

    def print_machine_state(self):
        CPU = self.CPU
        PC = self.CPU.PC
        CR = self.CPU.CR
        print("  %04X : %04X %04X %04X : %04X %04X %d %d %d %d %d %d %d  :" % \
        (PC & 0xFFFF,self.RAM[PC] & 0xFFFF ,self.RAM[PC+1] & 0xFFFF, self.RAM[PC+2] & 0xFFFF,\
         CPU.ACC & 0xFFFF ,CPU.OR & 0xFFFF ,CR.I,CR.Z,CPU.CR.V,CR.S,CR.C,CR.M,CR.F ))


if __name__ == "__main__" :
    filename = ""
    file_format = ""
    adsel = 1
    endianness = "little"
    traceon = False
    try:
        opts, args = getopt.getopt( sys.argv[1:], "a:e:f:g:h:t", ["adsel=","endianness=", "filename=","format=","help","traceon"])
    except getopt.GetoptError as  err:
        print(err)
        usage()

    for opt, arg in opts:
        if opt in ( "-f", "--filename" ) :
            filename = arg
        if opt in ( "-a", "--adsel" ) :
            adsel = int(arg)
        if opt in ( "-e", "--endianness" ) :
            endianness = arg
        if opt in ( "-g", "--format" ) :
            if (arg in ("hex", "bin", "ihex")):
                file_format = arg
            else:
                usage()
        if opt in ("-t", "--traceon") :
            traceon = True
        elif opt in ("-h", "--help" ) :
            usage()
    if filename=="" or file_format=="":
        usage()


    emu = F100Emu(adsel=adsel, traceon=traceon)

    # Initialise the hex2bin object with a 64Kbyte address space
    h = Hex2Bin(64*1024)
    h.read_file(filename, file_format, 0, 64*1024)
    # Now convert into the local RAM
    for i in range(0, 64*1024,2):
        local_addr = i >> 1
        if endianness == "little":
            (byte_lo,valid) = h.read_byte(i)
            i+=1
            (byte_hi,valid) = h.read_byte(i)
            i+=1
        else:
            (byte_hi,valid) = h.read_byte(i)
            i+=1
            (byte_lo,valid) = h.read_byte(i)
            i+=1
        emu.RAM[local_addr] = ((byte_hi << 8) | byte_lo ) & 0xFFFF

    emu.CPU.reset()

    # simple dummy loop - don't execute uninitialised RAM yet...
    i = 0
    print_header()
    while emu.memory_read(emu.CPU.PC) != 0xDEAD:
        emu.print_machine_state()
        try:
            emu.CPU.single_step()
        except F100HaltException as e:
            print(e)
            break
        i += 1
        if i> 100:
            break