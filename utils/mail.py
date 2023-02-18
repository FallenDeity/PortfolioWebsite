import typing

if typing.TYPE_CHECKING:
    from client import Website


__all__: tuple[str, ...] = ("Mail",)


class Mail:
    def __init__(self, website: "Website") -> None:
        self.app = website
        self.client = website.client
        self.url = str(website.config.DISCORD_WEBHOOK)

    async def send(self, content: str) -> bool:
        embed = {
            "title": "New Message",
            "description": content,
            "color": 0x00FF00,
        }
        async with self.client.post(self.url, json={"embeds": [embed]}) as resp:
            return resp.status == 204
