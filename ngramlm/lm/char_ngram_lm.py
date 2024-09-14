from collections import defaultdict
from typing import List, Generator

from ngramlm.lm.txt_utils import print_generation_end_message
from ngramlm.lm.types import (LanguageModel, EOS_TOKEN)
import random


class CharNGramLanguageModel(LanguageModel):

    def __init__(self, n, documents):
        self.n = n
        self.tokens = self.process_documents(documents)
        self.ngram_freq = self.generate_ngram(self.tokens, n)
        self.n_1gram_freq = self.generate_ngram(self.tokens, n - 1)

    def generate(self, prompt: str, limit: int) -> Generator[str, None, None]:
        next_token = ""
        output_token_limiter = 0
        len_prompt = len(prompt)
        while True:
            if next_token == EOS_TOKEN:
                print_generation_end_message(f'End of the Generation.')
                break
            elif output_token_limiter >= limit:
                print_generation_end_message(f'LIMIT {limit} tokens Reached.')
                break

            next_token = self.generate_character(prompt)
            prompt += next_token
            output_token_limiter += 1

        return prompt[len_prompt:]

    def generate_character(self, prompt: str) -> str:
        # last n-1 characters of prompt used to predict the next char
        prefix = "".join(prompt[-(self.n - 1):])

        # possible next char based on learned documents
        next_char_choices = [ngram_chars[-1] for ngram_chars in self.ngram_freq if ngram_chars.startswith(prefix)]

        next_char_probabilities = []
        # probabilities for char choices
        for char in next_char_choices:
            char_freq = self.ngram_freq.get(prefix + char, 0)
            prefix_freq = self.n_1gram_freq.get(prefix, 0)
            if prefix_freq == 0:
                next_char_probabilities.append(0)
            else:
                next_char_probabilities.append(char_freq / prefix_freq)

        # no possible char can be obtained
        if sum(next_char_probabilities) != 0:
            return random.choices(next_char_choices, next_char_probabilities)[0]

        return EOS_TOKEN

    def generate_ngram(self, tokens: List[str], n):
        assert n > 1, "gram n must be greater than 1"

        ngram_list = [tokens[i:i + n] for i in range(len(tokens) - n + 1)]
        count = defaultdict(int)
        # count ngram occurrences
        for tokens in ngram_list:
            ngram = "".join(tokens)
            count[ngram] += 1
        return count

    # tokenize documents into char and add EOS to each document
    def process_documents(self, documents: List[str]) -> List[str]:
        assert len(documents) > 0
        tokens = []
        for doc in documents:
            doc_tokens = list(doc)
            doc_tokens.append(EOS_TOKEN)
            tokens.extend(doc_tokens)

        return tokens
