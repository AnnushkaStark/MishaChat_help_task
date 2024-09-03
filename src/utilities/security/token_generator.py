from calendar import timegm
from datetime import datetime, timedelta

from jose import jwt

from schemas.token import TokenPayload


def create_access_token(
    data: dict,
    secret_key: str,
    algorithm: str,
    expires_delta: timedelta | None = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def extract_token_payload(
    token: str, secret_key: str, algorithm: str, check_expired: bool = False
) -> TokenPayload | None:
    try:
        payload = jwt.decode(token, secret_key, algorithm)
    except Exception as er:  # noqa: F841
        return None

    if check_expired:
        exp = payload["exp"]
        now = timegm(datetime.datetime.utcnow().utctimetuple())
        if now > exp:
            return None

    return TokenPayload(**payload["subject"])