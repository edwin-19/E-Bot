# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 21:21:32 2017

@author: Edwin
"""

from chatterbot import ChatBot
import logging

#small configuration for logic adapters
bestMatch = {
    "import_path": "chatterbot.logic.BestMatch",
    "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
    "response_selection_method": "chatterbot.response_selection.get_first_response"
}

timeLogic = {
    "import_path":"chatterbot.logic.TimeLogicAdapter"
}

mathematicsLogic = {
    "import_path":"chatterbot.logic.MathematicalEvaluation"
}

lowConfidence = {
    'import_path': 'chatterbot.logic.LowConfidenceAdapter',
    'threshold': 0.65,
    'default_response': 'I am sorry, but I do not understand.'
}

specificInput = {
    'import_path': 'chatterbot.logic.SpecificResponseAdapter',
    'input_text': 'Help me!',
    'output_text': 'Ok, here is a link: http://chatterbot.rtfd.org/en/latest/quickstart.html'
}

# Logging Settings
"""logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='chatbot/log/report.log',
                    filemode='w')"""

# Chatter bot
chatBot = ChatBot(
    "E-Bot",
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.convert_to_ascii'
    ],
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='chatbot/database/test',
    logic_adapters=[
        bestMatch,
        timeLogic,
        mathematicsLogic,
        lowConfidence,
        specificInput
    ],
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    output_format="text",
    filters=["chatterbot.filters.RepetitiveResponseFilter"],
)




