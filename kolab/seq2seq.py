import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import math
import time
import random
import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Encoder

MAX_LENGTH = 100


class EncoderRNN(nn.Module):
  def __init__(self, input_size, hidden_size):
    super(EncoderRNN, self).__init__()
    self.hidden_size = hidden_size
    # 行が各単語ベクトル、列が埋め込みの次元である行列を生成
    # Embedding(扱う単語の数, 隱れ層のサイズ(埋め込みの次元))
    self.embedding = nn.Embedding(input_size, hidden_size)
    self.gru = nn.GRU(hidden_size, hidden_size)

  def forward(self, input, hidden):
    embedded = self.embedding(input).view(1, 1, -1)
    # 1 x 1 x n 型にベクトルサイズを変える
    # n の値は自動的に設定される
    output = embedded
    output, hidden = self.gru(output, hidden)
    return output, hidden
    # output が各系列のGRUの隱れ層ベクトル

  def initHidden(self):
    return torch.zeros(1, 1, self.hidden_size, device=device)

# Decoder


class DecoderRNN(nn.Module):
  def __init__(self, hidden_size, output_size):
    super(DecoderRNN, self).__init__()
    self.hidden_size = hidden_size

    self.embedding = nn.Embedding(output_size, hidden_size)
    self.gru = nn.GRU(hidden_size, hidden_size)
    self.out = nn.Linear(hidden_size, output_size)
    self.softmax = nn.LogSoftmax(dim=1)

  def forward(self, input, hidden):
    output = self.embedding(input).view(1, 1, -1)
    output = F.relu(output)
    output, hidden = self.gru(output, hidden)
    output = self.softmax(self.out(output[0]))
    return output, hidden

  def initHidden(self):
    return torch.zeros(1, 1, self.hidden_size, device=device)


class AttnDecoderRNN(nn.Module):
  def __init__(self, hidden_size, output_size, dropout_p=0.1, max_length=MAX_LENGTH):
    super(AttnDecoderRNN, self).__init__()
    self.hidden_size = hidden_size
    self.output_size = output_size
    self.dropout_p = dropout_p
    self.max_length = max_length

    self.embedding = nn.Embedding(self.output_size, self.hidden_size)
    self.attn = nn.Linear(self.hidden_size * 2, self.max_length)
    self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
    # 線形結合を計算
    # hidden_size * 2
    # → 各系列のGRUの隠れ層とAttention層で計算したコンテキストベクトルをtorch.catでつなぎ合わせることで長さが２倍になる
    self.dropout = nn.Dropout(self.dropout_p)
    # 過学習の回避
    self.gru = nn.GRU(self.hidden_size, self.hidden_size)
    self.out = nn.Linear(self.hidden_size, self.output_size)

  def forward(self, input, hidden, encoder_outputs):
    embedded = self.embedding(input).view(1, 1, -1)
    embedded = self.dropout(embedded)

    attn_weights = F.softmax(
        self.attn(torch.cat((embedded[0], hidden[0]), 1)), dim=1)
    # 列方向を確率変換したいから dim = 1
    attn_applied = torch.bmm(attn_weights.unsqueeze(0),
                             encoder_outputs.unsqueeze(0))
    # bmm でバッチも考慮してまとめて行列計算
    # ここでバッチが考慮されるから unsqueeze(0) が必要

    output = torch.cat((embedded[0], attn_applied[0]), 1)
    output = self.attn_combine(output).unsqueeze(0)

    output = F.relu(output)
    output, hidden = self.gru(output, hidden)

    output = F.log_softmax(self.out(output[0]), dim=1)
    return output, hidden, attn_weights

  def initHidden(self):
    # コンテキストベクトルをまとめるための入れ物を用意する
    return torch.zeros(1, 1, self.hidden_size, device=device)

# train 関数


teacher_forcing_ratio = 0.5


def train(input_tensor, target_tensor, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion, max_length=MAX_LENGTH):
  encoder_hidden = encoder.initHidden()

  # 勾配の初期化
  encoder_optimizer.zero_grad()
  decoder_optimizer.zero_grad()

  # データをテンソルに変換する
  input_length = input_tensor.size(0)
  target_length = target_tensor.size(0)

  encoder_outputs = torch.zeros(
      max_length, encoder.hidden_size, device=device)

  loss = 0

  for ei in range(input_length):
    # for ei in range(5):
    encoder_output, encoder_hidden = encoder(
        input_tensor[ei], encoder_hidden)
    encoder_outputs[ei] = encoder_output[0, 0]

  decoder_input = torch.tensor([[SOS_token]], device=device)

  decoder_hidden = encoder_hidden

  use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False

  if use_teacher_forcing:
    # 教師強制を使用する場合
    # Teacher forcing: Feed the target as the next input
    # 教師強制 : 次の入力としてターゲットを送る
    for di in range(target_length):
      decoder_output, decoder_hidden, decoder_attention = decoder(
          decoder_input, decoder_hidden, encoder_outputs)
      loss += criterion(decoder_output, target_tensor[di])
      decoder_input = target_tensor[di]
  else:
    # Without teacher forcing: use its own predictions as the next input
    # 教師強制の使用をしない : 次の入力として独自の予測値を使用する
    for di in range(target_length):
      decoder_output, decoder_hidden, decoder_attention = decoder(
          decoder_input, decoder_hidden, encoder_outputs)
      topv, topi = decoder_output.topk(1)
      decoder_input = topi.squeeze().detach()  # detach from history as input

      loss += criterion(decoder_output, target_tensor[di])
      if decoder_input.item() == EOS_token:
          break

  # 誤差逆伝播
  loss.backward()

  # パラメータの更新
  encoder_optimizer.step()
  decoder_optimizer.step()

  return loss.item() / target_length


# Language

SOS_token = 0
EOS_token = 1

# デフォルト字句解析器


def defaultTokenizer(s):
  return s.split(' ')


class Lang(object):
  def __init__(self, name, tokenizer=defaultTokenizer):
    self.name = name
    self.tokenizer = tokenizer
    self.word2index = {}
    self.word2count = {}
    self.index2word = {0: "SOS", 1: "EOS"}
    self.n_words = 2

  def addSentence(self, sentence):
    tokenizer = self.tokenizer
    for word in tokenizer(sentence):
      self.addWord(word)

  def addWord(self, word):
    if word not in self.word2index:
      self.word2index[word] = self.n_words
      self.word2count[word] = 1
      self.index2word[self.n_words] = word
      self.n_words += 1
    else:
      self.word2count[word] += 1

  def indexesFromSentence(self, sentence):
    return [self.word2index[word] for word in self.tokenizer(sentence)]

  def tensorFromSentence(self, sentence):
    indexes = self.indexesFromSentence(sentence)
    indexes.append(EOS_token)
    return torch.tensor(indexes, dtype=torch.long, device=device).view(-1, 1)


def asMinutes(s):
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)


def timeSince(since, percent):
    now = time.time()
    s = now - since
    es = s / (percent)
    rs = es - s
    return '%s (- %s)' % (asMinutes(s), asMinutes(rs))

#plt.switch_backend('agg')


def showPlot(points):
    plt.figure()
    fig, ax = plt.subplots()
    loc = ticker.MultipleLocator(base=0.2)
    # this locator puts ticks at regular intervals
    # loc は定期的に ticker を配置する
    ax.yaxis.set_major_locator(loc)
    plt.plot(points)
    plt.savefig("plot.png")
    # content フォルダ下に保存される
    plt.show()


class Seq2SeqModel(object):

  def fit(self, pairs, inputTokenizer=defaultTokenizer, outputTokenizer=defaultTokenizer, hidden_size=256, n_iters=20000, print_every=2500):
    self.input_lang = Lang('Source', inputTokenizer)
    self.output_lang = Lang('Target', outputTokenizer)
    print(f'Read {len(pairs)} sentence pairs')
    for pair in pairs:
      if len(pair) >= 2:
        self.input_lang.addSentence(pair[0])
        self.output_lang.addSentence(pair[1])
    print("Counted words:")
    print(self.input_lang.name, self.input_lang.n_words)
    print(self.output_lang.name, self.output_lang.n_words)

    self.encoder = EncoderRNN(self.input_lang.n_words, hidden_size).to(device)
    self.decoder = AttnDecoderRNN(
        hidden_size, self.output_lang.n_words, dropout_p=0.1).to(device)
    self.trainIters(pairs, n_iters, print_every)

  def trainIters(self, pairs, n_iters, print_every=1000, plot_every=100, learning_rate=0.01):
    encoder = self.encoder
    decoder = self.decoder
    start = time.time()
    plot_losses = []
    print_loss_total = 0
    plot_loss_total = 0

    # 最適化
    encoder_optimizer = optim.SGD(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = optim.SGD(decoder.parameters(), lr=learning_rate)

    training_pairs = [self.tensorsFromPair(
        random.choice(pairs)) for i in range(n_iters)]

    # 損失関数
    criterion = nn.NLLLoss()

    for iter in range(1, n_iters + 1):
      training_pair = training_pairs[iter - 1]
      input_tensor = training_pair[0]
      target_tensor = training_pair[1]

      loss = train(input_tensor, target_tensor, encoder,
                   decoder, encoder_optimizer, decoder_optimizer, criterion)
      print_loss_total += loss
      plot_loss_total += loss

      if iter % print_every == 0:
          print_loss_avg = print_loss_total / print_every
          print_loss_total = 0
          print('%s (%d %d%%) %.4f' % (timeSince(start, iter / n_iters),
                                       iter, iter / n_iters * 100, print_loss_avg))

      if iter % plot_every == 0:
          plot_loss_avg = plot_loss_total / plot_every
          plot_losses.append(plot_loss_avg)
          plot_loss_total = 0

    showPlot(plot_losses)

  def tensorsFromPair(self, pair):
    input_tensor = self.input_lang.tensorFromSentence(pair[0])
    target_tensor = self.output_lang.tensorFromSentence(pair[1])
    return (input_tensor, target_tensor)

  def predict(self, sentence, max_length=MAX_LENGTH):
    encoder = self.encoder
    decoder = self.decoder
    with torch.no_grad():
      input_tensor = self.input_lang.tensorFromSentence(sentence)
      input_length = input_tensor.size()[0]
      encoder_hidden = encoder.initHidden()

      encoder_outputs = torch.zeros(
          max_length, encoder.hidden_size, device=device)
      # output_length =  encoder_outputs.size()[0]

      for ei in range(input_length):
        # for ei in range(5):
        encoder_output, encoder_hidden = encoder(
            input_tensor[ei], encoder_hidden)
        encoder_outputs[ei] += encoder_output[0, 0]

      decoder_input = torch.tensor([[SOS_token]], device=device)
      # SOS

      decoder_hidden = encoder_hidden

      decoded_words = []
      decoder_attentions = torch.zeros(max_length, max_length)

      for di in range(max_length):
        decoder_output, decoder_hidden, decoder_attention = decoder(
            decoder_input, decoder_hidden, encoder_outputs)
        decoder_attentions[di] = decoder_attention.data
        topv, topi = decoder_output.data.topk(1)
        if topi.item() == EOS_token:
            decoded_words.append('<EOS>')
            break
        else:
            decoded_words.append(self.output_lang.index2word[topi.item()])

        decoder_input = topi.squeeze().detach()

      return decoded_words, decoder_attentions[:di + 1]
