import time
from IPython.core.magic import register_cell_magic

original_input = input
magic_buffer = []
magic_pos = 0
magic_time = time.time()

@register_cell_magic
def In(line, src):
  global magic_buffer, magic_pos, magic_time
  magic_buffer = []
  magic_pos = 0
  for line in src.split('\n'):
    if len(line) == 0:
      continue
    magic_buffer.append(line)
  magic_time = time.time()
  return magic_buffer

def input(prompt = ''):
  global magic_buffer, magic_pos, magic_time
  if prompt != '' or len(magic_buffer) == 0:
    return original_input(prompt)
  if magic_pos == len(magic_buffer):
    magic_pos = 0
  if magic_pos > 0 and (time.time() - magic_time) > 10.0:
    magic_pos = 0
  if magic_pos < len(magic_buffer):
    magic_pos += 1
    magic_time = time.time()
    return magic_buffer[magic_pos-1]
  else:
    raise EOFError()

