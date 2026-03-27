from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from database import SessionLocal
from models import SoilData
import json

app = FastAPI()

# Stockage des clients connectés
clients = []

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)

    print("Client connecté")

    try:
        while True:
            data = await ws.receive_text()
            payload = json.loads(data)

            humidity = payload.get("humidity")
            led = payload.get("led")

            # 👉 Sauvegarde DB seulement si humidité existe
            if humidity is not None:
                db: Session = SessionLocal()
                soil = SoilData(humidity=humidity)
                db.add(soil)
                db.commit()
                db.close()

            # 👉 Broadcast à tous (frontend + esp32)
            for client in clients:
                try:
                    await client.send_text(json.dumps(payload))
                except:
                    pass

    except WebSocketDisconnect:
        print("Client déconnecté")
        clients.remove(ws)