import json

import websocket
import _thread
import time
import rel


def on_message(ws, message):
    msg = json.loads(message)
    print(msg)
    if 'cmd' in msg:
        eval(msg['cmd'])
    print(message)


def on_error(ws, error):
    print("error:",error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    ws.send('{"message":"hello"}')
    print("Opened connection")


if __name__ == "__main__":
    host = "localhost"
    port = 8000
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"ws://{host}:{port}/ws/chat/20/",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    print(ws.run_forever(reconnect=5))  # Set dispatcher to automatic reconnection
