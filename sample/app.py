from flask import Flask, request, jsonify
# importing libraries
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import bs4 as BeautifulSoup


app = Flask(__name__)


@app.route("/api", methods=['GET'])
def hello_world():
    d = {"Query": str(request.args['Query']), "Output": "hi"}
    print(d["Query"])
    d["Output"] = str(start(d["Query"]))

    return jsonify(d["Output"])


def _create_dictionary_table(text_string) -> dict:
    # removing stop words
    # print('_create_dictionary_table called')
    stop_words = set(stopwords.words("english"))

    words = word_tokenize(text_string)

    # reducing words to their root form
    stem = PorterStemmer()

    # creating dictionary for the word frequency table
    frequency_table = dict()
    for wd in words:
        wd = stem.stem(wd)
        if wd in stop_words:
            continue
        if wd in frequency_table:
            frequency_table[wd] += 1
        else:
            frequency_table[wd] = 1

    return frequency_table


def _calculate_sentence_scores(sentences, frequency_table) -> dict:
    # algorithm for scoring a sentence by its words
    # print('_calculate_sentence_scores called')
    sentence_weight = dict()

    for sentence in sentences:
        sentence_wordcount = (len(word_tokenize(sentence)))
        sentence_wordcount_without_stop_words = 0
        for word_weight in frequency_table:
            if word_weight in sentence.lower():
                sentence_wordcount_without_stop_words += 1
                if sentence[:7] in sentence_weight:
                    sentence_weight[sentence[:7]] += frequency_table[word_weight]
                else:
                    sentence_weight[sentence[:7]] = frequency_table[word_weight]

        sentence_weight[sentence[:7]] = sentence_weight[sentence[:7]] / sentence_wordcount_without_stop_words

    return sentence_weight


def _calculate_average_score(sentence_weight) -> int:
    # calculating the average score for the sentences
    # print('_calculate_average_score called')
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]

    # getting sentence average value from source text
    average_score = int(sum_values / len(sentence_weight))

    return average_score


def _get_file_summary(sentences, sentence_weight, threshold):
    # print('_get_file_summary called')
    sentence_counter = 0
    file_summary = ''

    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= (threshold):
            file_summary += " " + sentence
            sentence_counter += 1

    return file_summary


def _run_file_summary(file):
    # print('_run_file_summary called')
    # creating a dictionary for the word frequency table
    frequency_table = _create_dictionary_table(file)

    # tokenizing the sentences
    sentences = sent_tokenize(file)

    # algorithm for scoring a sentence by its words
    sentence_scores = _calculate_sentence_scores(sentences, frequency_table)

    # getting the threshold
    threshold = _calculate_average_score(sentence_scores)

    # producing the summary
    file_summary = _get_file_summary(sentences, sentence_scores, 1.5 * threshold)

    # print(file_summary)

    # fh = open('Summarize.txt', 'w')
    # fh.write(file_summary)
    # fh.close()
    return file_summary


def start(content):
    # parsing the file content and storing in a variable
    file_parsed = BeautifulSoup.BeautifulSoup(content, 'lxml')

    # returning <p> tags.
    paragraphs = file_parsed.find_all('p')

    file_content = ''

    # looping through the paragraphs and adding them to the variable
    for para in paragraphs:
        file_content = file_content + para.text

    return _run_file_summary(file_content)


if __name__ == '__main__':
    app.run()














