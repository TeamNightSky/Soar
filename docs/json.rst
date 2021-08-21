JSON structures
******************

API
====

User
-----

.. code_block:: json

    {
        "username": username,
        "password": sha256 hex digest,
        "created-at": time,
        "friends": list of usernames,
        "friend-reqs": inbound friend requests,
        "logins": list of logins
    }


Channel
--------

.. code_block:: json

    {
        "name": channel name,
        "scope": public, dm, personal, private,
        "public": bool,
        "members": [],
        "creator": user,
        "attrs": empty dict (for the future),
        "created-at": time,
        "message-tag": creator:channelname,
        "parent": server id, else null,
        "roles": unused, will eventually be a dict
    }

Message
--------

.. code_block:: json

    {
        "channel-tag": channel tag,
        "sender": user,
        "timestamp": time,
        "content": message
    }
