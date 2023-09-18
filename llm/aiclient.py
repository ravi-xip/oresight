import json
import logging
from hashlib import md5

import backoff as backoff

import openai

from config.settings import OPENAI_CHAT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS, SYSTEM_PROMPT, FALLBACK_ANSWER
from llm.conversation.conversation import Conversation
from llm.prompts.prompts import BIO_EXTRACTION_PROMPT_TMPL
from llm.util import Utils


class AIClient:
    def __init__(self):
        self._model = OPENAI_CHAT_MODEL
        self._temperature = DEFAULT_TEMPERATURE
        self._max_tokens = DEFAULT_MAX_TOKENS
        self._system_prompt = SYSTEM_PROMPT
        self._fallback_answer = FALLBACK_ANSWER
        self._hits = 0
        self._thor_client = None
        self._openai_client = openai

    def extract_bio(self, contents: str) -> dict:
        """
        Given the contents of a page (i.e. could be derived from a Webpage), extracts entities from the contents
        These entities are extracted in the format of a JSON dictionary.

        :param contents:
        :return:
        """
        prompt = BIO_EXTRACTION_PROMPT_TMPL.format(text=contents)
        response = self.__run(prompt)
        try:
            response_json = json.loads(response)
        except json.JSONDecodeError:
            response_json = {}
        return response_json

    def __run(self, prompt: str) -> str:
        """
        This function is used to generate a response from the OpenAI API.
        :param prompt: The command to be executed.
        :return: The response from the OpenAI API.
        """
        logging.debug(f'__run: prompt: {prompt}')
        conversation_string = (f'[{{"role": "system", "content": "{self._system_prompt}"}},'
                               f'{{"role": "user", "content": "{Utils.normalize(prompt)}"}}]')
        return self.__chat(Conversation(conversation_string))

    def __chat(self, conversation: Conversation) -> str:
        """
        Given a conversation, generates a response from the OpenAI API.
        :param conversation: The conversation to be used to generate the response.

        :return: A response for the query asked by the user in the conversation.
        """
        # Step I: Check if the explanation is already present in Redis
        hash_key = md5(conversation.__str__().encode('utf-8')).hexdigest()
        if self._thor_client and self._thor_client.exists(hash_key):
            self._hits += 1
            return self._thor_client.get(hash_key).decode('utf-8')

        # Step II: Generate the response from the OpenAI API
        response = self.__chat_with_backoff(
            model=self._model,
            messages=conversation.get_messages(),
            max_tokens=self._max_tokens
        )

        # Step III: Extract the response from the OpenAI API
        response_text = self.__extract_response(response)

        # Step IV: Store the response in Redis
        if self._thor_client:
            self._thor_client.set(hash_key, response_text)

        # Step V: Return the explanation to the client
        return response_text

    def __extract_response(self, response: openai.ChatCompletion) -> str:
        """
        Extract the response from the OpenAI API.
        :param response: ChatCompletion object from the OpenAI API that contains the response.
        :return:
        """
        response_text = (response.choices[0].message.content if response.choices else '').strip()
        return response_text or self._fallback_answer

    @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
    def __chat_with_backoff(self, **kwargs):
        return self._openai_client.ChatCompletion.create(**kwargs)


