import pymorphy2
class AnswerCorrector(object):
    morph = pymorphy2.MorphAnalyzer()

    def __init__(self):
        pass

    @classmethod
    def get_part(cls,word):
        return cls.morph.parse(word)[0].tag.POS
    @classmethod
    def correct_text(cls,answer):
        list_words = answer.split()
        i = 0
        for word in list_words:
            if (word == "ты" and cls.get_part(list_words[i + 1]) == "VERB"):
                if (list_words[i + 1].endswith("юсь")):
                    list_words[i + 1] = list_words[i + 1].replace("юсь", "ешься")
                    break
                if (list_words[i + 1].endswith("ю")):
                    list_words[i + 1] = list_words[i + 1].replace("ю", "ешь")
                    break

            i = i + 1
        return ' '.join(list_words)