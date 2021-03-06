from ._template import SimulationEngine

import numpy as np

class PP(SimulationEngine):
    G = 6.674 * 10 ** -11
    def simulate(self, steps):
        bodyref = self.bodies[0]
        if self.masslessbodies != None:
            lessref = self.masslessbodies[0]
        num = bodyref.shape[0]
        for i in range(steps):
            if self.masslessbodies != None:
                x_masd = np.hstack(bodyref[::,0]) - np.vstack(lessref[::,0])
                y_masd = np.hstack(bodyref[::,1]) - np.vstack(lessref[::,1])
                z_masd = np.hstack(bodyref[::,2]) - np.vstack(lessref[::,2])

                x_masdsq = x_masd**2
                y_masdsq = y_masd**2
                z_masdsq = z_masd**2

                masdsq = x_masdsq + y_masdsq + z_masdsq
                masd = np.sqrt(masdsq)
                masdsq = 1/masdsq

                masacceltot = self.G*np.hstack(bodyref[::,7])*masdsq
                massa_x = np.sum((masacceltot*(x_masd/masd)), axis=1)
                massa_y = np.sum((masacceltot*(y_masd/masd)), axis=1)
                massa_z = np.sum((masacceltot*(z_masd/masd)), axis=1)

                lessref[::,3] += massa_x * self.steptime
                lessref[::,4] += massa_y * self.steptime
                lessref[::,5] += massa_z * self.steptime
            
                lessref[::,0] += (lessref[::,3])*self.steptime
                lessref[::,1] += (lessref[::,4])*self.steptime
                lessref[::,2] += (lessref[::,5])*self.steptime

            x_dist = np.hstack(bodyref[::,0]) - np.vstack(bodyref[::,0])
            y_dist = np.hstack(bodyref[::,1]) - np.vstack(bodyref[::,1])
            z_dist = np.hstack(bodyref[::,2]) - np.vstack(bodyref[::,2])

            x_distsq = x_dist**2
            y_distsq = y_dist**2
            z_distsq = z_dist**2

            distsq = (x_distsq + y_distsq + z_distsq)
            dist = np.sqrt(distsq)
            dist = np.where(dist != 0, dist, np.inf)
            distsq = 1/np.where(distsq != 0, distsq, np.inf)

            acceltot = self.G*np.hstack(bodyref[::,7])*distsq
            accel_x = np.sum((acceltot*(x_dist/dist)), axis=1)
            accel_y = np.sum((acceltot*(y_dist/dist)), axis=1)
            accel_z = np.sum((acceltot*(z_dist/dist)), axis=1)

            bodyref[::,3] += accel_x * self.steptime
            bodyref[::,4] += accel_y * self.steptime
            bodyref[::,5] += accel_z * self.steptime
            
            bodyref[::,0] += (bodyref[::,3])*self.steptime
            bodyref[::,1] += (bodyref[::,4])*self.steptime
            bodyref[::,2] += (bodyref[::,5])*self.steptime