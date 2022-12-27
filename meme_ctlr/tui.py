from textual.app import App, ComposeResult
from textual.widgets import TextLog, Header, Footer, Static, Input

import asyncio

HOST = "127.0.0.1"
PORT = 65432
PACKET_SIZE = 64
killed = 0

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

        
        asyncio.create_task(self.recv_thread())

    def on_input_submitted(self, event : Input.Submitted):
        text = self.query_one("#i1").value
        self.query_one("#t2").write(text)

    async def recv_thread(self):
        self.reader, self.writer = await asyncio.open_connection(HOST, PORT)
        while True:
            data = await self.reader.read(PACKET_SIZE)
            self.query_one("#t2").write(data.decode('ascii'))


app = MEME()
app.run()