from dataclasses import dataclass

from sqlalchemy import select, delete, update, insert
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from models import Categories, Tasks
from shema import TaskCreateShema, TaskShema
from database.database import AsyncSessionFactory


@dataclass
class TaskRepository:

    db_session: AsyncSession


    async def get_tasks(self) -> list[Tasks]:
        async with self.db_session as session:
            task: list[Tasks] = (await session.execute(select(Tasks))).scalars().all()
        return task


    async def get_task(self, task_id: int) -> Tasks | None:
        async with self.db_session as session:
            task: Tasks = (await session.execute(select(Tasks).where(Tasks.id == task_id))).scalar_one_or_none()
        return task


    async def get_user_task(self, task_id: int, user_id: int) -> Tasks:
        query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        async with self.db_session as session:
            task: Tasks = (await session.execute(query)).scalar_one_or_none()
        return task


    async def create_task(self, task: TaskCreateShema, user_id: int) -> int:
        query = insert(Tasks).values(
            name=task.name,
            pomidoro_count=task.pomidoro_count,
            category_id=task.category_id,
            user_id=user_id).returning(Tasks.id)
        async with self.db_session as session:
            task_id = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
        return task_id


    async def delete_task(self, task_id: int, user_id: int) -> None:
        query = delete(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()

    async def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name == category_name)
        async with self.db_session as session:
            task: list[Tasks] = (await session.execute(query)).scalars().all()
        return task

    async def update_task_name(self, task_id: int, name: str) -> Tasks:
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        async with self.db_session as session:
            task_id: int = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return await self.get_task(task_id)




