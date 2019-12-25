def emulate_cycle():

    memory = [1110, 0000, 1110, 1110]
    pc = 0
    draw_flag = False
    stack = [0, 0, 0]
    sp = 0
    rom = True

    while rom != False:
        opcode = (
            hex(int(str((memory[pc] * 10000) + memory[pc + 1]), 2))).upper()
        print(opcode[2::])
        if opcode[2::] == 'E0':  # clear screen
            # clear_display()
            pc += 2
            draw_flag = True
            print('clear screen')
        elif opcode[2::] == 'EE':  # return from subroutine
            pc = stack[sp]
            pc += 2
        elif opcode == (opcode[2] == '1'):  # jump to address NNN (opcode = 1NNN)
            pc = opcode[3:6]
            pc += 2
        else:
            print('failure')


emulate_cycle()
