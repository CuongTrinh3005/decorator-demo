from app.main.util.decorators import singleton


@singleton
class Person:
    def __init__(self, name):
        self.name = name


if __name__ == "__main__":
    p1 = Person('liam')
    p2 = Person('cuong')
    print('First id: ', id(p1))
    print('Second id: ', id(p2))
    assert p1 is p2
