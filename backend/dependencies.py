from typing import Optional
from fastapi import Header
from security import decode_access_token

async def get_optional_user(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """ Header format: Bearer <token> """
    if authorization is None:
        return None # no header -> guest

    scheme, _, token = authorization.partition(" ") # scheme, separator, token

    if scheme.lower() != "bearer" or not token:
        return None # invalid header -> guest

    return decode_access_token(token)