class TableDoesNotExistError(ValueError):
    def __init__(self):
        super().__init__()
        raise ValueError('Specified table does not exist.')
