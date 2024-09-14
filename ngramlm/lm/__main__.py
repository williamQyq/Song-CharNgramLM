import os
from ngramlm.lm import CharNGramLanguageModel
from ngramlm.lm.txt_utils import process_documents, print_documents
from pathlib import Path
from ngramlm.config.defaults import (DATA_DIR,K)

def resolve_dataset_path(relative_path: str) -> Path:
    # Start from the current file's directory
    current_dir = Path(__file__).resolve().parent

    # Traverse upwards until you reach the main package directory
    for parent in current_dir.parents:
        # Check for an indicator that we've reached the main package (like a setup.py or .git folder)
        if (parent / 'setup.py').exists() or (parent / '.git').exists():
            # Construct the dataset path relative to the main package directory
            dataset_path = parent / relative_path
            if dataset_path.exists():
                return dataset_path
            else:
                raise FileNotFoundError(f"Dataset not found at {dataset_path}")

    # If we reach here, we didn't find a main package directory
    raise FileNotFoundError(f"Main package directory not found starting from {current_dir}")


# Example usage:
relative_path = DATA_DIR
try:
    data_dir = resolve_dataset_path(relative_path)
    print(f"Dataset directory found: {data_dir}")
except FileNotFoundError as e:
    print(e)

if __name__ == '__main__':
    data_dir = resolve_dataset_path("dataset/Olivia_Rodrigo_Songs")
    #retrieve documents from dir
    documents = process_documents(data_dir)

    model = CharNGramLanguageModel(K, documents)

    prompt = "What songs do you have"
    #generate response based on prompt
    response = model.generate(prompt, limit=5000)

    print(response)
