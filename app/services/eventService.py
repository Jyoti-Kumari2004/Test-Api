from ..models.event import Event
from ..repos.eventRepo import EventRepo


class EventService:
    eventRepo: EventRepo

    def __init__(self, eventRepo: EventRepo):
        self.eventRepo = eventRepo

    def get(self, id) -> Event:
        return self.eventRepo.get(id)

    def create(self, event):
        return self.eventRepo.create(event)

    def update(self, Event, id):
        return self.eventRepo.update(Event, id)

    def delete(self, id):
        return self.eventRepo.delete(id)
