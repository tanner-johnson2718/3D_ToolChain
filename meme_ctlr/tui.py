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
        self.cont = tree.root.add("Continuous Monitor", expand=True)
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
        self.sub = tree.root.add("Report Verbosity", expand=True)
        self.sub0 = self.sub.add_leaf("Off")
        self.sub1 =self.sub.add_leaf("Filtered")
        self.sub2 =self.sub.add_leaf("Unfiltered")

        yield Static("Sidebar", id="sidebar")
        yield tree
        yield TextLog(id="State_Term", classes="box")
        yield TextLog(id="Response_Term", classes="box")
        yield Input(id="i1", classes="box")
        yield TextLog(id="Debug_Term")

        self.writer_lock = asyncio.Lock()
        asyncio.create_task(self.recv_thread())

    async def on_input_submitted(self, event : Input.Submitted):
        text = self.query_one("#i1").value
        send_str = "cmdG " + str(text) + "\n"
        self.query_one("#Debug_Term").write("Send -> " + send_str[:-1])

        await self.writer_lock.acquire()
        self.writer.write(send_str.encode('ascii'))
        self.writer_lock.release()

    async def on_tree_node_selected(self, message : Tree.NodeSelected):
        send_str = ""
        if message.node._parent.id == self.cont.id:
            send_str = "subS " + str(message.node._label) + "\n"
        elif message.node.id == self.sub0.id:
            send_str = "subR 0\n"
        elif message.node.id == self.sub1.id:
            send_str = "subR 1\n"
        elif message.node.id == self.sub2.id:
            send_str = "subR 2\n"

        if not send_str == "":
            self.query_one("#Debug_Term").write("Send -> " + send_str[:-1])
            await self.writer_lock.acquire()
            self.writer.write((send_str).encode('ascii'))
            self.writer_lock.release()

    async def recv_thread(self):
        self.reader, self.writer = await asyncio.open_connection(HOST, PORT)
        buffer = ""
        while True:
            data = await self.reader.read(PACKET_SIZE)
            buffer = data.decode('ascii')

            self.query_one("#Debug_Term").write("Recv -> " + buffer[:-1])

            while ('\n' in buffer) and (len(buffer) > 5):
                index = buffer.find('\n')
                if index == -1:
                    break
                prefix = buffer[0:4]
                buffer_temp = buffer[5:index]
                if prefix == "subR":
                    self.query_one("#Response_Term").write(buffer_temp)
                elif prefix == "subS":
                    if len(buffer_temp) > 0:
                        self.query_one("#State_Term", TextLog).write(buffer_temp)
                    else:
                        self.query_one("#State_Term", TextLog).clear()
                else:
                    break
                buffer = buffer[(index+1):]


app = MEME()
app.run()