# Code occupies addresses 0..31. Data is separate within the same memory.
mem[512] = 7
mem[513] = 11
mem[514] = 19
# Address 700 holds a pointer to the first source element.
mem[700] = 512
mem[600] = mem[mem[700]]
# The other two elements use direct copies.
mem[601] = mem[513]
mem[602] = mem[514]
