class StringBuilder:
    def __init__(self):
        self.text = ""

    def __add__(self, other):
        self.text += other

    def __iadd__(self, other):
        self.text += other
        return self

    def __str__(self):
        return self.text