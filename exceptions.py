import exceptions

class Error(Exception):
    """
    Base class for other exceptions
    """
    pass

class tooManyPlayersError(Error):
    """
    Raised when there are too many players entered
    """
    pass

class zeroPlayersError(Error):
    """
    Raised when 0 is entered as number of players
    """
    pass

class zeroDecksError(Error):
    """
    Raised when 0 is entered as number of decks
    """
    pass

class tooManyDecksError(Error):
    """
    Raised when there are too many decks entered
    """
    pass
