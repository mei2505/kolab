import sentencepiece as spm
import pathlib


def load_tokenizer(model: str = None):
    import sentencepiece as spm
    if model is None:
        model = str(pathlib.Path(__file__).parent.resolve() / 'prog8k.model')
    sp = spm.SentencePieceProcessor()
    sp.Load(model)

    def tokenize(s: str) -> list[str]:
        tokens = sp.EncodeAsPieces(s)
        if len(tokens) > 0:
            if tokens[0] == '▁':
                tokens.pop(0)
            else:
                tokens[0] = tokens[0][1:]
        return tokens

    return tokenize
