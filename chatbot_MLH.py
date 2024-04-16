#Import libraries
import re 
import random

#Create a list of pre-defined similar reponses to Eliza's by using a dictionary 
response = {
    'hello' : ['hello! how can I help you.'], 
    'hi ': ['hello! how can I help you.'], 
    'hey': ['hello! how can I help you.'], 
    'i feel (.*)': ['Why do you feel {}.', 'How long have you been feeling {}?'],
    'i am (.*)' : ['Why do you say you are {}?', 'How long have you been {}?'], 
    'i am (.*)' : ['Why are you {}?', 'How long have you been {}?' ], 
    'i (.*) myself' : ['Why do you {} yourself?', 'What makes you think you {} yourself?'], 
    '(.*) sorry (.*)' : ['There is no need to apologise,', 'What are you apologising for?'], 
    '(.*) friend (.*)': ['Tell me more about your friend.', 'How do your friends make you feel?'],
    'yes': ['You seem quite sure.', 'Can you elaborate?'], 
    'no': ['Can you elaborate why?', 'Why not?'], 
    '(.*)': ['Please tell me more.', 'Lets change focus a bit, tell me about something else.', 'Can you elaborate on that?'],
    '': ['Why do you think that?', 'Please tell me more.', 'Can you elaborate on that?', 'Tell me about what else is on your mind.']
}

#Define a function to match the user's input to a predefined response 
def match_response(input_text):
    # Create a for loop to iterate over the items of the dictionary created above
    for pattern, response_list in response.items():
        matches = re.match(pattern, input_text.lower())
        if matches:
            chosen_response = random.choice(response_list)
            return chosen_response.format(*matches.groups())

    # if there is not pattern match
    return "I'm sorry, I don't understand what you are saying."

    
#Create the main loop to start the chatbot 
print('Welcome to the ELiza Chatbot')
while(True): 
    user_input = input("You: ")
    if user_input.lower() == "bye": 
        print('Eliza: Goodbye.')
        break
    else: 
        print("Eliza: " + match_response(user_input))