#!/usr/bin/env python3

"""
Generate different flavors of input assembly for testing.
"""

import os.path

from common import set_basename, gcc, disasm, grep

set_basename(os.path.basename(__file__))

for gdb in [False, True]:
    for pic in [False, True]:  # Do we need to test PIE too?
        for strip in [False, True]:
            # Print config

            disasm_type = 'GDB' if gdb else 'objdump'
            pic_type = 'position-INdependent' if pic else 'position-dependent'
            stripped = 'stripped' if strip else 'UNstripped'
            print(f"Checking {disasm_type} {pic_type} {stripped}")

            # Generate object code

            flags = ['jumptable.c', '-o', 'a.out',
                     '-Wl,--defsym,_start=0', '-nostdlib', '-nostartfiles', '-O2']
            # DLL or executable?
            if pic:
                flags += ['-fPIC', '-shared']
            # Include debuginfo?
            if not strip:
                flags.append('-g')

            gcc(flags)

            # Generate disasm

            caller = 'bar'
            out = disasm('a.out', not gdb, strip, caller)

            # Print snippets

            jumps = grep(out, r'\bjmp')
            print('''\
  table jumps:
    {}
'''.format('\n    '.join(jumps)))
