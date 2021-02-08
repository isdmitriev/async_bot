import re
import random
from ELIZA.answers_corrector import AnswerCorrector

# reflections = {
#     "am": "are",
#     "was": "were",
#     "i": "you",
#     "я":"ты",
#     "i'd": "you would",
#     "i've": "you have",
#     "i'll": "you will",
#     "my": "your",
#     "are": "am",
#     "you've": "I have",
#     "you'll": "I will",
#     "your": "my",
#     "yours": "mine",
#     "you": "me",
#     "me": "you"
# }

reflections = {

    "был": "были",
    "твоих":"моих",
    "твоем":"моем",
    "я": "ты",
    "я бы": "ты бы",
    "мне бы": "ты бы",
    "имею": "имеешь",
    "я буду": "ты будешь",
    "мой": "твой",
    "мою": "твою",

    "я имею": "у тебя есть",
    "ты будешь": "я буду",
    "твой": "мой",
    "твои": "мои",
    "тебе": "мне",
    "мне": "тебе",
    "меня": "тебя",
    "ты": "я",
    "тебя": "меня",
    "моей": "твоей"
}

psychobabble = [

    [r'Мне нужно(.*)',
     ["Зачем тебе {0} ?",
      "Это действительно поможет тебе  {0}?",
      "Ты уверен, что тебе нужно {0}?"]],

    [r'Мне нужна (.*)',
     ["Зачем тебе {0} ?",
      "Ты уверен, что тебе нужна {0}?"]],

    [r'Я нуждаюсь  (.*)',
     [
         "Ты уверен, что ты нуждаешься  {0}?"]],

    [r'Почему ты не можешь (.*)\?',
     ["Ты правда думаешь, что я не могу {0}?",
      "Возможно, в конце концов я буду {0}.",
      "Ты действительно хочешь, чтобы я {0}?"]],

    [r'Почему я не могу(.*)\?',
     ["Как ты думаешь, ты должен уметь {0}?",
      "Если бы ты мог {0}, Чтобы ты делал?",
      " Я не знаю - почему ты не можешь {0}",
      "Ты действительно пробовал?"]],

    [r'Я не могу (.*)',
     ["Откуда ты знаешь, что не можешь {0}?",
      "Возможно ты мог бы {0} если бы ты попробовал.",
      "Что тебе нужно, чтобы {0}?"]],

    [r'Могу ли я ([^\?]*)\?',
     ["Возможно ты не хочешь {0}.",
      "Вы хотите иметь возможность {0}?",
      "Если бы ты мог {0},что тогда?"]],

    [r'Я (.*)\?',
     [
         "Тебе нравится что ты {0}?",
         "Почему ты говоришь мне, что ты {0}?",
         "Как ты думаешь, почему ты {0}?"]],

    [r'Что (.*)',
     ["Почему ты спрашиваешь?",
      "Как ответ на это поможет тебе?",
      "Что вы думаешь?"]],

    [r'Как (.*)?',
     ["Как ты думаешь?",
      "Возможно, вы ответите на свой вопрос.",
      "Что ты действительно спрашиваешь?"]],

    [r'Потому что(.*)',
     ["Это настоящая причина?",
      "Какие еще причины приходят на ум?",
      "Эта причина применима к чему-либо еще?",
      "Если {0},что еще должно быть правдой?"]],

    [r'(.*) извините (.*)',
     ["Очень часто извинения не нужны",
      "Какие чувства у вас возникают, когда вы извиняетесь?"]],

    [r'Привет(.*)',
     ["Привет,я рада что вы зашли сегодня",
      "Привет,как ты сегодня?",
      "Привет,как ты себя чувствуешь сегодня?"]],

    [r'Я думаю (.*)',
     ["Ты сомневаешься в том что {0}?",
      "Ты действительно так думаешь?",
      "Но ты не уверен в том что {0}?"]],
    [r'(.*) друг (.*)',
     ["Расскажи мне больше о своих друзьях",
      "Что приходит на ум, когда ты думаешь о друге?",
      "Почему бы тебе не рассказать мне о друге детства?"]],

    [r'Да',
     ["ты, кажется, совершенно уверен",
      "Хорошо, но не мог бы ты немного уточнить?"]],

    [r'(.*) компьютер (.*)',
     ["Ты правда говоришь обо мне?",
      "Странно разговаривать с компьютером?",
      "Какие чувства вызывают у вас компьютеры?",
      "Вы чувствуете угрозу со стороны компьютеров?"]],

    [r'Это (.*)\?',
     ["Ты думаешь это {0}?",
      "Возможно это {0} -- Как ты думаешь?",
      "Если бы это было {0}, Чтобы ты делал?",
      "Вполне может быть, что {0}."]],

    [r'Это (.*)',
     ["Вы кажетесь очень уверенным",
      "Если бы я сказал вам, что, вероятно, это не  {0},что бы вы чувствовали ?"]],

    [r'Ты можешь (.*)\?',
     ["Почему ты думаешь, что я не могу {0}?",
      "Если бы я мог {0},и что ?",
      "Почему ты спрашиваешь, могу ли я {0}?"]],

    [r'Ты (.*)\?',
     ["Почему это важно, если я {0} ?",
      "Ты бы предпочел, если бы я не был {0} ?",
      "Возможно, ты веришь, что я {0}.",
      "я может быть {0} Как ты думаешь?"]],

    [r'Ты ([^\?]*)\??',
     ["Мы должны обсуждать тебя, а не меня.",
      "Почему ты так говоришь обо мне?",
      "Почему вас волнует, {0} ли я?"]],

    [r'Я не буду (.*)',
     ["Не правда ли ты не будешь {0}?",
      "Почему ты не будешь {0}?",
      "Ты хочешь{0}?"]],

    [r'Я чувствую (.*)',
     ["Хорошо, расскажи мне подробнее об этих чувствах",
      "Ты часто чувствуешь {0}?",
      "Когда ты обычно чувствуешь {0}?",
      "Когда ты чувствуешь {0},что ты делаешь?"]],

    [r'Я имею (.*)',
     ["Почему ты говоришь мне, что ты {0}?",
      "ты правда {0}?",
      "Теперь когда у тебя есть {0},что ты будешь делать дальше?"]],

    [r'Я бы (.*)',
     ["Не мог бы ты объяснить, почему ты бы {0}?",
      "Почему тебе бы{0}?",
      "Кто еще знает, что ты бы {0}?"]],

    [r'Это (.*)',
     ["Как ты думаешь, есть {0}?",
      "Вероятно, что есть {0}.",
      "Хочешь, чтобы там было {0}?"]],

    [r'Есть ли (.*)?',
     ["Как ты думаешь, есть {0}?",
      "Вероятно, что есть {0}.",
      "Ты бы хотел, чтобы там было {0}?"]],

    [r'Мой (.*)',
     ["Понятно твой {0}.",

      "Почему вы говорите, что ваш {0}?",
      "Когда у тебя {0},как ты себя чувствуешь?"]],



    [r'Зачем (.*)',
     ["Почему вы не называете мне причину, по которой {0}?",
      "Как вы думаете, почему {0}?"]],

    [r'Я хочу (.*)',
     ["Что для вас будет значить, если вы получите {0}?",
      "Почему ты хочешь{0}?",

      "Что бы ты сделал, если бы получил {0}?",
      "Если у тебя есть {0},тогда что бы ты делал?"]],

    [r'(.*) мама(.*)',
     ["Расскажи мне больше о своей матери.",
      "Какие у вас были отношения с матерью?",
      "Как ты относишься к своей матери?",
      "Как это соотносится с вашими сегодняшними чувствами?",
      "Важны хорошие семейные отношения."]],

    [r'(.*) папа(.*)',
     ["Расскажи мне больше о своем отце",
      "Как тебя чувствовал твой отец?",
      "Как ты относишься к своему отцу?",
      "Связаны ли ваши отношения с отцом с вашими сегодняшними чувствами?",
      "У вас есть проблемы с проявлением привязанности к семье?"]],

    [r'(.*) ребенок (.*)',
     ["Были ли у вас в детстве близкие друзья?",
      "Какое ваше любимое воспоминание из детства?",
      "Вы помните какие-нибудь сны или кошмары из детства?",
      "Другие дети иногда дразнили вас?",
      "Как вы думаете, как ваши детские переживания связаны с вашими сегодняшними чувствами?"]],

    [r'(.*)\?',
     ["Почему ты это спросил?",
      "Пожалуйста, подумайте, можете ли вы ответить на свой вопрос.",
      "Возможно, ответ кроется в тебе самом?",
      "Почему ты мне не скажешь?"]],

    [r'Я (.*)',
     ["Ты пришел ко мне, потому что ты {0}?",
      "как долго ты {0}?",
      "Как ты относишься к тому, что ты {0}?"]],

    [r'выход',
     ["Спасибо, что поговорил со мной.",
      "Пока",
      "Спасибо, это будет 150 долларов. Хорошего дня!"]],

    [r'(.*)',
     ["Расскажи, пожалуйста, подробнее",
      "Давай немного сменим фокус ... Расскажи мне о своей семье.",
      "Вы можете подробнее рассказать об этом?",
      "Почему вы так говорите {0}?",
      "Я вижу",
      "очень интересно",
      "{0}.",
      "Понимаю. И что это вам говорит?",
      "Как ты себя чувствуешь?",
      "Что вы чувствуете, когда говорите это?"]]]


def reflect(fragment):
    tokens = fragment.lower().split()
    print(tokens)
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)


def analyze(statement):
    for pattern, responses in psychobabble:
        match = re.match(pattern, statement.rstrip(".!"))
        if match:
            response = random.choice(responses)
            result = AnswerCorrector.correct_text(response.format(*[reflect(g) for g in match.groups()]))
            # 
            return result
