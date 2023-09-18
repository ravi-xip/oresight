
class Message:
    def __init__(self, message_obj: dict):
        """
        Breaks down a message object into its role and content.
        :param message_obj:
        """
        self._role = message_obj['role']
        self._content = message_obj['content']

    def to_dict(self) -> dict:
        return {'role': self._role, 'content': self._content}

    def __str__(self) -> str:
        return self.to_dict().__str__()

    @property
    def role(self) -> str:
        return self._role

    @property
    def content(self) -> str:
        return self._content

    @role.setter
    def role(self, role: str) -> None:
        self._role = role

    @content.setter
    def content(self, content: str) -> None:
        self._content = content
