from textual.app import App, ComposeResult
from textual.widgets import TextLog, Header, Footer, Static, Input
from textual import events
from textual.containers import Container

import threading
import socket
import time

HOST = "127.0.0.1"
PORT = 65432
PACKET_SIZE = 64
killed = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class MEME(App):
    CSS_PATH="tui.css"
    BINDINGS=[("a","a_binding","ASS")]

    def compose(self) -> ComposeResult:
        yield Static("Sidebar", id="sidebar")
        yield Header()
        yield Footer()
        yield TextLog(id="t1", classes="box")
        yield TextLog(id="t2", classes="box")
        yield Input(id="i1", classes="box")

    def on_input_submitted(self, event : Input.Submitted):
        text = self.query_one("#i1").value
        self.query_one("#t2").write(text)


app = MEME()
app.run()