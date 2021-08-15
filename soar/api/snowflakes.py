
def channel(name, creator, time):
    return str(int(time)) + str(int(name) + int(creator))[:10]
