#Assassination PaintRoom!
#An Assassination Classroom themed software graphics program that allows the user to draw or paint bitmapped images on a computer.
#Mark Zhang
#February 1st 2018

#######################################################################################
                                ####Features####
#0. Essentials: Pencil, Eraser, Ovals, Rectangles, Lines (Filled and Unfilled), Eraser,
#               6 Stamps, colour changer, loading and saving
#1. Music Pauser and Player
#2. Extra Tools: Fill Tool, Text Tool, Spraypaint, Eyedropper, Crop, Magnifier, Background changes
#                Polygon Tool, Clear All, Rainbow Spray, Mystery
#3. Size slider to select size, scroll for size
#4. Undo and Redo
#5. Undo and Redo if you've saved a file from before and opened it up (convenient if you want to make a change) VERY COOL
#6. Animaton for when mouse if hovering over tool
#7. Tool name is displayed on top to clear misunderstandings if it's misinterpreted
#8. Preview Circle to have an idea on the size and colour
#9. Separate fill and unfilled buttons to know if it's filled or unfilled
#10. Preview pane for loading images.
#11. Marker tool (size increases after pencil)
#12. Colour palette to change in between colours


#######################################################################################
                         #####Attention to Detail#####
#1. Pixel Array to quicken fill
#2. Functions to make code efficient (to stop repeats of code everywhere)
#3. Blitting only once for drawing to reduce extreme lag
#4. Undo redo is given drawing parameters to avoid pictures in lists (lag)
#5. Marker picture is shown instead of pencil when the size gets big
#6. Slider buttons to show where everything is (size, colour)
#7. Size automatically changes to a suitable size if you select eraser, spraypaint, stickers
# e.g. if you have pencil (size 1) and you select a sticker, the size will change to a larger size
#8. Keyboard shortcut for undo and redo
#9. Eraser subsurfaces and doesn't crash (if outside screen)
#10. Smooth ellipse and rectangle
#11. Polygon tool snaps back to original point if near
#12. Window coordinates are set to prevent window moving
#13. Window resolution set so that almost all screens will be able to see everything
#14. Tested for errors to prevent crashes
#15. All unnessecary files for users (assets, pckl file for undo redo) are hidden so users don't see it. 
#17. Use of personal code for save and load, increasing compatibility and reduction of errors
#18. Coordinates of mouse position become dashes if mouse is out of canvas
#19. Background Changes for undolist saves for easiness

#Attractive Layout
#Visual Graphics to make paint experience aesthetic and pleasing


#Importing all modules
from pygame import*
from math import*
from random import*
#To initialize
font.init()
mixer.init()
#Set window coord
import os
#Set files to hidden
import subprocess

#Find all files
from glob import*
#
import pickle

#Setting up screen/window
os.environ['SDL_VIDEO_WINDOW_POS'] = '20,30'
res=(1200,750)
screen=display.set_mode(res)
display.set_caption("Assassination PaintRoom!")
screen.fill((0,0,255))
running=True

#Pictures for the basic layout
paintLayout=image.load("Assets/Assassination PaintRoom.png")
grad=image.load("Assets/gradient.png")
board=image.load("Assets/Backgrounds/back1.png")
screen.blit(board,(0,0))#The actual board
screen.blit(paintLayout,(0,0))#The rest of the layout
screen.blit(grad,(0,0))#Colour Picker

#Music List
musicList=[int (m) for m in range(2)]#Make a playlist, then randomize
shuffle(musicList)
currentMusic=mixer.music.load("Assets/music"+str(musicList[0])+".mp3")
playnum=1#Which song we're on
mixer.music.set_volume(0.05)
mixer.music.play()
musicRect=Rect(1135,15,50,50)
musicPic=image.load("Assets/pause.png")
playing=True

#Background Canvas Change
backgroundNum=1

#Mouse Cursor
reticle = (               #sized 24x24
  "        ........        ",
  "      ..   ..   ..      ",
  "     ..    ..    ..     ",
  "    ..     ..     ..    ",
  "   ..      ..      ..   ",
  "  ..      oooo      ..  ",
  " ..        ..        .. ",
  "..         ..         ..",
  "..         ..         ..",
  "..         ..         ..",
  "..   o    X..X    o   ..",
  ".....o.....XX.....o.....",
  ".....o.....XX.....o.....",
  "..   o    X..X    o   ..",
  "..         ..         ..",
  "..         ..         ..",
  "..         ..         ..",
  " ..        ..        .. ",
  "  ..      oooo      ..  ",
  "   ..      ..      ..   ",
  "    ..     ..     ..    ",
  "     ..    ..    ..     ",
  "      ..   ..   ..      ",
  "        ........        ")#Took me 2 hours
datatuple,masktuple=cursors.compile(reticle,black='.',white='X',xor='o')#Compile the code
mouse.set_cursor((24,24),(12,12),datatuple,masktuple)

#Tools Rect:
rectTool=[]#[Pencil, eraser, fill, text, spray paint, eyedropper,...]
#Rect for tools
for yr in range(184,667,44):
    for xr in range(70,171,100):
        rectTool.append(Rect(xr-12,yr+53,40,40))
toolColour=[(0,0,0) for tol in range(22)]#Tool colour for tool responses
toolColour[0]=(255,255,255)#Sets pencil to selected (default)
tool=0 #0 for pencil, 1 for eraser, and so on...
size=1 #Size for tools like marker, eraser, etc...
rec=(0,0) #start of mx,my for drawing rectangles, text, anything that needs to stay put
marker=image.load("Assets/marker.png")#Marker Image
#To display and show what tool you're using
tlist=["Pencil","Eraser","Fill","Text","Spraypaint","Eyedropper","Crop","Magnify","Image","Rectangle","Line","Polygon","Ellipse","Clear All","Rainbow","Mystery","Sticker","Sticker","Sticker","Sticker","Sticker","Sticker"]


#Save and Load
saveRect=Rect(420,19,50,42)
loadRect=Rect(495,15,65,55)
loadpicRect=Rect(280,222,450,488)
saving=False
loading=False

py=220#The position of the image file names (for scrolling)
loadPic=image.load("Assets/loading.png")
exitPic=image.load("Assets/exit.png")
picboard=0#If the user loads an image, picboard will be an image

#saveloadRect=Surface((1200,750),SRCALPHA)
#draw.rect(saveloadRect,(255,0,0,80),(0,0,1200,750))

#Outline Fill
#The response rectangles for fill and unfill buttons
fillRect=Rect(365,110,60,60)
outlineRect=Rect(435,110,60,60)
outline=1 #Outline will change according to size
outlinefill=False#On fill, true on outline

#Colour Rect
rainbowRect=Rect(885,105,290,35)#Colourful slider
bwRect=Rect(885,140,290,35)#Black and white colour slider
slider=image.load("Assets/slider.png")
sliderpos=((885,143))
colour=[(0,0,0),(255,255,255)]#The two colour pallettes default black and white

#Slider for Size
slidersize=Rect(5,230,40,500)
slidersizepos=((15,230))

#Tool Variables
drawing=True #This if for appending "pencil", "eraser", etc for the undo redo
polyDraw=False#To see if the poly tool drawing or not
drawingBoard=Rect(267,222,893,488)
pic=screen.copy()

#Predifining mx my to not cause errors
mx=0
my=0

#Text
textB="" #Text that will show for typing, saving
typing=False
#Font
agencyfont=font.SysFont("Agency FB",40)

#Undo Redo
undolist=[]#Explained in the undoredo function
dellist=[]#where parameters go when user undoes.
#If mouse clicks in rectangles
undoRect=Rect(1010,15,50,50)
redoRect=Rect(1070,15,50,50)

#Sticker Dictionary for accessing stickers easier. They're named 16-21 because it's assigned to the Rectangle parameter in the toolsrect list
stickerD={16:"Assets/womansensei.png",17:"Assets/Kayano.png",18:"Assets/Korosensei.png",19:"Assets/Nagisa.png",20:"Assets/mansensei.png",21:"Assets/Karma.png"}


#Functions

def drawRect(colourR,point,mouseposR,outlineR):#Colour of rectangle, point that stays intact, the opposite point for the rectangle, and the outline
    rectangleR=Rect(point[0],point[1],mouseposR[0]-point[0],mouseposR[1]-point[1])
    rectangleR.normalize()#I have to normalize this because I'm using a surface (because surfaces cannot be negative!) for outline
    if outlineR>0 and min((rectangleR[2]),(rectangleR[3]))>outlineR*2:#To make sure that if the outline is larger than the minimum rectangle width and height, it'll turn into a filled rect
        unfilledS = Surface(((rectangleR[2]),(rectangleR[3])))
        unfilledS.set_colorkey((1,1,1))#makes this colour transparent
        unfilledS.fill((1,1,1))#fill the surface with transparency
        draw.rect(unfilledS,colourR,(0,0,rectangleR[2],rectangleR[3]))#draw a rectangle that is filled
        draw.rect(unfilledS,(1,1,1),(outlineR,outlineR,rectangleR[2]-outlineR-outlineR,rectangleR[3]-outlineR-outlineR),0)#draw filled transparent rectangle
        screen.blit(unfilledS,(rectangleR[0],rectangleR[1]))#blit the surface
    else:
        draw.rect(screen,colourR,rectangleR,0)

def drawEllipse(colourE,pointE,mouseposE,outlineE):#Same concept as the rectangle
    ellipseR=Rect(pointE[0],pointE[1],mouseposE[0]-pointE[0],mouseposE[1]-pointE[1])
    ellipseR.normalize()
    if outlineE>0 and min(ellipseR[3],ellipseR[2])>outlineE*2:#Same as rectangle, except this lil guy will give you an error if you don't fix it.
        unfilledS = Surface(((ellipseR[2]),(ellipseR[3])))
        unfilledS.set_colorkey((1,1,1))#makes this colour transparent
        unfilledS.fill((1,1,1))#fill the surface with transparency
        normalellip=Rect(outlineE,outlineE,ellipseR[2]-outlineE-outlineE,ellipseR[3]-outlineE-outlineE)
        draw.ellipse(unfilledS,colourE,(0,0,ellipseR[2],ellipseR[3]),0)
        draw.ellipse(unfilledS,(1,1,1),(normalellip),0)
        screen.blit(unfilledS,(ellipseR[0],ellipseR[1]))
    else:
        draw.ellipse(screen,colourE,ellipseR,0)

def crop(cx,cy,cdx,cdy):#Rectangle parameters
    screen.set_clip(drawingBoard)
    cropic=screen.copy()#I need to copy the screen at that moment to remove the blue transparent rectangle the user draws to show what they're cropping
    cropped=cropic.subsurface((cx,cy,cdx,cdy))
    screen.blit(board,(0,0))#reblit the board to 
    screen.blit(transform.scale(cropped,(int(cropped.get_width()*(488/cropped.get_height())),488)),(267,222))#blit at the (0,0) of the drawing board
    screen.set_clip(None)#Enable drawing outside of the drawing board

def fills(fc,fcol):#I needed to do this because my surface kept on getting locked (fc is the coordinates), fcol is the fill colour
    dxArray=PixelArray(screen)
    dxArray[fc]=screen.map_rgb(fcol)
    del dxArray #remove the pixel array just in case

def undoredo(reDraw,image=None): #reDraw is a boolean, image is a picture
    #Blitting the drawing screen
    #this lags the program, so we need if statements
    if reDraw:#for undo and redo when I must redraw everything
        #Undo Redo List
        screen.set_clip(drawingBoard)
        screen.blit(board,(0,0))
        if picboard!=0:#If there is an image loaded.
            screen.blit(picboard,(267,222))
        if len(undolist)!=0:#prevent crashes from for loop
            for undo in range(len(undolist)):#Goes through tools like pencil, eraser
                for drawp in range(1,len(undolist[undo])):#goes through every tool separately (colour, coordinates, size)
                    if undolist[undo][0]=="pencil" and len(undolist[undo])>1:
                        #draw pencil         colour,                 position                   other position              size
                        draw.line(screen,undolist[undo][drawp][0],(undolist[undo][drawp][1]),(undolist[undo][drawp][2]),undolist[undo][drawp][3])
                    elif undolist[undo][0]=="marker" and len(undolist[undo])>1:
                        #draw marker           colour                              position                                  radius
                        draw.circle(screen,undolist[undo][drawp][0],(undolist[undo][drawp][1],undolist[undo][drawp][2]),int(undolist[undo][drawp][3]/2))
                    elif undolist[undo][0][0:4]=="fill" and len(undolist[undo])>1:
                        #Fills function  position         colour
                        fills(undolist[undo][drawp],eval(undolist[undo][0][4:]))
                    elif undolist[undo][0]=="rect" and len(undolist[undo])>1:
                        #Function   colour,                        position             length, width                outline
                        drawRect(undolist[undo][drawp][0],(undolist[undo][drawp][1]),(undolist[undo][drawp][2]),undolist[undo][drawp][3])
                    elif undolist[undo][0]=="ellipse" and len(undolist[undo])>1:
                        #Function         colour                  position             length, width              outline
                        drawEllipse(undolist[undo][drawp][0],undolist[undo][drawp][1],undolist[undo][drawp][2],undolist[undo][drawp][3])
                    elif undolist[undo][0]=="eraser" and len(undolist[undo])>1:
                        #                                position                     along with width and height
                        erase=board.subsurface(undolist[undo][drawp][0]-int(undolist[undo][drawp][2]/2),undolist[undo][drawp][1]-int(undolist[undo][drawp][2]/2),undolist[undo][drawp][2],undolist[undo][drawp][2])
                        screen.blit(erase,(undolist[undo][drawp][0]-int(undolist[undo][drawp][2]/2),undolist[undo][drawp][1]-int(undolist[undo][drawp][2]/2)))
                    elif undolist[undo][0]=="text" and len(undolist[undo])>1:
                        #            font                   text             anti alias     colour                  position
                        screen.blit(agencyfont.render(undolist[undo][drawp][0],True,undolist[undo][drawp][1]),(undolist[undo][drawp][2]))
                    elif undolist[undo][0]=="poly" and len(undolist[undo])>1:
                        #draw.line          colour                        rec                     mx,my                  size
                        draw.line(screen,undolist[undo][drawp][0],undolist[undo][drawp][1],undolist[undo][drawp][2],undolist[undo][drawp][3])
                    elif undolist[undo][0]=="line" and len(undolist[undo])>1:
                        #Same as poly
                        draw.line(screen,undolist[undo][drawp][0],undolist[undo][drawp][1],undolist[undo][drawp][2],undolist[undo][drawp][3])
                    elif undolist[undo][0]=="sticker" and len(undolist[undo])>1:
                        #Sticker function   name of sticker   size                       position
                        sticker(undolist[undo][drawp][0],undolist[undo][drawp][1],undolist[undo][drawp][2])
                    elif undolist[undo][0]=="spraypaint" and len(undolist[undo])>1:
                        #                   position                                          colour
                        screen.set_at((undolist[undo][drawp][1],undolist[undo][drawp][2]),undolist[undo][drawp][0])
                    elif undolist[undo][0]=="crop" and len(undolist[undo])>1:
                        #Crop function               Rectangle parameters
                        crop(undolist[undo][drawp][0],undolist[undo][drawp][1],undolist[undo][drawp][2],undolist[undo][drawp][3])
        screen.set_clip(None)
        
    elif ((9<=tool<=12) or (16<=tool<=21) or tool==3 or saving or loading or tool==6 or tool==7) and image!=None:#If it's for shapes, stickers ,text, loading, saving, crop or magnify,
        #simply blit the image of the board. pic is the surface that is copied
        image=image.subsurface(drawingBoard)
        screen.blit(image,(267,222))

    else:
        #Undo Redo List for one draw things like pencil and eraser
        #Code exactly the same as the top undoredo except it only prints the last item from the list
        screen.set_clip(drawingBoard)
        if len(undolist)!=0:
            for drawp in range(1,len(undolist[-1])):
                if undolist[-1][0]=="pencil" and len(undolist[-1])>1:
                    draw.line(screen,undolist[-1][drawp][0],(undolist[-1][drawp][1]),(undolist[-1][drawp][2]),undolist[-1][drawp][3])
                elif undolist[-1][0]=="marker" and len(undolist[-1])>1:
                    draw.circle(screen,undolist[-1][drawp][0],(undolist[-1][drawp][1],undolist[-1][drawp][2]),int(undolist[-1][drawp][3]/2))
                elif undolist[-1][0]=="rect" and len(undolist[-1])>1:
                    #draw.rect(screen,  colour,             (mx, my ,length, width)        outline
                    #draw.rect(screen,undolist[-1][drawp][0],undolist[-1][drawp][1],undolist[-1][drawp][2])
                    drawRect(undolist[-1][drawp][0],(undolist[-1][drawp][1]),(undolist[-1][drawp][2]),undolist[-1][drawp][3])
                elif undolist[-1][0]=="ellipse" and len(undolist[-1])>1:
                    drawEllipse(undolist[-1][drawp][0],(undolist[-1][drawp][1]),(undolist[-1][drawp][2]),undolist[-1][drawp][3])
                elif undolist[-1][0]=="eraser" and len(undolist[-1])>1:
                    #draw.circle(screen,     colour,             mx,    my,                 radius/size
                    #draw.circle(screen,undolist[undo][drawp][0],undolist[undo][drawp][1],undolist[undo][drawp][2])
                    erase=board.subsurface(undolist[-1][drawp][0]-int(undolist[-1][drawp][2]/2),undolist[-1][drawp][1]-int(undolist[-1][drawp][2]/2),undolist[-1][drawp][2],undolist[-1][drawp][2])
                    screen.blit(erase,(undolist[-1][drawp][0]-int(undolist[-1][drawp][2]/2),undolist[-1][drawp][1]-int(undolist[-1][drawp][2]/2)))
                elif undolist[-1][0]=="poly" and len(undolist[-1])>1:            
                    #draw.line          colour                        rec                     mx,my                  size
                    draw.line(screen,undolist[-1][drawp][0],undolist[-1][drawp][1],undolist[-1][drawp][2],undolist[-1][drawp][3])
                elif undolist[-1][0]=="sticker" and len(undolist[-1])>1:
                    sticker(undolist[-1][drawp][0],undolist[-1][drawp][1],undolist[-1][drawp][2])
                elif undolist[-1][0]=="spraypaint" and len(undolist[-1])>1:
                    screen.set_at((undolist[-1][drawp][1],undolist[-1][drawp][2]),undolist[-1][drawp][0])
                elif undolist[-1][0]=="crop" and len(undolist[-1])>1:
                        crop(undolist[-1][drawp][0],undolist[-1][drawp][1],undolist[-1][drawp][2],undolist[-1][drawp][3])
        screen.set_clip(None)
    
#Sticker Function
def sticker(t,s,xy):
    screen.set_clip(drawingBoard)
    stick=transform.scale(image.load(stickerD[t]),(s*10,s*10))
    #stick=image.load(stickerD[t])
    screen.blit(stick,(xy[0]-(s*5),xy[1]-(s*5)))
    #size 26 is it's largest
    screen.set_clip(None)
    return (t,s,xy)

#All the blits on the paint layout, not the drawingboard
def blits():
    screen.blit(paintLayout,(0,0))
    screen.blit(grad,(0,0))
    if size>4:#If it's larger than size 4, it's a marker and not a pencil
        screen.blit(marker,(rectTool[0][0],rectTool[0][1]))
    
    #Music
    screen.blit(musicPic,(1135,15)) #Pause and unpause

    #Colour Slider
    screen.blit(slider,sliderpos)
    #Colour Pallete
    draw.rect(screen,colour[0],(875,15,50,50))
    draw.rect(screen,0,(874,14,52,52),1)
    draw.rect(screen,colour[1],(950,15,50,50))
    draw.rect(screen,0,(949,14,52,52),1)

    toolSelectionB=False#If a tool is selected, then display that tool name
    #Feedback Rectangles (drawing them)
    for feedback in range(len(rectTool)):
        draw.rect(screen,(toolColour[feedback]),rectTool[feedback],2)#normal colour black or white if selected
        if rectTool[feedback].collidepoint(mx,my):
            draw.rect(screen,(255,0,0),rectTool[feedback],2)#red if hovering over tool
            toolSelection=agencyfont.render(("Tool: "+str(tlist[feedback])),True,(0,0,0))
            screen.blit(toolSelection,(140,100))
            toolSelectionB=True#Prevents currently selected tool from printing
    
    if toolSelectionB==False:#print current tool name
        #Tool Selection Text
        toolSelection=agencyfont.render(("Tool: "+str(tlist[tool])),True,(0,0,0))
        screen.blit(toolSelection,(140,100))

    #Feedback Rectangles for Outline and Fill
    if outlinefill==False:#If the fill is selected
        draw.rect(screen,(255,255,255),fillRect,2)
        draw.rect(screen,(0,0,0),outlineRect,2)
    else:#If outline is selected
        draw.rect(screen,(0,0,0),fillRect,2)
        draw.rect(screen,(255,255,255),outlineRect,2)


    #Slider for size
    draw.rect(screen,(0,0,0),(25,230,10,500))
    screen.blit(slider,(slidersizepos))
    draw.circle(screen,colour[0],(75,150),int(size/2))#Preview circle

    #Text for coordinates of the mouse if it leaves the canvas
    coordinatet=agencyfont.render("X:--  Y:--",True,(0,0,0))
    screen.blit(coordinatet,(140,150))

#Fill Function
def fill(x,y,colourf):#x,y is the position, colourf is the colour to be filled with
    flist=[(x,y)]#The list of points I need to check
    fillcolour=screen.map_rgb(colourf)#Changes colour to something pixel array recognizes
    pxArray=PixelArray(screen)#makes pxArray an Array that holds the colour and position of the whole surface
    
    if screen.get_at((x,y))==colourf:#If the colour at x,y is the colour to be filled, make the fill list empty (which will not run the while loop which fills)
        flist=[]
    else:#Else, get the original colour and append fill parameters along with colour
        originalCol=pxArray[x,y]
        undolist.append(["fill"+str(colourf)])    
    while len(flist)!=0:
        testx,testy=flist.pop()#Pop out the coordinates and check if they match with the original colour. If they do,
        #change the colour to the fill colour and append colours near by which will be also checked by this. Once everything has been filled, the list will be empty,
        #and thus will end.
        if drawingBoard.collidepoint(testx,testy) and pxArray[testx,testy]==originalCol:
            flist.append((testx+1,testy))
            flist.append((testx-1,testy))
            flist.append((testx,testy+1))
            flist.append((testx,testy-1))
            undolist[-1].append((testx,testy))
            pxArray[testx,testy]=fillcolour#Changes colour of that pixel
    del pxArray#Delete the array to prevent screen locks during blit
blits()#To load the paint layout in advance
while running:
    #Variables by the user
    mx,my=mouse.get_pos()#Mouse position
    mb=mouse.get_pressed()#Mouse clicks
    keys=key.get_pressed()#Keyboard
    for e in event.get():
        if e.type==QUIT:
            running=False
        elif e.type==MOUSEBUTTONDOWN:
            if e.button==1 and saving==False and loading==False and typing==False:#My typing, saving, and loading are separated to prevent errors. e.button==1 is the primary button click
                pic=screen.copy()#copies the screen for the undoredo
                for t in range(len(rectTool)):#Goes through all the tools rectangles and check if the mouse collides
                    if rectTool[t].collidepoint(mx,my):
                        if t==13:#Clears all. Gets rid of EVERYTHING
                            picboard=0
                            screen.blit(board,(0,0))
                            undolist=[]
                            dellist=[]
                            pic=screen.copy()
                        elif t==8:#Changing the background
                            if backgroundNum+1==6:#If the background goes to the end, change it back to the first
                                backgroundNum=1
                            else:
                                backgroundNum+=1
                            board=image.load("Assets/Backgrounds/back"+str(backgroundNum)+".png")
                            screen.fill((0,0,0))#clears everything
                            blits()
                            undoredo(True)#reprint everything because the background changed
                            pic=screen.copy()
                        else:#This changes the tool colour for selected tools (white)
                            toolColour[tool]=(0,0,0)
                            tool=t
                            #If the tool is something that requres a size, change it to something larger (because size 1 there won't be a change)
                            if tool==1:#Eraser
                                size=50
                                slidersizepos=15,(size-1)*7+230
                            elif tool==4 or tool==14:#Spraypaints
                                size=40
                                slidersizepos=15,(size-1)*7+230
                            elif tool==11:#Poly
                                size=3
                                slidersizepos=((15,220))
                            elif 16<=tool<=21:#Sticker
                                size=30
                                slidersizepos=15,(size-1)*7+230
                            toolColour[t]=(255,255,255)#Black is normal
                            
                if undoRect.collidepoint(mx,my) and len(undolist)!=0:#Undo, undolist's most recent draw is popped and put in dellist
                    dellist.append(undolist.pop())
                    undoredo(True)#update the screen
                    pic=screen.copy()

                elif redoRect.collidepoint(mx,my) and len(dellist)!=0:#Redo, puts most recent undo back into undolist
                    undolist.append(dellist.pop())
                    undoredo(True)#update
                    pic=screen.copy()

                elif saveRect.collidepoint(mx,my):#Save is clicked
                    textB=""#Makes sure the text string is empty
                    undoredo(True)#Update with the latest changes
                    saving=True
                    rec=300,225 #Puts save in one spot
                    textTick=0 #Ticking rectangle at the end of text
                elif loadRect.collidepoint(mx,my):#Load is clicked
                    loading=True
                    pictures = glob("Saved Pictures/*.bmp")+glob("Saved Pictures/*.jpg")+glob("Saved Pictures/*.png")#Load up all the names of images in a list
                    
                elif musicRect.collidepoint(mx,my):#For pause and play
                    if playing==True:
                        musicPic=image.load("Assets/play.png")
                        mixer.music.pause()
                        playing=False
                    else:
                        musicPic=image.load("Assets/pause.png")
                        mixer.music.unpause()
                        playing=True
                    
                elif tool==2 and drawingBoard.collidepoint(mx,my):#Fill tool click
                    fill(mx,my,colour[0])
                    
                elif tool==3:#Typing
                    if typing==False and drawingBoard.collidepoint(mx,my):#If it hasn't been initialized yet: make typing true and set the anchor (rec) along with the tick
                        typing=True
                        rec=mx,my
                        textTick=0
                        
                elif (tool==6 or tool==9 or tool==10 or tool==12) and drawingBoard.collidepoint(mx,my):#If it's crop, shapes, then set the anchor point (rec)
                    rec=(mx,my)
            
                elif tool==11:#the start click for poly tool
                    if drawingBoard.collidepoint(mx,my) and polyDraw==True:#to make sure the poly tool is in use
                        if len(undolist[-1])>1 and Rect((undolist[len(undolist)-1][1][1][0]-25,undolist[len(undolist)-1][1][1][1]-25,40,40)).collidepoint(mx,my):#hits the starting position
                            undolist[-1].append((colour[0],undolist[-1][1][1],rec,1))
                            rec=(0,0)#reset variable
                        else:#proceed on and keep on drawing
                            undolist[-1].append((colour[0],(rec),(mx,my),1))
                            rec=(mx,my)
                    elif polyDraw==True:#if the user clicked outside without finishing, append and end the polydraw
                        undolist[-1].append((colour[0],(rec),(mx,my),1))
                        rec=(0,0)
                        drawing=False
                        polyDraw=False
                        
                elif Rect(875,15,50,50).collidepoint(mx,my):#front colour and background colour switching
                    colour=[colour[1],colour[0]]
                    
                elif fillRect.collidepoint(mx,my):#fill and outline
                    outlinefill=False
                elif outlineRect.collidepoint(mx,my):
                    outlinefill=True

            #Scrolling up and down for size
            elif (e.button==4 and (drawing==True or (16<=tool and 21>=tool))):
                if loading:#Scrolling up and down for the file names for pictures
                    py+=50
                elif ((slidersizepos[1]+20)<730):
                    slidersizepos=15,slidersizepos[1]+20
                    size=((slidersizepos[1]-230)//7)+1
                    blits()
            elif (e.button==5) and (drawing==True or (16<=tool and 21>=tool)):
                if loading:
                    py-=50
                elif slidersizepos[1]-20<230:
                    slidersizepos=15,230
                    size=((slidersizepos[1]-230)//7)+1
                else:
                    slidersizepos=15,slidersizepos[1]-20
                    size=((slidersizepos[1]-230)//7)+1
                blits()
        elif e.type==MOUSEBUTTONUP:
            if e.button==1 and saving==False and loading==False and typing==False:#Once again to prevent loading and saving and text to interfere with drawing code
              #If rectangle is let go, append to list
                if tool==6 and rec!=(0,0) and drawingBoard.collidepoint(mx,my):#crop
                    undolist.append(["crop"])
                    undolist[-1].append((cropRect[0],cropRect[1],cropRect[2],cropRect[3]))#appending to undolist
                    undoredo(True)#take out the transparent blue
                    rec=(0,0)#Reset anchor point
                elif tool==7 and drawingBoard.collidepoint(mx,my):#magnify
                    undoredo(False,pic)#to make sure screen.copy doesn't take the magnify into the picture
                elif tool==9 and rec!=(0,0) and drawingBoard.collidepoint(mx,my):
                    undolist.append(["rect"])
                    undolist[len(undolist)-1].append((colour[0],(rec),(mx,my),outline))#appending to undolist
                    rec=(0,0)#resetting the key point
                elif tool==10 and rec!=(0,0) and drawingBoard.collidepoint(mx,my):
                    undolist.append(["line"])
                    undolist[-1].append((colour[0],(rec[0],rec[1]),(mx,my),size))
                elif tool==11 and drawingBoard.collidepoint(mx,my) and rec==(0,0) and polyDraw==True and len(undolist)>0:#if the user clicked back to the original position,
                    #set polyDraw to False and drawing to False. Has to be in mousebutton up or the loop that sets PolyDraw back to True will be done.
                    #undoredo(True)
                    polyDraw=False
                    drawing=False
                elif tool==12 and rec!=(0,0) and drawingBoard.collidepoint(mx,my):#ellipse
                    undolist.append(["ellipse"])
                    undolist[len(undolist)-1].append((colour[0],(rec[0],rec[1]),(mx,my),outline))#appending to undolist
                    rec=(0,0)#resetting the key point
                elif 16<=tool and 21>=tool and drawingBoard.collidepoint(mx,my):
                    undolist.append(["sticker"])
                    undolist[len(undolist)-1].append((lastSticker))#appending to undolist
                if drawingBoard.collidepoint(mx,my):
                    pic=screen.copy()#To not copy the screen if a shape or sticker goes outside the board.
                undoredo(False,pic)
                
        elif e.type==KEYDOWN:
            keys=key.get_pressed()
            #Undo and redo for keyboard, same code
            if keys[K_LCTRL]==1 and keys[K_z]==1 and len(undolist)!=0 and mb[0]!=1 and typing==False and polyDraw==False and saving==False and loading==False:#undo
                dellist.append(undolist.pop())
                undoredo(True)
                pic=screen.copy()
            elif keys[K_LCTRL]==1 and keys[K_y]==1 and len(dellist)!=0 and mb[0]!=1 and typing==False and polyDraw==False and saving==False and loading==False:#redo
                undolist.append(dellist.pop())
                undoredo(True)
                pic=screen.copy()
            #For typing and saving    
            elif ((tool==3 and typing) or saving) and e.key < 256:
                if keys[K_BACKSPACE]==1:
                    textB=textB[:-1]#Removes last string character
                elif keys[K_RETURN]==1:
                    if saving:
                        undoredo(False,pic)#Reprints the picture to remove the save text
                        try:
                            image.save(screen.subsurface(drawingBoard),"Saved Pictures/"+str(textB)+".png")#Saves the image
                            undoredofile=open("Saved Pictures/"+str(textB),"wb")#For undo and redo later on in the future
                            pickle.dump(undolist,undoredofile)
                            undoredofile.close()
                            subprocess.check_call(["attrib","+H","+R","Saved Pictures/"+str(textB)])#Change to hidden so user cannot see it.
                            rec=(0,0)
                        except:
                            print("Error. I'm sorry :(")
                        textB=""
                        saving=False
                    else:#For the text tool
                        undoredo(False,pic)#Reprint original to get rid of the text tick
                        if len(textB)>0:
                            screen.set_clip(drawingBoard)
                            screen.blit(textBox,(rec))
                            screen.set_clip(None)
                            pic=screen.copy()
                            undolist.append(["text"])#Appending to undolist
                            undolist[-1].append((textB,colour[0],rec))
                        textB=""
                        typing=False
                else:
                    textB += e.unicode#Adding the things typed to string
                undoredo(False,pic)
            
            
    if saving==False and loading==False and typing==False:
        #Outline and Fill
        if outlinefill==True:
            outline=size
        else:
            outline=0#Set to fill

        #Appending the beginner so that undolist knows what to draw
        if drawingBoard.collidepoint(mx,my) and mb[0]==1 and drawing==True:
            if tool==0 or tool==15:
                if size<5:
                    undolist.append(["pencil"])
                else:
                    undolist.append(["marker"])
            elif tool==1:
                undolist.append(["eraser"])
            elif tool==3:
                None
            elif tool==4 or tool==14:
                undolist.append(["spraypaint"])
            elif tool==7:
                pic=screen.copy()#For magnifying glass
            elif tool==11 and polyDraw==False:#If polyDraw hasn't been used, start drawing.
                undolist.append(["poly"])
                rec=(mx,my)
                polyDraw=True
            drawing=False
            
            
        if drawingBoard.collidepoint(mx,my):
            undoredo(False,pic)
        #Most drawing and appending
        if mb[0]==1:
            screen.set_clip(drawingBoard)#Makes sure nothing leaves the board
            if drawingBoard.collidepoint(mx,my):
                if len(dellist)>0:
                    dellist=[]#When an undo is made and a new change is made, delete the undo
                elif tool==0:#Pencil and marker
                    if size>4:#Marker
                        undolist[len(undolist)-1].append(((colour[0]),mx,my,size))#Append the click
                        dx=(mx-oldMousePoint[0])#Slope
                        dy=(my-oldMousePoint[1])
                        distancetoTravel=max(abs(dx),abs(dy))#Finds the bigger slope to do similar triangles
                        for change in range(distancetoTravel):#Similar triangles go up one at a time
                            circx=oldMousePoint[0]+int((dx*change)/distancetoTravel)
                            circy=oldMousePoint[1]+int((dy*change)/distancetoTravel)
                            undolist[len(undolist)-1].append(((colour[0]),circx,circy,size))
                    else:
                        undolist[len(undolist)-1].append(((colour[0]),(mx,my),(oldMousePoint),size))#pencil
                elif tool==1:#Eraser
                    undolist[len(undolist)-1].append((mx,my,size))
                    screen.set_clip(drawingBoard)
                    draw.rect(screen,(0),(mx-int(size/2),my-int(size/2),size,size))#Show where you're erasing
                    screen.set_clip(None)
                elif tool==4:#Spraypaint
                    #Radius is size/2  
                    for sprayT in range(100):#Shotgun method: Append if it's in the circle. I randint square parameters then check if it's in the circle
                        sprayx=randint(mx-int(size/2),mx+int(size/2))
                        sprayy=randint(my-int(size/2),my+int(size/2))
                        if ((sprayx-mx)**2+(sprayy-my)**2)**(1/2)<int(size/2):#If distance if within radius
                            undolist[len(undolist)-1].append((colour[0],sprayx,sprayy))
                    
                elif tool==5:#Eyedropper
                    colour[0]=screen.get_at((mx,my))
                    blits()
                elif tool==6 and rec!=(0,0):#Crop
                    #Rectangle needs to be normalized for surface
                    cropRect=Rect(rec,(mx-rec[0],my-rec[1]))
                    cropRect.normalize()
                    cropSurf=Surface((cropRect[2],cropRect[3]),SRCALPHA)#Alpha surface
                    draw.rect(cropSurf,(0,0,255,80),(0,0,cropRect[2],cropRect[3]))
                    screen.blit(cropSurf,(cropRect[0],cropRect[1]))
                elif tool==7:#magnify
                    undoredo(False,pic)
                    screen.set_clip(drawingBoard)
                    magnified=pic.subsurface((mx-36,my-36,72,72))
                    screen.blit(transform.scale(magnified,(200,200)).subsurface(64,64,72,72),(mx-36,my-36))#Zoomed in and then blitted
                    draw.rect(screen,0,(mx-36,my-36,72,72),2)#Rectangle outline
                    screen.set_clip(None)
                elif tool==9 and rec!=(0,0):#rectangle
                    drawRect(colour[0],(rec),(mx,my),outline)#Rectangle function
                elif tool==10 and rec!=(0,0):#line
                    draw.line(screen,colour[0],(rec[0],rec[1]),(mx,my),size)#Simple line
                elif tool==12 and rec!=(0,0):#ellipse
                    drawEllipse(colour[0],(rec[0],rec[1]),(mx,my),outline)#Ellipse function
                elif tool==14:#Rainbow Spray, same code as spray but randomized colour
                    for sprayT in range(100):
                        sprayx=randint(mx-int(size/2),mx+int(size/2))
                        sprayy=randint(my-int(size/2),my+int(size/2))
                        if ((sprayx-mx)**2+(sprayy-my)**2)**(1/2)<int(size/2):
                            undolist[len(undolist)-1].append(((randint(0,255),randint(0,255),randint(0,255)),sprayx,sprayy))
                elif tool==15:#Rainbow paint
                    if size>4:#Marker
                        undolist[len(undolist)-1].append(((randint(0,255),randint(0,255),randint(0,255)),mx,my,size))#Append the click
                        dx=(mx-oldMousePoint[0])#Slope
                        dy=(my-oldMousePoint[1])
                        distancetoTravel=max(abs(dx),abs(dy))#Finds the bigger slope to do similar triangles
                        for change in range(distancetoTravel):#Similar triangles go up one at a time
                            circx=oldMousePoint[0]+int((dx*change)/distancetoTravel)
                            circy=oldMousePoint[1]+int((dy*change)/distancetoTravel)
                            undolist[len(undolist)-1].append(((randint(0,255),randint(0,255),randint(0,255)),circx,circy,size))
                    else:
                        undolist[len(undolist)-1].append(((randint(0,255),randint(0,255),randint(0,255)),(mx,my),(oldMousePoint),size))#pencil
        
                #16-21 are stickers
                elif 16<=tool and 21>=tool:
                    lastSticker=sticker(tool,size,(mx,my))#Sticker function returns parameters for sticker which is appended in mousebuttonup
            else:#For things outside the board
                if rainbowRect.collidepoint(mx,my):
                    colour[0]= grad.get_at((mx,my))  #For colour
                    sliderpos=mx-15,106
                elif bwRect.collidepoint(mx,my):
                    colour[0] = grad.get_at((mx,my))  #For colour
                    sliderpos=mx-15,143
                elif slidersize.collidepoint(mx,my):#Changes the slider for size
                    size=((my-230)//7)+1
                    if my-15<230:
                        slidersizepos=15,230
                    else:
                        slidersizepos=15,my-15
            screen.set_clip(None)
        oldMousePoint=(mx,my)#For pencil/marker
        
        #Blits
        if drawingBoard.collidepoint(mx,my)==False:#Outside of board
            blits()
        elif drawingBoard.collidepoint(mx,my):#Coordinates continuously blit
            coordBack=paintLayout.subsurface(131,150,170,51)
            screen.blit(coordBack,(131,150))
            coordinatet=agencyfont.render("X:%d  Y:%d"%(mx-267,my-222),True,(0,0,0))
            screen.blit(coordinatet,(140,150))
    
    if mb[0]==0:
        drawing=True#resets drawing back to True to be able to draw once again
        if tool==11 and polyDraw==True and drawingBoard.collidepoint(mx,my) and rec!=(0,0):#Enables the poly tool to snap to the original point is the width of height is within 40 pixels
            if len(undolist[-1])>1 and Rect((undolist[len(undolist)-1][1][1][0]-25,undolist[len(undolist)-1][1][1][1]-25,40,40)).collidepoint(mx,my):
                draw.line(screen,colour[0],(rec),(undolist[len(undolist)-1][1][1][0],undolist[len(undolist)-1][1][1][1]),1)
            else:#draw the poly line
                draw.line(screen,colour[0],(rec),(mx,my),1)
                
        elif (tool==3 and typing==True) or saving:#This is the text tick along with the text being blit
            undoredo(False,pic)
            textTick+=1
            screen.set_clip(drawingBoard)
            if saving==True:
                draw.rect(screen,(0,0,0),((rec),(1000,50)))
                textBox=agencyfont.render(textB,True,(255,255,255))
            else:
                textBox=agencyfont.render(textB,True,colour[0])
            
            screen.blit(textBox,(rec))#text
            if textTick//20%5!=1:#ticks
                draw.rect(screen,(colour[0]),(rec[0]+textBox.get_width(),rec[1]+8,2,35))
            screen.set_clip(None)

    if mixer.music.get_busy()==False:#To play the next song in the playlist
        if playnum==len(musicList):#If the song has reached the end, restart to starting song.
            playnum=0
        currentMusic=mixer.music.load("Assets/music"+str(musicList[playnum])+".mp3")
        mixer.music.play()
        playnum+=1#counter for song number
    
    if loading:#Loading pictures
        screen.blit(loadPic,(0,0))
        exitRect=screen.blit(exitPic,(900,600))#To exit if you don't want to load anything
            
        screen.set_clip(drawingBoard)
        
        for px in range(len(pictures)):#goes through the rect parameters of each picture filename
            if Rect(300,py+px*40,400,40).collidepoint(mx,my):
                draw.rect(screen,(255,255,255),(280,py+px*40+5,450,45))#response rectangle
                imagepreview=image.load(pictures[px])#preview picture
                imagepreview=transform.scale(imagepreview,(int(imagepreview.get_width()*(200/imagepreview.get_height())),200))
                screen.blit(imagepreview,(775,350))
            loadText=agencyfont.render(pictures[px],False,colour[0])#actual filenames
            screen.set_clip(loadpicRect)#If the filename is long, cut it off or it'll disturb the preview pane
            loadClick=screen.blit(loadText,(280,py+px*40))
            screen.set_clip(drawingBoard)
            if exitRect.collidepoint(mx,my):
                exitRect=screen.blit(transform.scale(exitPic,(100,100)),(886,586))#when hovering, exit becomes larger
                if mb[0]==1:#if clicked, set the mouse pos outside of the board because things will start drawing
                    mouse.set_pos(600,40)
                    mx,my=mouse.get_pos()
                    oldMousePoint=mx,my
                    screen.set_clip(None)
                    undoredo(True)
                    py=220#reset the filename position
                    loading=False
                    break #end the loop
            elif mb[0]==1 and loadClick.collidepoint(mx,my):#same except for printing of the picture loaded
                mouse.set_pos(600,40)
                mx,my=mouse.get_pos()
                oldMousePoint=mx,my
                screen.set_clip(None)
                undolist=[]
                dellist=[]
                try: #Check if there's an undolist associated with that picture.
                    undofile=open(pictures[px][:-4],'rb')
                    undolist=pickle.load(undofile)
                    undofile.close()
                except:#load the picture
                    picboard=image.load(pictures[px])
                    picboard=transform.scale(picboard,(int(picboard.get_width()*(488/picboard.get_height())),488))#resizes it so proportions do not change
                    pass
                undoredo(True)
                py=220
                loading=False
                break  
        screen.set_clip(None)
    display.flip()#updates the screen
quit()










































































































































































#CELEBRATING 1000 LINES OF CODE!!! YAY! Thank you Mr. McKenzie for checking over everyone's paint project, including mine!
