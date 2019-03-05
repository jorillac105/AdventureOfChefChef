class MouseBox:
    def __init__(self, x, y, w, h, title, cursorPos):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.title = title
        self.cursorPos = cursorPos

    def checkEvent(self, mX, mY):
        if (( mX > self.x ) and ( mX < self.x + self.w ) and ( mY > self.y ) and ( mY < self.y + self.h)):
            return self.title

    def checkMotion(self, mX, mY):
        return (( mX > self.x ) and ( mX < self.x + self.w ) and ( mY > self.y ) and ( mY < self.y + self.h))
