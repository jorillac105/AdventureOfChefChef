class Base: 
   def __init__(self, xPos, yPos, width, height, xCorrection, yCorrection):
      self.topRight = [xPos + width -  xCorrection, yPos + yCorrection]
      self.bottomLeft = [xPos + xCorrection, yPos + height] 

      #xCor/yCor
      #10/30 for rats
      #13/60 for chef
      #0/0 for objects/structures