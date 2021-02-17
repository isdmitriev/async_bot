import pymorphy2


class AnswerCorrector():
    morph = pymorphy2.MorphAnalyzer()

    @classmethod
    def get_part(cls, word):
        return cls.morph.parse(word)[0].tag.POS

    @classmethod
    def get_part_and_tense(cls, word):
        return (cls.morph.parse(word)[0].tag.POS, cls.morph.parse(word)[0].tag.tense)

    @classmethod
    def correct_text(cls, answer):

        list_words = answer.split()
        amount = len(list_words)
        i = 0
        for i, word in enumerate(list_words):
            pos, tense = cls.get_part_and_tense(word)

            if ((word == "ты" and i + 1 < amount) and (cls.get_part(list_words[i + 1]) == "VERB")):

                if (list_words[i + 1].endswith("люсь")):
                    list_words[i + 1] = list_words[i + 1].replace("люсь", "ишься")

                    continue

                if (list_words[i + 1].endswith("юсь")):
                    list_words[i + 1] = list_words[i + 1].replace("юсь", "ешься")

                    continue
                if (list_words[i + 1].endswith("ю")):
                    list_words[i + 1] = list_words[i + 1].replace("ю", "ешь")

                    continue
                if (list_words[i + 1].endswith("юсь")):
                    list_words[i + 1] = list_words[i + 1].replace("юсь", "ешься")

                    continue

            if ((word == "я" and i + 1 < amount) and (cls.get_part(list_words[i + 1]) == "VERB")):

                if (list_words[i + 1].endswith("ешься")):
                    list_words[i + 1] = list_words[i + 1].replace("ешься", "юсь")

                    continue
                if (list_words[i + 1].endswith("ешь")):
                    list_words[i + 1] = list_words[i + 1].replace("ешь", "ю")

                    continue
                if (list_words[i + 1].endswith("ть")):
                    list_words[i + 1] = list_words[i + 1].replace("ть", "л")

                    continue

            if ((pos == "ADVB" and i + 1 < amount) and (cls.get_part(list_words[i + 1]) == "VERB")):

                pos, tense_two = cls.get_part_and_tense(list_words[i + 1])

                word_value = list_words[i + 1]

                if (tense_two == "pres"):
                    if (list_words[i + 1].endswith("люсь")):
                        list_words[i + 1] = list_words[i + 1].replace("люсь", "ишься")

                        continue

                    if (list_words[i + 1].endswith("юсь")):
                        list_words[i + 1] = list_words[i + 1].replace("юсь", "ешься")

                        continue
                    if (word_value.endswith("ю")):
                        list_words[i + 1] = list_words[i + 1].replace("ю", "ешь")

                        continue
                    if (word_value.endswith("мся")):
                        list_words[i + 1] = list_words[i + 1].replace("мся", "тесь")

                        continue

            if ((pos == "VERB" and i + 1 < amount) and (
                    cls.get_part(list_words[i + 1]) == "INFN" or cls.get_part(list_words[i + 1]) == "VERB")):

                if (tense == "pres"):
                    if (word.endswith("юсь")):
                        list_words[i] = list_words[i].replace("юсь", "ешься")

                        continue
                    if (word.endswith("ю")):
                        list_words[i] = list_words[i].replace("ю", "ешь")

                        continue
            if ((word == "я" and i + 1 < amount) and (list_words[i - 1] == "чтобы") and (
                    cls.get_part(list_words[i + 1]) == "INFN")):
                pos, tense = cls.get_part_and_tense(list_words[i + 1])

                if (list_words[i + 1].endswith("ть")):
                    list_words[i + 1] = list_words[i + 1].replace("ть", "л")

                    continue

        return ' '.join(list_words)
