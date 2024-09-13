from collections import Counter
from tokenize import generate_tokens

from .types import (LanguageModel, EOS_TOKEN)
import random


class CharNGramLanguageModel(LanguageModel):

    def __init__(self, n, documents):
        self.n = n
        self.tokens = self.process_documents(documents)
        self.ngram_freq = self.generate_ngram(self.tokens, n)
        self.n_1gram_freq = self.generate_ngram(self.tokens, n - 1)

    def generate(self, prompt: str, limit: int) -> str:
        next_token = ""
        output_token_limiter = 0
        while True:
            if next_token == EOS_TOKEN or output_token_limiter >= limit:
                break

            next_token = self.generate_character(prompt)
            prompt += next_token

        return prompt

    def generate_character(self, prompt: str) -> str:
        # last n-1 characters of prompt used to predict the next char
        prefix = prompt[-(self.n - 1):]

        # possible next char based on learned documents
        next_char_choices = [ngram_chars[-1] for ngram_chars in self.ngram_freq if ngram_chars.startswith(prefix)]
        next_char_probabilities = []
        for char in next_char_choices:
            char_freq = self.ngram_freq.get(prefix + char, 0)
            prefix_freq = self.n_1gram_freq.get(prefix, 0)
            if prefix_freq == 0:
                next_char_probabilities.append(0)
            else:
                next_char_probabilities.append(char_freq / prefix_freq)

        yield random.choices(next_char_choices, next_char_probabilities)[0]

    def generate_ngram(self, tokens, n):
        assert n > 1, "gram n must be greater than 1"

        ngram_list = [tokens[i:i + n] for i in range(len(tokens) - n)]
        return Counter(ngram_list)

    # tokenize documents into char and add EOS to each document
    def process_documents(self, documents):
        assert len(documents) > 0
        tokens = []
        for doc in documents:
            tokens.extend(list(doc) + EOS_TOKEN)

        return tokens
