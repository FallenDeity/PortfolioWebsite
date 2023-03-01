# import asyncio

from client import Website

app = Website(docs="/docs", redoc="/redocs", debug=True)
# loop = asyncio.get_event_loop() or asyncio.new_event_loop()
# loop.create_task(app.on_startup())


if __name__ == "__main__":
    app.run()
