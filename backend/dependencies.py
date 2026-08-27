from typing import Optional
from fastapi import Header
from security import decode_access_token

async def get_optional_user(auth: Optional[str] = Header(None)) -> Optional[str]:
    if auth is None:
        return None # no header -> guest
    
    scheme, _, token = auth.partition(" ")

    if scheme.lower != "bearer" or not token:
        return None # invalid header -> guest

    return decode_access_token(token)