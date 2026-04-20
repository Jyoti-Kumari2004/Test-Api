from fastapi import FastAPI, APIRouter, HTTPException
from ..models.event import Event
from ..services.eventService import EventService
from fastapi.encoders import jsonable_encoder
from mysql.connector import Error
from ..repos.eventRepo import EventRepo

eventRepo = EventRepo()
eventService = EventService(eventRepo)

router = APIRouter()


@router.get("/event/{id}")
def get(id: int):
    try:
        result = eventService.get(id)
        return jsonable_encoder(result)
    except ValueError as err:
        raise HTTPException(status_code=404, detail={"message": f"{err}"})


@router.post("/event/create")
def create(event: Event):
    try:
        # print(event.model_validate(event))
        eventService.create(event)
        return {"message": "created!"}
    except ValueError as err:
        raise HTTPException(status_code=404, detail={"message": f"{err}"})


@router.put("/event/update/{id}")
def update(id: int, event: Event):
    try:
        result = eventService.update(id, event)
        return jsonable_encoder(result)
    except ValueError as err:
        raise HTTPException(status_code=404, detail={"message": f"{err}"})


@router.delete("/event/delete/{id}")
def delete(id: int):
    try:
        eventService.delete(id)
        return {"message": "event deleted from events!"}
    except Error as err:
        print(f"Error :{err}")
