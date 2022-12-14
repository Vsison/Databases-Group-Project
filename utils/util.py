def safe_int(input: str, default: int) -> int:
    """
        returns int
    """
    try:
        if (input.isdigit()):
            return int(str)
        else:
            return default
    except:
        return default