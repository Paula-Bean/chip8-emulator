def emulate_cycle():

    memory = [0x00, 0xE0, 0x10, 0x02, 0x00, 0xEE]
    pc = 0
    draw_flag = False
    stack = [0, 0, 0]
    sp = 0
    rom = True
    I = 0

    while rom != False:
        opcode = ((memory[pc] << 8) | memory[pc + 1])
        print(opcode & 0xF000)
        if opcode == 0x00E0:  # clear screen
            # clear_display()
            pc += 2
            draw_flag = True
            print('clear screen')
        elif opcode == 0x00EE:  # return from subroutine
            pc = stack[sp]
            pc += 2
        elif (opcode & 0xF000) == 0x1000:  # jump to address NNN (opcode = 1NNN)
            I = opcode & 0x0FFF
            pc += 2
        else:
            print('failure')


emulate_cycle()
