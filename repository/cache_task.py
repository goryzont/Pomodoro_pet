import json

from redis import asyncio as Redis


from shema.tasks import TaskShema


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_tasks(self) -> list[TaskShema]:
        async with self.redis as redis:
            tasks_json =await redis.lrange('tasks', 0, -1)
            return [TaskShema.model_validate(json.loads(task)) for task in tasks_json]

    async def set_tasks(self, tasks: TaskShema):
        tasks_json= [task.model_dump_json() for task in tasks]
        async with self.redis as redis:
            await redis.lpush('tasks', *tasks_json)

