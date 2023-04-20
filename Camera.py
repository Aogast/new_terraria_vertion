
WIDTH, HEIGHT = (1024, 760)
class Camera:
    """The class is responsible for finding the hero in the center of the screen"""
    def __init__(self) -> None:
        self.dx = 0
        self.dy = 0

    def apply(self, obj) -> None:
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target) -> None:
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)