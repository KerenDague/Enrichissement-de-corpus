import regex as re
import csv 

def filtre_corpus():
    with open('../B2_final.csv' ,'r') as f :
        corpus = f.readlines()
        corpus_filtre = []
        for line in corpus :
            balises = re.compile(r".?(<(i|n|a)>.*<\/(i|n|a)>).?")
            br = re.compile(r"<br \/>")
            result = balises.search(line)
            if result != None :
                line = re.sub(br, "", line)
                line = re.sub(balises, r' \1 ', line )
                corpus_filtre.append(line)  
        return corpus_filtre


def write_corpus(corpus):
    
    with open('corpus_filtre.csv', 'w') as f :
        writer = csv.writer(f)
        header = ["Réponse au test"]
        writer.writerow(header)
        for line in corpus : 
            data = []
            data.append(line)
            writer.writerow(data)

def main():

    corpus = filtre_corpus()
    write_corpus(corpus)

if __name__ == "__main__":
    main()
             