
def sql_parse_error_message(ex: str) -> str:
    """
    Парсит сообщение об ошибке по типу SQL
    """
    error = ex.args[0].split(':')[-1].strip()
    return error
