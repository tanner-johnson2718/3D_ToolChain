import FreeCAD
import Part
import Sketcher
import math

# Grab the current active document
DOC = FreeCAD.activeDocument()
SKETCH_NAME = "Sketch020"

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
        self.pos_contraints = []

    def define_horizontally(self, side_len, left_point_x, left_point_y):
        self.p1.x = left_point_x
        self.p1.y = left_point_y
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

        def contrain_pos(l,x,y):
            c_no = sketch_object.addConstraint(Sketcher.Constraint('DistanceX',-1,1,l,1,x))
            self.pos_contraints.append(c_no)
            c_no = sketch_object.addConstraint(Sketcher.Constraint('DistanceY',-1,1,l,1,y))
            self.pos_contraints.append(c_no)   
        
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

        contrain_pos(self.line_numbers[0], self.p1.x, self.p1.y)
        contrain_pos(self.line_numbers[1], self.p2.x, self.p2.y)
        contrain_pos(self.line_numbers[2], self.p3.x, self.p3.y)
        contrain_pos(self.line_numbers[3], self.p4.x, self.p4.y)
        contrain_pos(self.line_numbers[4], self.p5.x, self.p5.y)
        contrain_pos(self.line_numbers[5], self.p6.x, self.p6.y)       
        
class HexGrid:
    def __init__(self, side, start_x, start_y, n_row, n_col, brim_x, brim_y):
        self.side = side
        self.start_x = start_x
        self.start_y = start_y
        self.n_row = n_row
        self.n_col = n_col
        self.brim_x = brim_x
        self.brim_y = brim_y

        self.y_delta = self.side * math.sin(math.radians(60))
        self.x_delta = self.side * math.cos(math.radians(60))
        
        self.hexs = [0] * n_row
        for i in range(0,n_row):
            self.hexs[i] = [0] * n_col

    def compute(self):
        for i in range(0, self.n_row):
            for j in range(0, self.n_col):
                self.hexs[i][j] = Hexagon()

                grid_x = self.start_x + j*(self.side + self.x_delta + self.brim_x)
                grid_y = self.start_y - i*(2 * self.y_delta + self.brim_y)
                
                if j%2 == 0:
                    # even
                    self.hexs[i][j].define_horizontally(self.side, grid_x, grid_y)
                else:
                    # odd
                    self.hexs[i][j].define_horizontally(self.side, grid_x, grid_y - self.y_delta - (self.brim_y/2))

    def draw(self, sketch_object):
        for i in range(0, self.n_row):
            for j in range(0, self.n_col):
                self.hexs[i][j].draw(sketch_object)

# Specify a hexagon size, compute spacing and n_cols and n_rows matrix. Fix corner hexagons on perimeter.
# number of columns must be odd. Number of rows >= 2, Number of columns >= 3
class HexPlate:
    def __init__(self, hex_size, plate_x, plate_y, perimeter, min_brim, max_n_row, max_n_col):
        y_delta = hex_size * math.sin(math.radians(60))
        x_delta = hex_size * math.cos(math.radians(60))

        x_start = -(plate_x/2.0) + perimeter
        y_start = (plate_y/2.0) - perimeter - y_delta

        y_travel = plate_y - 2*perimeter

        for n in range(2, max_n_row):
            brim_y = (y_travel - n*2.0*y_delta) / (n-1)
            if brim_y < min_brim:
                break
            else:
                print("N_r = " + str(n) + "   B_y = " + str(brim_y))

        x_travel = plate_x - 2*perimeter

        for n in range(3, max_n_col):
            if n%2 == 0:
                continue

            brim_x = (x_travel - (((2.0*n) - ((n-1)/2))*hex_size)) / (n-1)
            if brim_x < min_brim:
                break
            else:
                print("N_c = " + str(n) + "   B_x = " + str(brim_x))



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

    hex_plate = HexPlate(hex_size=10, plate_x=130, plate_y=245, perimeter=5, min_brim=5, max_n_row=10, max_n_col=10)
    hex_grid = HexGrid(side=10, start_x=-60, start_y=108.84, n_row=9, n_col=5, brim_x=10, brim_y=9.889428414850133)
    hex_grid.compute()
    hex_grid.draw(sketch)
        
            
hexagon()