import re


class Route:
    def __init__(self, route_name, command_class, route_indicator='!',
                 class_args=None, class_kwargs=None):
        self.route_indicator = route_indicator
        self.route_name = route_name
        self.command_class = command_class
        self.route_regex = rf'{self.route_indicator}{route_name}[\s]+' \
                           rf'(?P<command>.*)$'
        class_args = class_args or tuple()
        self.class_args = class_args
        self.class_kwargs = class_kwargs or dict()

    async def call_command(self, command, message):
        return await self.command_class(
            message, *self.class_args, **self.class_kwargs
        ).run_command(command)

    def check_route(self, text):
        match = re.match(self.route_regex, text)
        return match.group('command') if match else False
