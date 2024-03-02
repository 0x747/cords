def choose_default_avatar(id):
    """ Chooses default avatar based on the modulo of the last two digits of a user's ID """

    avatars = ['default/blue.png', 'default/green.png', 'default/yellow.png', 'default/orange.png', 'default/pink.png', 'default/red.png']
    idx = (id % 100) % 6

    return avatars[idx]