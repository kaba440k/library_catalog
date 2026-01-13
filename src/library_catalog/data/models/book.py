import uuid
from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import Boolean, DateTime, Integer, JSON, String, Text, func, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ...core.database import Base


class Book(Base):
    """
    Модель книги в библиотечном каталоге.

    Содержит информацию о книгах: название, автора, год издания и т.д.
    Автоматически генерирует UUID, временные метки создания и обновления.

    """

    __tablename__ = "books"

    """Уникальный ID книги. Генерируется автоматически."""
    book_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,

    )
    """Название книги. Макс. 500 символов. Индексировано."""
    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        index=True,
    )
    """Автор книги. Макс. 300 символов. Индексировано."""
    author: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
        index = True,
    )
    """Год издания. Индексировано."""
    year: Mapped[int] = mapped_column(
        Integer,
        nullable = False,
        index = True,
    )
    """Жанр. Макс. 100 символов. Индексировано."""
    genre: Mapped[str] = mapped_column(
        String(100),
        nullable = False,
        index = True,
    )
    """Количество страниц."""
    pages: Mapped[int] = mapped_column(
        Integer,
        nullable= False,
    )
    """Доступность для выдачи. По умолчанию True. Индексировано."""
    available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        index = True,
    )
    """ISBN (уникальный). Макс. 20 символов. Может быть None."""
    isbn: Mapped[Optional][str] = mapped_column(
        String(20),
        unique=True,
        nullable = True,
        index = True,
        default=None,
    )
    """Описание книги. Неограниченная длина. Может быть None."""
    description: Mapped[Optional][str] = mapped_column(
        Text,
        nullable=True,
        default = None,
    )
    """Дополнительные данные в JSON. Может быть None."""
    extra: Mapped[Optional][Dict[str, Any]] = mapped_column(
        JSON,
        nullable = True,
        default = None,
    )
    """Дата создания. Автоматически устанавливается БД при INSERT."""
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable = False,
        server_default=func.now(),
    )
    """Дата обновления. Автоматически обновляется БД при UPDATE."""
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<Book(id={self.book_id}, title='{self.title}')>"