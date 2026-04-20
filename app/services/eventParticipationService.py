from ..repos.eventRepo import EventRepo
from ..repos.participationRepo import ParticipationRepo
from ..repos.eventParticipationRepo import EventParticipationRepo


class EventParticipationService:
    eventParticipationRepo: EventParticipationRepo
    userRepo: ParticipationRepo
    eventRepo: EventRepo

    def __init__(
        self,
        eventParticipationRepo: EventParticipationRepo,
        userRepo: ParticipationRepo,
        eventRepo: EventRepo,
    ):
        self.eventParticipationRepo = eventParticipationRepo
        self.userRepo = userRepo
        self.eventRepo = eventRepo

    def create(self, eventId, participantId):
        if self.isEventExist(eventId) and self.isParticationExist(participantId):
            return self.eventParticipationRepo.create(eventId, participantId)
        raise ValueError("Either event or user Id is invalid !!")

    def delete(self, id):
        return self.eventParticipationRepo.delete(id)

    def isEventExist(self, eventId) -> bool:
        return self.eventRepo.isExist(eventId)

    def isParticationExist(self, participantId) -> bool:
        return self.userRepo.isExist(participantId)
