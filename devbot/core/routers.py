import re


class Route:
    def __init__(self, route_name, command_class, route_indicator='!'):
        self.route_indicator = route_indicator
        self.route_name = route_name
        self.command_class = command_class
        self.route_regex = rf'{self.route_indicator}{route_name}[\s]+' \
                           rf'(?P<command>.*)$'

    def call_command(self, command):
        return self.command_class().run_command(command)

    def check_route(self, text):
        match = re.match(self.route_regex, text)
        return match.group('command') if match else False
