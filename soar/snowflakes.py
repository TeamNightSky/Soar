
def board_snowflake(title, owner, time):
    return str(int(time)) + str(int(title) + int(owner))[:10]


def creation_snowflake(title, author, time):
    return str(int(time)) + str(int(title) + int(author))[:10]


def user_snowflake(username, time):
    return (str(int(time)) + str(int(username)))[:10]
