from ._template import SimulationEngine

import numpy as np

class PP(SimulationEngine):
    G = 6.674 * 10 ** -11
    def simulate(self, steps):
        bodyref = self.bodies[0]
        num = bodyref.shape[0]
        for i in range(steps):
            distsq = np.zeros((num, num))
            dist = np.zeros((num, num))
            x_dist = np.zeros((num, num))
            y_dist = np.zeros((num, num))
            z_dist = np.zeros((num, num))
            for i in range(num):
                padargs = [(0, num - i + 1), 'constant']
                x_dist[i] = np.pad((bodyref[:i - 1,0]-bodyref[i,0]), *padargs)
                y_dist[i] = np.pad((bodyref[:i - 1,1]-bodyref[i,1]), *padargs)
                z_dist[i] = np.pad((bodyref[:i - 1,2]-bodyref[i,2]), *padargs)
                distsq[i] = np.pad((x_dist[:i - 1]**2 + y_dist[:i - 1]**2 + z_dist[:i - 1]**2), *padargs, constant_values = 0)
                dist[i] = np.pad(np.sqrt(distsq[i,:i-1]), *padargs, constant_values = 0)
                distsq[i] = np.pad(1/distsq[i,:i-1], *padargs, constant_values = 0)
            dist += dist.T
            distsqr += distsqr.T
            x_dist -= x_dist.T
            y_dist -= y_dist.T
            z_dist -= z_dist.T
            acceltot = self.G*np.hstack(bodyref[7,::])*distsq
            accel_x = np.sum(-(acceltot*(x_dist/dist)), axis=0)
            accel_y = np.sum(-(acceltot*(y_dist/dist)), axis=0)
            accel_z = np.sum(-(acceltot*(z_dist/dist)), axis=0)
            dvx = accel_x * self.steptime
            dvy = accel_y * self.steptime
            dvz = accel_z * self.steptime
            bodyref[::,0] += (bodyref[::,3] + dvx/2)*self.steptime
            bodyref[::,1] += (bodyref[::,4] + dvy/2)*self.steptime
            bodyref[::,2] += (bodyref[::,5] + dvz/2)*self.steptime
            bodyref[::,3] += dvx
            bodyref[::,4] += dvy
            bodyref[::,5] += dvz

