from devbot.core.commands import BaseCommand


class GreetCommand(BaseCommand):
    actions = {
        'say_hi': {'arguments': {'to': {'dtype': 'str'}}}
    }

    async def say_hi(self, to):
        name = to
        if to == 'me':
            name = self._message.author.name
        return f'Hello {name}, how are you?'
