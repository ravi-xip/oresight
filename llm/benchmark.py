import time

from llm.aiclient import AIClient
from llm.prompts.prompts import SUMMARY_GENERATOR_PROMPT_TMP
from reader.file import File


class Benchmark:
    def __init__(self):
        self._contents = File.read("/Users/ravitandon/Desktop/attention.pdf")
        self._words = self._contents.split(" ")
        self._client = AIClient()

    def run(self):
        """Triggers the following benchmark."""
        """
        Make three API calls to the OpenAI server:
        
        a) Embedding API call
            --> Token count: 256, 512, 1024, 2048, 4096
        b) Chat API call
            b.1) Chat API call to OpenAI-3.5
                --> Token count: 256, 512, 1024, 2048, 4096
            b.2) Chat API call to OpenAI-4.0
                --> Token count: 256, 512, 1024, 2048, 4096        
        """
        self.__run_embed()
        # self.__run_chat()

    def __run_embed(self):
        """Runs the embedding API call."""
        for w_len in [256, 512, 1024, 2048, 4096]:
            start_time = time.time()
            self._client.embedding(" ".join(self._words[:w_len]))
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
            print("{}, {}, {}".format(self._client.model, w_len, time_taken))

    def __run_chat(self):
        """Runs the chat API call to OpenAI-3.5."""
        self.__run_chat_3_5()
        self.__run_chat_4_0()

    def __run_chat_3_5(self):
        """Runs the chat API call."""
        # Trigger the call on the client.
        # Word count: 256, 512, 1024, 2048, 4096 words
        # 256 words
        for w_len in [256, 512, 1024, 2048, 4096]:
            start_time = time.time()
            self._client.summarize(" ".join(self._words[:w_len]))
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
            print("{}, {}, {}".format(self._client.model, w_len, time_taken))

    def __run_chat_4_0(self):
        """Runs the chat API call to OpenAI-4.0."""
        for w_len in [256, 512, 1024, 2048, 4096]:
            start_time = time.time()
            self._client.model = "gpt-4"
            self._client.summarize(" ".join(self._words[:w_len]))
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
            print("{}, {}, {}".format(self._client.model, w_len, time_taken))


if __name__ == "__main__":
    benchmark = Benchmark()
    benchmark.run()
