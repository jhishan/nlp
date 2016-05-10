import math
queries = open('cran/cran.qry', 'r')


'''
code given in class
'''
def cos_sim(vect1, vect2):
    numerator = 0
    sum_of_squares1 = 0
    sum_of_squares2 = 0
    length = len(vect1)
    length2 = len(vect2)
    ans = 10

    try:
        for index in range(len(vect1)):
            numerator = numerator + vect1[index]*vect2[index]
            sum_of_squares1 += math.pow(vect1[index], 2)
            sum_of_squares2 += math.pow(vect2[index],2)
        ans = numerator / (sum_of_squares1 * sum_of_squares2)
    except IndexError:
        ans = numerator/(sum_of_squares1*sum_of_squares2)

    return ans

closed = ['a', 'the', 'an', 'and', 'or', 'but', 'about', 'above', 'after', 'along', 'amid', 'among', \
                           'as', 'at', 'by', 'for', 'from', 'in', 'into', 'like', 'minus', 'near', 'of', 'off', 'on', \
                           'onto', 'out', 'over', 'past', 'per', 'plus', 'since', 'till', 'to', 'under', 'until', 'up', \
                           'via', 'vs', 'with', 'that', 'can', 'cannot', 'could', 'may', 'might', 'must', \
                           'need', 'ought', 'shall', 'should', 'will', 'would', 'have', 'had', 'has', 'having', 'be', \
                           'is', 'am', 'are', 'was', 'were', 'being', 'been', 'get', 'gets', 'got', 'gotten', \
                           'getting', 'seem', 'seeming', 'seems', 'seemed', \
                           'enough', 'both', 'all', 'your' 'those', 'this', 'these', \
                           'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my', \
                           'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another', \
                           'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not', \
                           'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more', \
                           'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite', \
                           'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such', \
                           'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which', \
                           'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', \
                           'anything', 'anytime' 'anywhere', 'everybody', 'everyday', \
                           'everyone', 'everyplace', 'everything' 'everywhere', 'whatever', \
                           'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he', \
                           'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their', 'theirs', \
                           'you', 'your', 'yours', 'me', 'my', 'mine', 'I', 'we', 'us', 'much', 'and/or'
                           ]

dict_of_queries = {}

for q in queries:
    if q.startswith('.I'):
        id = q.split(" ")[1].rstrip('\r\n')
        dict_of_queries[id] = []
        last_id_set = id
        processing = False
    if processing:
        orig_strip = (q.rstrip('\r\n')).split(" ")
        new_strip = []
        for item in orig_strip:
            if item not in closed:
                new_strip.append(item)
        dict_of_queries[last_id_set] = dict_of_queries[last_id_set] + new_strip


    if q.startswith('.W'):
        processing = True
word_count_in_query_dict = {}
for q in dict_of_queries:
    word_count_in_query_dict[q] = {}
    for word in dict_of_queries[q]:
        word_count_in_query_dict[q][word] = dict_of_queries[q].count(word)

word_dict = {}
for id in dict_of_queries:
    for word in dict_of_queries[id]:
        if word not in word_dict:
            if word != '':
                word_dict[word] = True

word_query_count = {}

for word in word_dict:
    count = 0
    for id in dict_of_queries:
        if dict_of_queries[id].count(word) > 0:
            count += 1
    word_query_count[word] = count

tfidf_dict = {}

for query_id in dict_of_queries:
    tfidf_dict[query_id] = []
    for word in dict_of_queries[query_id]:
        # TODO calculate TFIDF OF EACH WORD AND APPEND TO ARRAY
        # TF(t) = (Number of times term t appears in a query) / (Total number of terms in the query).
        # IDF(t) = log_e(Total number of queries / Number of queries with term t in it).
        # multiply both for tfidf score
        if word != '':
            number_of_times_word_appears_in_query = word_count_in_query_dict[query_id][word]
            total_number_of_terms_in_the_query = len(dict_of_queries[query_id])
            tf_score = number_of_times_word_appears_in_query / float(total_number_of_terms_in_the_query)

            total_number_of_queries = len(dict_of_queries.keys())
            number_of_queries_with_word_in_it = word_query_count[word]
            idf_score = math.log(total_number_of_queries/float(number_of_queries_with_word_in_it))
            tf_idf_score = tf_score * idf_score
            tfidf_dict[query_id].append(tf_idf_score)

dict_of_abstract_queries = {}
abstract_queries = open('cran/cran.all.1400', 'r')

for q in abstract_queries:
    if q.startswith('.I'):
        id = q.split(" ")[1].rstrip('\r\n')
        dict_of_abstract_queries[id] = []
        last_id_set = id
        processing = False
    if q.startswith('.A'):
        processing = False
    if q.startswith('.B'):
        processing = False
    if processing:
        orig_set = (q.rstrip('\r\n')).split(" ")
        new_set = []
        for item in orig_set:
            if item not in closed:
                new_set.append(item)
        dict_of_abstract_queries[last_id_set] = dict_of_abstract_queries[last_id_set] + new_set
    if q.startswith('.W'):
        processing = True
    if q.startswith('.T'):
        processing = True


word_count_in_query_dict_abstract = {}
for q in dict_of_abstract_queries:
    word_count_in_query_dict_abstract[q] = {}
    for word in dict_of_abstract_queries[q]:
        word_count_in_query_dict_abstract[q][word] = dict_of_abstract_queries[q].count(word)

word_dict_abstract = {}
for id in dict_of_abstract_queries:
    for word in dict_of_abstract_queries[id]:
        if word not in word_dict_abstract:
            if word != '':
                word_dict_abstract[word] = True

word_query_count_abstract = {}

for word in word_dict_abstract:
    count = 0
    for id in dict_of_abstract_queries:
        if dict_of_abstract_queries[id].count(word) > 0:
            count += 1
    word_query_count_abstract[word] = count

tfidf_dict_abstract = {}

for query_id in dict_of_abstract_queries:
    tfidf_dict_abstract[query_id] = []
    for word in dict_of_abstract_queries[query_id]:
        # TODO calculate TFIDF OF EACH WORD AND APPEND TO ARRAY
        # TF(t) = (Number of times term t appears in a query) / (Total number of terms in the query).
        # IDF(t) = log_e(Total number of queries / Number of queries with term t in it).
        # multiply both for tfidf score
        if word != '':
            number_of_times_word_appears_in_query = word_count_in_query_dict_abstract[query_id][word]
            total_number_of_terms_in_the_query = len(dict_of_abstract_queries[query_id])
            tf_score = number_of_times_word_appears_in_query / float(total_number_of_terms_in_the_query)

            total_number_of_queries = len(dict_of_abstract_queries.keys())
            number_of_queries_with_word_in_it = word_query_count_abstract[word]
            idf_score = math.log(total_number_of_queries/float(number_of_queries_with_word_in_it))
            tf_idf_score = tf_score * idf_score
            tfidf_dict_abstract[query_id].append(tf_idf_score)



#tfidf_dict
query_vector_final = []

for key in tfidf_dict:
    tfidf_sentence = tfidf_dict[key]
    query_vector_final.append(tfidf_sentence)

abstract_vector_final = []

for key in tfidf_dict_abstract:
    tfidf_sentence = tfidf_dict_abstract[key]
    abstract_vector_final.append([])
    abstract_vector_final[-1].append(tfidf_sentence)


final_vector = []
q_index = 0
for q in query_vector_final:
    final_vector.append([])
    a_index = 0

    for index, a in enumerate(abstract_vector_final[q_index][a_index]):
        values = []
        values.append(q_index)
        values.append(index)
        # print q
        # print a
        # break
        if type(q) == float:
            new_q= []
            new_q.append(q)
            q = new_q
        if type(a) == float:
            new_q = []
            new_q.append(a)
            a = new_q
        cosine_sim = cos_sim(q, a)
        values.append(cosine_sim)
        a_index+=1

        if cosine_sim != 0:
            final_vector[-1].append(values)

    q_index+=1

final_output_array = []
countof = len(final_vector)
for index,values in enumerate(final_vector):
    values.sort(key=lambda x: x[2])
    values.reverse()

    final_output_array.append(values)

output_file = open("output.txt", "w")

for values in final_output_array:
    for group in values:
        first = str(group[0] + 1)
        second = str(group[1] + 1)
        third = str(group[2])
        output_file.write(first +' '+second+ ' ' +third + '\n')