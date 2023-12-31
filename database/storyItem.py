import json
from types import SimpleNamespace


class StoryItem:
    """ The set of available information for each story. """

    id = None
    link = None
    title = None
    rating = None
    reading_time = None
    categories = None
    text = None
    probability = None
    category_tokens = None
    category_spans = None
    category_sentiments = None
    story_tokens = None
    story_spans = None
    story_sentiments = None
    topic = None

    def __init__(self, json_input=None):
        """ Initialize a StoryItem using the provided JSON string. """

        if json_input is not None:
            json_input = json_input.replace("\n", "").replace("\r", "")
            obj = json.loads(json_input, object_hook=lambda d: SimpleNamespace(**d))

            self.id = obj.id
            self.link = obj.link
            self.title = obj.title
            self.rating = obj.rating
            self.reading_time = obj.reading_time
            self.categories = obj.categories
            self.text = obj.text.encode("utf-8").decode("unicode-escape")

    def print(self):
        """ Print the resulting object, formatted by probability. """

        out_txt = "Title: " + str(self.title) \
                  + "\nRating: " + str(self.rating) \
                  + "\nProbability: " + str(self.probability) \
                  + "\nCategories: " + " | ".join(self.categories) \
                  + "\nTopic: " + self.topic \
                  + "\nSentiment: " + (" | ".join(self.story_sentiments)
                                       if self.story_sentiments is not None
                                       else " | ".join(self.story_sentiments)) + "\n"
        if self.probability > 70:
            print("\033[92m{}\033[00m".format(out_txt))
        elif self.probability >= 50:
            print("\033[93m{}\033[00m".format(out_txt))
        else:
            print("\033[91m{}\033[00m".format(out_txt))

    def add_tokenizer_result(self, category_tokens, category_spans, category_sentiments,
                             story_tokens, story_spans, story_sentiments):
        """ Enrich the existing object with tokens, spans and sentiments. """

        self.category_tokens = category_tokens
        self.category_spans = category_spans
        self.category_sentiments = category_sentiments
        self.story_tokens = story_tokens
        self.story_spans = story_spans
        self.story_sentiments = story_sentiments
