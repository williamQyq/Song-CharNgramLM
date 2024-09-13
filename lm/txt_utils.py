import os
import glob
from lm.types import (EOS_TOKEN)


class Scanner:
    def __init__(self):
        pass

    @staticmethod
    def process_documents(self, type="txt", directory_path=""):
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(directory_path)

        if type == "txt":
            return self._process_txt_documents(directory_path)
        else:
            raise NotImplementedError(type)

    def _process_txt_documents(self, directory_path):
        all_texts = []
        txt_files = glob.glob(os.path.join(directory_path, '**', '*.txt'), recursive=True)

        for file_path in txt_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    all_texts.append(file.read())
                print(f"Loaded {file_path}")
            except FileNotFoundError as e:
                print(f"Error loading {file_path}")

        return all_texts
