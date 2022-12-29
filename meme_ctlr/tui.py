from textual.app import App, ComposeResult
from textual.widgets import TextLog, Header, Footer, Static, Input, Tree

import asyncio
import os

HOST = "127.0.0.1"
PORT = 65432
PACKET_SIZE = 64
killed = 0

class MEME(App):
    CSS_PATH="tui.css"

    def compose(self) -> ComposeResult:
        tree: Tree[dict] = Tree("Clicky Tree", id="tree")
        tree.root.expand()
        self.cont = tree.root.add("Monitor", expand=True)
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
        self.cont.add_leaf("SD Progress")
        self.cont.add_leaf("SD Total")
        self.sub = tree.root.add("Report Verbosity", expand=True)
        self.sub0 = self.sub.add_leaf("Off")
        self.sub1 =self.sub.add_leaf("Filtered")
        self.sub2 =self.sub.add_leaf("Unfiltered")
        self.macros = tree.root.add("Macros", expand=True)
        self.macros.add_leaf("Home")
        self.macros.add_leaf("Tram")
        self.macros.add_leaf("Level")
        self.macros.add_leaf("Emergency Stop")
        self.macros.add_leaf("Disable Steppers")
        self.macros.add_leaf("Pull SD Files")
        self.macros.add_leaf("Firmware Settings")
        self.files = tree.root.add("Local .GCO (CLICK)", expand=True)

        yield Static("Sidebar", id="sidebar")
        yield tree
        yield TextLog(id="State_Term", classes="box", max_lines=13)
        yield TextLog(id="Response_Term", classes="box", max_lines=1024)
        yield Input(id="i1", classes="box")
        yield TextLog(id="Debug_Term", max_lines=1024)

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
        elif message.node._parent.id == self.macros.id:
            send_str = "cmdM " + str(message.node._label) + "\n"
        elif message.node.id == self.files.id:
            self.files._children = []
            for file in os.listdir("./"):
                if file.endswith(".GCO"):
                    self.files.add_leaf(file)
            return
        elif message.node._parent.id == self.files.id:
            await self.writer_lock.acquire()
            self.writer.write(("cmdG M110 N0\n").encode('ascii'))
            self.writer.write(("cmdG M28 " + str(message.node._parent.id) + "\n").encode('ascii'))
            with open(str(message.node._label), encoding="utf-8") as my_file_handle:
                    line = 1

                    for chunk in my_file_handle:

                        if not (chunk.find("G") == 0 or chunk.find("M") == 0):
                            continue

                        # Add line number and strip trailing new line
                        chunk = "N" + str(line) + " " + chunk.rstrip()
                        line += 1

                        # strip comments
                        off = chunk.find(";")
                        if off > -1:
                            chunk = chunk[0:off]
                        sum = 0
                        for c in chunk:
                            sum ^= ord(c)
                        chunk = chunk + '*' + str(sum)

                        self.writer.write(("cmdG " + chunk + "\n").encode('ascii'))
            self.writer_lock.release()
        else:
            return
                    

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
            buffer += data.decode('ascii')

            self.query_one("#Debug_Term").write("Recv -> " + buffer[:-1])

            while ('\n' in buffer) and (len(buffer) > 5):
                index = buffer.find('\n')
                prefix = buffer[0:4]
                buffer_temp = buffer[5:index]
                if prefix == "subR":
                    self.query_one("#Response_Term").write(buffer_temp)
                elif prefix == "subS":
                    if len(buffer_temp) > 2:
                        self.query_one("#State_Term", TextLog).write(buffer_temp)
                    #else:
                        # self.query_one("#State_Term", TextLog).clear()
                        #self.query_one("#State_Term", TextLog).write("\n\n")
                else:
                    break
                buffer = buffer[(index+1):]


app = MEME()
app.run()