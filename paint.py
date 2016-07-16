import Tkinter
import ttk
import math
import copy
import drawPattern as draw
import initState as init
import tkMessageBox
import tkFileDialog
from config import *
from Tkinter import *
from PIL import Image, ImageTk

class App(dict):
  def __getattr__(self, attr):
    return self.get(attr)
  __setattr__= dict.__setitem__
  __delattr__= dict.__delitem__

  def __init__(self, master):
    init.configureFrame(self, master)
    init.initIconToolbar(self)
    init.initMenubar(self)
    init.initToolbar(self)
    init.initDrawToolbar(self)
    init.initColorToolbar(self)
    init.initFrame(self)

  def callAbout(self):
    tkMessageBox.showinfo("About", "This product was made by Trieu Trang Vinh.")    

  def callNew(self):
    self.myCanvas.delete("all")
    self.paper = Image.new("RGB", (self.paperWidth,self.paperHeight), self.bgColor)
    self.usePaper = ImageTk.PhotoImage(self.paper)

    self.myCanvas.img = self.usePaper
    self.myCanvas.create_image(0, 0, image=self.myCanvas.img)

  def callOpenImage(self):
    self.fOpenName = tkFileDialog.askopenfilename(filetypes=(("Supported Image Files", "*.jpg; *.jpeg; *.png; *.bmp; *.ico"),
                                       ("All files", "*.*") ))

    if not self.fOpenName:
      return
    self.myCanvas.delete("all")

    self.paper = Image.open(self.fOpenName).resize((self.paperWidth,self.paperHeight))
    self.usePaper = ImageTk.PhotoImage(self.paper)

    self.myCanvas.img = self.usePaper
    self.myCanvas.create_image(0, 0, image=self.myCanvas.img)

  def callSaveImage(self):
    if self.fOpenName != None:
      self.paper.save(self.fOpenName)      
      return

    fname = tkFileDialog.asksaveasfilename(defaultextension=".png")
    if not fname: # asksaveasfile return `None` if dialog closed with "cancel".
      return
    self.paper.save(fname)

  def callSaveAsImage(self):
    fname = tkFileDialog.asksaveasfilename(defaultextension=".png")
    if not fname: # asksaveasfile return `None` if dialog closed with "cancel".
      return
    self.paper.save(fname)

  def onChangeColor(self, colorName, colorNameButton):      
    self.color_button.config(relief=RAISED)
    self.color_button = self[colorNameButton]
    self.color_button.config(relief=SUNKEN)
    self.chooseColor = colorName

  def callback(self):
    print "A button was pressed"

  def flippingHorizontalTool(self):
    print "Flip horizontal tool"
    self.active_button.config(relief=RAISED)
    self.active_button = self.flipHorizonToolBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_choosing_place_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_choosing_place_flip_horizon)
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())

  def flippingVerticalTool(self):
    print "Flip vertical tool"
    self.active_button.config(relief=RAISED)
    self.active_button = self.flipVeticalToolBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_choosing_place_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_choosing_place_flip_vertical)
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())

  def rotationTool(self):
    print "Rotate tool"
    self.active_button.config(relief=RAISED)
    self.active_button = self.rotateToolBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_choosing_place_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_choosing_place_rotate)
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())

  def transitionTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.moveToolBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_choosing_place_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_choosing_place)    
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())

  def shearingTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.shearToolBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_choosing_place_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_choosing_place_shear)    
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())

  def scalingTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.scaleToolBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_choosing_place_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_choosing_place_scale)    
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())

  def drawPencilTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.pencilBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="pencil")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_draw_pencil)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_draw_pencil)

  def eraserTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.eraserBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="dotbox")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_draw_eraser)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_draw_eraser)

  def drawCurveTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.curveBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.p0 = self.p1 = self.p2 = None
    self.listChosenPoint = []
    self.myCanvas.bind("<ButtonPress-1>", self.addChosenPoint)
#    if len(self.listChosenPoint) >= 2:
    self.myCanvas.bind("<B1-Motion>", self.on_button_curve_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_curve)

  def addChosenPoint(self, event):
    print (event.x, event.y)
    self.listChosenPoint.append((event.x, event.y))


  def drawLineTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.lineToolBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_release_line_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release)

  def onChangeDefaultState(self):
    self.defaultState = 1

  def fillColorTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.fillBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="spraycan")
    self.myCanvas.bind("<ButtonPress-1>", self.on_fill_color)
    self.myCanvas.bind("<ButtonRelease-1>", lambda event: self.callback)

  def on_fill_color(self, event):
    self.busy()
    self.filled = draw.fillColor(self.paper, (event.x, event.y), self.bgColor, self.chooseColor, self.paperWidth, self.paperHeight)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.filled)
    self.notbusy("spraycan")

  def drawDiamondTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.diamondBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_diamond_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_diamond)    
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())

  def drawPolygonFiveTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.polygonFiveBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_polygon_five_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_polygon_five)    
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())

  def drawPolygonSixTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.polygonSixBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_polygon_six_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_polygon_six)    
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())

  def drawStarFourTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.starFourBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_star_four_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_star_four)    
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())

  def drawStarSixTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.starSixBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_star_six_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_star_six)    
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())

  def drawTriangleTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.triangleBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_triangle_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_triangle)    
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())

  def drawTriangleSquareTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.triangleSquareBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_triangle_square_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_triangle_square)
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())

  def drawStarTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.starBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_star_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_star)    
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())

  def drawArrowRightTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.arrowRightBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_arrow_right_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_arrow_right)    
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())

  def drawRectangleTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.rectangleBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_rectangle_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_rectangle)    
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())

  def drawCircleTool(self):
    self.active_button.config(relief=RAISED)
    self.active_button = self.circleBtn
    self.active_button.config(relief=SUNKEN)
    self.myCanvas.config(cursor="circle")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_circle_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_circle)  
    self.master.bind("<Shift_L>", lambda event: self.onChangeDefaultState())


  def on_button_draw_pencil(self, event):
    previousPoint = (self.x, self.y)
    pointNow = (event.x, event.y)
    self.pencilImg = draw.pencil(previousPoint, pointNow, self.chooseColor, self.paper)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.pencilImg)
    self.x = event.x
    self.y = event.y

  def on_button_draw_eraser(self, event):
    previousPoint = (self.x, self.y)
    pointNow = (event.x, event.y)
    self.eraserImg = draw.eraser(previousPoint, pointNow, self.bgColor, self.paper)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.eraserImg)
    self.x = event.x
    self.y = event.y

  def on_button_diamond_motion(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    paper = copy.copy(self.paper)
    self.diamondImg = draw.diamond((x0,y0), (x1, y1), self.chooseColor, paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.diamondImg)
    self.defaultState = 0

  def on_button_release_diamond(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    self.diamondImg = draw.diamond((x0,y0), (x1, y1), self.chooseColor, self.paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.diamondImg)
    self.defaultState = 0

  def on_button_star_four_motion(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    paper = copy.copy(self.paper)
    self.starFourImg = draw.starFour((x0,y0), (x1, y1), self.chooseColor, paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.starFourImg)
    self.defaultState = 0

  def on_button_release_star_four(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    self.starFourImg = draw.starFour((x0,y0), (x1, y1), self.chooseColor, self.paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.starFourImg)
    self.defaultState = 0

  def on_button_star_six_motion(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    paper = copy.copy(self.paper)
    self.starSixImg = draw.starSix((x0,y0), (x1, y1), self.chooseColor, paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.starSixImg)
    self.defaultState = 0

  def on_button_release_star_six(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    self.starSixImg = draw.starSix((x0,y0), (x1, y1), self.chooseColor, self.paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.starSixImg)
    self.defaultState = 0

  def on_button_polygon_five_motion(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    paper = copy.copy(self.paper)
    self.polygonFiveImg = draw.polygonFive((x0,y0), (x1, y1), self.chooseColor, paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.polygonFiveImg)
    self.defaultState = 0

  def on_button_release_polygon_five(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    self.polygonFiveImg = draw.polygonFive((x0,y0), (x1, y1), self.chooseColor, self.paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.polygonFiveImg)
    self.defaultState = 0

  def on_button_polygon_six_motion(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    paper = copy.copy(self.paper)
    self.polygonSixImg = draw.polygonSix((x0,y0), (x1, y1), self.chooseColor, paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.polygonSixImg)
    self.defaultState = 0

  def on_button_release_polygon_six(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    self.polygonSixImg = draw.polygonSix((x0,y0), (x1, y1), self.chooseColor, self.paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.polygonSixImg)
    self.defaultState = 0

  def on_button_triangle_motion(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    paper = copy.copy(self.paper)
    self.triangleImg = draw.triangle((x0,y0), (x1, y1), self.chooseColor, paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.triangleImg)
    self.defaultState = 0

  def on_button_release_triangle(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    self.triangleImg = draw.triangle((x0,y0), (x1, y1), self.chooseColor, self.paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.triangleImg)
    self.defaultState = 0

  def on_button_triangle_square_motion(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    paper = copy.copy(self.paper)
    self.triangleSquareImg = draw.triangleSquare((x0,y0), (x1, y1), self.chooseColor, paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.triangleSquareImg)
    self.defaultState = 0

  def on_button_release_triangle_square(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    self.triangleSquareImg = draw.triangleSquare((x0,y0), (x1, y1), self.chooseColor, self.paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.triangleSquareImg)
    self.defaultState = 0

  def on_button_star_motion(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    paper = copy.copy(self.paper)
    self.starImg = draw.star((x0,y0), (x1, y1), self.chooseColor, paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.starImg)
    self.defaultState = 0

  def on_button_release_star(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    self.starImg = draw.star((x0,y0), (x1, y1), self.chooseColor, self.paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.starImg)
    self.defaultState = 0

  def on_button_arrow_right_motion(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    paper = copy.copy(self.paper)
    self.arrowRightImg = draw.arrowRight((x0,y0), (x1, y1), self.chooseColor, paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.arrowRightImg)
    self.defaultState = 0

  def on_button_release_arrow_right(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    self.arrowRightImg = draw.arrowRight((x0,y0), (x1, y1), self.chooseColor, self.paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.arrowRightImg)
    self.defaultState = 0

  def on_button_choosing_place_motion(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    paper = copy.copy(self.paper)
    self.rectangleImg = draw.rectangle((x0,y0), (x1, y1), dark, paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.rectangleImg)

    self.defaultState = 0

  def on_button_release_choosing_place(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    
    self.transitionPlace = ((x0, y0), (x1, y1))
    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_transition_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_transition)    

  def on_button_transition_motion(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    paper = copy.copy(self.paper)

    if not self.pixelList:
      self.pixelList = draw.cropping(self.transitionPlace[0], self.transitionPlace[1], self.bgColor, paper)

    self.transitImg = draw.moveTransition(self.pixelList, (x1, y1), self.bgColor, paper)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.transitImg)
    self.defaultState = 0

  def on_button_release_transition(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    if self.pixelList:
      draw.eraseSelectedCropping(self.pixelList, self.bgColor, self.paper)

    self.transitImg = draw.moveTransition(self.pixelList, (x1, y1), self.bgColor, self.paper)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.transitImg)

    self.pixelList = None
    self.transitionTool()
    self.defaultState = 0

  def on_button_release_choosing_place_flip_horizon(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    
    self.transitionPlace = ((x0, y0), (x1, y1))

    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.callback)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_flip_horizon)    

  def on_button_release_choosing_place_flip_vertical(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    
    self.transitionPlace = ((x0, y0), (x1, y1))

    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.callback)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_flip_vertical)    

  def on_button_release_choosing_place_rotate(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    
    self.transitionPlace = ((x0, y0), (x1, y1))

    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_rotation_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_rotation)    

  def on_button_release_choosing_place_shear(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    
    self.transitionPlace = ((x0, y0), (x1, y1))

    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_shear_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_shear)    

  def on_button_release_choosing_place_scale(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    
    self.transitionPlace = ((x0, y0), (x1, y1))

    self.myCanvas.config(cursor="crosshair")
    self.myCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.myCanvas.bind("<B1-Motion>", self.on_button_scale_motion)
    self.myCanvas.bind("<ButtonRelease-1>", self.on_button_release_scale)    


  def on_button_shear_motion(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    paper = copy.copy(self.paper)

    if x1 > y1:
      shearX = x1/float(x0)
      shearY = 0
    else:
      shearX = 0
      shearY = y1/float(y0)

    if not self.pixelList:
      self.pixelList = draw.cropping(self.transitionPlace[0], self.transitionPlace[1], self.bgColor, paper)

    self.shearImg = draw.shearing(self.pixelList, (x0, y0), (shearX, shearY), paper)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.shearImg)
    self.defaultState = 0

  def on_button_scale_motion(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    paper = copy.copy(self.paper)
    scaleX = x1/float(x0)
    scaleY = y1/float(y0)

    if not self.pixelList:
      self.pixelList = draw.cropping(self.transitionPlace[0], self.transitionPlace[1], self.bgColor, paper)

    self.scaleImg = draw.scalling(self.pixelList, (x0, y0), (scaleX, scaleY), paper)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.scaleImg)
    self.defaultState = 0

  def on_button_release_shear(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    if x1 > y1:
      shearX = x1/float(x0)
      shearY = 0
    else:
      shearX = 0
      shearY = y1/float(y0)

    if self.pixelList:
      draw.eraseSelectedCropping(self.pixelList, self.bgColor, self.paper)

    self.shearImg = draw.shearing(self.pixelList, (x0, y0), (shearX, shearY), self.paper)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.shearImg)

    self.pixelList = None
    self.shearingTool()
    self.defaultState = 0

  def on_button_release_scale(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    scaleX = x1/float(x0)
    scaleY = y1/float(y0)

    if self.pixelList:
      draw.eraseSelectedCropping(self.pixelList, self.bgColor, self.paper)

    self.scaleImg = draw.scalling(self.pixelList, (x0, y0), (scaleX, scaleY), self.paper)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.scaleImg)

    self.pixelList = None
    self.scalingTool()
    self.defaultState = 0


  def on_button_rotation_motion(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    paper = copy.copy(self.paper)

    if x1 > x0:
      alpha = math.atan((y0-y1) / float(x0-x1))    
    else:
      alpha = math.pi + math.atan((y0-y1) / float(x0-x1))    

    print alpha

    if not self.pixelList:
      self.pixelList = draw.cropping(self.transitionPlace[0], self.transitionPlace[1], self.bgColor, paper)

    self.rotateImg = draw.moveRotation(self.pixelList, (x0, y0), alpha, self.bgColor, paper)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.rotateImg)
    self.defaultState = 0

  def on_button_release_rotation(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    
    alpha = math.atan(y1 / float(x1))

    if x1 > x0:
      alpha = math.atan((y0-y1) / float(x0-x1))    
    else:
      alpha = math.pi + math.atan((y0-y1) / float(x0-x1))    

    if self.pixelList:
      draw.eraseSelectedCropping(self.pixelList, self.bgColor, self.paper)

    self.rotateImg = draw.moveRotation(self.pixelList, (x0, y0), alpha, self.bgColor, self.paper)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.rotateImg)

    self.rotationTool()
    self.pixelList = None
    self.defaultState = 0

  def on_button_release_flip_horizon(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    self.flipImg = draw.flipHorizontal(self.transitionPlace[0], self.transitionPlace[1], (x1, y1), self.bgColor, self.paper)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.flipImg)

    self.flippingHorizontalTool()
    self.defaultState = 0

  def on_button_release_flip_vertical(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    self.flipImg = draw.flipVertical(self.transitionPlace[0], self.transitionPlace[1], (x1, y1), self.bgColor, self.paper)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.flipImg)

    self.flippingVerticalTool()
    self.defaultState = 0

  def on_button_rectangle_motion(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    paper = copy.copy(self.paper)
    self.rectangleImg = draw.rectangle((x0,y0), (x1, y1), self.chooseColor, paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.rectangleImg)
    self.defaultState = 0

  def on_button_release_rectangle(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)    

    self.rectangleImg = draw.rectangle((x0,y0), (x1, y1), self.chooseColor, self.paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.rectangleImg)    
    self.defaultState = 0

  def on_button_circle_motion(self, event):

    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)

    paper = copy.copy(self.paper)
    rx = x1 - x0

    if self.defaultState == 1:     
      ry = rx
    else:
      ry = y1 - y0

    self.circleImg = draw.eclipseMidPoint((x0,y0), rx, ry, self.chooseColor, paper)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.circleImg)
    self.defaultState = 0

  def on_button_release_circle(self, event):

    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)

    rx = x1 - x0

    if self.defaultState == 1:     
      ry = rx
    else:
      ry = y1 - y0

    self.circleImg = draw.eclipseMidPoint((x0,y0), rx, ry, self.chooseColor, self.paper)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.circleImg)
    self.defaultState = 0


  def on_button_press(self, event):
    self.x = event.x
    self.y = event.y

  def on_button_curve_motion(self, event):
    self.p1 = (event.x, event.y)

    paper = copy.copy(self.paper)
    self.curveImg = draw.curve(self.listChosenPoint[0], self.p1, self.listChosenPoint[1], self.chooseColor, paper)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.curveImg)

    self.defaultState = 0

  def on_button_release_curve(self, event):
    self.p1 = (event.x, event.y)

    self.curveImg = draw.curve(self.listChosenPoint[0], self.p1, self.listChosenPoint[1], self.chooseColor, self.paper)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.curveImg)

    self.defaultState = 0
    self.listChosenPoint = []
    
  def on_button_release_line_motion(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)

    paper = copy.copy(self.paper)
    self.lineImg = draw.lineDDA(draw.Point(x0,y0), draw.Point(x1,y1), self.chooseColor, paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.lineImg)
    self.defaultState = 0

  def on_button_release(self, event):
    x0,y0 = (self.x, self.y)
    x1,y1 = (event.x, event.y)

    self.lineImg = draw.lineDDA(draw.Point(x0,y0), draw.Point(x1,y1), self.chooseColor, self.paper, self.defaultState)
    self.myCanvas.create_image(self.paperWidth / 2, self.paperHeight / 2, image=self.lineImg)
    self.defaultState = 0

  def busy(self):
    self.myCanvas.config(cursor="wait")

  def notbusy(self, cursor = ""):
    self.myCanvas.config(cursor=cursor)


root = Tkinter.Tk()
root.geometry("640x480")
root.style = ttk.Style()
#('clam', 'alt', 'default', 'classic')
root.style.theme_use('clam')

app = App(root)
root.mainloop()
