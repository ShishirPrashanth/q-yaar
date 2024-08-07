from account.models import PlatformUser

from .constants import UserRolesType


def get_base_jwt_payload(user: PlatformUser, profile_role: str = None, profile_suspended: bool = False) -> dict:
    payload = {
        "user_id": user.pk,
        "is_active": user.is_active,
        "is_suspended": user.is_suspended,
        "email": user.email,
        "phone": user.phone,
    }

    if profile_role:
        payload["profile"] = {"role": profile_role, "suspended": profile_suspended}
    return payload


def get_role_from_request_auth(request_auth: dict) -> tuple[UserRolesType | None, bool]:
    role: UserRolesType | None = None
    suspended: bool = False

    if request_auth and "profile" in request_auth and request_auth["profile"]["role"]:
        profile = request_auth["profile"]
        role = UserRolesType.tokentype_from_string(profile["role"])
        suspended = profile["suspended"]

    return role, suspended
