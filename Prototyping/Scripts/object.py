import math

class Object:
    def __init__(self, name='object', bnd_box=[0,0,0,0], score=0.5):
        self.name = name
        self.bnd_box = bnd_box
        self.score = score
        x = (self.bnd_box[0] + self.bnd_box[2]) // 2
        y = (self.bnd_box[1] + self.bnd_box[3]) // 2
        self.center = [x, y]


    def get_object_position(self, known_width=10): # known width in cm
        x = self.center[0]
        y = self.center[1]

        width_pix = self.bnd_box[2] - self.bnd_box[0] # xmax - xmin
        # camera parameters after calibration with open cv
        # x & y focal lengths of the camera
        fx = 1.01228658 * math.exp(3)
        fy = 1.01955224 * math.exp(3)

        # x & y optical center points of the camera
        cx = 6.51698659 * math.exp(2)
        cy = 3.83238934 * math.exp(2)


        z_world = (fx * known_width) / (width_pix)

        x_world = ((x-cx)*z_world)/fx
        y_world = ((y-cy)*z_world)/fy

        return x_world, y_world, z_world
