
class Responder():
    def __init__(self,logging,respond):
        self.logging = logging
        self.respond = respond

    def respond(self,result):
        self.respond(result,logging)