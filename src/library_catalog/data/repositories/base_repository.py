from typing import Generic, TypeVar, Type
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def create(self, **kwargs) -> T:
        """Создать запись."""
        new_data = self.model(**kwargs)
        self.session.add(new_data)
        await self.session.commit()
        await self.session.refresh(new_data)
        return new_data

    async def get_by_id(self, id: UUID) -> T | None:
        """
        Получить по ID.

        📝 Примечание: session.get() автоматически работает с primary key модели,
        независимо от его названия (id, book_id, user_id и т.д.)
        """
        return await self.session.get(self.model, id)

    async def update(self, id: UUID, **kwargs) -> T | None:
        """Обновить запись."""
        instance = await self.get_by_id(id)

        if not instance:
            return None

        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, id: UUID) -> bool:
        """Удалить запись."""
        instance = await self.get_by_id(id)

        if not instance:
            return False

        await self.session.delete(instance)
        await self.session.commit()
        return True

    async def get_all(
            self,
            limit: int = 100,
            offset: int = 0,
    ) -> list[T]:
        """Получить все записи с пагинацией."""
        stmt = select(self.model)
        stmt = stmt.order_by(self.model.created_at.desc())
        stmt = stmt.limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
