import sys

training_file = open(sys.argv[1], 'r')
count_of_words = {}
count_of_pos = {}
sentences_with_bigrams = []
pos_sequences = []
word_used_as_pos = {}

current_sentence = []
current_pos_sequence = []

# some needed parsing
for line in training_file:
    line = line.split("\t")
    if not len(line) < 2:
        word = line[0]
        pos = line[1].strip('\n')

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

        if word not in word_used_as_pos:
            word_used_as_pos[word] = {}
            word_used_as_pos[word][pos] = 1
        else:
            if pos not in word_used_as_pos[word]:
                word_used_as_pos[word][pos] = 1
            else:
                word_used_as_pos[word][pos] += 1

    else:
        sentences_with_bigrams.append(current_sentence)
        pos_sequences.append(current_pos_sequence)
        current_pos_sequence = []
        current_sentence = []

pos_prev_next_dict = {}

# build prior probability table
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


working_file = open(sys.argv[2])
output_file = open("output.pos", "w")

output_sentences = []
current_sentence = []

# generate sentence array from output file
for line in working_file:
    if line == '\n':
        output_sentences.append(current_sentence)
        current_sentence = []
    else:
        line = line.strip('\n')
        current_sentence.append(line)
# do naive virturbi
for sentence in output_sentences:
    output_sentence = []
    for index, word in enumerate(sentence):
        probability_array = []
        for pos_index, current_pos in enumerate(pos_prev_next_dict):
            if index == 0:
                if current_pos != "start":
                    # get probability that start goes to current_pos
                    total = 0
                    pos_after_start = 0
                    for pos in pos_prev_next_dict["start"]:
                        total += pos_prev_next_dict["start"][pos]
                    if current_pos in pos_prev_next_dict["start"]:
                        pos_after_start = pos_prev_next_dict["start"][current_pos] / float(total)
                    total = 0
                    if word in word_used_as_pos:
                        for pos in word_used_as_pos[word]:
                            total += word_used_as_pos[word][pos]
                        if current_pos in word_used_as_pos[word]:
                            probability = word_used_as_pos[word][current_pos] / float(total)
                        else:
                            probability = 0
                    else:
                        probability = 0

                    probability_array.append([current_pos, pos_after_start*probability])
            else:
                total = 0
                previous_pos = output_sentence[index-1][1]
                probability_that_pos_comes_after_prev = 0
                if previous_pos in pos_prev_next_dict:
                    for pos in pos_prev_next_dict[previous_pos]:
                        total += pos_prev_next_dict[previous_pos][pos]
                    if total == 0:
                        pos_prev_next_dict[previous_pos][current_pos] = 0
                    else:
                        if current_pos in pos_prev_next_dict[previous_pos]:
                            probability_that_pos_comes_after_prev = pos_prev_next_dict[previous_pos][current_pos] / float(total)

                total = 0;
                if word in word_used_as_pos:
                    for pos in word_used_as_pos[word]:
                        total += word_used_as_pos[word][pos]
                    if current_pos in word_used_as_pos[word]:
                        probability = word_used_as_pos[word][current_pos] / float(total)
                    else:
                        probability = 0
                else:
                    probability = 0
                probability_array.append([current_pos, probability_that_pos_comes_after_prev * probability])

        max_pos = ''
        max_count = 0
        for bigram in probability_array:
            if bigram[1] > max_count:
                max_count = bigram[1]
                max_pos = bigram[0]
        if max_pos == '':
            greatest_pos = ''
            if index != 0:
                previous_pos = output_sentence[index-1][1]
                greatest = 0
                if previous_pos in pos_prev_next_dict:
                    greatest_pos = ''
                    for pos in pos_prev_next_dict[previous_pos]:
                        if pos_prev_next_dict[previous_pos][pos] > greatest:
                            greatest = pos_prev_next_dict[previous_pos][pos]
                            greatest_pos = pos
            max_pos = greatest_pos
        if max_pos == '':
            max_pos = 'NNP'
        output_sentence.append([word, max_pos])
    for index, bigram in enumerate(output_sentence):
        word = bigram[0]
        pos = bigram[1]

        output_file.write(word + "\t" + pos + "\n")
    output_file.write("\n")
