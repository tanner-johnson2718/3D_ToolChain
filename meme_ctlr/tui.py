from textual.app import App, ComposeResult
from textual.widgets import TextLog, Header, Footer, Static, Input, Tree

import asyncio

HOST = "127.0.0.1"
PORT = 65432
PACKET_SIZE = 64
killed = 0

class MEME(App):
    CSS_PATH="tui.css"

    def compose(self) -> ComposeResult:
        tree: Tree[dict] = Tree("Subscriptions", id="tree")
        tree.root.expand()
        self.cont = tree.root.add("Continuous Monitor", expand=False)
        self.cont.add_leaf("Nozzle Temp Current")
        self.cont.add_leaf("Nozzle Temp Target")
        self.cont.add_leaf("Bed Temp Current")
        self.cont.add_leaf("Bed Temp Target")
        self.cont.add_leaf("X Pos")
        self.cont.add_leaf("Y Pos")
        self.cont.add_leaf("Z Pos")
        self.cont.add_leaf("E Pos")
        self.cont.add_leaf("Print Accel")
        self.cont.add_leaf("Retract Accel")
        self.cont.add_leaf("Travel Accel")
        one = tree.root.add("One Time", expand=False)
        one.add_leaf("X Steps per mm")
        one.add_leaf("Y Steps per mm")
        one.add_leaf("Z Steps per mm")
        one.add_leaf("E Steps per mm")
        one.add_leaf("Max X Vel mm/s")
        one.add_leaf("Max Y Vel mm/s")
        one.add_leaf("Max Z Vel mm/s")
        one.add_leaf("Max E Vel mm/s")
        one.add_leaf("Max X Accel mm/s2")
        one.add_leaf("Max Y Accel mm/s2")
        one.add_leaf("Max Z Accel mm/s2")
        one.add_leaf("Max E Accel mm/s2")
        sub = tree.root.add("Report Verbosity", expand=False)
        sub.add_leaf("Off")
        sub.add_leaf("Filtered")
        sub.add_leaf("Unfiltered")

        yield Static("Sidebar", id="sidebar")
        yield Header(show_clock=True)
        yield tree
        yield TextLog(id="t1", classes="box")
        yield TextLog(id="t2", classes="box")
        yield Input(id="i1", classes="box")

        self.writer_lock = asyncio.Lock()
        asyncio.create_task(self.recv_thread())

    async def on_input_submitted(self, event : Input.Submitted):
        text = self.query_one("#i1").value
        self.query_one("#t2").write("Sending -> " + text)

        await self.writer_lock.acquire()
        self.writer.write((text+"\n").encode('ascii'))
        self.writer_lock.release()

    async def on_tree_node_selected(self, message : Tree.NodeSelected):
        if message.node._parent.id == self.cont.id:
            await self.writer_lock.acquire()
            send_str = "subS " + str(message.node._label) + "\n"
            self.query_one("#t2").write("Sending -> " + send_str)
            self.writer.write((send_str).encode('ascii'))
            self.writer_lock.release()

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
                if prefix == "subR":
                    self.query_one("#t2").write(buffer_temp)
                else:
                    target = "#t1"
                buffer = buffer[(index+1):]


app = MEME()
app.run()