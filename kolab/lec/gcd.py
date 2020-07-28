
gcd_data = [
    {
        'input': (6215, 4746),
        'output': 113,
    },
    {
        'input': (4746, 6215),
        'output': 113,
    },
]

judge_data = {
    'gcd': gcd_data,
}


def show(name, ins):
  if isinstance(ins, tuple) and len(ins) > 1:
    return f'{name}{repr(ins)}'
  return f'{name}({repr(ins)})'


def match(a, b):
  return a == b

def judge(name, names = globals()):
  #names = globals()
  print(names)
  f = names[name]
  for data in judge_data[name]:
    print(show(name, data['input']), '=>', end='')
    output = f(*data['input'])
    print(output, data['output'])
