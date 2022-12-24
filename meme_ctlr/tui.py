from textual.app import App, ComposeResult
from textual.widgets import TextLog, Header, Footer, Static
from textual import events
from textual.containers import Container


class MEME(App):
    CSS_PATH="tui.css"
    BINDINGS=[("a","a_binding","ASS")]

    def compose(self) -> ComposeResult:
        yield Static("Sidebar", id="sidebar")
        yield Header()
        yield Footer()
        yield TextLog(id="t1", classes="box")
        yield TextLog(id="t2", classes="box")

    def on_key(self, event: events.Key) -> None:
        self.query_one("#t1",TextLog).write(event.character)


if __name__ == "__main__":
    app = MEME()
    app.run()