from sqlalchemy import text
from .baseRepo import BaseRepo
from sqlalchemy import create_engine
from ..models.event import Event
from mysql.connector import Error


class EventRepo(BaseRepo):
    def __init__(self):
        super().__init__()

    def get(self, id):
        with self.engine.connect() as conn:
            query = text(
                f"""SELECT 
                    id, 
                    name, 
                    venue, 
                    startDate, 
                    endDate, 
                    description 
                    FROM event 
                    WHERE id = {id};"""
            )
            result = conn.execute(query)
            row = result.fetchone()
            return Event.model_construct(
                {"id", "name", "venue", "startDate", "endDate", "description"},
                **row._mapping,
            )

    def create(self, event: Event):
        with self.engine.connect() as conn:
            query = text(
                """
                        INSERT INTO event (
                            id, 
                            name, 
                            venue, 
                            startDate, 
                            endDate, 
                            description
                        ) 
                        VALUES (
                            :id, 
                            :name, 
                            :venue, 
                            :startDate, 
                            :endDate, 
                            :description
                        )
                    """
            )
            conn.execute(
                query,
                {
                    "id": event.id,
                    "name": event.name,
                    "venue": event.venue,
                    "startDate": event.startDate,
                    "endDate": event.endDate,
                    "description": event.description,
                },
            )
            conn.commit()

    def update(self, id, event: Event):
        with self.engine.connect() as conn:
            query = text(
                """
                    UPDATE event 
                    SET 
                        name = :name,
                        venue = :venue,
                        startDate = :startDate,
                        endDate = :endDate,
                        description = :description 
                    WHERE 
                        id = :id;
                """
            )
            result = conn.execute(
                query,
                {
                    "name": event.name,
                    "venue": event.venue,
                    "startDate": event.startDate,
                    "endDate": event.endDate,
                    "description": event.description,
                },
            )
            conn.commit()
            row = result.fetchone()
            return Event.model_construct(
                {"name", "venue", "startDate", "endDate", "description"}, **row._mapping
            )

    def delete(self, id):
        with self.engine.connect() as conn:
            query = f"DELETE FROM event WHERE id={id}"
            conn.execute(text(query))
            conn.commit()

    def isExist(self, id):
        with self.engine.connect() as conn:
            query = f"select 1 from event where id={id}"
            count = conn.execute(text(query))
            if count.rowcount == 0:
                return False
            return True
