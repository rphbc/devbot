from devbot.core.commands import BaseCommand


class GreetCommand(BaseCommand):
    actions = {
        'greet': {'arguments': {'name': {'dtype': 'str'}}}
    }

    def greet(self, name):
        return f'Hello {name}, how are you?'
