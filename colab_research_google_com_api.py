import base64
import ctypes
import hashlib
import json
import random
import re
import string
import time
import typing

import requests
import requests.cookies

# Global references :
# https://dagshub.com/blog/reverse-engineering-google-colab/

GOOGCRYPTO = ctypes.CDLL("./libgoogcrypto.so")

# COOKIES

cookies_to_dict: typing.Callable[[str], dict] = lambda cookies: dict(
    [cookie.split("=", 1) for cookie in cookies.split("; ")]
)

# CCU_INFO

ccu_info: typing.Callable[[requests.Session], dict] = lambda session: json.loads(
    session.get(
        "https://colab.research.google.com/tun/m/ccu-info", params=dict(authuser=0)
    ).text[4:]
)

# SPAPISIDHASH
# References :
# https://gist.github.com/eyecatchup/2d700122e24154fdc985b7071ec7764a
# https://stackoverflow.com/questions/16907352/reverse-engineering-javascript-behind-google-button

craft_sapisidhash: typing.Callable[
    [requests.Session, str], str
] = lambda sessions, origin: (
    lambda timestamp: str(timestamp)
    + "_"
    + hashlib.sha1(
        "{0} {1} {2}".format(
            timestamp,
            sessions.cookies.get("SAPISID" if origin.startswith("https") else "APISID"),
            origin,
        ).encode()
    ).hexdigest()
)(
    int(time.time())
)


# DRIVE API

# XXX: MIGHT CHANGE IN THE FUTURE
DRIVE_API_KEY_REGEX = re.compile(
    r"\\x22drive_api_key\\x22: ?\\x22([^\\]+)\\x22", flags=re.MULTILINE
)

extract_drive_api_key: typing.Callable[
    [requests.Session, str], str | None
] = lambda session, notebook_url: (
    lambda match: match[0] if match is not None and len(match) > 0 else None
)(
    DRIVE_API_KEY_REGEX.findall(
        session.get(notebook_url).text,
    )
)

get_drive_files_references: typing.Callable[
    [
        requests.Session,
        str,
        str,
        typing.Literal["preferences.json", "access_history.json"],
    ],
    dict,
] = lambda session, drive_api_key, sapisidhash, filename: session.get(
    "https://clients6.google.com/drive/v3/files",
    params={
        "q": "name = '{0}'".format(filename),
        "fields": "files(id,headRevisionId)",
        "spaces": "appDataFolder",
        "maxResults": 1,
        "orderBy": "quotaBytesUsed desc",
        "supportsTeamDrives": True,
        "key": drive_api_key,
        "$unique": "gc"
        + str(int("".join([random.choice(string.hexdigits) for _ in range(8)]), 16))[
            1:
        ],
    },
    headers={
        "Authorization": "SAPISIDHASH " + sapisidhash,
        "Origin": "https://colab.research.google.com",
    },
).json()

get_user_about: typing.Callable[
    [requests.Session, str, str], dict
] = lambda session, drive_api_key, sapisidhash: session.get(
    "https://clients6.google.com/drive/v2beta/about",
    params={
        "fields": "user",
        "supportsTeamDrives": True,
        "key": drive_api_key,
        "$unique": "gc"
        + str(int("".join([random.choice(string.hexdigits) for _ in range(8)]), 16))[
            1:
        ],
    },
    headers={
        "Authorization": "SAPISIDHASH " + sapisidhash,
        "Origin": "https://colab.research.google.com",
    },
).json()

get_beta_drive_files_reference: typing.Callable[
    [requests.Session, str, str, str, str | None], dict
] = lambda session, drive_api_key, sapisidhash, notebook_id, revision_id: (
    lambda response: response.json()
    if revision_id is None
    else json.loads(base64.b64decode(response.content).decode())
)(
    session.get(
        "https://clients6.google.com/drive/v2beta/files/" + notebook_id,
        params={
            **(
                {
                    "fields": ",".join(
                        [
                            "resourceKey",
                            "alternateLink",
                            "capabilities/canReadRevisions",
                            "createdDate",
                            "downloadUrl",
                            "fileSize",
                            "headRevisionId",
                            "id",
                            "labels",
                            "mimeType",
                            "originalFilename",
                            "owners",
                            "parents",
                            "properties",
                            "shared",
                            "teamDriveId",
                            "title",
                            "userPermission",
                        ]
                    )
                }
                if revision_id is None
                else {"revisionId": revision_id, "alt": "media"}
            ),
            "supportsTeamDrives": True,
            "key": drive_api_key,
            "$unique": "gc"
            + str(
                int("".join([random.choice(string.hexdigits) for _ in range(8)]), 16)
            )[1:],
        },
        headers={
            "Authorization": "SAPISIDHASH " + sapisidhash,
            "Origin": "https://colab.research.google.com",
            **(
                {"X-Goog-Encode-Response-If-Executable": "base64"}
                if revision_id is not None
                else {}
            ),
        },
    )
)

get_desktop_notification_prompt: typing.Callable[
    [requests.Session, str, str, str], bool
] = lambda session, drive_api_key, sapisidhash, notebook_id: json.loads(
    base64.b64decode(
        session.get(
            "https://clients6.google.com/drive/v2beta/files/" + notebook_id,
            params={
                "alt": "media",
                "supportsTeamDrives": True,
                "key": drive_api_key,
                "$unique": "gc"
                + str(
                    int(
                        "".join([random.choice(string.hexdigits) for _ in range(8)]), 16
                    )
                )[1:],
            },
            headers={
                "Authorization": "SAPISIDHASH " + sapisidhash,
                "Origin": "https://colab.research.google.com",
                "X-Goog-Encode-Response-If-Executable": "base64",
            },
        ).content
    ).decode()
)[
    "desktopNotificationPrompt"
]

get_page_config: typing.Callable[
    [requests.Session, str], list
] = lambda session, notebook_id: (lambda response: json.loads(response[4:]))(
    session.get(
        "https://colab.research.google.com/page-config",
        headers={"Referer": "https://colab.research.google.com/drive/" + notebook_id},
    ).text
)

get_comments_list: typing.Callable[
    [requests.Session, str, str, str], bool
] = lambda session, drive_api_key, sapisidhash, notebook_id: session.get(
    "https://clients6.google.com/drive/v2beta/files/" + notebook_id,
    params={
        "includeDeleted": True,
        "maxResults": 100,
        "updatedMin": "1970-01-01T00:00:00.001Z",
        "supportsTeamDrives": True,
        "key": drive_api_key,
        "$unique": "gc"
        + str(int("".join([random.choice(string.hexdigits) for _ in range(8)]), 16))[
            1:
        ],
    },
    headers={
        "Authorization": "SAPISIDHASH " + sapisidhash,
        "Origin": "https://colab.research.google.com",
        "X-Goog-Encode-Response-If-Executable": "base64",  # XXX: Required, else request is 'insecure', yet JSON is returned at thsi endpoint.
    },
).json()

get_self_app: typing.Callable[
    [requests.Session, str, str], dict
] = lambda session, drive_api_key, sapisidhash: session.get(
    "https://clients6.google.com/drive/v2beta/apps/self",
    params={
        "supportsTeamDrives": True,
        "key": drive_api_key,
        "$unique": "gc"
        + str(int("".join([random.choice(string.hexdigits) for _ in range(8)]), 16))[
            1:
        ],
    },
    headers={
        "Authorization": "SAPISIDHASH " + sapisidhash,
        "Origin": "https://colab.research.google.com",
        "X-Goog-Encode-Response-If-Executable": "base64",  # XXX: Required, else request is 'insecure', yet JSON is returned at thsi endpoint.
    },
).json()

put_beta_drive_files: typing.Callable[
    [requests.Session, str, str, str, dict], dict
] = lambda session, drive_api_key, sapisidhash, notebook_id, body: (
    session.put(
        "https://clients6.google.com/drive/v2beta/files/" + notebook_id,
        params={
            "modifiedDateBehavior": "no_change",
            "updateViewedDate": True,
            "alt": "json",
            "supportsTeamDrives": True,
            "key": drive_api_key,
            "$unique": "gc"
            + str(
                int("".join([random.choice(string.hexdigits) for _ in range(8)]), 16)
            )[1:],
        },
        headers={
            "Authorization": "SAPISIDHASH " + sapisidhash,
            "Origin": "https://colab.research.google.com",
            "X-Goog-Encode-Response-If-Executable": "base64",  # XXX: Required, else request is 'insecure', yet JSON is returned at thsi endpoint.
            "Content-Type": "application/json",
        },
        json=body,
    )
).json()

get_notebooks_list: typing.Callable[
    [requests.Session, str, str, str], dict
] = lambda session, drive_api_key, sapisidhash, file_access_id: (
    json.loads(
        base64.b64decode(
            session.get(
                "https://clients6.google.com/drive/v2beta/files/" + file_access_id,
                params={
                    "alt": "media",
                    "supportsTeamDrives": True,
                    "key": drive_api_key,
                    "$unique": "gc"
                    + str(
                        int(
                            "".join(
                                [random.choice(string.hexdigits) for _ in range(8)]
                            ),
                            16,
                        )
                    )[1:],
                },
                headers={
                    "Authorization": "SAPISIDHASH " + sapisidhash,
                    "Origin": "https://colab.research.google.com",
                    "X-Goog-Encode-Response-If-Executable": "base64",
                },
            ).content
        ).decode()
    )
)

get_notebook_revisions: typing.Callable[
    [requests.Session, str, str, str], dict
] = lambda session, drive_api_key, sapisidhash, notebook_id: (
    session.get(
        "https://clients6.google.com/drive/v2beta/files/" + notebook_id + "/revisions",
        params={
            "maxResults": 1000,
            "supportsTeamDrives": True,
            "key": drive_api_key,
            "$unique": "gc"
            + str(
                int("".join([random.choice(string.hexdigits) for _ in range(8)]), 16)
            )[1:],
        },
        headers={
            "Authorization": "SAPISIDHASH " + sapisidhash,
            "Origin": "https://colab.research.google.com",
            "X-Goog-Encode-Response-If-Executable": "base64",  # XXX: Required, else request is 'insecure', yet JSON is returned at thsi endpoint.
        },
    ).json()
)

get_notebook_permissions: typing.Callable[
    [requests.Session, str, str, str], dict
] = lambda session, drive_api_key, sapisidhash, notebook_id: (
    session.get(
        "https://clients6.google.com/drive/v2beta/files/"
        + notebook_id
        + "/permissions",
        params={
            "supportsTeamDrives": True,
            "key": drive_api_key,
            "$unique": "gc"
            + str(
                int("".join([random.choice(string.hexdigits) for _ in range(8)]), 16)
            )[1:],
        },
        headers={
            "Authorization": "SAPISIDHASH " + sapisidhash,
            "Origin": "https://colab.research.google.com",
            "X-Goog-Encode-Response-If-Executable": "base64",  # XXX: Required, else request is 'insecure', yet JSON is returned at thsi endpoint.
        },
    ).json()
)

get_files_with_included_embedded_items: typing.Callable[
    [requests.Session, str, str, str], list
] = lambda session, drive_api_key, sapisidhash, notebook_id: (
    session.get(
        "https://clients6.google.com/drive/v2beta/files",
        params={
            "includeEmbeddedItems": True,
            "q": 'embeddingParent = "{0}" and title = "tagged-revisions"'.format(
                notebook_id
            ),
            "fields": "items(id)",
            "orderBy": "modifiedDate desc",
            "supportsTeamDrives": True,
            "key": drive_api_key,
            "$unique": "gc"
            + str(
                int("".join([random.choice(string.hexdigits) for _ in range(8)]), 16)
            )[1:],
        },
        headers={
            "Authorization": "SAPISIDHASH " + sapisidhash,
            "Origin": "https://colab.research.google.com",
            "X-Goog-Encode-Response-If-Executable": "base64",  # XXX: Required, else request is 'insecure', yet JSON is returned at thsi endpoint.
        },
    ).json()
)


def get_assign_nbh_token(notebook_id: str) -> str:
    file = [["fileId"], [notebook_id]]
    json_data = json.dumps(file, separators=(",", " "))
    c_json_data = json_data.encode("utf-8")

    GOOGCRYPTO.hash_json_file_object.argtypes = [ctypes.c_char_p]
    GOOGCRYPTO.hash_json_file_object.restype = ctypes.POINTER(ctypes.c_ubyte)

    GOOGCRYPTO.free_hash.argtypes = [ctypes.POINTER(ctypes.c_ubyte)]

    result = GOOGCRYPTO.hash_json_file_object(c_json_data)
    result_string = ctypes.string_at(result).decode("utf-8")

    GOOGCRYPTO.free_hash(result)

    return result_string


get_assign_tunnel: typing.Callable[
    [requests.Session, str, str], dict
] = lambda session, notebook_id: (
    (lambda response: json.loads(response[4:]))(
        session.get(
            "https://colab.research.google.com/tun/m/assign",
            params={
                "authuser": 0,
                "match_any": 1,
                "nbh": get_assign_nbh_token(notebook_id=notebook_id),
            },
        ).text
    )
)

get_notebook_ws_session: typing.Callable[
    [requests.Session, str, str, str], dict
] = lambda session, endpoint, notebook_name, notebook_id: (
    session.post(
        "https://colab.research.google.com/tun/m/" + endpoint + "/api/sessions",
        params={
            "authuser": 0,
        },
        json={
            "name": notebook_name,
            "path": "fileId=" + notebook_id,
            "type": "notebook",
            "kernel": {"name": "python3"},
        },
        headers={
            "Origin": "https://colab.research.google.com",
            "X-Colab-Tunnel": "Google"
        }
    ).json()
)

# get_sid_socketio: typing.Callable[[requests.Session, str, str], str] = lambda session, endpoint, t: (
#     session.get("https://colab.research.google.com/tun/m/" + endpoint + "/socket.io",
#         params={
#             "authuser": 0,
#             "EIO": 3,
#             "transport": "polling",
#             "t": t
#         },
#         headers={
#             "Origin": "https://colab.research.google.com",
#             "X-Colab-Tunnel": "Google"
#         }
#     ).text
# )