import re
from uuid import UUID


def extract_params(body: str) -> list[str]:
    res = []
    body = re.sub(r"[^\w\s]", "", body)
    for el in body.split():
        try:
            int(el)
            res.append(el)
        except ValueError:
            continue
        else:
            try:
                UUID(el)
                res.append(el)
            except ValueError:
                continue
    return res
