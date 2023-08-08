from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from db import database
from jose import jwt
from models.users import Users
from models.notifications import Notifications
from functions.notifications import manager
from schemas.notifications import NotificationSchema
from utils.auth import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session

notifications_router = APIRouter()


@notifications_router.websocket("/ws/connection")
async def websocket_endpoint(
        token: str,
        websocket: WebSocket,
        db: Session = Depends(database)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")

    user: Users = db.query(Users).filter_by(
        username=username, status=True).first()

    await manager.connect(websocket, user)

    if user:

        for ntf in user.notifications:
            message = NotificationSchema(
              title=ntf.title,
              body=ntf.body,
              user_id=ntf.user_id,

            )
            await manager.send_personal_json(message, (websocket, user))
        db.query(Notifications).filter_by(user_id=user.id).delete()
        db.commit()

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
