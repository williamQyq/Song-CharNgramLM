from abc import ABC, abstractmethod

EOS_TOKEN = 'END_OF_SEQUENCE'
TXT_DOCUMENTS = "TXT"

class LanguageModel:
    @abstractmethod
    def generate_character(self, prompt) -> str:
        """Adding the generated character to the end of the prompt"""

    @abstractmethod
    def generate(self, prompt, limit) -> str:
        """Iteratively call generate_character, until it returns the <end-of-sequence>, or reach the limit. """
