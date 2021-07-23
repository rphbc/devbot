from unittest.mock import MagicMock

import pytest

from devbot.core.commands import BaseCommand

pytestmark = pytest.mark.asyncio


class TestCommand(BaseCommand):
    """
    Class DocTest
    Here.
    """
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

    async def action1(self, arg1):
        """Run Action1
        :param arg1: str - Required
        :return: str
        """
        return f'action1={arg1}'

    async def action2(self, arg1, arg2):
        """Run Action2
        :param arg1: int - Not Required
        :param arg2: float - Required
        :return: str
        """
        return f'action2={arg1},{arg2}'

    async def action3(self):
        """Run Action3
        :return: str
        """
        return 'action3'

    async def action4(self, arg1):
        return f'action4={arg1}'


@pytest.fixture
async def message():
    return MagicMock()


@pytest.fixture
async def command_class(message):
    return TestCommand(message)


async def test_action1_called(command_class):
    result = await command_class.run_command('action1 arg1 algumacoisa')
    assert result == 'action1=algumacoisa'


async def test_action2_called(command_class):
    result = await command_class.run_command('action2 arg1 123 arg2 44.3')
    assert result == 'action2=123,44.3'


async def test_action3_called(command_class):
    result = await command_class.run_command('action3')
    assert result == 'action3'


async def test_action2_without_non_required(command_class):
    result = await command_class.run_command('action2 arg2 44.3')
    assert result == 'action2=None,44.3'


async def test_action4__not_required(command_class):
    result = await command_class.run_command('action4')
    assert result == 'action4=None'


async def test_class_description():
    desc = TestCommand.describe_class()
    assert desc == """
    Class DocTest
    Here.
    """

async def test_class_actions_description():
    description = TestCommand.describe_actions()
    assert description == """.action1:
Run Action1
        :param arg1: str - Required
        :return: str
        
.action2:
Run Action2
        :param arg1: int - Not Required
        :param arg2: float - Required
        :return: str
        
.action3:
Run Action3
        :return: str
        
.action4:"""
