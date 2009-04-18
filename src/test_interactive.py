import wx
import os

os.environ['CSF_GraphicShr'] = "/usr/local/lib/libTKOpenGl.so"

from OCC.Display.wxDisplay import wxViewer3d
from OCC import BRepPrimAPI, AIS

class MyCanvas(wxViewer3d):
    def __init__(self, *args, **kwds):
        super(MyCanvas, self).__init__(*args, **kwds)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.inited = False
        
    def OnPaint(self, event):
        if not self.inited:
            self.InitDriver()
            self.viewer = self._display
            self.context = self.viewer.Context
            self.inited = True
        event.Skip()

class TestFrame(wx.Frame):
    def __init__(self):
        super(TestFrame,self).__init__(None, -1, "test frame", size=(600,500))
        self.canvas = MyCanvas(self)
        self.viewer = None
        #self.Show()
        
        self.slider1 = wx.Slider(self, -1, 20, 1,100, style=wx.SL_HORIZONTAL)
        self.slider1.Bind(wx.EVT_SLIDER, self.OnSlider)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND|wx.ALL, 3)
        sizer.Add(self.slider1, 0, wx.EXPAND|wx.ALL, 3)
        self.SetSizer(sizer)
        self.Fit()
        
        self.cyl = BRepPrimAPI.BRepPrimAPI_MakeCylinder(25,20).Shape()
        self.ais_shape = AIS.AIS_Shape(self.cyl)  
        
    def OnSlider(self, event):
        #print event.GetInt()
        cyl = BRepPrimAPI.BRepPrimAPI_MakeCylinder(25,event.GetInt()).Shape()
        self.ais_shape.Set(cyl)
        self.context.Redisplay(AIS.AIS_KOI_Shape)

app = wx.App()

frame = TestFrame()
frame.Show()
app.MainLoop()