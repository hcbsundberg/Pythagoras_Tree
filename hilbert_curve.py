import math
import Image, ImageDraw
import Tkinter as Tk
import tkColorChooser

'''
A list of all the classes, methods and procedures used in the program:

class Curve:
    A Curve object represents a Hilbert curve.

    def __init__(self, order, position, angle, size):
        Initiates an object of the class Curve.

    def makeCurve(self, order, factor):
        Recursive procedure that creates a Hilbert curve.

    def newPosition(self):
        Calculates the following position for the curve using the current position, the segment
        length and the direction of the curve.

    def drawCurve(self, draw):
        Draws a Hilbert curve using the positions stored in self.lineList.

    def makeImage(self):
        Creates an image with a Hilbert curve.

def drawLine(draw, startPoint, endPoint, lineWidth, colour):
    Draws a line between two given points.

    
#############################################################################################

A list of procedures and closures used for creating the GUI:

def convertToPhotoimage(background, image):
    Converts a PIL Image to a Tk.PhotoImage.

def makeGUI():
    Creates a graphical user interface for creating an image with a Hilbert curve.

    def updateImage():
        Replaces the image in the Label thumbnail with a new image.

    def chooseMidColour():
        Lets the user pick a colour for the line at the beginning of the curve.

    def chooseEdgeColour():
        Lets the user pick a colour for the edges of the line at the beginning of the curve.

    def chooseEndMidColour():
        Lets the user pick a colour for the line at the end of the curve.

    def chooseEndEdgeColour():
        Lets the user pick a colour for the edges of the line at the end of the curve.

    def chooseBackgroundColour():
        Lets the user pick a colour for the background of the image.

    def rotate():
        Rotates the curve by the given angle.

    def changeOrder(arg):
        Updates the order of the object line.

    def thickness(event):
        Updates the thickness of the object line when pressing + or -.

    def setFocus(event):
        Sets the focus to the widget that was clicked.

    def saveImage():
        Opens a window where the user can specify the wanted name and size for
        the image that is being saved.

        def saveIt():
            Creates a new image of the specified size and saves it.

        def cancel():
            Destroys the save_ window.

    def killRoot():
        Destroys the GUI window and ends the program.
'''
class Curve:
    '''
    A Curve object represents a Hilbert curve.

    Attributes:
        order: The order of the Hilbert curve.
        position: The position where the end of the curve is located at
                  the moment. Before the creation ov the curve has started
                  this will be the start position for the curve. 
        angle: Angle in degrees. Represents the direction of the curve.
        size: The length of one segment in the Hilbert curve.
        midColour: Tuple containing the RGB and the hexadecimal values
                   for the colour of the line at the beginning of the
                   curve.
        edgeColour: Tuple containing the RGB and the hexadecimal values
                    for the colour of the line edges at the beginning of
                    the curve.
        endMidColour: Tuple containing the RGB and the hexadecimal values
                      for the colour of the line at the end of the curve.
        endEdgeColour: Tuple containing the RGB and the hexadecimal values
                       for the colour of the line edges at the end of
                       the curve.
        background: Tuple containing the RGB and the hexadecimal values
                    for the background of the curve.
        thickness: The width of the line.
        lineList: A list containing the positions of every corner in the
                  curve.
    '''
    
    def __init__(self, order, position, angle, size):
        '''
        Initiates an object of the class Curve.

        self: Object that is to be initiated.
        order: See Attributes.
        position: See Attributes.
        angle: See Attributes.
        size: See Attributes.
        On exit: A Curve object has been initiated with the given parameters.
                 Note that the lineList is initiated as an empty list.
        '''
        self.order = order
        self.position = position
        self.angle = angle
        self.size = size
        self.midColour = ((255, 255, 255), "#FFFFFF")
        self.edgeColour = ((0, 0, 0), "#000000")
        self.endMidColour = ((255, 255, 255), "#FFFFFF")
        self.endEdgeColour = ((0, 0, 0), "#000000")
        self.background = ((0, 255, 0), "#00FF00")
        self.thickness = 26
        self.lineList = []
        

    def makeCurve(self, order, factor):
        '''
        Recursive procedure that creates a Hilbert curve.

        self: An object of the class Curve.
        order: The amount of remaining recursion levels.
        factor: Can be 1 or -1. Changes the way the curve turns.
        On exit: A hilbert Curve has been created and the positions
                 of every corner in the cruve added to self.lineList.
        '''
        if order == self.order:
            self.lineList.append(self.position)
            return
        
        self.angle = self.angle - factor * 90
        self.makeCurve(order + 1, -factor)
        self.newPosition()
        
        self.angle = self.angle + factor * 90
        self.makeCurve(order + 1, factor)
        self.newPosition()
        
        self.makeCurve(order + 1, factor)
        self.angle = self.angle + factor * 90
        self.newPosition()
        
        self.makeCurve(order + 1, -factor)
        self.angle = self.angle - 90 * factor

    def newPosition(self):
        '''
        Calculates the following position for the curve using the current position, the segment
        length and the direction of the curve.

        self: An object of the class Curve.
        On exit: A new position has been calculated for the curve using the current position,
                 the segment length and the direction of the curve. self.position has been
                 updated.
        '''
        if self.angle % 90 == 0:
            self.position = (self.position[0] + int(math.cos(math.radians(self.angle))* self.size),
                             self.position[1] + int(math.sin(math.radians(self.angle))* self.size))
        else:
            self.position = (self.position[0] + math.cos(math.radians(self.angle))* self.size,
                             self.position[1] + math.sin(math.radians(self.angle))* self.size)          

    def drawCurve(self, draw):
        '''
        Draws a Hilbert curve using the positions stored in self.lineList.

        self: An object of the class Curve.
        draw: Draw object.
        On exit: The curve has been drawn using the attributes of self and the
                 procedure drawLine(...). The colours of the curve change gradually
                 from the beginning to the end of the curve.
        '''
        colour1Step = []
        colour2Step = []
        # Calculate the gradiant step between every segment in the curve
        # for the line (colour1Step) and its edges(colour2Step).
        for i in range(3):
            colour1Step.append((self.midColour[0][i] - self.endMidColour[0][i]) / float(len(self.lineList) - 1))
            colour2Step.append((self.edgeColour[0][i] - self.endEdgeColour[0][i]) / float(len(self.lineList) - 1))
        for i in range(0, self.thickness, 2):
            for j in range(1, len(self.lineList)):
                colour1 = []
                colour2 = []
                colourStep = []
                for k in range(3):
                    # Calculate the colour of the line and its edges at the segment j.
                    colour1.append(self.midColour[0][k] - colour1Step[k] * j)
                    colour2.append(self.edgeColour[0][k] - colour2Step[k] * j)
                    # Gradiant step for the line.
                    colourStep.append((colour1[k] - colour2[k]) / self.thickness)
                drawLine(draw, (int(self.lineList[j - 1][0]), int(self.lineList[j - 1][1])),
                        (int(self.lineList[j][0]), int(self.lineList[j][1])), self.thickness - i,
                         [int(colour2[k] + (i + 1) * colourStep[k]) for k in range(3)])

    def makeImage(self):
        '''
        Creates an image with a Hilbert curve.

        self: An object of the class Curve.
        On exit: An image has been created to fit the rotation and the size of
                 the curve. The curve has been drawn on the image using drawCurve(...).
        '''
        sideLength = (2 ** (self.order) - 1) * self.size #Length of one side of the rectangle filled by the curve.
        gap = self.size # Space added around the curve.
        cosine = math.cos(math.radians(self.angle % 90))
        sine = math.sin(math.radians(self.angle % 90))
        imageSize = int(math.ceil((cosine + sine) * sideLength + 2 * self.size))
        img = Image.new("RGB", (imageSize, imageSize), self.background[0])
        # Change the start position for the curve so that the curve will fit in the picture.
        if self.angle < 90:
            x = 0
            y = cosine
        elif self.angle < 180:
            x = sine
            y = 0
        elif self.angle < 270:
            x = cosine + sine
            y = sine
        else:
            x = cosine
            y = cosine + sine
        self.position = (gap + x * sideLength, gap + y * sideLength)
        self.lineList = []
        draw = ImageDraw.Draw(img)
        self.makeCurve(0, 1)
        self.drawCurve(draw)
        return img
        
def drawLine(draw, startPoint, endPoint, lineWidth, colour):
    '''
    Draws a line between two given points.

    draw: Draw object.
    startPoint: Tuple containing the start point for the line.
    endPoint: Tuple containing the end point for the line.
    lineWidth: Width of the line.
    colour: The colour of the line.
    On exit: The startpoint and the endpoint have been adjusted
             in order to make sure two lines connect smoothly, and
             a line has been drawn between these points.
    '''
    vector = (endPoint[0] - startPoint[0], endPoint[1] - startPoint[1])
    vectorLength = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    normalizedVector = (vector[0] / vectorLength, vector[1] / vectorLength)
    changex = normalizedVector[0] * lineWidth / 2.0
    changey = normalizedVector[1] * lineWidth / 2.0
    draw.line((startPoint[0] - changex,
               startPoint[1] - changey,
               endPoint[0] + changex,
               endPoint[1] + changey),
              fill = (colour[0], colour[1], colour[2]), width = lineWidth)

#############################################################################################
#
# GUI creation starts here.
#
#############################################################################################


def convertToPhotoimage(background, image):
    '''
    Converts a PIL Image to a Tk.PhotoImage.

    background: The background of the image.
    image: The Image object that will be converted.
    On exit: A Tk.PhotoImage has been created and the data transferred from the
             PIL image. The PhotoImage is returned.
    '''
    colDict = {}
    newImage = Tk.PhotoImage(width=image.size[0], height=image.size[1])
    newImage.put(background[1], (0, 0, image.size[0], image.size[1]))
    data = image.getdata()
    for i,c in enumerate(data):
        if c != background[0]:
            if c not in colDict:
                colDict[c] = "#%02x%02x%02x" % c
            newImage.put(colDict[c], (i % image.size[0], int(i / image.size[0])))
    return newImage

def makeGUI():
    '''
    Creates a graphical user interface for creating an image with a Hilbert curve.

    On exit: A GUI window has been created, opened and closed by the user. An image with
             a Hilbert curve has been saved if the user chose to do so. 
    '''
    # Initiate Curve object that will be used throughout the GUI creation.
    line = Curve(4, (0, 0), 0, 100)

    # Create and configure root window.
    root = Tk.Tk()
    root.wm_title("Hilbert Curve")
    root.columnconfigure((1, 3), pad = 10)
    root.rowconfigure((0, 1, 2, 4, 5, 6, 7, 8), pad = 10)

    # Create labels with instructions.
    midColourLabel = Tk.Label(root, text = " Pick the colour for the center of the line:")
    midColourLabel.grid(row = 0, column = 0,  sticky="W")
    edgeColourLabel = Tk.Label(root, text = " Pick the colour for the edges of the line:")
    edgeColourLabel.grid(row = 1, column = 0,  sticky="W")
    endMidColourLabel = Tk.Label(root, text = " Pick the colour for the center at the end of the curve:")
    endMidColourLabel.grid(row = 2, column = 0,  sticky="W")
    endEdgeColourLabel = Tk.Label(root, text = " Pick the colour for the edges at the end of the curve:")
    endEdgeColourLabel.grid(row = 3, column = 0,  sticky="W")
    backgroundLabel = Tk.Label(root, text = " Pick the colour for the background:")
    backgroundLabel.grid(row = 4, column = 0,  sticky="W")
    orderLabel = Tk.Label(root, text = " Set the order of the hilbert curve:")
    orderLabel.grid(row = 5, column = 0,  sticky="W")
    rotationLabel = Tk.Label(root, text = "Give an angle between 0 and 360 degrees to rotate the curve:")
    rotationLabel.grid(row = 6, column = 0, sticky = "W")
    thicknessLabel = Tk.Label(root, text = "Press +/- to change the thickness of the curve.")
    thicknessLabel.grid(row = 7, column = 2)

    # Create a thumbnail image.
    img = line.makeImage()
    tkImg = convertToPhotoimage(line.background, img.resize((250,250), Image.ANTIALIAS))
    thumbnail = Tk.Label(root, image = tkImg) 
    thumbnail.grid(row = 0, column = 2, rowspan = 7)
    
    def updateImage():
        '''
        Replaces the image in the Label thumbnail with a new image.

        On exit: A new image has been created with the updated attributes for the object
                 line and converted to a Tk PhotoImage using convertToPhotoImage(...). The
                 image displayed in the thumbnail Label has been replaced with the new
                 image. 
        '''
        img = line.makeImage()
        tkImg = convertToPhotoimage(line.background, img.resize((250, 250), Image.ANTIALIAS))
        thumbnail.configure(image = tkImg)
        thumbnail.image = tkImg

    # Create colour buttons with callback procedures.
    
    def chooseMidColour():
        '''
        Lets the user pick a colour for the line at the beginning of the curve.

        On exit: The user has been allowed to pick a colour in a separate window,
                 and unless the window was dismissed the midColour attribute for
                 the object line has been updated to match the choice. The procedure
                 updateImage() has been called.
        '''
        colour = tkColorChooser.askcolor(line.midColour[0])
        if colour[0] != None:
            line.midColour = colour
            midColour.configure(background = line.midColour[1])
            updateImage()
        
    midColour = Tk.Button(root, background = line.midColour[1],
                          width = 10, command = chooseMidColour)
    midColour.grid(row = 0, column = 1)

    def chooseEdgeColour():
        '''
        Lets the user pick a colour for the edges of the line at the beginning of the curve.

        On exit: The user has been allowed to pick a colour in a separate window,
                 and unless the window was dismissed the edgeColour attribute for
                 the object line has been updated to match the choice. The procedure
                 updateImage() has been called.
        '''
        colour = tkColorChooser.askcolor(line.edgeColour[0])
        if colour[0] != None:
            line.edgeColour = colour
            edgeColour.configure(background = line.edgeColour[1])
            updateImage()

    edgeColour = Tk.Button(root, background = line.edgeColour[1],
                           width = 10, command = chooseEdgeColour)
    edgeColour.grid(row = 1, column = 1)
    
    def chooseEndMidColour():
        '''
        Lets the user pick a colour for the line at the end of the curve.

        On exit: The user has been allowed to pick a colour in a separate window,
                 and unless the window was dismissed the endMidColour attribute for
                 the object line has been updated to match the choice. The procedure
                 updateImage() has been called.
        '''
        colour = tkColorChooser.askcolor(line.endMidColour[0])
        if colour[0] != None:
            line.endMidColour = colour
            endMidColour.configure(background = line.endMidColour[1])
            updateImage()
        
    endMidColour = Tk.Button(root, background = line.endMidColour[1],
                             width = 10, command = chooseEndMidColour)
    endMidColour.grid(row = 2, column = 1)
    
    def chooseEndEdgeColour():
        '''
        Lets the user pick a colour for the edges of the line at the end of the curve.

        On exit: The user has been allowed to pick a colour in a separate window,
                 and unless the window was dismissed the endEdgeColour attribute for
                 the object line has been updated to match the choice. The procedure
                 updateImage() has been called.
        '''
        colour = tkColorChooser.askcolor(line.endEdgeColour[0])
        if colour[0] != None:
            line.endEdgeColour = colour
            endEdgeColour.configure(background = line.endEdgeColour[1])
            updateImage()     

    endEdgeColour = Tk.Button(root, background = line.endEdgeColour[1],
                              width = 10, command = chooseEndEdgeColour)
    endEdgeColour.grid(row = 3, column = 1)
    
    def chooseBackgroundColour():
        '''
        Lets the user pick a colour for the background of the image.

        On exit: The user has been allowed to pick a colour in a separate window,
                 and unless the window was dismissed the background attribute for
                 the object line has been updated to match the choice. The procedure
                 updateImage() has been called.
        '''
        colour = tkColorChooser.askcolor(line.background[0])
        if colour[0] != None:
            line.background = colour
            backgroundColour.configure(background = line.background[1])
            updateImage()     

    backgroundColour = Tk.Button(root, background = line.background[1],
                                 width = 10, command = chooseBackgroundColour)
    backgroundColour.grid(row = 4, column = 1)

    # Create rotation entry field with callback procedure.

    def rotate():
        '''
        Rotates the curve by the given angle.

        On exit: If rotationVar is between 0 and 360, the attribute
                 line.angle has been updated.
        '''
        try:
            if int(rotationVar.get()) < 0 or int(rotationVar.get()) > 360:
                return False
            
            line.angle = int(rotationVar.get())
            updateImage()
            return True
        except ValueError:
            return False

    rotationVar = Tk.StringVar(root)
    rotationVar.set("0")       
    rotationEntry = Tk.Entry(root, textvariable = rotationVar ,width = 10,
                             validate= "focusout", validatecommand = rotate)
    rotationEntry.grid(row = 6, column = 1)

    # Create optionmenu and callback procedure for the order.

    def changeOrder(arg):
        '''
        Updates the order of the object line.

        On exit: The order of line has been updated to match orderVariable
                 and the procedure updateImage() has been called.
        '''
        line.order = int(orderVariable.get())
        updateImage()

    orderVariable = Tk.StringVar(root)
    orderVariable.set("4")
    orderMenu = Tk.OptionMenu(root, orderVariable, "1", "2", "3", "4",
                              "5", "6", "7", command = changeOrder)
    orderMenu.grid(row = 5, column = 1, columnspan = 1)

    # Bind the procedure thickness to the event "<Key>".
    
    def thickness(event):
        '''
        Updates the thickness of the object line when pressing + or -.

        event: Tk Event object.
        On exit: line.thickness has been increased/decreased by 4. The procedure
                 updateImage() has been called.
        '''
        if event.char == "+":
            line.thickness = line.thickness + 4
            updateImage()
        if event.char == "-":
            line.thickness = line.thickness - 4
            if line.thickness <= 0:
                line.thickness = 2
            updateImage()
            
    root.bind("<Key>", thickness)

    # Bind procedure setFocus to event "<Button-1>"

    def setFocus(event):
        '''
        Sets the focus to the widget that was clicked.

        On exit: The focus has been moved to the widget that was clicked.
        '''
        event.widget.focus_set()

    root.bind("<Button-1>", setFocus)

    def saveImage():
        '''
        Opens a window where the user can specify the wanted name and size for
        the image that is being saved.

        On exit: The image has been saved or the window dismissed. In both cases
                 the save_ window was destroyed.
        '''
        # Create and configure toplevel window.
        save_ = Tk.Toplevel()
        save_.wm_title("Save Image")
        save_.columnconfigure((1,2), pad = 10)
        save_.rowconfigure((0,1), pad = 10)

        # Create label and entry field for entering image name.
        nameLabel = Tk.Label(save_, text = " Give the file a name:")
        nameLabel.grid(row = 0, column = 0, sticky = "W")
        nameVar = Tk.StringVar(save_)
        nameEntry = Tk.Entry(save_, textvariable = nameVar, width = 10)
        nameEntry.grid(row = 0, column = 1)

        #Create options menu for the file format.
        formatVariable = Tk.StringVar(root)
        formatVariable.set(".png")
        formatMenu = Tk.OptionMenu(save_, formatVariable, ".jpg", ".png", ".bmp",
                                   ".gif")
        formatMenu.grid(row = 0, column = 2)

        #Create label and entry field for the image size.
        sizeLabel = Tk.Label(save_, text = " Set the size for the image in pixels:")
        sizeLabel.grid(row = 1, column = 0, sticky = "W")
        sizeVar = Tk.StringVar(save_)
        sizeVar.set("1000")
        sizeEntry = Tk.Entry(save_, textvariable = sizeVar, width = 10)
        sizeEntry.grid(row = 1, column = 1)

        def saveIt():
            '''
            Creates a new image of the specified size and saves it.

            On exit: A new image has been created and saved using makeImage(...).
                     The save_ window has been destroyed.
            '''
            size = int(sizeVar.get())
            oldLineSize = line.size
            line.size = math.ceil(float(size)/(2**(line.order)))
            line.thickness = int(line.thickness * line.size /(2 * oldLineSize))*2
            img = line.makeImage()
            img = img.resize((int(sizeVar.get()),int(sizeVar.get())), Image.ANTIALIAS)
            img.save(nameVar.get() + formatVariable.get())
            save_.destroy()
                
        def cancel():
            '''
            Destroys the save_ window.

            On exit: The save_window has been destroyed.
            '''
            save_.destroy()

        # Create save and cancel buttons.
        saveImage_ = Tk.Button(save_, text = "Save", command = saveIt)
        saveImage_.grid(row = 2, column = 0)
        cancelButton = Tk.Button(save_, text = "Cancel", command = cancel)
        cancelButton.grid(row = 2, column = 1)

    # Create save button for the root window.    
    saveImage = Tk.Button(root, text = "Save Image", command = saveImage)
    saveImage.grid(row = 7, column = 0, columnspan = 2)

    def killRoot():
        '''
        Destroys the GUI window and ends the program.

        On exit: The GUI window has been destroyed and the program ended.
        '''
        root.quit()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", killRoot) # If root is dismissed killRoot will be called. 
    root.mainloop()

makeGUI()
    
