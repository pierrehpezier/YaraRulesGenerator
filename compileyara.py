
class yaragen:
    def __init__(self):
        self.history = []
        self.oldopcodeslist = ''

    def update(self, data):
        #DETERMINE DISTANCE
        opcodeslist = ''
        for item in data.split('\n'):
            _, _, opcodes, _ = item.split(' ', 3)
            opcodeslist += opcodes
        self.isupdate = self.hamming_distance(opcodeslist, self.oldopcodeslist) < 5
        self.oldopcodeslist = opcodeslist
        retval = '$bbl = {\n'
        history = []
        for counter, item in enumerate(data.split('\n')):
            _, _, opcodes, instructions = item.split(' ', 3)
            if self.isupdate:
                opcodes = self.computediff(opcodes, self.history[counter])
            retval += self.align(self.opcodeToYar(opcodes)) + '// {} \n'.format(instructions.strip(' '))
            history.append(opcodes)
        self.history = history
        return retval + '}\n'

    @staticmethod
    def computediff(i1, i2):
        if len(i1) != len(i2): return i1
        retval = ''
        for i in range(0, len(i1), 2):
           b1 = i1[i: i+2]
           b2 = i2[i: i+2]
           if b2 == '??': retval += '??'
           elif b1 != b2: retval += '??'
           else: retval += b2
        return retval

    @staticmethod
    def align(data, alignment=32):
        if len(data) > alignment: return data
        return data + ' '*(alignment - len(data))

    @staticmethod
    def hamming_distance(s1, s2):
        print(s1, s2)
        if len(s1) != len(s2): return 100
        return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

    def opcodeToYar(self, opcode):
        retval = ''
        for i in range(0, len(opcode), 2):
            retval += opcode[i: i + 2] + ' '
        return retval

if __name__ == '__main__':
    gen = yaragen()
    a=gen.update('''00000000  4831C0            xor rax,rax
00000003  90                nop
00000004  6748895805        mov [eax+0x5],rbx
00000009  C3                ret
0000000A  4831C0            xor rax,rax
0000000D  90                nop
0000000E  58                pop rax''')
    print(a)
    a=gen.update('''00000000  4831C0            xor rax,rax
00000003  90                nop
00000004  6748895805        mov [eax+0x5],rbx
00000009  C3                ret
0000000A  4831C3            xor rbx,rax
0000000D  90                nop
0000000E  58                pop rax''')
    print(a)
    a=gen.update('''00000000  4831D8            xor rax,rbx
00000003  91                nop
00000004  6748895805        mov [eax+0x5],rbx
00000009  C3                ret
0000000A  4831C3            xor rbx,rax
0000000D  90                nop
0000000E  58                pop rax''')
    print(a)
