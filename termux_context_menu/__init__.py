from types import SimpleNamespace
import sys

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button
import requests

BUTTONS: tuple[Button, ...] = (
    Button("Open on PC", id="to-pc"),
)
SERVER = SimpleNamespace(
    addr="192.168.0.22:23325",
    token="rT3ktWBG7CLmD-xwGJkUuQSzfBKaRYu0oljzlpv8j5o"
)


def request(route: str, data: dict):
    requests.post(
        SERVER.addr + route,
        headers={"Authorization": SERVER.token},
        json=data
    )


class MenuApp(App):
    CSS_PATH = "menu.css"

    def compose(self) -> ComposeResult:
        with Container(id="root"):
            buttons = list(BUTTONS)
            for but in buttons:
                but.add_class("main-button")

            thic = None
            if len(buttons) & 1:
                thic = buttons.pop()
            yield from buttons

            if thic is not None:
                thic.add_class("thic")
                yield thic

    @on(Button.Pressed, "#to-pc")
    def but_to_pc(self):
        request("open-url", {"url": sys.argv[1]})

    @on(Button.Pressed, ".main-button")
    def after_selection(self):
        exit()
