import asyncio
import sys

from . import init, run, create_token, shutdown

loop = asyncio.get_event_loop_policy().get_event_loop()


async def main():
    try:
        await init()

        match sys.argv[1]:
            case "start":
                await run()
            case "token":
                print(await create_token())
            case _:
                raise AssertionError()
    finally:
        await shutdown()

loop.run_until_complete(main())
