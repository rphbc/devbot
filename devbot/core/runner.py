from devbot.core.commands import DevBot
from devbot.core.routers import Route


def append_devbot_class(routes):
    if DevBot not in routes:
        routes.append(
            Route('devbot', DevBot, class_args=(routes, ))
        )


async def execute_command(routes, message):
    append_devbot_class(routes)
    for route in routes:
        command = route.check_route(message.content)
        if command:
            return await route.call_command(command, message)
