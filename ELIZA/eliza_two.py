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
    "i": "you",
    "я": "ты",
    "я бы": "ты бы",
    "мне бы": "ты бы",
    "имею": "имеешь",
    "я буду": "ты будешь",
    "мой": "твой",
    "мою":"твою",

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
    [r'I need (.*)',
     ["Why do you need {0}?",
      "Would it really help you to get {0}?",
      "Are you sure you need {0}?"]],
    [r'Мне нужно(.*)',
     ["Зачем тебе {0} ?",
      "Это действительно поможет тебе  {0}?",
      "Ты уверен, что тебе нужно {0}?"]],

    [r'Мне нужна (.*)',
     ["Зачем тебе {0} ?",
      "Ты уверен, что тебе нужна {0}?"]],

    [r'Я нуждаюсь  (.*)',
     [
         "Ты уверен, что ты нуждаешься в {0}?"]],

    [r'Почему ты не можешь (.*)\?',
     ["Ты правда думаешь, что я не могу {0}?",
      "Возможно, в конце концов я буду {0}.",
      "Ты действительно хочешь, чтобы я {0}?"]],

    [r'Why don\'?t you ([^\?]*)\??',
     ["Do you really think I don't {0}?",
      "Perhaps eventually I will {0}.",
      "Do you really want me to {0}?"]],

    [r'Почему я не могу(.*)\?',
     ["Как ты думаешь, ты должен уметь {0}?",
      "Если бы ты мог {0}, Чтобы ты делал?",
      " Я не знаю - почему ты не можешь {0}",
      "Ты действительно пробовал?"]],

    [r'Why can\'?t I ([^\?]*)\??',
     ["Do you think you should be able to {0}?",
      "If you could {0}, what would you do?",
      "I don't know -- why can't you {0}?",
      "Have you really tried?"]],

    [r'Я не могу (.*)',
     ["Откуда ты знаешь, что не можешь {0}?",
      "Возможно ты мог бы {0} если бы ты попробовал.",
      "Что тебе нужно, чтобы {0}?"]],

    [r'I can\'?t (.*)',
     ["How do you know you can't {0}?",
      "Perhaps you could {0} if you tried.",
      "What would it take for you to {0}?"]],

    [r'Могу ли я ([^\?]*)\?',
     ["Возможно ты не хочешь {0}.",
      "Вы хотите иметь возможность {0}?",
      "Если бы ты мог {0},что тогда?"]],

    [r'Can I ([^\?]*)\??',
     ["Perhaps you don't want to {0}.",
      "Do you want to be able to {0}?",
      "Если бы ты мог{0}, would you"]],

    # [r'Я (.*)',
    #      ["Ты пришел ко мне, потому что ты {0}?",
    #       "как долго ты {0}?",
    #       "Как ты относишься к тому, что ты {0}?"]],

    [r'I am (.*)',
     ["Did you come to me because you are {0}?",
      "How long have you been {0}?",
      "How do you feel about being {0}?"]],

    [r'I\'?m (.*)',
     ["How does being {0} make you feel?",
      "Do you enjoy being {0}?",
      "Why do you tell me you're {0}?",
      "Why do you think you're {0}?"]],

    # [r'Ты\'? (.*)?',
    #      ["Почему это так важно {0}?",
    #       "Вы бы предпочли, если бы я не был{0}?",
    #       "Возможно, вы верите, что я{0}.",
    #       "я может быть{0} --Как вы думаете ?"]],

    [r'Are you ([^\?]*)\??',
     ["Why does it matter whether I am {0}?",
      "Would you prefer it if I were not {0}?",
      "Perhaps you believe I am {0}.",
      "I may be {0} -- what do you think?"]],

    [r'Что (.*)',
     ["Почему ты спрашиваешь?",
      "Как ответ на это поможет тебе?",
      "Что вы думаешь?"]],

    [r'What (.*)',
     ["Why do you ask?",
      "How would an answer to that help you?",
      "What do you think?"]],

    [r'Как (.*)?',
     ["Как ты думаешь?",
      "Возможно, вы ответите на свой вопрос.",
      "Что ты действительно спрашиваешь?"]],

    [r'How (.*)',
     ["How do you suppose?",
      "Perhaps you can answer your own question.",
      "Что ты действительно спрашиваешь?"]],

    [r'Потому что(.*)',
     ["Это настоящая причина?",
      "Какие еще причины приходят на ум?",
      "Эта причина применима к чему-либо еще?",
      "Если {0},что еще должно быть правдой?"]],

    [r'Because (.*)',
     ["Is that the real reason?",
      "What other reasons come to mind?",
      "Does that reason apply to anything else?",
      "If {0}, what else must be true?"]],

    [r'(.*) извините (.*)',
     ["Очень часто извинения не нужны",
      "Какие чувства у вас возникают, когда вы извиняетесь?"]],

    [r'(.*) sorry (.*)',
     ["There are many times when no apology is needed.",
      "What feelings do you have when you apologize?"]],

    [r'Привет(.*)',
     ["Привет,я рада что вы зашли сегодня",
      "Привет,как ты сегодня?",
      "Привет,как ты себя чувствуешь сегодня?"]],

    [r'Hello(.*)',
     ["Hello... I'm glad you could drop by today.",
      "Hi there... how are you today?",
      "Hello, how are you feeling today?"]],

    [r'I think (.*)',
     ["Do you doubt {0}?",
      "Do you really think so?",
      "But you're not sure {0}?"]],
    [r'Я думаю (.*)',
     ["Ты сомневаешься в том что {0}?",
      "Ты действительно так думаешь?",
      "Но ты не уверен в том что {0}?"]],
    [r'(.*) друг (.*)',
     ["Расскажи мне больше о своих друзьях",
      "Что приходит на ум, когда ты думаешь о друге?",
      "Почему бы тебе не рассказать мне о друге детства?"]],

    [r'(.*) friend (.*)',
     ["Tell me more about your friends.",
      "When you think of a friend, what comes to mind?",
      "Why don't you tell me about a childhood friend?"]],

    [r'Да',
     ["ты, кажется, совершенно уверен",
      "Хорошо, но не мог бы ты немного уточнить?"]],

    [r'(.*) компьютер (.*)',
     ["Ты правда говоришь обо мне?",
      "Странно разговаривать с компьютером?",
      "Какие чувства вызывают у вас компьютеры?",
      "Вы чувствуете угрозу со стороны компьютеров?"]],

    [r'(.*) computer(.*)',
     ["Are you really talking about me?",
      "Does it seem strange to talk to a computer?",
      "How do computers make you feel?",
      "Do you feel threatened by computers?"]],

    [r'Это (.*)\?',
     ["Ты думаешь это {0}?",
      "Возможно это {0} -- Как ты думаешь?",
      "Если бы это было {0}, Чтобы ты делал?",
      "Вполне может быть, что {0}."]],

    [r'Is it (.*)',
     ["Do you think it is {0}?",
      "Perhaps it's {0} -- what do you think?",
      "If it were {0}, what would you do?",
      "It could well be that {0}."]],

    [r'Это (.*)',
     ["Вы кажетесь очень уверенным",
      "Если бы я сказал вам, что, вероятно, это не  {0},что бы вы чувствовали ?"]],

    [r'It is  (.*)',
     ["You seem very certain.",
      "If I told you that it probably isn't {0}, what would you feel?"]],

    [r'Ты можешь (.*)\?',
     ["Почему ты думаешь, что я не могу {0}?",
      "Если бы я мог {0},и что ?",
      "Почему ты спрашиваешь, могу ли я {0}?"]],

    [r'Can you ([^\?]*)\??',
     ["What makes you think I can't {0}?",
      "If I could {0}, then what?",
      "Why do you ask if I can {0}?"]],

    [r'You are (.*)',
     ["Why do you think I am {0}?",
      "Does it please you to think that I'm {0}?",
      "Perhaps you would like me to be {0}.",
      "Perhaps you're really talking about yourself?"]],

    [r'Ты (.*)\?',
     ["Почему это важно, если я {0} ?",
      "Вы бы предпочли, если бы я не был {0} ?",
      "Возможно, вы верите, что я {0}.",
      "я может быть {0} Как вы думаете?"]],

    [r'Ты ([^\?]*)\??',
     ["Мы должны обсуждать тебя, а не меня.",
      "Почему ты так говоришь обо мне?",
      "Почему вас волнует, {0} ли я?"]],

    [r'You\'?re (.*)',
     ["Why do you say I am {0}?",
      "Why do you think I am {0}?",
      "Are we talking about you, or me?"]],

    [r'Я не буду (.*)',
     ["Не правда ли ты не будешь {0}?",
      "Почему ты не будешь {0}?",
      "Ты хочешь{0}?"]],

    [r'I don\'?t (.*)',
     ["Don't you really {0}?",
      "Why don't you {0}?",
      "Do you want to {0}?"]],

    [r'Я чувствую (.*)',
     ["Хорошо, расскажи мне подробнее об этих чувствах",
      "Ты часто чувствуешь {0}?",
      "Когда вы обычно чувствуете {0}?",
      "Когда ты чувствуешь {0},что ты делаешь?"]],

    [r'I feel (.*)',
     ["Good, tell me more about these feelings.",
      "Do you often feel {0}?",
      "When do you usually feel {0}?",
      "When you feel {0}, what do you do?"]],

    [r'Я имею (.*)',
     ["Почему ты говоришь мне, что ты {0}?",
      "ты правда {0}?",
      "Теперь когда у тебя есть {0},что ты будешь делать дальше?"]],

    [r'I have (.*)',
     ["Why do you tell me that you've {0}?",
      "Have you really {0}?",
      "Now that you have {0}, what will you do next?"]],

    [r'Я бы (.*)',
     ["Не могли бы вы объяснить, почему ты бы {0}?",
      "Почему тебе бы{0}?",
      "Кто еще знает, что ты бы {0}?"]],

    [r'I would (.*)',
     ["Could you explain why you would {0}?",
      "Why would you {0}?",
      "Who else knows that you would {0}?"]],

    [r'Это (.*)',
     ["Как вы думаете, есть {0}?",
      "Вероятно, что есть {0}.",
      "Хотите, чтобы там было {0}?"]],

    [r'Is there (.*)',
     ["Do you think there is {0}?",
      "It's likely that there is {0}.",
      "Would you like there to be {0}?"]],

    [r'Мой (.*)',
     ["Понятно ваш {0}.",

      "Почему вы говорите, что ваш {0}?",
      "Когда у вас {0},как вы себя чувствуете?"]],

    [r'My (.*)',
     ["I see, your {0}.",
      "Why do you say that your {0}?",
      "When your {0}, how do you feel?"]],

    # [r'Ты (.*)[^?]',
    #      ["Мы должны обсуждать тебя, а не меня.",
    #       "Почему ты так говоришь обо мне?",
    #       "Почему вас волнует, {0} ли я?"]],

    [r'You (.*)',
     ["We should be discussing you, not me.",
      "Why do you say that about me?",
      "Why do you care whether I {0}?"]],

    [r'Зачем (.*)',
     ["Почему вы не называете мне причину, по которой {0}?",
      "Как вы думаете, почему {0}?"]],

    [r'Why (.*)',
     ["Why don't you tell me the reason why {0}?",
      "Why do you think {0}?"]],

    [r'Я хочу (.*)',
     ["Что для вас будет значить, если вы получите {0}?",
      "Почему ты хочешь{0}?",

      "Что бы ты сделал, если бы получил {0}?",
      "Если у тебя есть {0},тогда что бы ты делал?"]],

    [r'I want (.*)',
     ["What would it mean to you if you got {0}?",
      "Why do you want {0}?",
      "What would you do if you got {0}?",
      "If you got {0}, then what would you do?"]],

    [r'(.*) мама(.*)',
     ["Расскажи мне больше о своей матери.",
      "Какие у вас были отношения с матерью?",
      "Как ты относишься к своей матери?",
      "Как это соотносится с вашими сегодняшними чувствами?",
      "Важны хорошие семейные отношения."]],

    [r'(.*) mother(.*)',
     ["Tell me more about your mother.",
      "What was your relationship with your mother like?",
      "How do you feel about your mother?",
      "How does this relate to your feelings today?",
      "Good family relations are important."]],

    [r'(.*) папа(.*)',
     ["Расскажи мне больше о своем отце",
      "Как тебя чувствовал твой отец?",
      "Как ты относишься к своему отцу?",
      "Связаны ли ваши отношения с отцом с вашими сегодняшними чувствами?",
      "У вас есть проблемы с проявлением привязанности к семье?"]],

    [r'(.*) father(.*)',
     ["Tell me more about your father.",
      "Как тебя чувствовал твой отец?",
      "How do you feel about your father?",
      "Does your relationship with your father relate to your feelings today?",
      "Do you have trouble showing affection with your family?"]],

    [r'(.*) ребенок (.*)',
     ["Были ли у вас в детстве близкие друзья?",
      "Какое ваше любимое воспоминание из детства?",
      "Вы помните какие-нибудь сны или кошмары из детства?",
      "Другие дети иногда дразнили вас?",
      "Как вы думаете, как ваши детские переживания связаны с вашими сегодняшними чувствами?"]],

    [r'(.*) child(.*)',
     ["Did you have close friends as a child?",
      "What is your favorite childhood memory?",
      "Do you remember any dreams or nightmares from childhood?",
      "Did the other children sometimes tease you?",
      "How do you think your childhood experiences relate to your feelings today?"]],

    [r'(.*)\?',
     ["Почему ты это спросил?",
      "Пожалуйста, подумайте, можете ли вы ответить на свой вопрос.",
      "Возможно, ответ кроется в тебе самом?",
      "Почему ты мне не скажешь?"]],

    [r'(.*)\?',
     ["Why do you ask that?",
      "Please consider whether you can answer your own question.",
      "Perhaps the answer lies within yourself?",
      "Why don't you tell me?"]],

    [r'Я (.*)',
     ["Ты пришел ко мне, потому что ты {0}?",
      "как долго ты {0}?",
      "Как ты относишься к тому, что ты {0}?"]],

    [r'выход',
     ["Спасибо, что поговорил со мной.",
      "Пока",
      "Спасибо, это будет 150 долларов. Хорошего дня!"]],

    [r'quit',
     ["Thank you for talking with me.",
      "Good-bye.",
      "Thank you, that will be $150.  Have a good day!"]],
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
      "Что вы чувствуете, когда говорите это?"]],

    [r'(.*)',
     ["Please tell me more.",
      "Let's change focus a bit... Tell me about your family.",
      "Can you elaborate on that?",
      "Why do you say that {0}?",
      "I see.",
      "Very interesting.",
      "{0}.",
      "I see.  And what does that tell you?",
      "How does that make you feel?",
      "How do you feel when you say that?"]]
]


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
