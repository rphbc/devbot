def execute_command(routes, message):
    for route in routes:
        command = route.check_route(message)
        if command:
            return route.call_command(command)
