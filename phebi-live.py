# pip3 install websocket-client

import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    # Message contains the Phebi Response.
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("### opened ###")
    def run(*args):
    
        # Open the test audio file.
        with open("test.wav", "rb") as f:
            # Read the audio file in 1KB blocks.
            byte = f.read(1024)
            while byte:
                # Send the binary data to the Phebi-Live WebSocket.
                ws.send(byte, websocket.ABNF.OPCODE_BINARY)
                byte = f.read(1024)
        
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(False)
    # Create a new websocket connection to the Phebi-Live WebSocket endpoint.
    ws = websocket.WebSocketApp(
        "ws://dev.phebi.ai/sockets/live/Test_Project/python/speaker1",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header = ["Subscription:b97076b5-faf4-4c66-8123-1deb12db9817"]
    )

    ws.run_forever()
