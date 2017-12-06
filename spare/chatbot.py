"""
def getResponse():
    while True:
        try:
            bot_input = chatBot.get_response(str(input("Enter: ")))
            print(bot_input)
        except (KeyboardInterrupt, EOFError, SystemExit):
            break

def getSingleResponse(query):
    return chatBot.get_response(query)

class EChatBot(object):
    CONVERSATION_ID = ""

    def get_feedback(self):
        text = input_function()

        if 'yes' in text.lower():
            return False
        elif 'no' in text.lower():
            return True
        else:
            print('Please type either "Yes" or "No"')
            return self.get_feedback()


    def learnFromInput(self):
        try:
            input_statement = chatBot.input.process_input_statement()
            statement, response = chatBot.generate_response(input_statement, self.CONVERSATION_ID)

            chatBot.output.process_response(response)
            print('\n Is "{}" a coherent response to "{}"? \n'.format(response, input_statement))
            if self.get_feedback():
                print("please input the correct one")
                response1 = chatBot.input.process_input_statement()
                chatBot.learn_response(response1, input_statement)
                chatBot.storage.add_to_conversation(self.CONVERSATION_ID, statement, response1)
                print("Responses added to bot!")
        except (KeyboardInterrupt, EOFError, SystemExit) as error:
            print("Error")
"""