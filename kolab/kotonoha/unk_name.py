import re
import sys

prefix_list_bool = {
  'is': '期待する状態になっているか',
  'can': '期待する処理ができるか',
  'should': '命令を実行するべきか',
  'need': '命令を実行する必要があるか',
  'has': '期待するデータやプロパティを持っているか',
}

prefix_list_verb = {
  'find': '検索',
  'search': '探索',
  'set': '設定',
  'add': '追加',
  'put': '追加',
  'insert': '挿入',
  'append': '末尾に追加',
  'push': '先頭に追加',
  'prepend': '先頭に追加',
  'register': '登録',
  'create': '作る',
  'new': '作る', 
  'make': '作る',
  'build': '組み立てる',
  'from': '流用して作る',
  'generate': 'ルールに従って作る',
  'update': 'アップデート',
  'upgrade': 'アップグレード',
  'apply': '適用',
  'refresh': '更新',
  'changed': '変更',
  'modified': '修正',
  'revised': '改版',
  'enable': '使用可能に',
  'disable': '使用不可に',
  'fix': '解決',
  'repair': '修理',
  'restore': '復元',
  'recover': '復旧',
  'edit': '編集',
  'adjust': '調整',
  'adapt': '適合',
  'convert': '変換',
  'to': '変換',
  'delete': '削除',
  'remove': '除去',
  'trash': '廃棄',
  'erase': '消去',
  'clear': '初期化',
  'flush': '初期化',
  'reset': '初期化',
  'dispose': '開放',
  'destroy': '破棄',
  'unregister': '解除',
  'unset': '未定義に',
  'pop': '先頭のデータを取り出して取り除く',
  'save': '保存',
  'output': '出力',
  'export': '書き出す',
  'write': '書き込む',
  'store': '貯蔵',
  'send': '送信',
  'commit': '確定',
  'get': '取得',
  'load': '呼び出す',
  'input': '入力',
  'import': '読み出す',
  'read': '読み込む',
  'restore': '復元',
  'fetch': '取得',
  'check': '条件に適合',
  'test': 'ルールを満たすか確認',
  'validate': '正しいか検証',
  'compare': '比較',
  'verify': '照合',
  'allow': '権限付与',
  'disallow': '権限付与なし',
  'accept': '承認',
  'deny': '否認',
  'refuse': '辞退',
  'reject': '拒否',
  'grant': '与える',
  'revoke': '剥奪',
}

abbreviation_list = {
  'buf': '一時格納',
  'tmp': '仮',
  'cnt': 'カウンター',
  'msg': 'メッセージ',
  'flag': 'フラグ',
  'n': '数',
  'num': '数',
  's': '文字列',
  'str': '文字列'
}

def toSepList(s):
  sepList = []
  if '_' in s:
    sepList = s.split('_')
  elif '-' in s:
    sepList = s.split('-')
  elif s.islower() == False:
    s = s[0].upper() + s[1:]
    sepList = re.findall('[A-Z][^A-Z]*', s)
  else:
    sepList.append(s)
  # print('@@', *sepList)
  return sepList

def unk(named_list):
  sepList = toSepList(named_list)
  sepList = list(map(str.lower, sepList))
  if sepList[0] in prefix_list_verb.keys():
    sepList.append('を')
    sepList.append(prefix_list_verb[sepList[0]])
    sepList.pop(0)
  if len(sepList & abbreviation_list.keys()) != 0:
    for word in list(sepList & abbreviation_list.keys()):
      idx = sepList.index(word)
      sepList[idx] = abbreviation_list[word]
  # print('@@', sepList)
  return sepList

def toStr(named_list):
  named_str = ' '.join(unk(named_list))
  named_str = '{{' + named_str + '}}'
  print('@@', named_list)
  print('@@', named_str)
  return named_str

if __name__ == '__main__':
  for s in sys.argv[1:]:
    # toSepList(s)
    # unk(s)
    toStr(s)
