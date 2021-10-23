class Ponto:
    def __init__(self, x: float, y: float):
        self.x = round(x, 3)
        self.y = round(y, 3)

    def __str__(self):
        return f"{(self.x, self.y)}"

    def __repr__(self):
        return f"{(self.x, self.y)}"

    def __call__(self):
        return (self.x, self.y)

    def __gt__(self, max_range):
        if isinstance(max_range, float) or isinstance(max_range, int):
            if self.x > max_range or self.y > max_range:
                return True
        return False

    def __eq__(self, p2):
        if isinstance(p2, Ponto):
            if p2.x == self.x and p2.y == self.y:
                return True
        return False
