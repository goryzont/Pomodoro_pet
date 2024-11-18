from dataclasses import dataclass

from exception import TaskNotFound
from repository import TaskRepository, TaskCache
from shema import TaskShema, TaskCreateShema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    async def get_tasks(self) -> list[TaskShema]:
        if tasks := await self.task_cache.get_tasks():
            return tasks
        else:
            tasks = await self.task_repository.get_tasks()
            tasks_shema = [TaskShema.model_validate(task) for task in tasks]
            await self.task_cache.set_tasks(tasks_shema)
            return tasks_shema

    async def create_task(self, body: TaskCreateShema, user_id: int) -> TaskShema:
        task_id = await self.task_repository.create_task(body, user_id)
        task = await self.task_repository.get_task(task_id)
        return TaskShema.model_validate(task)

    async def update_task_name(self, task_id: int, name: str, user_id: int) -> TaskShema:
        task = await self.task_repository.get_user_task(task_id, user_id)
        if not task:
            raise TaskNotFound
        task = await self.task_repository.update_task_name(task_id, name)
        return  TaskShema.model_validate(task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        task = await self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        await self.task_repository.delete_task(task_id=task_id, user_id=user_id)


