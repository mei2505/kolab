from IPython.core.magic import register_cell_magic

original_input = input
magic_buffer = []
magic_pos = 0

@register_cell_magic
def In(lines, src):
  global magic_buffer
  magic_buffer = []
  for line in lines.split('\n'):
    if len(line) == 0:
      continue
    magic_buffer.append(line)
  return lines, magic_buffer

def input(prompt = ''):
  global magic_buffer, magic_pos
  if prompt != '' or len(magic_buffer) == 0:
    return original_input(prompt)
  if magic_pos < len(magic_buffer):
    magic_pos += 1
    return magic_buffer[magic_pos-1]
  else:
    raise EOFError()

