from sqlalchemy import text
from .baseRepo import BaseRepo
from sqlalchemy import create_engine
from ..models.participant import Participant
from mysql.connector import Error


class ParticipationRepo(BaseRepo):
    def __init__(self):
        super().__init__()

    def get(self, id):
        with self.engine.connect() as conn:
            query = f"""SELECT 
                        id, 
                        name, 
                        contact,
                        email
                    FROM participant 
                    WHERE id = {id};"""
            result = conn.execute(text(query))
            row = result.fetchone()
            return Participant.model_construct(
                {"id", "name", "contact", "email"}, **row._mapping
            )

    def create(self, participant: Participant):
        with self.engine.connect() as conn:
            query = text(
                """
                    INSERT INTO participant (
                        id, 
                        name, 
                        contact, 
                        email
                    ) 
                    VALUES (
                        :id, 
                        :name, 
                        :contact, 
                        :email
                    );
                """
            )
            conn.execute(
                query,
                {
                    "id": participant.id,
                    "name": participant.name,
                    "contact": participant.contact,
                    "email": participant.email,
                },
            )
            conn.commit()

    def update(self, id, user):

        with self.engine.connect() as conn:
            query = text(
                """
                    UPDATE participant 
                    SET 
                    name = :name, 
                    contact = :contact, 
                    email = :email 
                    WHERE 
                    id = :id;
                """
            )

            result = conn.execute(
                query, {"name": user.name, "contact": user.contact, "email": user.email}
            )
            conn.commit()
            row = result.fetchone()
            return Participant.model_construct(
                {"name", "contact", "email"}, **row._mapping
            )

    def delete(self, id):
        with self.engine.connect() as conn:
            query = f"DELETE FROM participant WHERE id={id}"
            conn.execute(text(query))
            conn.commit()

    def isExist(self, id):
        with self.engine.connect() as conn:
            query = f"select 1 from participant where id={id}"
            count = conn.execute(text(query))
            if count.rowcount == 0:
                return False
            return True
