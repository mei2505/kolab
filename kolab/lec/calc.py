from kolab.lec.judge import Judge

judge_data = [
    {
        'input': '1',
        'output': 1,
    },
    {
        'input': '123',
        'output': 123,
    },
    {
        'input': '1+2',
        'output': 3,
    },
    {
        'input': '1+2+3',
        'output': 6,
    },
    {
        'input': '1+2+3+4+5+6+7+8+9+0',
        'output': 45,
    },
    {
        'input': '1+2*3',
        'output': 7,
    },
    {
        'input': '1*2+3',
        'output': 5,
    },
    {
        'input': '1*2+3*4',
        'output': 14,
    },
    {
        'input': '1*2+3*4+5*6+7*8+9',
        'output': 109,
    },
    {
        'input': '1-2',
        'output': -1,
    },
    {
        'input': '1-2-3',
        'output': -4,
    },
    {
        'input': '7/2',
        'output': 3,
    },
    {
        'input': '1+2*3/4',
        'output': -4,
    },
    {
        'input': '(1+2)*3',
        'output': 9,
    },
]

def judge(func):
  oj = Judge(judge_data)
  oj.judge('calc', func)


