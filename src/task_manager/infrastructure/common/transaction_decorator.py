from functools import wraps
from typing import Any, Callable
import logging

logger = logging.getLogger(__name__)

def transactional(func: Callable) -> Callable:
    """
    Декоратор для управления транзакциями базы данных.
    Автоматически открывает соединение, управляет commit/rollback и закрывает соединение.
    """
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        conn = None
        try:
            conn = self.get_connection()
            kwargs['conn'] = conn
            result = await func(self, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Transaction error in {func.__name__}: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    return wrapper
