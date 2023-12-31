import time
from gensim.corpora.dictionary import Dictionary
from database.storyItem import StoryItem
from database.storyReader import StoryReader
from database.storyWriter import StoryWriter
from classify.tokenizer import Tokenizer


class TextProcessor:
    """ Coordinates text mining actions. """

    @staticmethod
    def mine_text(story_data: list[StoryItem], training_set=False):
        """ Mines stories for tokens, spans and sentiments, found in either the categories or the story text. """

        stories = []
        categories = []
        for sd in story_data:
            stories.append(sd.text.lower())
            categories.append((', '.join(sd.categories)).lower())

        category_tokens, category_spans, category_sentiments, story_tokens, story_spans, story_sentiments =\
            Tokenizer.extract_parts_analyze_sentiment(categories, stories)

        for i in range(len(story_data)):
            story_data[i].add_tokenizer_result(category_tokens[i], category_spans[i], category_sentiments[i],
                                               story_tokens[i], story_spans[i], story_sentiments[i])

        if training_set:
            half_processed = StoryReader.get_unprocessed(story_data)

            story_writer = StoryWriter()
            story_writer.insert_remaining_items(half_processed, story_data)

    @staticmethod
    def retrieve_filtered_dictionary(tokens, no_above, keep_n, keep_tokens=None, training_set=True):
        """ Returns a corpus and a dictionary after filtering out extremes. """

        print("Creating dictionary")
        start = time.time()
        dictionary = Dictionary(tokens)
        print("--- %s seconds ---" % (time.time() - start))

        if training_set:
            no_below = 50
            no_above = no_above
        else:
            no_below = 1
            no_above = 1

        print("Filtering extremes")
        start = time.time()
        dictionary.filter_extremes(no_below=no_below, no_above=no_above, keep_n=keep_n, keep_tokens=keep_tokens)
        print("--- %s seconds ---" % (time.time() - start))

        print("Creating corpus")
        start = time.time()
        corpus = [dictionary.doc2bow(doc) for doc in tokens]
        print("--- %s seconds ---" % (time.time() - start))

        return corpus, dictionary
