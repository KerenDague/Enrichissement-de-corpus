import regex as re

def filtre_corpus():
    with open('B2data_essai.csv' ,'r') as f :
        corpus = f.readlines()
        corpus_filtre = []
        for line in corpus :
            balises = re.compile(r"<(i|n|a)>.*<\/(i|n|a)>")
            br = re.compile(r"<br \/>")
            result = balises.search(line)
            if result != None :
                line = re.sub(br, "", line)
                corpus_filtre.append(line)  
        return corpus_filtre


def write_corpus(corpus):
    with open('corpus_filtre.txt', 'w') as f :
        for line in corpus : 
            f.write(line+",")

def main():

    corpus = filtre_corpus()
    write_corpus(corpus)

if __name__ == "__main__":
    main()
             