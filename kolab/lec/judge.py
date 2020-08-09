def naming(name, ins):
  if isinstance(ins, tuple) and len(ins) > 1:
    return f'{name}{repr(ins)}'
  return f'{name}({repr(ins)})'


def testData(f, data):
  result = f(*data)
  return result


def match(a, b):
  return a == b


def chk(c):
  return '✅' if c else '❌'


class Judge(object):
  def __init__(self, data):
    self.judge_data = data

  def judge(self, name, f):
    results = []
    c = 0
    for i, data in enumerate(self.judge_data):
      case = data['case'] if 'case' in data else naming(name, data['input'])
      self.showing(i, case)
      output = data['output']
      method = f'test{i}'
      if hasattr(self, method):
        testFunction = getattr(self, method)
      else:
        testFunction = testData
      try:
        input_data = data.get('input', tuple())
        if not isinstance(input_data, tuple):
          input_data = tuple(input_data)
        result = testFunction(f, input_data)
      except Exception as e:
        result = e
      # data
      checked = match(result, output)
      hint = '' if checked else data.get('hint', '')
      self.show(i, case, result, checked, output)
      results.append((i, case, result, checked, output, hint))
      if checked:
        c += 1
    self.showall(c, results)

  def showing(self, i, title):
    pass
    #print(f'[{i}] {title} => ...')

  def show(self, i, title, result, checked, output):
    if isinstance(result, Exception):
      print(f'[{i}] {title} => {chk(checked)} {result.__class__.__name__}')
      print(' エラー:', result)
      return
    print(f'[{i}] {title} => {chk(checked)} {repr(result)}')
    if not checked:
      if type(output) != type(result):
        print(' 結果の型が違う:', '(正)', type(output), '(誤)', type(result))
      else:
        print(' 正解:', repr(output))
      #print(' 誤り:', result)

  def showall(self, c, results):
    print(f'[{c}/{len(results)}] AC')
