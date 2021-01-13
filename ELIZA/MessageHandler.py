from ELIZA.eliza import Eliza

class MessageHandler(object):
    def __init__(self):
        self.eliza_ob=Eliza()
    def get_answer(self,question):
        return self.eliza_ob.respond(question)


