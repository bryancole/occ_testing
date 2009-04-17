import wx
import os

os.environ['CSF_GraphicShr'] = "/usr/local/lib/libTKOpenGl.so"

from wxDisplay import GraphicsCanva3D
from OCC import BRepPrimAPI

class TestFrame(wx.Frame):
    def __init__(self):
        super(TestFrame,self).__init__(None, -1, "test frame", size=(600,500))
        self.canvas = GraphicsCanva3D(self)
        self.viewer = None
        #self.Show()
        
        self.slider1 = wx.Slider(self, -1, 20, 1,100, style=wx.SL_HORIZONTAL)
        self.slider1.Bind(wx.EVT_SLIDER, self.OnSlider)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND|wx.ALL, 3)
        sizer.Add(self.slider1, 0, wx.EXPAND|wx.ALL, 3)
        self.SetSizer(sizer)
        #self.Fit()
        
        self.cyl = BRepPrimAPI.BRepPrimAPI_MakeCylinder(25,20)
        
        
    def Show(self, bool=True):
        super(TestFrame,self).Show(bool)
        wx.SafeYield()
        self.canvas.Init3dViewer()
        self.viewer = self.canvas._3dDisplay
        
        self.viewer.DisplayShape(self.cyl.Shape())
        
    def OnSlider(self, event):
        print event.GetInt()
        self.cyl.

app = wx.App()

frame = TestFrame()
frame.Show()
app.MainLoop()