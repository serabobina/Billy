from modules import Log
from datetime import datetime
from modules import Configuration


def getTime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get():
    """
    Return users {ID: {"language": "eng", 
                    "permissions": {"allowed": [], "forbidden": []}}}
    """

    configuration = Configuration.get()

    users = configuration['Users']

    return users


def check(message, permission: str):
    users = get()

    id = str(message.from_user.id)

    is_valid_user = check_permission(users, id, permission)

    if is_valid_user:
        Log.add(message, getTime(), "Successfull", permission)
    else:
        Log.add(message, getTime(), " Forbidden ", permission)

    return is_valid_user


def check_permission(users, id, permission):
    if id not in users.keys():
        return 0

    parent = getParent(permission)
    permission_type = getType(parent, permission)

    allowed = users[id]['permissions']["allowed"]
    forbidden = users[id]['permissions']["forbidden"]

    if permission_type == 'PARENT':
        # 1. if Parent/permission in allowed or Parent in allowed
        for perm in allowed:
            perm_parent = getParent(perm)

            if perm_parent == parent:
                return 1

        # 2. if Parent in forbidden
        if parent in forbidden:
            return 0

        # 3. if ALL in allowed
        if 'ALL' in allowed:
            return 1

        return 0

    if permission_type == 'PERMISSION':
        # 1. if Permission in forbidden
        if permission in forbidden:
            return 0

        # 2. if Permission in allowed
        if permission in allowed:
            return 1

        # 3. if Parent in allowed
        if parent in allowed:
            return 1

        # 4. if Parent in forbidden
        if parent in forbidden:
            return 0

        # 5. if ALL in allowed
        if 'ALL' in allowed:
            return 1

        return 0


def update(users):
    configuration = Configuration.get()

    configuration['Users'] = users

    Configuration.update(configuration)


def add(new_permissions):
    users = get()

    id, permissions = new_permissions[0], new_permissions[1]

    if id in users:
        users[id]['permissions'] = permissions
    else:
        users[id] = {'language': 'eng', 'permissions': permissions}

    update(users)


def getParent(permission):
    parent = permission
    if '/' in permission:
        parent = '/'.join(permission.split('/')[0:-1])
    return parent


def getType(parent, permission):
    if parent == permission:
        return 'PARENT'
    else:
        return 'PERMISSION'
