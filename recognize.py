import numpy as np
import matplotlib
matplotlib.use("WXAgg")
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import wx
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

import time

import ckmeans_v1
import ckmeans_v2
import ckmeans_v3
import kmeans

###############################################################################################################

class Model:
    def __init__(self):
        # the number of clusters
        self.K_value = 2
        # the stop point
        self.STOP = 2
        # whether show diagram, default not
        self.pic = 0

    def Predict(self, characteristics):
        start = time.clock()

        #centroids, clusterAssment, n = kmeans.kmeans(characteristics, self.K_value, self.STOP, self.pic)
        #centroids, clusterAssment, n = ckmeans_v1.kmeans(characteristics, self.K_value, self.STOP, self.pic)
        #centroids, clusterAssment, n = ckmeans_v2.kmeans(characteristics, self.K_value, self.STOP, self.pic)
        print self.pic
        centroids, clusterAssment, n = ckmeans_v3.kmeans(characteristics, self.K_value, self.STOP, self.pic)
        end = time.clock()
        print "time is %f" %((end - start)/n)
        return centroids, clusterAssment


###############################################################################################################

class View(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title="Main View")
        panel = wx.Panel(self)

        self.panel1 = wx.Panel(panel)
        self.panel1.SetBackgroundColour('#4f5049')
        panel2 = wx.Panel(panel)
        panel2.SetBackgroundColour('#ededed')

        # sizer, set display area and ctrl area
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(self.panel1, 0, wx.EXPAND|wx.ALL)
        sizer.Add(panel2, 1, wx.EXPAND|wx.ALL)
        panel.SetSizer(sizer)

        # convert img to bitmap
        self.img = wx.Image('6.JPG', wx.BITMAP_TYPE_ANY)
        self.img = self.img.Scale(500, 400, wx.IMAGE_QUALITY_HIGH)
        self.sb1 = wx.StaticBitmap(self.panel1, -1, wx.BitmapFromImage(self.img))
        self.w = self.img.GetWidth()
        self.h = self.img.GetHeight()

        # get RGB
        self.rgb = self.img.GetData()

        # set img2
        self.img2 = wx.EmptyImage(self.w, self.h)
        self.img2.SetData(self.rgb)
        self.sb2 = wx.StaticBitmap(self.panel1, -1, wx.BitmapFromImage(self.img2))

        # set plot
        self.sp = MatplotPanel(panel2, self.w)

        # set sizer1: image area
        self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer1.Add(self.sb1, 0, wx.EXPAND|wx.ALL)
        self.sizer1.Add(self.sb2, 0, wx.EXPAND|wx.ALL)
        self.panel1.SetSizer(self.sizer1)

        # set sizer2: ctrl area
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        panel21 = wx.Panel(panel2)
        sizer2.Add(panel21, 1, wx.EXPAND|wx.ALL)
        sizer2.Add(self.sp, 1, wx.EXPAND|wx.ALL)
        panel2.SetSizer(sizer2)

        sizer21 = wx.FlexGridSizer(2, 2, 9, 25)
        self.posCtrl = (wx.TextCtrl(panel21, -1, ""))
        self.colorCtrl = (wx.TextCtrl(panel21, -1, ""))
        sizer21.AddMany([
            (wx.StaticText(panel21, label='pos: (X, Y)')),
            self.posCtrl,
            (wx.StaticText(panel21, label='color: (R, G, B)')),
            self.colorCtrl
        ])
        panel21.SetSizer(sizer21)
        choice = ['RGB','RG','RB', 'GB', 'R', 'G', 'B']
        diagram = ['On', 'Off']
        self.choice = wx.RadioBox(panel21, -1, "Characteristic Choice", (0, 100), wx.DefaultSize, choice, 1, wx.RA_SPECIFY_COLS)
        self.diagram = wx.RadioBox(panel21, -1, "Diagram Choice", (200, 100), wx.DefaultSize, diagram, 1, wx.RA_SPECIFY_COLS)
        self.button1 = wx.Button(panel21, -1, "Cluster", pos=(0, 300))

class MatplotPanel(wx.Panel):
    def __init__(self, parent, size):
        wx.Panel.__init__(self, parent,-1,size=(size, size))
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(111, projection='3d')

        #self.addPoints((1,1,1), 'bx--')

        self.canvas = FigureCanvas(self,-1,self.fig)

        #self.addPoints((1,1,2), 'bx--')


    ## func: add new point to a renewed disgram, one at a time
    ## input:
    #  - pos: list, [122, 231, 111], the position in characteristic space, eg rgb
    #  - color: list, [0, 0, 0], rgb number of this point
    def addPoints(self, pos, type):
        self.axes.scatter(pos[0],pos[1],pos[2], color=type)

###############################################################################################################

#### func: change rgb string to rgb number
def getRGB(rgb, w, h, which):
    rgbd = []
    if which == 0:
        for i in range(h):
            for j in range(w):
                r = ord(rgb[(i*w+j)*3])
                g = ord(rgb[(i*w+j)*3+1])
                b = ord(rgb[(i*w+j)*3+2])
                rgbd.append((r, g, b))
    elif which == 1:
        for i in range(h):
            for j in range(w):
                r = ord(rgb[(i*w+j)*3])
                g = ord(rgb[(i*w+j)*3+1])
                b = 0
                rgbd.append((r, g, b))
    elif which == 2:
        for i in range(h):
            for j in range(w):
                r = ord(rgb[(i*w+j)*3])
                g = 0
                b = ord(rgb[(i*w+j)*3+2])
                rgbd.append((r, g, b))
    elif which == 3:
        for i in range(h):
            for j in range(w):
                r = 0
                g = ord(rgb[(i*w+j)*3+1])
                b = ord(rgb[(i*w+j)*3+2])
                rgbd.append((r, g, b))
    elif which == 4:
        for i in range(h):
            for j in range(w):
                r = ord(rgb[(i*w+j)*3])
                g = 0
                b = 0
                rgbd.append((r, g, b))
    elif which == 5:
        for i in range(h):
            for j in range(w):
                r = 0
                g = ord(rgb[(i*w+j)*3+1])
                b = 0
                rgbd.append((r, g, b))
    else:
        for i in range(h):
            for j in range(w):
                r = 0
                g = 0
                b = ord(rgb[(i*w+j)*3+2])
                rgbd.append((r, g, b))
    rgbd = np.array(rgbd)
    return rgbd

#### func: change clusterinfo to color of every catogory in the final picture
## input:
#  - clusterAssment, 2 * samples ndarray, [[cato_number, error],[],[]...all samples...[]]
def clusterColor(clusterAssment):
    cato_color = {}
    done = []
    for i in xrange(clusterAssment.shape[0]):
        if clusterAssment[i,0] not in done:
            done.append(clusterAssment[i,0])
            cato_color[clusterAssment[i,0]] = (chr(np.random.randint(0,255)),chr(np.random.randint(0,255)),chr(np.random.randint(0,255)))
    return cato_color
## output:
#  - cato_color, dict, {cato_number, (r_str, g_str, b_str)}

#########################################################

class Controller:
    def __init__(self, app):
        self.model = Model()
        self.view = View()
        self.view.SetSize((1306,1056))
        self.view.Show()

        self.view.sb1.Bind(wx.EVT_MOTION, self.OnMove)
        self.view.button1.Bind(wx.EVT_BUTTON, self.OnPredict)
        pub.subscribe(self.UpdateMatplot, "Centriods CHANGED")

        self.STEP = 1000

    def OnMove(self, event):
        pos = event.GetPosition()
        R = ord(self.view.rgb[(pos.y*self.view.w+pos.x)*3])
        G = ord(self.view.rgb[(pos.y*self.view.w+pos.x)*3+1])
        B = ord(self.view.rgb[(pos.y*self.view.w+pos.x)*3+2])
        self.view.posCtrl.SetValue("%s, %s" % (pos.x, pos.y))
        self.view.colorCtrl.SetValue("%s, %s, %s" % (R, G, B))

    def OnPredict(self, event):
        self.model.pic = self.view.diagram.GetSelection()

        ## get characteristic
        #transform the rgb string to rgb
        which = self.view.choice.GetSelection()
        self.rgb = getRGB(self.view.rgb, self.view.h, self.view.w, which)

        ## transform to other charteristics
        self.sample = self.rgb

        ## train
        centroids, clusterAssment = self.model.Predict(self.sample)

        ## use cato to show the final picture
        color = clusterColor(clusterAssment)
        rgb2 = self.convertFinalPicture(color, self.view.w, self.view.h, clusterAssment)

        self.view.img2.SetData(rgb2)
        self.view.sb2 = wx.StaticBitmap(self.view.panel1, -1, wx.BitmapFromImage(self.view.img2))

    ## func: use the cato_color info to get the final cluster picture
    def convertFinalPicture(self, cato_color, w, h, clusterAssment):
        rgbs = ''
        for i in xrange(h):
            for j in xrange(w):
                cato = clusterAssment[i*w+j,0]
                r = cato_color[cato][0]
                g = cato_color[cato][1]
                b = cato_color[cato][2]
                rgbs = rgbs+r+g+b
        return rgbs

    #### func: update the diagram of this circle when get message
    ## input:
    #  - data: int, to identify the message
    #  - extra1: n * 2 ndarray, clusterAssement
    #  - extra2: K * 3 ndarray, centriods
    def UpdateMatplot(self, data, extra1, extra2):
        #have to be extra1 not centriods
        cato_color = clusterColor(extra1)
        self.view.sp.axes.clear()
        #draw the basic color
        # for i in xrange(extra2.shape[0]):
        #     self.view.sp.addPoints(extra2[i,:], 'bx--')
        for i in xrange(0, extra1.shape[0], self.STEP):
            self.view.sp.addPoints(self.sample[i,:], (float(ord(cato_color[extra1[i,0]][0]))/256, float(ord(cato_color[extra1[i,0]][1]))/256, float(ord(cato_color[extra1[i,0]][2]))/256))

        #print("draw pic done")
        self.view.sp.canvas.draw()

###############################################################################################################

if __name__ == '__main__':
    app = wx.App()
    controller = Controller(app)
    app.MainLoop()