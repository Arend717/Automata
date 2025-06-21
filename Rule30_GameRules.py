def rule30_console(generations=32, size=64):
    state = 1 << (size // 2)
    for _ in range(generations):
        line = ''.join('O' if (state >> i) & 1 else '.' for i in reversed(range(size)))
        print(line)
        state = (state >> 1) ^ (state | (state << 1))
