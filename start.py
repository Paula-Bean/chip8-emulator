
class chip8:
    def initialize(self):
        global opcode = 0
        global memory = [0 for x in range(4096)]  # initializing memory array
        global V = [x for x in range(16)]  # initializing cpu registers
        global I = 0  # index register
        global pc = 0x200  # program counter always starts here
        global gfx = [0 for x in range(64*32)]  # pixel screen
        global delay_timer = 0  # 60hz timer
        global sound_timer = 0  # 60hz timer
        # stack for emulating instruction stack
        global stack = [x for x in range(16)]
        global sp = 0  # stack pointer
        global key = [x for x in range(16)]  # keypad
        global fontset = []  # fonts and sprites

        for i in range(80):    # loading fontset at location 80. ###come back
            memory[i] = fontset[i]

        with open('rom.ch8', 'rb') as rom:
            rom_load = (byte for byte in rom.read(4096-512))
            for i, byte in enumerate(rom_load, pc):
                memory[i] = byte

    def clear_display(self):
        gfx = [0 for x in range(64*32)]

    def emulate_cycle():
        opcode = ((memory[pc] << 8) | memory[pc + 1])
        print(opcode & 0xF000)
        if opcode == 0x00E0:  # clear screen
            clear_display()
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

        if delay_timer > 0:
            delay_timer -= delay_timer
        if sound_timer > 0:
            if sound_timer == 1:
                print('beep')
            else:
                sound_timer -= sound_timer


class main:
    init_graphics()
    init_input()
    chip8.initialize()
    chip8.load_game()

    while True == True:
        chip8.emulate_cycle()
        if draw_flag:
            draw_graphics()
        chip8.set_keys()

    return 0
