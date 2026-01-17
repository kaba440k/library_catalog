from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.library_catalog.data.models.book import Book
from src.library_catalog.data.repositories.base_repository import BaseRepository


class BookRepository(BaseRepository[Book]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Book)

    async def find_by_filters(
            self,
            title: str | None = None,
            author: str | None = None,
            genre: str | None = None,
            year: int | None = None,
            available: bool | None = None,
            limit: int = 20,
            offset: int = 0,
    ) -> list[Book]:
        """Поиск книг с фильтрацией."""

        stmt = select(self.model)

        if title:
            stmt = stmt.where(self.model.title.ilike(f"%{title}%"))
        if author:
            stmt = stmt.where(self.model.author.ilike(f"%{author}%"))
        if genre:
            stmt = stmt.where(self.model.genre.ilike(f"%{genre}%"))
        if year is not None:
            stmt = stmt.where(self.model.year == year)
        if available is not None:
            stmt = stmt.where(self.model.available == available)

        stmt = stmt.limit(limit).offset(offset)
        stmt = stmt.order_by(self.model.created_at.desc())

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def find_by_isbn(self, isbn: str) -> Book | None:
        """Найти книгу по ISBN."""
        stmt = select(self.model)
        stmt = stmt.where(self.model.isbn == isbn)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def count_by_filters(
            self,
            title: str | None = None,
            author: str | None = None,
            genre: str | None = None,
            year: int | None = None,
            available: bool | None = None,
    ) -> int:
        """Подсчитать количество книг по фильтрам."""
        stmt = select(func.count(self.model.book_id))
        if title:
            stmt = stmt.where(self.model.title.ilike(f"%{title}%"))
        if author:
            stmt = stmt.where(self.model.author.ilike(f"%{author}%"))
        if genre:
            stmt = stmt.where(self.model.genre.ilike(f"%{genre}%"))
        if year is not None:
            stmt = stmt.where(self.model.year == year)
        if available is not None:
            stmt = stmt.where(self.model.available == available)

        result = await self.session.execute(stmt)

        return result.scalar_one()
