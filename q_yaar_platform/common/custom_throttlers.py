from rest_framework.throttling import AnonRateThrottle


class TokenLessAPIThrottle(AnonRateThrottle):
    scope = "token-less-url"


class TokenLessAuthAPIThrottleBurst(AnonRateThrottle):
    # Authentication related tokenless calls
    # Finding Users exist
    # Gettig OTPs etc.
    # These shall be severly throttled, but may be slighly more allowed than anon throttling.
    scope = "token-less-auth-url-burst"


class TokenLessAuthAPIThrottleSustained(AnonRateThrottle):
    # Authentication related tokenless calls
    # Finding Users exist
    # Gettig OTPs etc.
    # These shall be severly throttled, but may be slighly more allowed than anon throttling.
    scope = "token-less-auth-url-sustained"
