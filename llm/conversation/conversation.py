import json

from llm.conversation.message import Message


# Define a conversation class that can be used to generate responses.
# The format of the conversation is as follows:
# {"role": "system", "content": "You are a helpful assistant."},
# {"role": "user", "content": "Who won the world series in 2020?"},
# {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
# {"role": "user", "content": "Where was it played?"}
# Each message is a dictionary with two keys: role and content.
# The role can be either "system", "user" or "assistant".
# The content is the text of the message.
# The conversation is a list of messages.
class Conversation:
    def __init__(self, conversation_string):
        self.conversation_str = conversation_string
        self.messages = []
        self.__extract_messages()

    def __extract_messages(self):
        messages_json_array = json.loads(self.conversation_str)
        # Create an array of ConversationMessage objects.
        self.messages = [
            Message(message_obj).to_dict()
            for message_obj in messages_json_array
            if message_obj is not None and message_obj != ''
        ]

    def get_messages(self):
        return self.messages

    def get_last_user_query(self):
        for message in reversed(self.messages):
            if message['role'] == 'user':
                return message['content']
        return None

    def __str__(self):
        return self.conversation_str


if __name__ == '__main__':
    system_prompt = "Please input your query."
    query = "What is the weather today?"
    conversation_str = f'[{{"role": "system", "content": "{system_prompt}"}}, ' \
                       f'{{"role": "assistant", "content": "Hello"}}, ' \
                       f'{{"role": "user", "content": "{query}"}}]'
    conversation = Conversation(conversation_str)
    print(conversation.get_messages())
    print(conversation.get_last_user_query())
    print(conversation)
