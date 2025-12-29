from urllib.parse import quote


def include_user_info_headers(headers, user):
    return {
        **headers,
        "X-ANSWERAI-User-Name": quote(user.name, safe=" "),
        "X-ANSWERAI-User-Id": user.id,
        "X-ANSWERAI-User-Email": user.email,
        "X-ANSWERAI-User-Role": user.role,
    }
