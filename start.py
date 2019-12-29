#!/usr/bin/env python3

# See https://massung.github.io/CHIP-8/
#     and/or
#     https://en.wikipedia.org/wiki/CHIP-8
#     http://devernay.free.fr/hacks/chip8/C8TECH10.HTM


# Empty object, used as a container for variables. Allows access to global variables
# from within functions, without having to write 'global' everywhere.
class Bag:
    pass


# Machine
machine = Bag()
machine.memory = [0 for x in range(4096)]  # 4K of memory, initialized to zeros
machine.gfx = [0 for x in range(64 * 32)]  # Memory-mapped pixel screen
machine.stack = [] # Up to 16 return adresses
machine.key = [x for x in range(16)]  # Keypad
machine.delay_timer = 0
machine.sound_timer = 0


# Processor state
cpu = Bag()
cpu.V = [0 for x in range(16)]  # Data registers
cpu.I = 0  # Index register
cpu.PC = 0 # Program counter


# Emulator settings
em = Bag()
em.draw_flag = False # True if the CHIP-8's screen has been drawn to
em.emulate = False # True if the emulator is running, False if it should stop


# Font bitmaps
fontset = (0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
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
           0xF0, 0x80, 0xF0, 0x80, 0x80   # F
           )


# Small test program, intended to be loaded at 0x200
testprog = (0x00, 0xE0, # clear screen
            0x12, 0x04, # jump to 0x204 (the next instruction)

                        # test sprite drawing
            0xA0, 0x87, # I = 0x87 (where the sprite bitmap for letter 'B' is located)
            0x60, 0x03, # V0 = 3
            0x61, 0x07, # V1 = 7
            0xD0, 0x15, # Display sprite I at (3, 7), height=5.

            0xA0, 0x82, # I = 0x82 (letter 'A')
            0x60, 0x0A, # V0 = 10
            0x61, 0x07, # V1 = 7
            0xD0, 0x15, # Display sprite I at 8, 7

                        # test addition
            0x64, 0x0f, # V4 = 15
            0x65, 0x1b, # V5 = 27
            0x84, 0x54, # V4 = V4 + V5

            0x00, 0xEE, # return from subroutine (or halt the progam, if the stack is empty)
            )


def initialize():
    cpu.PC = 0x200  # Program counter always starts here after a CPU reset
    machine.stack = [] # Empty the stack

    # Load fontset into memory at position 80
    addr = 80
    for b in fontset:
        machine.memory[addr] = b
        addr += 1

    # Load test program at 0x200
    addr = 0x200
    for b in testprog:
        machine.memory[addr] = b
        addr += 1

    '''
    # Read ROM image at 0x200
    addr = 0x200
    with open("rom.ch8", "rb") as f:
        bs = f.read()
        for b in bs:
            machine.memory[addr] = b
            addr += 1
    '''
    em.emulate = True # Start running! ;-)


def memory_dump():
    print(machine.memory) # TODO: probably want neat hex dump here


def register_dump():
    print("  Registers:", cpu.V) # TODO: nicer format


def clear_display():
    machine.gfx = [0 for x in range(64 * 32)]


def emulate_cycle():
    em.draw_flag = False
    opcode = (machine.memory[cpu.PC] << 8) | machine.memory[cpu.PC + 1]
    print(f'PC is 0x{cpu.PC:04x}, opcode is 0x{opcode:04x}')
    if opcode == 0x00E0:  # clear screen
        print("  Clear screen")
        clear_display()
        cpu.PC += 2
        em.draw_flag = True
    elif opcode == 0x00EE:  # return from subroutine
        if not machine.stack:
            print("  Return from subroutine, but the stack is empty. Stopping program.")
            register_dump()
            em.emulate = False
        else:
            addr = machine.stack.pop()
            print("  Return from subroutine to 0x{addr:04x}")
            cpu.PC = addr
    elif (opcode & 0xF000) == 0x1000:  # jump to address NNN (opcode = 1NNN)
        addr = opcode & 0x0FFF
        print(f"  Jump to address 0x{addr:04x}")
        cpu.PC = addr
    elif (opcode & 0xF000) == 0x2000:  # jump to subroutine
        addr = opcode & 0x0FFF
        print(f"  Jump to subroutine at 0x{addr:04x}")
        machine.stack.push(cpu.PC + 2)
        cpu.PC = addr
    elif (opcode & 0xF000) == 0xA000:  # Annn - LD I, addr; Set I = nnn. The value of register I is set to nnn.
        val = opcode & 0x0FFF
        print(f"  Load 0x{val:04x} into I")
        cpu.I = val
        cpu.PC += 2
    elif (opcode & 0xF000) == 0x6000:  # 6xkk - LD Vx, byte; Set Vx = kk.
        reg = (opcode & 0x0F00) >> 8
        val = opcode & 0x00FF
        print(f"  Load 0x{val:04x} into V{reg}")
        cpu.V[reg] = val
        cpu.PC += 2
    elif (opcode & 0xF00F) == 0x8004: # add the value of VY to VX (opcode = 0x8XY4)
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        f = 15
        print(f'  Add V{y} ({cpu.V[y]}) into V{x} ({cpu.V[x]})')
        val = cpu.V[x] + cpu.V[y]
        if val <= 255:
            cpu.V[f] = 0 # result fits in a byte, clear carry
        else:
            cpu.V[f] = 1 # result overflowed, set carry
            val -= 255
        cpu.V[x] = val
        cpu.PC += 2
        print(f"  Result is {val}, carry={cpu.V[f]}")
    elif (opcode & 0xF0FF) == 0xF033: # Store the decimal value of Vx, and places the hundreds digit in memory at location in I, the tens digit at location I+1, and the ones digit at location I+2.
        x = (opcode & 0x0F00) >> 8
        bcd = "%03d" % cpu.V[x]
        machine.memory[cpu.I + 0] = ord(bcd[0]) - ord("0")
        machine.memory[cpu.I + 1] = ord(bcd[1]) - ord("0")
        machine.memory[cpu.I + 2] = ord(bcd[2]) - ord("0")
        cpu.PC += 2
    # pixel drawer, draw sprite at coordinate (VX, VY) that has a width of 8 pixels and a height of N pixels (opcode = DXYN)
    elif (opcode & 0xF000) == 0xD000:
        x = cpu.V[(opcode & 0x0F00) >> 8]
        y = cpu.V[(opcode & 0x00F0) >> 4]
        height = opcode & 0x000F
        print(f"  Draw sprite at memory 0x{cpu.I:04x} on screen coordinates ({x}, {y})")
        cpu.V[0xF] = 0
        for yline in range(height):
            spritebits = machine.memory[cpu.I + yline]
            for xline in range(8):
                if spritebits & (0x80 >> xline):
                    if machine.gfx[(y + yline) * 64 + x + xline] == 1: # collision detection
                        cpu.V[0xF] = 1
                    machine.gfx[((y + yline) * 64) + x + xline] ^= 1
        em.draw_flag = True
        cpu.PC += 2
    elif (opcode & 0xF000) == 0xE000:
        if (opcode & 0x00FF) == 0x009E and key[cpu.V[(opcode & 0x0F00) >> 8]] != 0:
            cpu.PC += 4
        else:
            cpu.PC += 2
        print("  Key pressed")
    else:
        print(f"Unrecognized opcode 0x{opcode:04x} at address 0x{cpu.PC:04x}. Emulator stopping.")
        em.emulate = False

    # CHIP-8 has two timers. They both count down at 60 hertz, until they reach 0.
    # Delay timer: This timer is intended to be used for timing the events of games. Its value can be set and read.
    # Sound timer: This timer is used for sound effects. When its value is nonzero, a beeping sound is made.
    #
    # if delay_timer > 0:
    #     delay_timer -= delay_timer
    # if sound_timer > 0:
    #     if sound_timer == 1:
    #         print('beep')
    #     else:
    #         sound_timer -= sound_timer


def draw_graphics():
    for row in range(32):
        line = ""
        for col in range(64):
            addr = 64 * row + col
            if machine.gfx[addr]:
                line += "#"
            else:
                line += "."
        print(line)
    print()


if __name__ == "__main__":
    clear_display()
    initialize()
    while em.emulate == True:
        emulate_cycle()
        if em.draw_flag:
            draw_graphics()
