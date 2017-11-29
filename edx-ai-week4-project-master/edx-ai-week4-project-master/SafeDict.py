class SafeDict(dict):
    def __missing__(self, key):
        return None