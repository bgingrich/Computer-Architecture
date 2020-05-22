"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # PC
        self.pc = 0
        # 8 Registers
        self.reg = [0] * 8
        # 256 RAM
        self.ram = [0] * 256
        # Internal Register
        self.ir = 0
        # Stack Pointer
        self.sp = 7
        # Flag
        self.fl = 6
        # Operation Table
        self.op_table = {
            0b10000010: self._ldi,
            0b01000111: self._prn,
            0b10100010: self._mult,
            0b00000001: self._hlt,
            0b01000101: self._push,
            0b01000110: self._pop,
            0b01010000: self._call,
            0b00010001: self._ret,
            0b10100000: self._add,
            0b01010110: self._jne,
            0b01010100: self._jmp,
            0b01010101: self._jeq,
            0b10100111: self._cmp
        }

    def _ldi(self, reg_a, reg_b):
        self.reg[reg_a] = reg_b

    def _prn(self, reg_a, reg_b):
        print(self.reg[reg_a])

    def _add(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] + self.reg[reg_b]

    def _mult(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]

    def _hlt(self, reg_a, reg_b):
        sys.exit()

    def _push(self, reg_a, reg_b):
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.reg[reg_a]

    def _pop(self, reg_a, reg_b):
        self.reg[reg_a] = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1

    def _call(self, reg_a, reg_b):
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.pc + 2
        self.pc = self.reg[reg_a]
        return True

    def _ret(self, reg_a, reg_b):
        self._pop(reg_a, 0)
        self.pc = self.reg[reg_a]
        return True

    def _jne(self, reg_a, reg_b):
        val = self.reg[self.fl]
        if val == 2 or val == 4:
            return self._jmp(reg_a, 0)
    
    def _jmp(self, reg_a, reg_b):
        self.pc = self.reg[reg_a]
        return True

    def _jeq(self, reg_a, reg_b):
        if self.reg[self.fl] == 1:
            return self._jmp(reg_a, 0)

    def _cmp(self, reg_a, reg_b):
        self.alu('CMP', self.ram[self.pc + 1], self.ram[self.pc +2])
    
    # RAM Read
    def ram_read(self, mar):
        # Memory Access Register
        return self.ram[mar]

    # RAM Write
    def ram_write(self, mdr, mar):
        # Memory Data Register
        self.ram[mar] = mdr

    def load(self, prog):
        """Load a program into memory."""

        address = 0
        with open(prog) as program:
            for instruction in program:
                instruction_split = instruction.split('#')
                instruction_stripped = instruction_split[0].strip()

                if instruction_stripped == '':
                    continue
                instruction_num = int(instruction_stripped, 2)
                self.ram_write(instruction_num, address)
                address += 1

    # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        # elif op == "SUB": etc
        if op == 'OR':
            if reg_a == 1 and reg_b == 0:
                return True
            elif reg_a == 0 and reg_b == 1:
                return True
            elif reg_a == 1 and reg_b == 1:
                return True
            else:
                return False

        if op == 'XOR':
            if reg_a == 1 and reg_b == 0:
                return True
            if reg_a == 0 and reg_b == 1:
                return True
            else:
                return False

        if op == 'NOR':
            if reg_a == 0 and reg_b == 0:
                return True
            else:
                return False
        
        elif op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:
                self.reg[self.fl] = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.reg[self.fl] = 2
            else:
                self.reg[self.fl] = 4

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while True:
            self.ir = self.ram[self.pc]
            reg_a = self.ram[self.pc + 1]
            reg_b = self.ram[self.pc + 2]

            jump = self.op_table[self.ir](reg_a, reg_b)
            if not jump:
                self.pc += (self.ir >> 6) + 1






# instruction = self.ram_read(self.pc)
            # reg_a = self.ram_read(self.pc + 1)
            # reg_b = self.ram_read(self.pc + 2)
            # if instruction == HLT:
            #     running = False
            #     self.pc += 1
            #     sys.exit()
            # elif instruction == LDI:
            #     self.reg[reg_a] = reg_b
            #     self.pc += 3
            # elif instruction == PRN:
            #     print(self.reg[reg_a])
            #     self.pc += 2
            # elif instruction == MUL:
            #     self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
            #     self.pc += 3
            # elif instruction == PUSH:
            #     reg = self.ram[self.pc+1]
            #     val = self.reg[reg]
            #     self.reg[self.sp] -= 1
            #     self.ram[self.reg[self.sp]] = val
            #     self.pc += 2
            # elif instruction == POP:
            #     reg = self.ram[self.pc+1]
            #     val = self.ram[self.reg[self.sp]]
            #     self.reg[reg] = val
            #     self.reg[self.sp] += 1
            #     self.pc += 2  
            # else:
            #     print(f'This instruction is not valid: {hex(instruction)}')
            #     running = False
            #     sys.exit()            
