import Image, ImageDraw
import random, math
import Tkinter as Tk
import tkColorChooser
import time

'''
A list of all the classes, methods and procedures used in the program:

class Square:
    A Square object represents one of the squares in the pythagorean tree.

    def __init__(self, corners, order):
        Initiates a Square object.

    def rotateSquare(self, cornerNum, angle):
        Rotates a square the given angle around the given corner.

    def drawSquare(self, draw, outlineColour, fillColour):
        Draws the given square.

    def makeTree(self, leftAngle, rightAngle, order, listOfSquares):
        Recursive procedure that creates all the squares for a tree of the given order.

class Tree:
    Class representing a pythagorean tree.

    def __init__(self, order, rootColour, branchColour, outline, background, angles, scale):
        Initiates a Tree object.

    def firstSquare(self, size):
        Initiates the root Square object of the tree.

    def drawTree(self, size, save = False, name = "pythagorasTree"):
        Creates an image and draws a tree on it.

def matrixMultiplication(matrix1, matrix2):
    Multiplies two matrices.

#############################################################################################

A list of procedures and closures used for creating the GUI:

def convertToPhotoImage(background, image):
    Converts a PIL Image to a Tk.PhotoImage.

def createGUI():
    Creates a graphical user interface for creating an image with the pythagorean tree.

    def updateImage():
        Replaces the image in the Label thumbnail with a new image.

    def chooseRootColour():
        Lets the user pick a colour for the root of the object tree.

    def chooseBranchColour():
        Lets the user pick a colour for the branches of the object tree.

    def chooseOutlineColour():
        Lets the user pick a colour for the outline of the object tree.

    def chooseBackgroundColour():
        Lets the user pick a colour for the background of the image.

    def noOutline():
        Updates the outline attribute for the object tree.

    def changeIterations(arg):
        Updates the order of the object tree.

    def changeAngleL():
        Updates the attribute angleL for the object tree.

    def changeAngleR():
        Updates the attribute angleR for the object tree.

    def leftMouseDown(event):
        Stores the position of the mouse when clicked over the thumbnail image.

    def leftMouseUp(event):
        Updates the offset for the object tree based on how the mouse was moved.

    def scale(event):
        Updates the scale of the object tree when pressing + or -.

    def pressUp(event):
        Decreases tree.positionChangey.

    def pressDown(event):
        Increases tree.positionChangey.

    def pressRight(event):
        Increases tree.positionChangex.

    def pressLeft(event):
        Decreases tree.positionChangex.

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

class Square:
    '''
    A Square object represents one of the squares in the pythagorean tree.

    Attributes:
        side: The length of one side of the square.
        corners: A list with four tuples that contain the coordinates for the
                 corners of the square. The first element in the list is the
                 lower left corner (before the square has been rotated), and
                 the other corners follow in a counterclockwise order.
        order: This is the order the square has in the tree, i.e. how far away
               from the root of the tree the square is. The order for the root
               square is 0.
        angle: This is the angle in radians that the square is rotated. 
    '''
    
    def __init__(self, corners, order):
        '''
        Initiates a Square object.

        self: An object of the class Square.
        corners: See Attributes.
        order: See Attributes.
        On exit: A square object has been initiated with the given arguments.
                 Note that the angle is initiated as 0.
        '''
        self.side = math.sqrt(math.pow(corners[1][0] - corners[0][0], 2) +
                              math.pow(corners[1][1] - corners[0][1], 2))
        self.corners = corners
        self.order = order
        self.angle = 0

    def rotateSquare(self, cornerNum, angle):
        '''
        Rotates a square the given angle around the given corner.

        self: An object of the class Square.
        cornerNum: The index in self.corners for the corner which the square will be rotated around.
        angle: The angle in radians by which the square will be rotated.
        On exit: The corners for the square have been rotated around the given corner,
                 and self.corners has been updated accordingly.    
        '''
        sine = math.sin(angle)
        cosine = math.cos(angle)
        translatex = self.corners[cornerNum][0] * (1 - cosine) + self.corners[cornerNum][1] * sine
        translatey = self.corners[cornerNum][1] * (1 - cosine) - self.corners[cornerNum][0] * sine
        transformMatrix = [(cosine    , sine      , 0), # Every row here represents a column in the matrix.
                           (-1 * sine , cosine    , 0),
                           (translatex, translatey, 1)]
        for i in range(4):
            corner = matrixMultiplication(transformMatrix, [[self.corners[i][0], self.corners[i][1], 1]])
            self.corners[i] = corner[0][:2]

        
    def drawSquare(self, draw, outlineColour, fillColour):
        '''
        Draws the given square.

        self: Object that is to be initiated.
        draw: The Draw object that will be used to draw the square.
        outlineColour: Can either be a tuple with the RGB colour value for the outline,
                       or None, if the square will not have an outline.
        fillColour: A tuple with the RGB colour the square will have.
        On exit: A square has been drawn with the given colours.
        '''
        draw.polygon(self.corners[0] + self.corners[1] + self.corners[2] + self.corners[3],
                     outline = outlineColour, fill = fillColour)

    def makeTree(self, leftAngle, rightAngle, order, listOfSquares):
        '''
        Recursive procedure that creates all the squares for a tree of the given order.

        self: An object of the class Square.
        leftAngle: The angle the left child of the square will be rotated relative
                   to the rotation of the square.
        rightAngle: The angle the right child of the square will be rotated relative
                    to the rotation of the square.
        order: The order of the tree, in other words, the highest order a square in the tree
               can have.
        listOfSquares: A list containing all the squares that have been created so far.
        On exit: All the squares of a tree have been created according to the given order and angles.
                 A list is returned containing the squares.
        '''
        if self.order == order:
            return listOfSquares
        
        leftSquareSide = self.side * math.sin(math.radians(rightAngle)) / math.sin(math.radians(180 - (leftAngle + rightAngle)))
        leftSquare = Square([self.corners[3], (self.corners[3][0] + leftSquareSide, self.corners[3][1]),
                             (self.corners[3][0] + leftSquareSide, self.corners[3][1] - leftSquareSide),
                             (self.corners[3][0], self.corners[3][1] - leftSquareSide)], self.order + 1)
        leftSquare.angle = self.angle + math.radians(-leftAngle)
        leftSquare.rotateSquare(0, leftSquare.angle)
        listOfSquares.append(leftSquare)
        leftSquare.makeTree(leftAngle, rightAngle, order, listOfSquares)
        
        rightSquareSide = self.side * math.sin(math.radians(leftAngle)) / math.sin(math.radians(180 - (leftAngle + rightAngle)))
        rightSquare = Square([(self.corners[2][0] - rightSquareSide, self.corners[2][1]), self.corners[2],
                             (self.corners[2][0], self.corners[2][1] - rightSquareSide),
                             (self.corners[2][0] - rightSquareSide, self.corners[2][1] - rightSquareSide)], self.order + 1)
        rightSquare.angle = self.angle + math.radians(rightAngle)
        rightSquare.rotateSquare(1, rightSquare.angle)
        listOfSquares.append(rightSquare)
        rightSquare.makeTree(leftAngle, rightAngle, order, listOfSquares)
        return listOfSquares            

class Tree:
    '''
    Class representing a pythagorean tree.

    Attributes:
        order: The order of the tree, i.e. the number of iterations for the procedure makeTree(...).
        rootColour: Tuple containing the RGB and the hexadecimal values for the colour the root square
                    of the tree will have.
        branchColour:  Tuple containing the RGB and the hexadecimal values for the colour the squares
                       of the highest order will have.
        outline: Tuple containing the RGB and the hexadecimal values for the colour of the outline for
                 the squares. If the tree has no outline this is (None, None).
        outlineColour: Same as outline, but stores the outline colour for the tree even if outline is
                       (None, None).
        background: Tuple containing the RGB and the hexadecimal values for the colour of the background
                    of the image the tree is drawn on.
        angleL: The angle the left child of a square will be rotated relative to its parent.
        angleR: The angle the right child of a square will be rotated relative to its parent.
        scale: The scale of the first square in the tree, where a scale of 1 means that the side of the
               square is one eight of the width of the image.
        positionChangex: The offset of the tree along the x-axis.
        positionChangey: The offset of the tree along the y-axis.
    '''
    def __init__(self, order, rootColour, branchColour, outline, background, angles, scale):
        '''
        Initiates a Tree object.

        self: Object that is to be initiated.
        order: See Attributes.
        rootCOlour: See Attributes.
        branchColour: See Attributes.
        outline: See Attributes.
        background: See Attributes.
        angles: Tuple containing angleL and angleR (see Attributes).
        scale: See Attributes.
        On exit: A Tree object has been initiated. Note that the positionChange is initiated
                 as 0 for both x and y.
        '''
        self.order = order
        self.rootColour = rootColour
        self.branchColour = branchColour
        self.outline = outline
        self.background = background
        self.angleL = angles[0]
        self.angleR = angles[1]
        self.scale = scale
        self.positionChangex = 0
        self.positionChangey = 0

    def firstSquare(self, size):
        '''
        Initiates the root Square object of the tree.

        self: An object of the class Tree.
        size: The size of the image the tree will be drawn on.
        On exit: A Square object has been initiated, taking into account the scale and the
                 offset for the tree. The Square object is returned.
        '''
        width = size[0] / 8.0 * self.scale
        x1 = size[0] / 2.0 - width / 2.0 + self.positionChangex
        x2 = size[0] / 2.0 + width / 2.0 + self.positionChangex
        y1 = 8.0 / 10 * size[1] + self.positionChangey
        y2 = y1 - width
        return Square([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], 0)

    def drawTree(self, size, save = False, name = "pythagorasTree"):
        '''
        Creates an image and draws a tree on it.

        self: An object of the class Tree.
        size: The size of the image.
        save: A boolean variable determining whether the image should be saved or not.
        name: The name the image will have if saved.
        On exit: An image with a pythagorean tree has been drawn using the attributes of
                 the Tree object to define colours and the shape of the tree. The image
                 is returned and if save the image has been saved.
        '''
        img = Image.new("RGB", size, self.background[0])
        draw = ImageDraw.Draw(img)
        square = self.firstSquare(size)
        listOfSquares = [square]
        square.makeTree(self.angleL, self.angleR, self.order, listOfSquares)
        # Calculate gradiant step for the fill colour of the squares.
        colourStep = [0,0,0]
        if self.order != 0:
            colourStep = [(self.branchColour[0][i] - self.rootColour[0][i]) / float(self.order) for i in range(3)]
        for i in range(self.order + 1):
            fillColour = (int(self.rootColour[0][0] + colourStep[0] * i),
                          int(self.rootColour[0][1] + colourStep[1] * i),
                          int(self.rootColour[0][2] + colourStep[2] * i))
            for j in listOfSquares:
                if (j.order == i):
                    j.drawSquare(draw,self.outline[0], fillColour)
        if save:
            img.save(name)
        return img

def matrixMultiplication(matrix1, matrix2):
    '''
    Multiplies two matrices.

    matrix1: The leftmost matrix in the multiplication.
    matrix2: The rightmost matrix in the multiplication.
    On exit: The two matrices have been multiplied and the result matrix
             is returned. If the matrices cannot be multiplied None is returned.
             Note that all matrices are given in the form of a list containing
             three 3-tuples that represent the columns in the matrix.
    '''
    if (len(matrix1) != len(matrix2[0])):
        return None

    resultMatrix = []
    for i in range(len(matrix2)): # Create matrix with the right size.
        column = []
        for j in range(len(matrix1[0])):
            column.append(0)
        resultMatrix.append(column)       
    for i in range(len(resultMatrix[0])): # Replace elements in the matrix with the correct elements.
        for j in range(len(resultMatrix)):
            for k in range(len(matrix1)): 
                resultMatrix[j][i] = resultMatrix[j][i] + matrix1[k][i] * matrix2[j][k]
    return resultMatrix

########################################################################################################
#
# GUI creation starts here.
#
########################################################################################################

def convertToPhotoImage(background, image):
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

def createGUI():
    '''
    Creates a graphical user interface for creating an image with the pythagorean tree.

    On exit: A GUI window has been created, opened and closed by the user. An image with
             the pythagorean tree has been saved if the user chose to do so. 
    '''
    # Initiate Tree object that will be used throughout the GUI creation.
    tree = Tree(10, ((0, 255, 0), "#00FF00"), ((0, 0, 0), "#000000"),
                ((255, 255, 255), "#FFFFFF"),((0, 0, 0), "#000000"), (45, 45), 1)

    # Create and configure root window.
    root = Tk.Tk()
    root.wm_title("Pythagoras tree")
    root.columnconfigure((1, 3), pad = 10)
    root.rowconfigure((0, 1, 2, 4, 5, 6, 7, 8), pad = 10)

    # Create labels with instructions.
    rootColourLabel = Tk.Label(root, text = " Pick the colour for the root of the tree:")
    rootColourLabel.grid(row = 0, column = 0,  sticky="W")
    branchColourLabel = Tk.Label(root, text = " Pick the colour for the branches of the tree:")
    branchColourLabel.grid(row = 1, column = 0,  sticky="W")
    outlineColourLabel = Tk.Label(root, text = " Pick the colour for the outlines:")
    outlineColourLabel.grid(row = 2, column = 0,  sticky="W")
    noOutlinesLabel = Tk.Label(root, text = "No outlines:")
    noOutlinesLabel.grid(row = 3, column = 1, sticky = "N")
    backgroundColourLabel = Tk.Label(root, text = " Pick the colour for the background:")
    backgroundColourLabel.grid(row = 4, column = 0,  sticky="W")
    iterationsLabel = Tk.Label(root, text = " Set the number of iterations:")
    iterationsLabel.grid(row = 5, column = 0,  sticky="W")
    angle1Label = Tk.Label(root, text = " Set the lower left angle:")
    angle1Label.grid(row = 6, column = 0,  sticky="W")
    angle2Label = Tk.Label(root, text = " Set the lower right angle:")
    angle2Label.grid(row = 7, column = 0,  sticky="W")
    dragLabel = Tk.Label(root, text = "Click and drag to position the tree and use +/- to scale it.")
    dragLabel.grid(row = 9, column = 3)

    # Create a thumbnail image.
    img = tree.drawTree((250, 250))
    tkImage = convertToPhotoImage(tree.background, img)
    thumbnail = Tk.Label(root, image = tkImage) 
    thumbnail.grid(row = 0, column = 3, rowspan=9)
    
    def updateImage():
        '''
        Replaces the image in the Label thumbnail with a new image.

        On exit: A new image has been created with the updated attributes for the object
                 tree and converted to a Tk PhotoImage using convertToPhotoImage(...). The
                 image displayed in the thumbnail Label has been replaced with the new
                 image. 
        '''
        img = tree.drawTree((250,250))
        tkImg = convertToPhotoImage(tree.background, img)
        thumbnail.configure(image = tkImg)
        thumbnail.image = tkImg

    # Create colour buttons with callback procedures.
    def chooseRootColour():
        '''
        Lets the user pick a colour for the root of the object tree.

        On exit: The user has been allowed to pick a colour in a separate window,
                 and unless the window was dismissed the rootColour attribute for
                 tree has been updated to match the choice. The procedure updateImage()
                 has been called.
        '''
        colour = tkColorChooser.askcolor(tree.rootColour[0])
        if colour[0] != None:
            tree.rootColour = colour
            rootColour.configure(background = tree.rootColour[1])
            updateImage()
        
    rootColour = Tk.Button(root, background = tree.rootColour[1],
                           width = 10, command = chooseRootColour)
    rootColour.grid(row = 0,column = 1, columnspan = 2)
    
    def chooseBranchColour():
        '''
        Lets the user pick a colour for the branches of the object tree.

        On exit: The user has been allowed to pick a colour in a separate window,
                 and unless the window was dismissed the branchColour attribute for
                 tree has been updated to match the choice. The procedure updateImage()
                 has been called.
        '''        
        colour = tkColorChooser.askcolor(tree.branchColour[0])
        if colour[0] != None:
            tree.branchColour = colour
            branchColour.configure(background = tree.branchColour[1])
            updateImage()
        
    branchColour = Tk.Button(root, background = tree.branchColour[1],
                             width = 10, command = chooseBranchColour)
    branchColour.grid(row = 1,column = 1, columnspan = 2)
    
    def chooseOutlineColour():
        '''
        Lets the user pick a colour for the outline of the object tree.

        On exit: The user has been allowed to pick a colour in a separate window,
                 and unless the window was dismissed the outline attribute for
                 tree has been updated to match the choice. The procedure updateImage()
                 has been called.
        '''
        outline = tkColorChooser.askcolor(tree.outline[0])
        if outline[0] != None:
            global storeOutlineColour
            outlineColour.configure(background = outline[1])
            storeOutlineColour = outline
            if outlineVar.get() == "0":
                tree.outline = outline
                updateImage()     

    global storeOutlineColour
    storeOutlineColour = tree.outline
    outlineColour = Tk.Button(root, background = tree.outline[1],
                              width = 10, command = chooseOutlineColour)
    outlineColour.grid(row = 2,column = 1, columnspan = 2)
    
    def chooseBackgroundColour():
        '''
        Lets the user pick a colour for the background of the image.

        On exit: The user has been allowed to pick a colour in a separate window,
                 and unless the window was dismissed the background attribute for
                 tree has been updated to match the choice. The procedure updateImage()
                 has been called.
        '''
        colour = tkColorChooser.askcolor(tree.background[0])
        if colour[0] != None:
            tree.background = colour
            backgroundColour.configure(background = tree.background[1])
            updateImage()

    backgroundColour = Tk.Button(root, background = tree.background[1],
                                 width = 10, command = chooseBackgroundColour)
    backgroundColour.grid(row = 4,column = 1, columnspan = 2)

    # Create checkbutton with callback procedure.
    def noOutline():
        '''
        Updates the outline attribute for the object tree.

        On exit: The outline attribute for the tree has been updated to match the
                 Checkbutton outlines. The procedure updateImage() has been called.
        '''
        if outlineVar.get() == "0":
            tree.outline = storeOutlineColour
        else:
            tree.outline = (None, None)
        updateImage()

    outlineVar = Tk.StringVar()
    outlineVar.set("0")
    outlines = Tk.Checkbutton(root, variable = outlineVar, command = noOutline)
    outlines.grid(row = 3, column = 2, sticky = "N")

    # Create optionmenu and callback procedure for the iterations.
    
    def changeIterations(arg):
        '''
        Updates the order of the object tree.

        On exit: The order of tree has been updated to match iterationsVariable
                 and the procedure updateImage() has been called.
        '''
        tree.order = int(iterationsVariable.get())
        updateImage()

    iterationsVariable = Tk.StringVar(root)
    iterationsVariable.set("10")
    iterationsMenu = Tk.OptionMenu(root, iterationsVariable, "0", "1", "2", "3",
                                   "4", "5", "6", "7", "8", "9", "10", "11",
                                   "12", "13", "14", command = changeIterations)
    iterationsMenu.grid(row = 5, column = 1, columnspan = 2)

    # Create angle entry fields with callback procedures.
    
    def changeAngleL():
        '''
        Updates the attribute angleL for the object tree.

        On exit: If angleVar1 is between 0 and 90, the angleL attribute for the tree
                 has been updated and the procedure updateImage() has been called.
                 True is returned to satisfy the validatecommand.
        '''
        try:
            if int(angleVar1.get()) < 0 or int(angleVar1.get()) > 90:
                return False
            
            tree.angleL = int(angleVar1.get())
            updateImage()
            return True
        except ValueError:
            return False

    angleVar1 = Tk.StringVar(root)
    angleVar1.set("45")       
    angleEntry1 = Tk.Entry(root, textvariable = angleVar1, width = 10,
                           validate= "focusout", validatecommand = changeAngleL)
    angleEntry1.grid(row = 6, column = 1, columnspan = 2)
    
    def changeAngleR():
        '''
        Updates the attribute angleR for the object tree.

        On exit: If angleVar2 is between 0 and 90, the angleL attribute for the tree
                 has been updated and the procedure updateImage() has been called.
                 True is returned to satisfy the validatecommand.
        '''
        try:
            if int(angleVar2.get()) < 0 or int(angleVar2.get()) > 90:
                return False
            
            tree.angleR = int(angleVar2.get())
            updateImage()
            return True
        except ValueError:
            return False
    
    angleVar2 = Tk.StringVar(root)
    angleVar2.set("45")  
    angleEntry2 = Tk.Entry(root, textvariable = angleVar2, width = 10,
                           validate= "focusout", validatecommand = changeAngleR)
    angleEntry2.grid(row = 7, column = 1, columnspan = 2)

    # Bind procedures to certain events.

    def leftMouseDown(event):
        '''
        Stores the position of the mouse when clicked over the thumbnail image.

        event: Tk Event object.
        On exit: The position of the mouse has been stored in the global variable
                 mousePosition.
        '''
        global mousePosition
        mousePosition = (event.x, event.y)

    thumbnail.bind("<Button-1>", leftMouseDown)

    def leftMouseUp(event):
        '''
        Updates the offset for the object tree based on how the mouse was moved.

        event: Tk Event object.
        On exit: tree.positionChangex and tree.positionChangey has been updated
                 to match the movement of the mouse while the left mouse button
                 was held down. The procedure updateImage() has been called.
        '''
        tree.positionChangex = tree.positionChangex + event.x - mousePosition[0]
        tree.positionChangey = tree.positionChangey + event.y - mousePosition[1]
        updateImage()

    thumbnail.bind("<ButtonRelease-1>", leftMouseUp)

    def scale(event):
        '''
        Updates the scale of the object tree when pressing + or -.

        event: Tk Event object.
        On exit: tree.scale has been increased/decreased by 0.1. The procedure
                 updateImage() has been called.
        '''
        if event.char == "+":
            tree.scale = tree.scale + 0.1
            updateImage()
        if event.char == "-":
            tree.scale = tree.scale - 0.1
            updateImage()

    root.bind("<Key>", scale)

    positionDelta = 5
        
    def pressUp(event):
        '''
        Decreases tree.positionChangey.

        On exit: tree.positionChangey has been decreased by positionDelta and
                 The procedure updateImage() has been called.
        '''
        tree.positionChangey = tree.positionChangey - positionDelta
        updateImage()

    root.bind("<Up>", pressUp)

    def pressDown(event):
        '''
        Increases tree.positionChangey.

        On exit: tree.positionChangey has been increased by positionDelta and
                 The procedure updateImage() has been called.
        '''
        tree.positionChangey = tree.positionChangey + positionDelta
        updateImage()

    root.bind("<Down>", pressDown)

    def pressRight(event):
        '''
        Increases tree.positionChangex.

        On exit: tree.positionChangex has been increased by positionDelta and
                 The procedure updateImage() has been called.
        '''
        tree.positionChangex = tree.positionChangex + positionDelta
        updateImage()

    root.bind("<Right>", pressRight)

    def pressLeft(event):
        '''
        Decreases tree.positionChangex.

        On exit: tree.positionChangex has been decreased by positionDelta and
                 The procedure updateImage() has been called.
        '''
        tree.positionChangex = tree.positionChangex - positionDelta
        updateImage()

    root.bind("<Left>", pressLeft)

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

            On exit: A new image has been created and saved using drawTree(...).
                     The save_ window has been destroyed.
            '''
            size = int(sizeVar.get())
            oldPosition = (tree.positionChangex, tree.positionChangey)
            # Change offset to match the large image.
            tree.positionChangex = oldPosition[0] * size / 250.0
            tree.positionChangey = oldPosition[1] * size / 250.0
            tree.drawTree((size, size), True, nameVar.get() + formatVariable.get())
            # Change offset back in case the user want to continue working with the tree.
            tree.positionChangex = oldPosition[0]
            tree.positionChangey = oldPosition[1]           
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
    saveImage.grid(row = 9, column = 0, columnspan = 3)

    def killRoot():
        '''
        Destroys the GUI window and ends the program.

        On exit: The GUI window has been destroyed and the program ended.
        '''
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", killRoot)# If root is dismissed killRoot will be called.
    root.mainloop()

createGUI()

