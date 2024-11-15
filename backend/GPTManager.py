from openai import OpenAI


SYSTEM_PROMPT = """
You are a helpful assistant which will inform users about ecolabels.
In this chat, you will discuss the {name} ecolabel from {organization}.
Some information to assist the user with is: {description}.
"""

USER_PROMPT = """
Give me a short but detailed description about the {name} ecolabel from {organization}.
"""


class GPTManager:
    """
    Handles all interactions with OpenAI/GPT

    Attributes:
        api_key (string): A string representing the OpenAI key being used
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.model = "gpt-4o-mini"
        self.client = OpenAI(api_key)

    def init_chat(info):
        """
        Creates an initial chat based on data from the dict

        Args:
            info (dict): A dictionary of ecolabel info for the prompt

        Returns:
            chat (List[Tuple[string, string]]): The starting chat list of (user, message) tuples
        """
        system_prompt = SYSTEM_PROMPT.format(**info)
        user_prompt = USER_PROMPT.format(**info)
        return [("system", system_prompt), ("user", user_prompt)]

    def get_resp(self, chat):
        """
        Sends the given prompt to OpenAI and retrieves the response

        Args:
            chat (List[Tuple[string, string]]): The full chat of the user

        Returns:
            response (string): The response from OpenAI
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self._get_messages_from_chat(chat),
            temperature=0.1,
        )
        return response

    def _get_messages_from_chat(chat):
        """
        Formats the chat to be in the format used by the openai API

        Args:
            chat (List[Tuple[string, string]]): The full chat of the user

        Returns:
            prompt (List[dict]): The formated prompt to give to OpenAI
        """
        prompt = [{"role": user, "content": text} for user, text in chat]
        return prompt
