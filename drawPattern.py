import math
from PIL import Image, ImageTk, ImageDraw

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

def eraseSelectedCropping(pixelList, bc, img):
  for i in pixelList:
    img.putpixel(i[0], bc)

def cropping(startPoint, endPoint, bc, img):
  pixelList = []

  x0 = startPoint[0]
  y0 = startPoint[1]
  x1 = endPoint[0]
  y1 = endPoint[1]

  if y0 > y1:
    y0, y1 = y1, y0
  if x0 > x1:
    x0, x1 = x1, x0   

  for j in range(y0, y1):
    for i in range(x0, x1):
      if img.getpixel((i, j)) != bc:
        color = img.getpixel((i, j))
        pixelObj = ((i,j), color)
        pixelList.append(pixelObj)
        img.putpixel((i,j), bc)
  
  return pixelList

def scalling(pixelList, center, scale, img):
  centerX = center[0]
  centerY = center[1]

  # render new pattern based on coordinate of newPoint
  for i in range(0, len(pixelList) - 1):
    pixel = pixelList[i]

    x = centerX + int(round((pixel[0][0] - centerX) * scale[0]))
    y = centerY + int(round((pixel[0][1] - centerY) * scale[1]))

    img.putpixel((x, y), pixel[1])

  scaleImg = ImageTk.PhotoImage(img)
  return scaleImg

def curve(p0, p1, p2, color, img):
  t = 0
  while t < 1:
    x = int(p0[0]*(1-t)**2 + 2*(1-t)*t*p1[0] + p2[0]*t**2)
    y = int(p0[1]*(1-t)**2 + 2*(1-t)*t*p1[1] + p2[1]*t**2)
    img.putpixel((x,y), color)
    t = t + 0.001
  curveImg = ImageTk.PhotoImage(img)
  return curveImg

def drawEclipse(centerPoint, x, y, color, img):
  img.putpixel((centerPoint[0]+x, centerPoint[1]+y), color);
  img.putpixel((centerPoint[0]-x, centerPoint[1]+y), color);
  img.putpixel((centerPoint[0]+x, centerPoint[1]-y), color);
  img.putpixel((centerPoint[0]-x, centerPoint[1]-y), color);

def eclipseMidPoint(centerPoint, rx, ry, color, img):
  rxSq = rx ** 2
  rySq = ry ** 2
  x = 0
  y = ry
  px = 0
  py = 2 * rxSq * y
  drawEclipse(centerPoint, x, y, color, img)
  p = rySq - (rxSq * ry) + (0.25 * rxSq)
  while px < py:
    x = x + 1
    px = px + 2*rySq
    if p < 0:
      p = p + rySq + px
    else:
      y = y - 1
      py = py - 2*rxSq
      p = p + rySq + px - py
    drawEclipse(centerPoint, x, y, color, img)

  p = rySq*(x+0.5)*(x+0.5) + rxSq*(y-1)*(y-1) - rxSq*rySq
  while y > 0:
    y = y - 1
    py = py - 2 * rxSq;
    if p > 0:
      p = p + rxSq - py;
    else:
      x = x + 1
      px = px + 2 * rySq;
      p = p + rxSq - py + px;
    drawEclipse(centerPoint, x, y, color, img);

  eclipseImg = ImageTk.PhotoImage(img)
  return eclipseImg

def flipHorizontal(startPoint, endPoint, center, bc, img):
  pixelList = []

  x0 = startPoint[0]
  y0 = startPoint[1]
  x1 = endPoint[0]
  y1 = endPoint[1]

  if y0 > y1:
    y0, y1 = y1, y0
  if x0 > x1:
    x0, x1 = x1, x0   

  for j in range(y0, y1):
    for i in range(x0, x1):
      if img.getpixel((i, j)) != bc:
        color = img.getpixel((i, j))
        pixelObj = ((i,j), color)
        pixelList.append(pixelObj)
        img.putpixel((i,j), bc)    

  # render new pattern based on coordinate of newPoint
  for i in range(0, len(pixelList) - 1):
    pixel = pixelList[i]
    x = pixel[0][0]
    y = 2 * center[1] - pixel[0][1]
    img.putpixel((x, y), pixel[1])

  flipVerticalImg = ImageTk.PhotoImage(img)
  return flipVerticalImg

def flipVertical(startPoint, endPoint, center, bc, img):
  pixelList = []

  x0 = startPoint[0]
  y0 = startPoint[1]
  x1 = endPoint[0]
  y1 = endPoint[1]

  if y0 > y1:
    y0, y1 = y1, y0
  if x0 > x1:
    x0, x1 = x1, x0   

  for j in range(y0, y1):
    for i in range(x0, x1):
      if img.getpixel((i, j)) != bc:
        color = img.getpixel((i, j))
        pixelObj = ((i,j), color)
        pixelList.append(pixelObj)
        img.putpixel((i,j), bc)    

  # render new pattern based on coordinate of newPoint
  for i in range(0, len(pixelList) - 1):
    pixel = pixelList[i]
    x = 2 * center[0] - pixel[0][0]
    y = pixel[0][1]
    img.putpixel((x, y), pixel[1])

  flipVerticalImg = ImageTk.PhotoImage(img)
  return flipVerticalImg

def shearing(pixelList, center, shear, img):
  centerX = center[0]
  centerY = center[1]

  if shear[0] != 0:  # shearing x axis
#     for i in range(0, len(pixelList) - 1):
#       pixel = pixelList[i]
# #      deltaX = pixel[0][0] - centerX
#       deltaY = pixel[0][1] - centerY

#       x = int(round(pixel[0][0] + 0.5 * deltaY))
#       y = pixel[0][1]

    print 'go x axis'
    for i in range(0, len(pixelList) - 1):
      pixel = pixelList[i]
      x = int(round((pixel[0][0]) + (pixel[0][1]) * (0.95)))
      y = int(round((pixel[0][1]) ))

    img.putpixel((x, y), pixel[1])

  else:   # shearing y axis
    # for i in range(0, len(pixelList) - 1):
    #   pixel = pixelList[i]
    #   deltaX = pixel[0][0] - centerX
    #   deltaY = pixel[0][1] - centerY

    #   x = pixel[0][0]
    #   y = centerY + deltaY + shear[1] * deltaX

    #   img.putpixel((x, y), pixel[1])

    print 'go y axis'
    for i in range(0, len(pixelList) - 1):
      pixel = pixelList[i]
      x = int(round((pixel[0][0]) + (pixel[0][1]) * (0.95)))
      y = int(round((pixel[0][1]) ))

    img.putpixel((x, y), pixel[1])

  shearImg = ImageTk.PhotoImage(img)
  return shearImg

def moveRotation(pixelList, center, alpha, bc, img):
  for i in range(0, len(pixelList) - 1):
    pixel = pixelList[i]

    centerX = center[0]
    centerY = center[1]

    x = centerX + int(math.cos(alpha) * (pixel[0][0] - centerX) - math.sin(alpha) * (pixel[0][1] - centerY ))
    y = centerY + int(math.sin(alpha) * (pixel[0][0] - centerX) + math.cos(alpha) * (pixel[0][1] - centerY ))

    img.putpixel((x, y), pixel[1])

  roateImg = ImageTk.PhotoImage(img)
  return roateImg

def moveTransition(pixelList, newPoint, bc, img):
  deltaX = newPoint[0] - pixelList[0][0][0]
  deltaY = newPoint[1] - pixelList[0][0][1]

  for i in range(0, len(pixelList) - 1):
    pixel = pixelList[i]
    img.putpixel((pixel[0][0] + deltaX, pixel[0][1] + deltaY), pixel[1])

  transitImg = ImageTk.PhotoImage(img)
  return transitImg

def pencil(previousPoint, pointNow, color, img):
    draw = ImageDraw.Draw(img)    
    draw.line((previousPoint, pointNow), color)

    pencilImg = ImageTk.PhotoImage(img)
    return pencilImg

def eraser(previousPoint, pointNow, color, img):
    draw = ImageDraw.Draw(img)    
    draw.rectangle([previousPoint, pointNow], fill=color)

    eraserImg = ImageTk.PhotoImage(img)
    return eraserImg

def diamond(startPoint, endPoint, color, img, defaultState):
    a = (endPoint[1] - startPoint[1]) / float(2)
    b = (endPoint[0] - startPoint[0]) / float(2)    

    A = (int(startPoint[0] + b), int(startPoint[1]))
    B = (int(startPoint[0]), int(startPoint[1] + a))
    C = (int(startPoint[0] + b), int(startPoint[1]) + 2*a)
    D = (int(startPoint[0] + 2*b), int(startPoint[1] + a))

    draw = ImageDraw.Draw(img)
    
    draw.line((A, B), color)
    draw.line((B, C), color)
    draw.line((C, D), color)
    draw.line((D, A), color)

    triangleImg = ImageTk.PhotoImage(img)
    return triangleImg

def polygonFive(startPoint, endPoint, color, img, defaultState):
    a = (endPoint[1] - startPoint[1]) / float(2)
    b = (endPoint[0] - startPoint[0]) / float(2)    

    A = (int(startPoint[0] + b), int(startPoint[1]))
    B = (int(startPoint[0]), int(startPoint[1] + a))
    C = (int(startPoint[0] + b/2), int(startPoint[1]) + 2*a)
    D = (int(startPoint[0] + 3*b/2), int(startPoint[1] + 2*a))
    E = (int(startPoint[0] + 2*b), int(startPoint[1] + a))

    draw = ImageDraw.Draw(img)
    
    draw.line((A, B), color)
    draw.line((B, C), color)
    draw.line((C, D), color)
    draw.line((D, E), color)
    draw.line((E, A), color)

    triangleImg = ImageTk.PhotoImage(img)
    return triangleImg

def polygonSix(startPoint, endPoint, color, img , defaultState):
    a = (endPoint[1] - startPoint[1]) / float(2)
    b = (endPoint[0] - startPoint[0]) / float(2)    

    A = (int(startPoint[0] + b), int(startPoint[1]))
    B = (int(startPoint[0]), int(startPoint[1] + a/2))
    C = (int(startPoint[0]), int(startPoint[1]) + 3*a/2)
    D = (int(startPoint[0] + b), int(startPoint[1] + 2*a))
    E = (int(startPoint[0] + 2*b), int(startPoint[1] + 3*a/2))
    F = (int(startPoint[0] + 2*b), int(startPoint[1] + a/2))

    draw = ImageDraw.Draw(img)
    
    draw.line((A, B), color)
    draw.line((B, C), color)
    draw.line((C, D), color)
    draw.line((D, E), color)
    draw.line((E, F), color)
    draw.line((F, A), color)

    triangleImg = ImageTk.PhotoImage(img)
    return triangleImg

def starFour(startPoint, endPoint, color, img, defaultState):
    a = (endPoint[1] - startPoint[1]) / float(2)
    b = (endPoint[0] - startPoint[0]) / float(2)    

    A = (int(startPoint[0] + b), int(startPoint[1]))
    B = (int(startPoint[0] + 3*b/4), int(startPoint[1] + 3*a/4))
    C = (int(startPoint[0]), int(startPoint[1]) + a)
    D = (int(startPoint[0] + 3*b/4), int(startPoint[1] + 1.25*a))
    E = (int(startPoint[0] + b), int(startPoint[1] + 2*a))
    F = (int(startPoint[0] + 1.25*b), int(startPoint[1] + 1.25*a))
    G = (int(startPoint[0] + 2*b), int(startPoint[1] + a))
    H = (int(startPoint[0] + 1.25*b), int(startPoint[1] + 3*a/4))

    draw = ImageDraw.Draw(img)
    
    draw.line((A, B), color)
    draw.line((B, C), color)
    draw.line((C, D), color)
    draw.line((D, E), color)
    draw.line((E, F), color)
    draw.line((F, G), color)
    draw.line((G, H), color)
    draw.line((H, A), color)

    triangleImg = ImageTk.PhotoImage(img)
    return triangleImg

def starSix(startPoint, endPoint, color, img, defaultState):
    a = (endPoint[1] - startPoint[1]) / float(2)
    b = (endPoint[0] - startPoint[0]) / float(2)    

    A = (int(startPoint[0] + b), int(startPoint[1]))
    B = (int(startPoint[0] + 3*b/4), int(startPoint[1] + a/2))
    C = (int(startPoint[0]), int(startPoint[1]) + a/2)
    D = (int(startPoint[0] + b/2), int(startPoint[1] + a))
    E = (int(startPoint[0]), int(startPoint[1] + 1.5*a))
    F = (int(startPoint[0] + 3*b/4), int(startPoint[1] + 1.5*a))
    G = (int(startPoint[0] + b), int(startPoint[1] + 2*a))
    H = (int(startPoint[0] + 1.25*b), int(startPoint[1] + 1.5*a))
    I = (int(startPoint[0] + 2*b), int(startPoint[1] + 1.5*a))
    J = (int(startPoint[0] + 1.5*b), int(startPoint[1] + a))
    K = (int(startPoint[0] + 2*b), int(startPoint[1] + a/2))
    L = (int(startPoint[0] + 1.25*b), int(startPoint[1] + a/2))

    draw = ImageDraw.Draw(img)
    
    draw.line((A, B), color)
    draw.line((B, C), color)
    draw.line((C, D), color)
    draw.line((D, E), color)
    draw.line((E, F), color)
    draw.line((F, G), color)
    draw.line((G, H), color)
    draw.line((H, I), color)
    draw.line((I, J), color)
    draw.line((J, K), color)
    draw.line((K, L), color)
    draw.line((L, A), color)

    triangleImg = ImageTk.PhotoImage(img)
    return triangleImg

def triangle(startPoint, endPoint, color, img, defaultState):
    a = (endPoint[1] - startPoint[1]) / float(2)
    b = (endPoint[0] - startPoint[0]) / float(2)    

    A = (int(startPoint[0]), int(endPoint[1]))
    B = (int(endPoint[0]), int(endPoint[1]))
    C = (int(startPoint[0] + b), int(startPoint[1]))

    draw = ImageDraw.Draw(img)
    
    draw.line((A, B), color)
    draw.line((B, C), color)
    draw.line((C, A), color)

    triangleImg = ImageTk.PhotoImage(img)
    return triangleImg

def triangleSquare(startPoint, endPoint, color, img, defaultState):
    a = (endPoint[1] - startPoint[1]) / float(2)
    b = (endPoint[0] - startPoint[0]) / float(2)    

    A = (int(startPoint[0]), int(startPoint[1]))
    B = (int(startPoint[0]), int(endPoint[1]))
    C = (int(endPoint[0]), int(endPoint[1]))

    draw = ImageDraw.Draw(img)
    
    draw.line((A, B), color)
    draw.line((B, C), color)
    draw.line((C, A), color)

    triangleSquareImg = ImageTk.PhotoImage(img)
    return triangleSquareImg

def star(startPoint, endPoint, color, img, defaultState):
    a = (endPoint[1] - startPoint[1]) / float(2)
    b = (endPoint[0] - startPoint[0]) / float(2)
    
    A  = (int(startPoint[0] + b), int(startPoint[1]))
    A1 = (int(startPoint[0] + 3*b/4), int(startPoint[1] + 3*a/4))
    A2 = (int(startPoint[0]), int(0.8*a + startPoint[1]))
    A3 = (int(startPoint[0] + b*0.65), int(startPoint[1] + 1.25*a))
    A4 = (int(startPoint[0] + b/2), int(startPoint[1] + 2*a))

    B = (int(startPoint[0] + b), int(1.25*a + startPoint[1]))
    B1 = (int(startPoint[0] + 1.5*b), int(2*a + startPoint[1]))
    B2 = (int(startPoint[0] + 1.35*b), int(1.25*a + startPoint[1]))
    B3 = (int(startPoint[0] + 2*b), int(0.8*a + startPoint[1]))
    B4 = (int(startPoint[0] + 1.25*b), int(3*a/4 + startPoint[1]))

    draw = ImageDraw.Draw(img)
    
    draw.line((A, A1), color)
    draw.line((A1, A2), color)
    draw.line((A2, A3), color)    
    draw.line((A3, A4), color)
    draw.line((A4, B), color)
    draw.line((B, B1), color)

    draw.line((A, B4), color)
    draw.line((B4, B3), color)
    draw.line((B3, B2), color)
    draw.line((B1, B2), color)

    starImg = ImageTk.PhotoImage(img)
    return starImg

def arrowRight(startPoint, endPoint, color, img, defaultState):
    a = (endPoint[1] - startPoint[1]) / float(2)
    b = (endPoint[0] - startPoint[0]) / float(2)
    
    A1 = (int(startPoint[0]), int(a/2 + startPoint[1]))
    A2 = (int(startPoint[0] + 4*b/3), int(a/2 + startPoint[1]))
    A3 = (int(startPoint[0] + 4*b/3), int(startPoint[1]))

    B1 = (int(startPoint[0]), int(3*a/2 + startPoint[1]))
    B2 = (int(startPoint[0] + 4*b/3), int(3*a/2 + startPoint[1]))
    B3 = (int(startPoint[0] + 4*b/3), int(2*a + startPoint[1]))

    C =  (int(startPoint[0] + 2*b), int(a + startPoint[1]))

    draw = ImageDraw.Draw(img)
    
    draw.line((A1, A2), color)
    draw.line((A2, A3), color)
    draw.line((A3, C), color)    
    draw.line((A1, B1), color)
    draw.line((B1, B2), color)
    draw.line((B2, B3), color)
    draw.line((B3, C), color)

    arrowRightImg = ImageTk.PhotoImage(img)
    return arrowRightImg

def rectangle(pointA, pointB, color, img, defaultState):
    draw = ImageDraw.Draw(img)
    if defaultState:  # draw square
        edge = abs(pointB[0] - pointA[0])
        if pointB[1] > pointA[1]:            
            pointB = (pointB[0], edge + pointA[1])
        else:
            pointB = (pointB[0], abs(pointA[1] - edge))
        draw.rectangle([pointA, pointB], None, color)        
    else:
        draw.rectangle([pointA, pointB], None, color)                    

    rectangleImg = ImageTk.PhotoImage(img)
    return rectangleImg

def lineDDA(startPoint, endPoint, color, img, defaultState):
    dx = endPoint.x - startPoint.x
    dy = endPoint.y - startPoint.y

    if defaultState == 1:
        if abs(dx) > abs(dy):
            dy = 0
        else:
            dx = 0

    if dx == 0:
        if dy > 0:
            delta = 1            
        else:
            delta = -1
        x = startPoint.x
        y = startPoint.y
        while y != endPoint.y:
            img.putpixel((x,y), color)
            y = y + delta

    elif dy == 0:
        if dx > 0:
            delta = 1            
        else:
            delta = -1
        x = startPoint.x
        y = startPoint.y
        while x != endPoint.x:
            img.putpixel((x,y), color)
            x = x + delta            

    else:
        if abs(dx) > abs(dy):
            m = dy / float(dx)
            if m > 0:
                if startPoint.x > endPoint.x:
                    startPoint.x, endPoint.x = endPoint.x, startPoint.x

                if startPoint.y > endPoint.y:
                    startPoint.y, endPoint.y = endPoint.y, startPoint.y
            else:
                if startPoint.x > endPoint.x:
                    startPoint.x, endPoint.x = endPoint.x, startPoint.x

                if startPoint.y < endPoint.y:
                    startPoint.y, endPoint.y = endPoint.y, startPoint.y

            x = startPoint.x
            y = startPoint.y
            while x <= endPoint.x:
                img.putpixel((x, int(round(y))), color)
                y = y + m
                x = x + 1

        else:
            m = dx / float(dy)
            if m > 0:
                if startPoint.x > endPoint.x:
                    startPoint.x, endPoint.x = endPoint.x, startPoint.x

                if startPoint.y > endPoint.y:
                    startPoint.y, endPoint.y = endPoint.y, startPoint.y
            else:
                if startPoint.x < endPoint.x:
                    startPoint.x, endPoint.x = endPoint.x, startPoint.x

                if startPoint.y > endPoint.y:
                    startPoint.y, endPoint.y = endPoint.y, startPoint.y

            x = startPoint.x
            y = startPoint.y
            while y <= endPoint.y:
                img.putpixel((int(round(x)), y), color)
                x = x + m
                y = y + 1

    lineImg = ImageTk.PhotoImage(img)
    return lineImg

def generateSymmetricPixel(point, centerPoint):
    x = point.x
    y = point.y
    return [
        Point(centerPoint.x + x, centerPoint.y + y),
        Point(centerPoint.x - x, centerPoint.y - y),
        Point(centerPoint.x + x, centerPoint.y - y),
        Point(centerPoint.x - x, centerPoint.y + y)
    ]

def generateCirclePixel(arrayPixel, centerPoint):
    list = []
    for i in arrayPixel:
        list.append(generateSymmetricPixel(
            Point(i.x, i.y),
            centerPoint
        ))
        list.append(generateSymmetricPixel(
            Point(i.y, i.x),
            centerPoint
        ))
    return list


def circleMidPoint(centerPoint, radius, color, circle):
    print 'radius ', radius

    arrayPixel = []
    x = 0
    y = radius
    f = 1 - radius
    while(x <= y):
        arrayPixel.append(Point(x, y))
        if(f < 0):            
            f = f + 2*x + 3
#            y = y - 1  # fractal
        else:
            y = y - 1   # circle
            f = f + 2 * (x - y) + 5
        x = x + 1

    list = generateCirclePixel(arrayPixel, centerPoint)

    for obj in list:
        for j in obj:
            circle.putpixel((j.x, j.y), color)

    circleImg = ImageTk.PhotoImage(circle)
    return circleImg


def fillColor(img, center, bc,newColor, paperWidth, paperHeight):
    print 'center ', center

    oldColor = img.getpixel(center)
    if oldColor == newColor:
      return    

    listSeed = []
    listSeed.append(center)
    while listSeed:
        seed = listSeed.pop(0)
        try:
          seedColor = img.getpixel(seed)
        except IndexError:
          seedColor = None
        if  seedColor == oldColor:
            img.putpixel(seed, newColor)
            x, y = seed[0], seed[1]
            listSeed.append((x+1, y))
            listSeed.append((x-1, y))
            listSeed.append((x, y+1))
            listSeed.append((x, y-1))

    filledImg = ImageTk.PhotoImage(img)
    return filledImg
