class AppException(Exception):
    """Базовое исключение приложения с HTTP-статусом."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(AppException):
    """Ресурс не найден."""
    def __init__(self, resource, identifier):
        self.message = f"{resource} с ID '{identifier}' не найдена"
        super().__init__(message = self.message, status_code=404)