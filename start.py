
class chip8:
    def initialize(self):
        global opcode = 0
        global memory = [0 for x in range(4096)]  # initializing memory array
        global V = [x for x in range(16)]  # initializing cpu registers
        global I = 0  # index register
        global pc = '0x200'  # program counter always starts here
        global gfx = [0 for x in range(64*32)]  # pixel screen
        global delay_timer = 0  # 60hz timer
        global sound_timer = 0  # 60hz timer
        global stack = [x for x in range(16)]
        global sp = 0
        global key = [x for x in range(16)]
        global fontset = []

        for i in range(80):    # loading fontset at location 80. ###come back
            memory[i] = fontset[i]

        with open('rom.rom') as rom:
            for i in range(len(rom)):
                memory[i + 512] = rom[i]

    def emulate_cycle(self):
        opcode = (memory[pc] * 10000000) + memory[pc + 1]


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
