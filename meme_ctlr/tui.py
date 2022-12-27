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

    async def on_input_submitted(self, event : Input.Submitted):
        text = self.query_one("#i1").value
        self.query_one("#t2").write("Sending -> " + text)
        self.writer.write((text+"\n").encode('ascii'))

    async def recv_thread(self):
        self.reader, self.writer = await asyncio.open_connection(HOST, PORT)
        buffer = ""
        while True:
            data = await self.reader.read(PACKET_SIZE)
            buffer += data.decode('ascii')

            while '\n' in buffer:
                index = buffer.find('\n')
                prefix = buffer[0:4]
                buffer_temp = buffer[5:index]
                target = "#t2"
                if prefix == "subR":
                    target = "#t2"
                else:
                    target = "#t1"
                self.query_one(target).write(buffer_temp)
                buffer = buffer[(index+1):]


app = MEME()
app.run()