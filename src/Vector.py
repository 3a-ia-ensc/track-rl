class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x * other, self.y * other)
        elif isinstance(other, Vector):
            return Vector(self.x * other.x + self.y * other.y)
        else:
            raise TypeError('Alors... Non!')

    def __eq__(self, other):
        if isinstance(other, tuple):
            return other[0] == self.x and other[1] == self.y
        elif isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        else:
            raise TypeError('N\'importe quoi...')

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError('Faut pas pousser mémé là...')
