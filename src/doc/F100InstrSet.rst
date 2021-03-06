==========================
The F100-L Instruction Set
==========================

The following pages present complete descriptions for all instructions implemented in the F100-L.

.. automodule:: InstructionReg
  :members:


Instruction Timings
-------------------

All instruction timings are defined using the following definitions

  * Ra1 = Program memory read access time
  * Ra2 = Data memory read access time
  * Rc1 = Program memory read cycle time
  * Rc2 = Data memory read cycle time
  * M   = Read-modify-write cycle time
  * Wc  = Data memory write cycle time
  * L   = 1 Logic cycle time (2x period of the CPU clock input)

Abbrieviations
--------------

Definitions ::

  N      11 bit memory address (associated with opcode field N above)
  P       8 bit memory address (associated with opcode field P above)
  W      15 bit memory address
  D      16 bit immediate data
  (N)    Contents of memory location N
  (P)    Contents of memory location P
  (W)    Contents of memory location W
  PC     Value of the Program Counter (when pointing at the opcode word)
  (PC+d) Contents of memory location offset by d words from the opcode

Instruction Definitions
=======================

.. ADD - Add (with Carry)
.. automodule:: F100_Opcodes.OpcodeF9
   :members:

.. ADS - Add (with Carry), Store to Memory
.. automodule:: F100_Opcodes.OpcodeF5
   :members:

.. AND - Logical And of Accumulator and Operand
.. automodule:: F100_Opcodes.OpcodeF12
   :members:

.. CAL - Store Link in Link Stack
.. automodule:: F100_Opcodes.OpcodeF2
   :members:

.. CLR, SET - Bit manipulation
.. automodule:: F100_Opcodes.OpcodeF0_Bit
   :members:

.. CMP - Compare Accumulator with Operand
.. automodule:: F100_Opcodes.OpcodeF11
   :members:

.. HALT - Stop Program Execution
.. automodule:: F100_Opcodes.OpcodeF0_Halt
   :members:

.. ICZ - Jump to (PC) if non-zero
.. automodule:: F100_Opcodes.OpcodeF7
   :members:

.. JBC,JBS,JCS,JSC - Conditional Jump
.. automodule:: F100_Opcodes.OpcodeF0_Jump
   :members:

.. JMP - Unconditional Jump
.. automodule:: F100_Opcodes.OpcodeF15
   :members:

.. LDA - Load Accumulator from Memory
.. automodule:: F100_Opcodes.OpcodeF8
   :members:

.. NEQ - Logical XOR of Accumulator and Operand
.. automodule:: F100_Opcodes.OpcodeF13
   :members:

.. RTC, RTN - Return from Subroutine
.. automodule:: F100_Opcodes.OpcodeF3
   :members:

.. SBS - Subtract (with Carry), Store to Memory
.. automodule:: F100_Opcodes.OpcodeF6
   :members:

.. SJM - Switch Jump
.. automodule:: F100_Opcodes.OpcodeF1
   :members:

.. SLA,SLE,SLL,SRA,SRE,SRL - Shift and Rotation
.. automodule:: F100_Opcodes.OpcodeF0_Shift
   :members:

.. STO - Store Accumulator to Memory
.. automodule:: F100_Opcodes.OpcodeF4
   :members:

.. SUB - Subtract (with Carry)
.. automodule:: F100_Opcodes.OpcodeF10
   :members:
