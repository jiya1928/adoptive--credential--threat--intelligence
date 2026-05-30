from fastapi import WebSocket
from fastapi import WebSocketDisconnect


class ConnectionManager:

    def __init__(self):

        self.active_connections = []

    async def connect(
        self,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.active_connections.append(
            websocket
        )

    def disconnect(
        self,
        websocket: WebSocket
    ):

        if websocket in self.active_connections:

            self.active_connections.remove(
                websocket
            )

    async def broadcast(
        self,
        message: str
    ):

        disconnected = []

        for connection in self.active_connections:

            try:

                await connection.send_text(
                    message
                )

            except Exception:

                disconnected.append(
                    connection
                )

        for connection in disconnected:

            self.disconnect(
                connection
            )


manager = ConnectionManager()


async def websocket_endpoint(
    websocket: WebSocket
):

    await manager.connect(
        websocket
    )

    try:

        while True:

            data = await websocket.receive_text()

            await manager.broadcast(
                f"SECURITY_ALERT: {data}"
            )

    except WebSocketDisconnect:

        manager.disconnect(
            websocket
        )


async def send_security_alert(
    event_type: str,
    details: str
):

    await manager.broadcast(
        f"[{event_type}] {details}"
    )