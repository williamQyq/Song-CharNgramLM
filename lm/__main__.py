from lm.char_ngram_lm import CharNGramLanguageModel
from lm.txt_utils import Scanner

if __name__ == "__main__":
    training_path = "../dataset/Olivia_Rodrigo_Songs"
    #read documents for training
    documents = Scanner.process_documents(training_path)
    print(f'Documents:/n{documents}')
    # model = CharNGramLanguageModel(n=3, documents=documents)
    #
    # prompt= "What songs do you have?"
    # model.generate(prompt,limit=5000)