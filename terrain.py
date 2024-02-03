import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
from PyQt5 import QtWidgets 
import sys
from OpenGL import GL
from opensimplex import OpenSimplex


class Terrain(object):
    def __init__(self):
        # Create and customize GUI window
        self.app = QtWidgets.QApplication(sys.argv) 
        self.window = gl.GLViewWidget()
        self.window.setGeometry(0, 0, 2560, 1440)
        self.window.show()
        self.window.setWindowTitle("Terrain")
        self.window.setCameraPosition(distance=30, elevation=8)
        
        # Create grid
        grid = gl.GLGridItem()
        grid.scale(2, 2, 2)
        grid.setDepthValue(10)
        self.window.addItem(grid)
        
        self.nsteps = 1
        self.ypoints = range(-20, 22, self.nsteps)
        self.xpoints = range(-20, 22, self.nsteps)
        self.nfaces = len(self.ypoints)
 
        verts = np.array([
            [
                x, y, 0
            ] for n, x in enumerate(self.xpoints) for m, y in enumerate(self.ypoints)
        ], dtype=np.float32) 
        
        faces = []
        colors = []
        for m in range(self.nfaces - 1):
            yoff = m * self.nfaces
            for n in range(self.nfaces - 1):
                faces.append([n + yoff, yoff + n + self.nfaces, yoff + n + self.nfaces + 1])
                faces.append([n + yoff, yoff + n + 1, yoff + n + self.nfaces + 1]) 
                colors.append([0, 0, 0, 0])
                colors.append([0, 0, 0, 0])
        
        faces = np.array(faces)
        colors = np.array(colors) 
        self.m1 = gl.GLMeshItem(
            vertexes = verts,
            faces = faces, faceColors = colors,
            smooth = False, drawEdges = True
        )
        self.m1.setGLOptions('additive')
        self.window.addItem(self.m1)
        

    def start(self):  
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtWidgets.QApplication.instance().exec() 

if __name__ == "__main__":
    terrain = Terrain()
    terrain.start()
    