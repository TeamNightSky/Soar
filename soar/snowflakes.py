
def channel_snowflake(name, creator, time):
    return str(int(time)) + str(int(name) + int(creator))[:10]


def user_snowflake(username, time):
    return (str(int(time)) + str(int(username)))[:10]
