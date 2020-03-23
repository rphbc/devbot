from devbot.core.commands import BaseCommand


class GreetCommand(BaseCommand):
    """
    Greets People
    """
    actions = {
        'say_hi': {'arguments': {'to': {'dtype': 'str'}}},
        'hello': {'arguments': {}}
    }

    async def say_hi(self, to):
        """
        Says hi to the person passed as the "to" argument.
        If value me is passed, it greets your name instead.
        :param to: str
        :return: str
        """
        name = to
        if to == 'me':
            name = self._message.author.name
        return f'Hello {name}, how are you?'

    async def hello(self):
        """
        Greets you back.
        :return: str
        """
        return f'Hello {self._message.author.name}!'
