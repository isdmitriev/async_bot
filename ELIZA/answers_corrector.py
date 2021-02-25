import pymorphy2


class AnswerCorrector():
    morph = pymorphy2.MorphAnalyzer()

    @classmethod
    def correct_word(cls, word, sufix, new_sufix):
        last_index = word.rindex(sufix)
        new_word = word[:last_index] + new_sufix
        return new_word

    @classmethod
    def remove_word_prefix(cls, word, prefix):
        len_prefix = len(prefix)
        return word[len_prefix:]

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

        for i, word in enumerate(list_words):
            pos, tense = cls.get_part_and_tense(word)

            if ((word == "ты" and i + 1 < amount) and (cls.get_part(list_words[i + 1]) == "VERB")):

                if (list_words[i + 1].endswith("люсь")):
                    list_words[i + 1] = cls.correct_word(list_words[i + 1], "люсь", "ишься")

                    continue

                if (list_words[i + 1].endswith("юсь")):
                    list_words[i + 1] = cls.correct_word(list_words[i + 1], "юсь", "ешься")

                    continue
                if (list_words[i + 1].endswith("ю")):
                    list_words[i + 1] = cls.correct_word(list_words[i + 1], "ю", "ешь")

                    continue
                if (list_words[i + 1].endswith("юсь")):
                    list_words[i + 1] = cls.correct_word(list_words[i + 1], "юсь", "ешься")

                    continue

            if ((word == "я" and i + 1 < amount) and (cls.get_part(list_words[i + 1]) == "VERB")):

                if (list_words[i + 1].endswith("ешься")):
                    list_words[i + 1] = cls.correct_word(list_words[i + 1], "ешься", "юсь")

                    continue
                if (list_words[i + 1].endswith("ешь")):
                    list_words[i + 1] = cls.correct_word(list_words[i + 1], "ешь", "ю")

                    continue
                if (list_words[i + 1].endswith("ть")):
                    list_words[i + 1] = cls.correct_word(list_words[i + 1], "ть", "л")

                    continue
            if ((word == "не") and (i + 1 < amount) and (cls.get_part(list_words[i + 1]) == "VERB")):

                if (list_words[i + 1].endswith("ю")):
                    list_words[i + 1] = cls.correct_word(list_words[i + 1], "ю", "ешь")

                    continue

            if ((pos == "ADVB" and i + 1 < amount) and (cls.get_part(list_words[i + 1]) == "VERB")):

                pos, tense_two = cls.get_part_and_tense(list_words[i + 1])

                word_value = list_words[i + 1]

                if (tense_two == "pres"):
                    if (list_words[i + 1].endswith("люсь")):
                        list_words[i + 1] = cls.correct_word(list_words[i + 1], "люсь", "ишься")

                        continue

                    if (list_words[i + 1].endswith("юсь")):
                        list_words[i + 1] = cls.correct_word(list_words[i + 1], "юсь", "ешься")

                        continue
                    if (word_value.endswith("ю")):
                        list_words[i + 1] = cls.correct_word(list_words[i + 1], "ю", "ешь")

                        continue
                    if (word_value.endswith("мся")):
                        list_words[i + 1] = cls.correct_word(list_words[i + 1], "мся", "тесь")

                        continue

            if ((pos == "VERB" and i + 1 < amount) and (
                    cls.get_part(list_words[i + 1]) == "INFN" or cls.get_part(list_words[i + 1]) == "VERB")):

                if (tense == "pres"):
                    if (word.endswith("юсь")):
                        list_words[i + 1] = cls.correct_word(list_words[i + 1], "юсь", "ешься")

                        continue
                    if (word.endswith("ю")):
                        list_words[i] = cls.correct_word(list_words[i], "ю", "ешь")

                        continue
            if ((word == "я" and i + 1 < amount) and (list_words[i - 1] == "чтобы") and (
                    cls.get_part(list_words[i + 1]) == "INFN")):
                pos, tense = cls.get_part_and_tense(list_words[i + 1])

                if (list_words[i + 1].endswith("ть")):
                    list_words[i + 1] = cls.correct_word(list_words[i + 1], "ть", "л")

                    continue

        return ' '.join(list_words)
