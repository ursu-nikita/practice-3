# Indirect square root. The source value is preserved at 512.
mem[512] = 9
mem[700] = 512
mem[600] = sqrt(mem[mem[700]])
