from wisekmapy.wisekma import Wisekma


class SingletonInstane():
    _instance = None

    @classmethod
    def _get_instance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._get_instance
        return cls._instance


class WisekmaInstance(Wisekma, SingletonInstane):
    pass


if __name__ == '__main__':
    wisekma = WisekmaInstance.instance()
    res = wisekma.pos('안녕하세요')
    print(res)
