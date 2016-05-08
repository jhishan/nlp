training_file = open("wordFiles/WSJ_02-21.pos", 'r')
count_of_words = {}
count_of_pos = {}
sentences_with_bigrams = []
pos_sequences = []

current_sentence = []
current_pos_sequence = []
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
        current_pos_sequence.append(pos)
    else:
        sentences_with_bigrams.append(current_sentence)
        pos_sequences.append(current_pos_sequence)
        current_pos_sequence = []
        current_sentence = []

pos_prev_next_dict = {}

for pos_sentence in pos_sequences:
    for index, current_pos in enumerate(pos_sentence):
        if index == 0:
            if "start" not in pos_prev_next_dict:
                pos_prev_next_dict["start"] = {}
                pos_prev_next_dict["start"][current_pos] = 1
            else:
                if current_pos not in pos_prev_next_dict["start"]:
                    pos_prev_next_dict["start"][current_pos] = 1
                else:
                    pos_prev_next_dict["start"][current_pos] += 1

        if current_pos not in pos_prev_next_dict:
            pos_prev_next_dict[current_pos] = {}
            if index + 1 == len(pos_sentence):
                # means we are at the last word
                if "end" in pos_prev_next_dict[current_pos]:
                    pos_prev_next_dict[current_pos]["end"] += 1
                else:
                    pos_prev_next_dict[current_pos]["end"] = 1
            else:
                next_pos = pos_sentence[index+1]
                if next_pos not in pos_prev_next_dict[current_pos]:
                    pos_prev_next_dict[current_pos][next_pos] = 1
                else:
                    pos_prev_next_dict[current_pos][next_pos] += 1
        else:
            if index + 1 == len(pos_sentence):
                # we are at end of sentence
                if "end" not in pos_prev_next_dict[current_pos]:
                    pos_prev_next_dict[current_pos]["end"] = 1
                else:
                    pos_prev_next_dict[current_pos]["end"] += 1
            else:
                # not end of word
                next_pos = pos_sentence[index+1]
                if next_pos not in pos_prev_next_dict[current_pos]:
                    pos_prev_next_dict[current_pos][next_pos] = 1
                else:
                    pos_prev_next_dict[current_pos][next_pos] += 1

#TODO READ IN OUTPUT FILE