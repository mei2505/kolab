judge_data = [
    {
      'input': (6215, 4746),
      'output': 113,
    }
    
]


def judge_gcd(func):
  oj = Judge(judge_data_gcd)
  oj.judge('gcd', func)
