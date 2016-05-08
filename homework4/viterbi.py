training_file = open("wordFiles/WSJ_02-21.pos", 'r')
count_of_words = {}
count_of_pos = {}
sentences_with_bigrams = []

current_sentence = []
for line in training_file:
    line = line.split("\t")
    if not len(line) < 2:
        word = line[0]
        pos = line[1].strip('\n')

        # TODO add to sentence with bigrams
        if word in count_of_words:
            count_of_words[word] += 1
        else:
            count_of_words[word] = 1

        if pos in count_of_pos:
            count_of_pos[pos] += 1
        else:
            count_of_pos[pos] = 1
        current_sentence.append([word, pos])
    else:
        sentences_with_bigrams.append(current_sentence)
        current_sentence = []

print sentences_with_bigrams[0]