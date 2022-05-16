class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwds):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwds)

        # return super().__call__(*args, **kwds)
        return cls._instances[cls]