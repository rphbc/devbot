async def execute_command(routes, message):
    for route in routes:
        command = route.check_route(message.content)
        if command:
            return await route.call_command(command, message)
