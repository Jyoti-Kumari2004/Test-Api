from fastapi import FastAPI, APIRouter, HTTPException
from ..models.participant import Participant
from ..services.userService import UserService
from fastapi.encoders import jsonable_encoder
from mysql.connector import Error
from ..repos.participationRepo import ParticipationRepo

userRepo = ParticipationRepo()
userService = UserService(userRepo)


router = APIRouter()


@router.get("/home/{id}")
def get(id: int):
    try:
        return {"message": "welcome to fastapi {id}"}
    except ValueError as err:
        raise HTTPException(status_code=404, detail={"message": f"{err}"})


@router.get("/participant/{id}")
def get(id: int):
    try:
        resultUser = userService.get(id)
        return jsonable_encoder(resultUser)
    except ValueError as err:
        raise HTTPException(status_code=404, detail={"message": f"{err}"})


@router.post("/participant/create")
def create(user: Participant):
    try:
        userService.create(user)
        return {"message": "created!"}
    except ValueError as err:
        raise HTTPException(status_code=404, detail={"message": f"{err}"})


@router.put("/participant/update/{id}")
def update(id: int, user: Participant):
    try:
        result = userService.update(id, user)
        return jsonable_encoder(result)
    except ValueError as err:
        raise HTTPException(status_code=404, detail={"message": f"{err}"})


@router.delete("/participant/delete/{id}")
def delete(id: int):
    try:
        userService.delete(id)
        return {"message": "user deleted!"}
    except Error as err:
        print(f"Error :{err}")
