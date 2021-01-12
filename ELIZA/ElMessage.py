from ELIZA.eliza import Eliza

class MessageHandler(object):
    eliza_ob=Eliza()
    def __init__(self):
        self.eliza_ob=Eliza()
        self.eliza_ob.load('ELIZA/doctor.txt')
        self.eliza_ob.initial()

    def get_answer(self,question):
        return self.eliza_ob.respond(question)



