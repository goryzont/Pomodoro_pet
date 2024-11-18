from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException

from app.exception import TaskNotFound
from app.shema import TaskShema, TaskCreateShema
from app.dependency import get_tasks_service, get_request_user_id
from app.service import TaskService


router = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)

@router.get('/all', response_model=list[TaskShema])
async def get_tasks(
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
):
    return await task_service.get_tasks()


@router.post('/', response_model=TaskShema)
async def create_task(
        body: TaskCreateShema,
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
        user_id: int = Depends(get_request_user_id)
):

    task = await task_service.create_task(body, user_id)
    return task



@router.patch('/{task_id}', response_model=TaskShema)
async def update_task(
        task_id: int,
        name:str,
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
        user_id: int = Depends(get_request_user_id)
):
    try:
        return await task_service.update_task_name(task_id=task_id, name=name, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )



@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
        user_id: int = Depends(get_request_user_id)
):
    try:
        await task_service.delete_task(task_id=task_id, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )




