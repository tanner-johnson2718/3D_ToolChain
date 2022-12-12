import FreeCAD
import Part
import Sketcher
import math

# Grab the current active document
DOC = FreeCAD.activeDocument()
SKETCH_NAME = "TARGET"

print("Hex Tile Maco starting..")

class Hexagon:
    class Point:
        def __init__(self,x,y):
            self.x= x
            self.y = y

    def __init__(self):
        self.p1 = Hexagon.Point(0,0)    # Far left
        self.p2 = Hexagon.Point(0,0)    # Top Left
        self.p3 = Hexagon.Point(0,0)    # Top Right
        self.p4 = Hexagon.Point(0,0)    # Far right
        self.p5 = Hexagon.Point(0,0)    # Bottom right
        self.p6 = Hexagon.Point(0,0)    # Bottom left

        self.length = 0

        self.line_numbers = []
        self.coincident_constraints = []
        self.len_constraints = []
        self.horizontal_contraints = []
        self.angle_contraints = []
        self.pos_contraints = []

    def define_horizontally(self, side_len, left_point_x, left_point_y):
        self.p1.x = left_point_x
        self.p2.y = left_point_y
        self.length = side_len

        delta_x = side_len * math.cos(math.radians(60))
        delta_y = side_len * math.sin(math.radians(60))

        # Top Left calc
        self.p2.x = self.p1.x + delta_x
        self.p2.y = self.p1.y + delta_y

        # Top Right calc
        self.p3.x = self.p2.x + side_len
        self.p3.y = self.p2.y

        # Far Right calc
        self.p4.x = self.p3.x + delta_x
        self.p4.y = self.p1.y

        # Bottom Right calc
        self.p5.x = self.p3.x
        self.p5.y = self.p1.y - delta_y

        # Bottom Left calc
        self.p6.x = self.p2.x
        self.p6.y = self.p5.y

        return

    def draw(self, sketch_object):
        def draw_line(p1, p2):
            line_no = sketch_object.addGeometry(Part.LineSegment(FreeCAD.Vector(p1.x,p1.y,0),FreeCAD.Vector(p2.x,p2.y,0)),False)
            self.line_numbers.append(line_no)

        # connect right end point of l1 to left end point of l2
        def connect_line(l1,l2):
            c_no = sketch_object.addConstraint(Sketcher.Constraint('Coincident', l1,2,l2,1))
            self.coincident_constraints.append(c_no)

        def constrain_line_len(l):
            c_no = sketch_object.addConstraint(Sketcher.Constraint('Distance',l,self.length))
            self.len_constraints.append(c_no)
        
        draw_line(self.p1,self.p2)
        draw_line(self.p2,self.p3) 
        draw_line(self.p3,self.p4) 
        draw_line(self.p4,self.p5) 
        draw_line(self.p5,self.p6) 
        draw_line(self.p6,self.p1)

        connect_line(self.line_numbers[0], self.line_numbers[1])
        connect_line(self.line_numbers[1], self.line_numbers[2])
        connect_line(self.line_numbers[2], self.line_numbers[3])
        connect_line(self.line_numbers[3], self.line_numbers[4])
        connect_line(self.line_numbers[4], self.line_numbers[5])
        connect_line(self.line_numbers[5], self.line_numbers[0])

        constrain_line_len(self.line_numbers[0])
        constrain_line_len(self.line_numbers[1])
        constrain_line_len(self.line_numbers[2])
        constrain_line_len(self.line_numbers[3])
        constrain_line_len(self.line_numbers[4])
        constrain_line_len(self.line_numbers[5])

        self.horizontal_contraints.append(sketch_object.addConstraint(Sketcher.Constraint('Horizontal',self.line_numbers[1])))
        self.horizontal_contraints.append(sketch_object.addConstraint(Sketcher.Constraint('Horizontal',self.line_numbers[4])))

        self.angle_contraints.append(sketch_object.addConstraint(Sketcher.Constraint('Angle',self.line_numbers[0],2,self.line_numbers[1],1,math.radians(120))))
        self.angle_contraints.append(sketch_object.addConstraint(Sketcher.Constraint('Angle',self.line_numbers[5],2,self.line_numbers[0],1,math.radians(120))))

        self.pos_contraints.append(sketch_object.addConstraint(Sketcher.Constraint('DistanceX',-1,1,self.line_numbers[0],1,self.p1.x)))
        self.pos_contraints.append(sketch_object.addConstraint(Sketcher.Constraint('DistanceY',-1,1,self.line_numbers[0],1,self.p1.y)))         
        

# Main macro code
def hexagon():
    # Scan through documents and find keyed sketch named "TARGET"
    sketch = 0
    for obj in DOC.Objects:
        if obj.Label.find(SKETCH_NAME) > -1:
            print("Found Target Sketch")
            sketch = obj
            break
        else:
            continue

    if sketch == 0:
        print("Could not find target sketch")
        return

    print("Found Sketch")

    hex = Hexagon()
    hex.define_horizontally(10,0,0)
    hex.draw(sketch)

    hex2 = Hexagon()
    hex2.define_horizontally(10,20,0)
    hex2.draw(sketch)
        
        
            
hexagon()