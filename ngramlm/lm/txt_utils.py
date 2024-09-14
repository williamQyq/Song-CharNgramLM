import os
import glob


def process_documents(data_dir, type="txt"):
    if not os.path.isdir(data_dir):
        raise NotADirectoryError(data_dir)

    if type == "txt":
        return _process_txt_documents(data_dir)
    else:
        raise NotImplementedError(type)


def _process_txt_documents(data_dir):
    all_texts = []
    txt_files = glob.glob(os.path.join(data_dir, '**', '*.txt'), recursive=True)

    for file_path in txt_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                all_texts.append(file.read())
            print(f"Loaded {file_path}")
        except FileNotFoundError as e:
            print(f"Error loading {file_path}")

    return all_texts


def print_documents(documents):
    dash = '-'

    for idx, document in enumerate(documents):
        print(f"{dash *50}")
        print(f'Document{idx + 1}:')
        print(dash * 50)
        for i in range(0, len(document), 78):
            print(f'{document[i:i + 78]:78}')

        print(dash * 50)
        print()

def print_generation_end_message(message:str):
    """Print formatted generation message."""
    print('-' * 50)
    print(message)
    print('-' * 50)