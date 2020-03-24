import re

dtype_regex = {
    'str': r'\w+',
    'integer': r'[-+]?[1-9][0-9]*',
    'float': r'[-+]?[1-9][0-9]*\.?[0-9]+'
}

class BaseCommand:
    def __init__(self, message):
        self._message = message

    actions = {}

    async def _create_arguments_regex(self, arguments):
        regex = r''
        for argument, argument_info in arguments.items():
            arg_dtype = argument_info['dtype']
            arg_regex = rf'{argument}[\s]+(?P<{argument}>' \
                        rf'{dtype_regex[arg_dtype]})([\s]|$)'
            if not argument_info.get('required', True):
                arg_regex = f'({arg_regex})?'
            regex += arg_regex
        return regex

    async def _search_actions(self, content):
        for action, action_data in self.actions.items():
            arg_required = [arg_data.get('required', True) for arg_data in
                            action_data['arguments'].values()]
            if self.actions[action]['arguments'] and any(arg_required):
                regex = rf'{action}[\s]+(?P<arguments>.*)$'
            elif self.actions[action]['arguments']:
                regex = rf'{action}'+r'([\s]+(?P<arguments>.*)$|[\s]{0,}$)'
            else:
                regex = rf'{action}'+r'[\s]{0,}$'
            match = re.match(regex, content)
            if match and 'arguments' in match.groupdict():
                arguments = match.group('arguments') or ''
                return (action, arguments)
            elif match:
                return (action, '')
        raise ValueError('Action not Found')

    async def _get_action_arguments(self, action, content):
        action_data = self.actions[action]
        args_regex = await self._create_arguments_regex(arguments=action_data[
            'arguments'])
        if not args_regex:
            return {}
        match = re.match(args_regex, content)
        is_required = [arg_data.get('required', True) for arg_data in
                       action_data['arguments'].values()]
        if not match and any(is_required):
            raise ValueError('Arguments not found.')
        elif not match:
            return {}
        return match.groupdict()

    async def run_command(self, command_text):
        action, action_content  = await self._search_actions(command_text)
        if not action:
            return False
        action_args = await self._get_action_arguments(action, action_content)
        return await getattr(self, action)(**action_args)
