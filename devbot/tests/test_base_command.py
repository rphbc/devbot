from devbot.core.commands import BaseCommand


class TestCommand(BaseCommand):
    actions = {
        'action1': {
            'arguments': {'arg1': {'dtype': 'str'}},
        },
        'action2': {
            'arguments': {'arg1': {'dtype': 'integer', 'required': False},
                          'arg2': {'dtype': 'float'}}
        },
        'action3': {
            'arguments': {}
        },
        'action4': {
            'arguments': {'arg1': {'dtype': 'integer', 'required': False}}
        }
    }

    def action1(self, arg1):
        return f'action1={arg1}'

    def action2(self, arg1, arg2):
        return f'action2={arg1},{arg2}'

    def action3(self):
        return 'action3'

    def action4(self, arg1):
        return f'action4={arg1}'


command = TestCommand()


def test_action1_called():
    result = command.run_command('action1 arg1 algumacoisa')
    assert result == 'action1=algumacoisa'


def test_action2_called():
    result = command.run_command('action2 arg1 123 arg2 44.3')
    assert result == 'action2=123,44.3'


def test_action3_called():
    result = command.run_command('action3')
    assert result == 'action3'


def test_action2_without_non_required():
    result = command.run_command('action2 arg2 44.3')
    assert result == 'action2=None,44.3'

def test_action4__not_required():
    result = command.run_command('action4')
    assert result == 'action4=None'
