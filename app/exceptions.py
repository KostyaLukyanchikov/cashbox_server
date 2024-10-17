import json
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional, Dict, Any


class ErrorCodes(Enum):
    # Общая системная ошибка. Данная ошибка используется при возникновении системной ошибки,
    # например, недоступность системы, к которой выполняется запрос
    EX_SYSTEM_ERROR = "EX_SYSTEM_ERROR"
    # Ошибка валидации параметров запрос. Данный код используется при ошибках анализа запроса,
    # например, отсутствуют обязательные параметры, переданы параметры не того типа.
    EX_VALIDATION_ERROR = "EX_VALIDATION_ERROR"
    # Неизвестная ошибка. Все остальные ошибки, не имеющие отдельного обработчика
    EX_UNKNOWN_ERROR = "EX_UNKNOWN_ERROR"

    EX_ILLEGAL_ARGUMENT = "EX_ILLEGAL_ARGUMENT"
    EX_NOT_FOUND = "EX_NOT_FOUND"
    EX_FORBIDDEN = "EX_FORBIDDEN"
    EX_WEBSOCKET_ERROR = "EX_WEBSOCKET_ERROR"
    EX_TASK_EXEC_ERROR = "EX_TASK_EXEC_ERROR"


class ErrorMessages(Enum):
    DEFAULT_MESSAGE = "Произошла ошибка при выполнении действия. Попробуй выполнить действие позже"


@dataclass
class AppError(Exception):
    # HTTP код ответа
    status_code: int = 500
    # Текстовый код ошибки
    error: str = ErrorCodes.EX_UNKNOWN_ERROR.value
    # Машиночитаемая дополнительная информация об ошибке,
    # например структура с детальной информацией об ошибках валидации от pydantic
    detail: Optional[Any] = None
    # Текстовое сообщение об ошибке
    message: Optional[str] = ErrorMessages.DEFAULT_MESSAGE.value
    # Заголовки ответа, добавлено для совместимости с fastapi.HTTPException
    headers: Optional[Dict[str, str]] = None
    # Нужно ли логировать ошибку.
    log: bool = True

    def get_data(self) -> Dict[str, Any]:
        data = asdict(self)

        data.pop("status_code", None)
        data.pop("headers", None)
        data.pop("log", None)
        data.pop("detail", None)

        if self.detail:
            data["detail"] = self.detail
        if self.__cause__:
            data["reason"] = repr(self.__cause__)

        return data

    def __str__(self):
        return json.dumps(self.get_data(), ensure_ascii=False)


@dataclass
class WebsocketError(AppError):
    status_code: int = 503
    error: str = ErrorCodes.EX_WEBSOCKET_ERROR.value
    message: Optional[str] = ErrorMessages.DEFAULT_MESSAGE.value

    log: bool = True


class CheckPostponedError(AppError):
    def __init__(self, cancel_postponement):
        self.cancel_postponement = cancel_postponement

    status_code: int = 202
    log: bool = False

    def get_data(self) -> Dict[str, Any]:
        return {"cancelPostponement": self.cancel_postponement}


@dataclass
class TaskError(AppError):
    error: str = ErrorCodes.EX_TASK_EXEC_ERROR.value


@dataclass
class HttpError(AppError):
    log: bool = False


@dataclass
class ValidationError(HttpError):
    status_code: int = 400
    error: str = ErrorCodes.EX_VALIDATION_ERROR.value
    message: Optional[str] = ErrorMessages.DEFAULT_MESSAGE.value


@dataclass
class ForbiddenError(HttpError):
    status_code: int = 403
    error: str = ErrorCodes.EX_FORBIDDEN.value
    message: Optional[str] = ErrorMessages.DEFAULT_MESSAGE.value


@dataclass
class IllegalArgumentError(HttpError):
    status_code: int = 400
    error: str = ErrorCodes.EX_ILLEGAL_ARGUMENT.value
    message: Optional[str] = ErrorMessages.DEFAULT_MESSAGE.value


@dataclass
class NotFoundError(HttpError):
    status_code: int = 404
    error: str = ErrorCodes.EX_NOT_FOUND.value
    message: Optional[str] = ErrorMessages.DEFAULT_MESSAGE.value


@dataclass
class MethodNotAllowedError(HttpError):
    status_code: int = 405
    error: str = ErrorCodes.EX_VALIDATION_ERROR.value
    message: Optional[str] = ErrorMessages.DEFAULT_MESSAGE.value


_CODE_TO_CLASS_MAP = {
    **{422: ValidationError},
    **{cls.status_code: cls for cls in [ValidationError, ForbiddenError, NotFoundError, MethodNotAllowedError]},
}
