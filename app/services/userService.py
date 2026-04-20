from ..models.participant import Participant
from ..repos.participationRepo import ParticipationRepo


class UserService:
    userRepo: ParticipationRepo

    def __init__(self, userRepo: ParticipationRepo):
        self.userRepo = userRepo

    def get(self, id) -> Participant:
        return self.userRepo.get(id)

    def create(self, User):
        self.userRepo.create(User)

    def update(self, id, user):
        return self.userRepo.update(id, user)

    def delete(self, id):
        return self.userRepo.delete(id)
