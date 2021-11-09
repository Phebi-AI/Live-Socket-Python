# Phebi-Live WebSocket Endpoint (Python)
The Phebi-Live WebSocket Endpoint is to enable 3rd party Applications access to Phebi's realtime emotion analysis and speech-to-text transcription.

Phebi-Live does not support speaker diarization, it is highly recommended to have a separate socket and audio stream per speaker to ensure capturing the correct emotions for respondents.

## 1. The socket endpoint

The url to the Phebi-Live socket consists of

* The host, your own environment and analysis portal (provided to you by Phebi)
* The project name, where the live session should be saved to
* The session (appears as respondent-id in the analysis portal)
* The speaker (respondent, moderator etc.)


## 2. Prerequisites

We will use the websocket python package to connect to the Phebi-Live WebSocket

```
pip3 install websocket-client
```

## 3. Establish a socket connection

To establish a connection to the Phebi-Live WebSocket you have to provide the subscription key 'Subscription' in the request headers.

```
import websocket

subscription_key = "b97076b5-faf4-4c66-8123-1deb12db9817"
project = "Test_Project"
session = "python"
speaker = "speaker1"

# Create a new websocket connection to the Phebi-Live WebSocket endpoint.
ws = websocket.WebSocketApp(
    "ws://dev.phebi.ai/sockets/live/" + project + "/" + session + "/" + speaker,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
    header = ["Subscription:" + subscription_key]
)
```

## 4. Receiving data from the socket

```
def on_message(ws, message):
    # Message contains the Phebi Response.
    print(message)
```

## 5. Sending audio data to the socket

The Phebi-Live WebSocket requires wave RIFF audio data with 16k sample rate, 16 bits per sample and 1 audio channel.

```
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
```

## 6. Ending the transmission

When the Live session has ended, we need to tell Phebi-Live that' we're at the end of the file and we need the last final transcription.
If we close the session now, without sending the EOF message, the final transcription will not be sent to the client.

The EOF message is a single byte with value 1.

```
// Send EOF message.
ws.send([0x01], websocket.ABNF.OPCODE_BINARY)
```
