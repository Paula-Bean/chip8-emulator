
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
        global fontset = [0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
                            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
                            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
                            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
                            0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
                            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
                            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
                            0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
                            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
                            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
                            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
                            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
                            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
                            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
                            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
                            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
                        ]  # fonts and sprites

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
                elif (opcode & 0xF00F) == 0x8004:   # add the value of VY to VX (opcode = 0x8XY4)
            # carry info
            if (V[(opcode & 0x00F0) >> 4]) > (0xFF - V[(opcode & 0x0F00) >> 8]):
                V[0xF] = 1
            else:
                V[0xF] = 0
            V[(opcode & 0x0F00) >> 8] += V[(opcode & 0x00F0) >> 4]
            pc += 2
        # elif (opcode & 0x00FF) == 0x0033:
        #     memory[I] = bin(V[(opcode & 0x0F00)])
        #     memory[I + 1] = bin(V[(opcode & 0x0F00)])
        #     memory[I + 2] = bin(V[(opcode & 0x0F00)])
        #     pc += 2

        # pixel drawer, draw sprite at coordinate (VX, VY) that has a width of 8 pixels and a height of N pixels (opcode = DXYN)
        elif (opcode & 0xF000) == 0xD000:
            x = V[(opcode & 0x0F00) >> 8]
            y = V[(opcode & 0x00F0) >> 4]
            height = opcode & 0x000F
            pixel = 1
            yline = 0
            xline = 0
            V[0xF] = 0
            while yline < height:
                pixel = memory[I + yline]
                yline += 1
                while xline < 8:
                    if (pixel & (0x80 >> xline)) != 0:
                        if gfx[(x + xline + ((y + yline) * 64)] == 1:
                            V[0xF]=1
                        gfx[x + xline + ((y + yline) * 64)] ^= 1
                    xline += 1
            draw_flag=True
            pc += 2

        elif (opcode & 0xF000) == 0xE000:
            if (opcode & 0x00FF) == 0x009E and key[V[(opcode & 0x0F00) >> 8]] != 0:
                pc += 4
            else:
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

    def draw_graphics(self):
        print(gfx)

class main:
    chip8.clear_display()
    chip8.initialize()


    while True == True:
        chip8.emulate_cycle()
        if draw_flag:
            chip8.draw_graphics()

    return 0
