class Bishop:
    def __init__(self, x = None, y = None, path = None, square = None):
        self.x = x
        self.y = y
        self.image_path = path
        self.image = None
        self.square = square
        self.height = 80
        self.width = 96