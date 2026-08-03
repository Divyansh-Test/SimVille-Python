# interface/camera.py
class Camera:
    def __init__(self, viewport_width, viewport_height, map_width_pixels, map_height_pixels):
        self.x = 0
        self.y = 0
        self.width = viewport_width
        self.height = viewport_height
        self.map_width = map_width_pixels
        self.map_height = map_height_pixels

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.x = max(0, min(self.x, self.map_width - self.width))
        self.y = max(0, min(self.y, self.map_height - self.height))

    def update_target(self, target_x_pixels, target_y_pixels):
        self.x = target_x_pixels - (self.width // 2)
        self.y = target_y_pixels - (self.height // 2)
        self.x = max(0, min(self.x, self.map_width - self.width))
        self.y = max(0, min(self.y, self.map_height - self.height))
