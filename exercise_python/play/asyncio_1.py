import asyncio,time

async def hello():
    asyncio.sleep(1)
    print(f'{time.time()}')

def run():
    for i in range(5):
        loop.run_until_complete(hello())


loop=asyncio.get_event_loop()


if __name__ == '__main__':
    run()