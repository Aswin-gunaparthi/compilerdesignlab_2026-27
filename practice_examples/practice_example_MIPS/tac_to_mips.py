"""
Three-Address Code to MIPS generator.

# Pending
"""
from three_address_code import BinOpTAC, CopyTAC, is_literal

MIPS_OP = {
    '+': 'add',
    '-': 'sub',
    '*': 'mul',   # SPIM pseudo-instruction: 3-operand mul $d,$s,$t
    '/': 'div',   # SPIM pseudo-instruction: 3-operand div $d,$s,$t
}


class MIPSGenerator:
    def __init__(self):
        self.data_names = []       
        self._declared = set()     
        self.mips_lines = []

    def allocate(self, name):
        """
        Call this every
        time you're about to lw/sw a variable or temporary name -- not
        for literals/constants (see is_literal() in three_address_code.py). Stores
        the ORIGINAL name in self.data_names
        """
        if name not in self._declared:
            self._declared.add(name)
            self.data_names.append(name)

    def addMIPS(self, line):
        """Provided. Appends one line of MIPS assembly """
        self.mips_lines.append(line)

    def load(self, operand, reg):
        """
          - If is_literal(operand) is True: emit `li reg, operand`
          - Otherwise:
            `lw reg, name`
        """
        if is_literal(operand):


        raise NotImplementedError("implement MIPSGenerator.load()")

    def store(self, reg, name):
        """
        TODO(week-4): self.allocate(name), then emit
        `sw reg, {safe_label(name)}`.
        """
        raise NotImplementedError("implement MIPSGenerator.store()")

    def gen_instr(self, instr):
        """
        TODO(week-4): dispatch on instr's type and emit MIPS for it.

          isinstance(instr, BinOpTAC):
              self.load(instr.src1, '$t0')
              self.load(instr.src2, '$t1')
              self.emit(f"{MIPS_OP[instr.op]} $t2, $t0, $t1")
              self.store('$t2', instr.dest)

          isinstance(instr, CopyTAC):
              self.load(instr.src, '$t0')
              self.store('$t0', instr.dest)

          isinstance(instr, PrintTAC):
              self.load(instr.src, '$a0')
              self.emit("li $v0, 1")
              self.emit("syscall")
        """
        raise NotImplementedError("implement MIPSGenerator.gen_instr()")

    def generate(self, instructions):
        """
        Provided. Runs gen_instr() over the whole 3AC list, then appends
        the program-exit syscall sequence, then renders the final .s
        text. You should not need to change this method.
        """
        for instr in instructions:
            self.gen_instr(instr)
        self.emit("li $v0, 10")
        self.emit("syscall")
        return self.render()

    def render(self):
        """
        Provided. Assembles the final .data/.text sections, applying
        safe_label() to every name written as a .data label. Every
        variable/temporary gets exactly one .word, initialized to 0
        (the initial value doesn't matter -- every one is written by a
        CopyTAC or BinOpTAC before it's ever read, since TinyCStr has no
        uninitialized reads in Level 1's grammar).
        """
        lines = [".data"]
        for name in self.data_names:
            lines.append(f"{safe_label(name)}: .word 0")
        lines.append(".text")
        lines.append(".globl main")
        lines.append("main:")
        lines.extend(f"    {line}" for line in self.text_lines)
        return "\n".join(lines) + "\n"


def generate_mips(instructions):
    """Convenience wrapper: generate() a fresh MIPSGenerator for one function's 3AC."""
    return MIPSGenerator().generate(instructions)
