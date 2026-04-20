from fastapi import FastAPI, APIRouter, HTTPException
from ..repos.eventRepo import EventRepo
from ..repos.participationRepo import ParticipationRepo
from ..services.eventParticipationService import EventParticipationService
from ..repos.eventParticipationRepo import EventParticipationRepo

router = APIRouter()

eventParticipationRepo = EventParticipationRepo()
participationRepo = ParticipationRepo()
eventRepo = EventRepo()
eventParticipationService = EventParticipationService(
    eventParticipationRepo, participationRepo, eventRepo
)


@router.post("/event/{eventId}/participant/{participanId}")
def create(eventId: int, participantid: int):
    try:
        eventParticipationService.create(eventId, participantid)
        return {"message": "created!!"}
    except ValueError as error:
        return HTTPException(status_code=404, detail={"message": f"{error}"})


@router.delete("/event/participant/delete/{eventParticipationid}")
def delete(eventParticipationid: int):
    try:
        eventParticipationService.delete(eventParticipationid)
        return {"message": "deleted from EventParticipation!!"}
    except Exception as error:
        return HTTPException(status_code=404, detail={"message": f"{error}"})
