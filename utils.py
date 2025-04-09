from datetime import datetime, date


def json_serialize(obj):
    if isinstance(obj, datetime):
        return obj.astimezone().isoformat()
    elif isinstance(obj, date):
        return obj.astimezone().isoformat()
    else:
        return str(obj, encoding="utf-8")
