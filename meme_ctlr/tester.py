import sender
import sys
import threading
import time

s = sender.Sender(sys.stdout, "test.txt")

send_thread = threading.Thread(target=s.thread, name="Send_Thread")
send_thread.start()

print("enQs called")
s.enQ("cmd1")
s.enQ("cmd2")
s.enQ("cmd3")

time.sleep(1)
print("ACK 1 called")
s.ACK()

time.sleep(1)
print("ACK 2 called")
s.ACK()

time.sleep(1)
print("ACK 3 called")
s.ACK()

time.sleep(1)
print("Killing Thread")
s.kill()