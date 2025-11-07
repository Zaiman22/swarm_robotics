import numpy as np
import matplotlib.pyplot as plt
import time
import cProfile
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation


from Simulation.quadFiles.quad import Quadcopter
from Simulation.utils.windModel import Wind
import Simulation.utils as utils
import Simulation.config as config
from controller.pid_helper import PIDController
from controller.GA_helper import genetic_helper


def motor_input(thrust,yaw,pitch,roll):
    return np.array([thrust+roll+pitch+yaw,
                     thrust-pitch+roll-yaw,
                     thrust-roll-pitch+yaw,
                     thrust+pitch-roll-yaw])





def quad_sim(t, Ts, quad, motor_control, wind):
    
    # Dynamics (using last timestep's commands)
    # ---------------------------
    quad.update(t, Ts, motor_control, wind)
    t += Ts

    return t


if __name__ == "__main__":
    start_time = time.time

    # Simulation Setup
    # --------------------------- 
    Ti = 0
    Ts = 0.005
    Tf = 20
    ifsave = 0


    # Initialize Quadcopter, Controller, Wind, Result Matrixes
    # ---------------------------
    quad = Quadcopter(Ti)
    wind = Wind('None', 2.0, 90, -15)

    altitude_controller = PIDController(kp=2.7, ki=5.5, kd=60.0, dt=Ts)
    alt_pid_coef = genetic_helper(4,10, 0.2)
    alt_pid_coef.min_value = 0
    alt_pid_coef.number_of_children = 8
    alt_score = np.zeros([alt_pid_coef.size_population,2])


    altitude_setpoint = 1.0
    ffHover =523
    
    quad_input = np.zeros(4)
    # Initialize Result Matrixes
    # ---------------------------
    for i in range(10): # 10 generation
        for j in range(len(alt_pid_coef.size_population)):
            
    numTimeStep = int(Tf/Ts+1)

    t_all          = np.zeros(numTimeStep)
    s_all          = np.zeros([numTimeStep, len(quad.state)])
    pos_all        = np.zeros([numTimeStep, len(quad.pos)])
    vel_all        = np.zeros([numTimeStep, len(quad.vel)])
    quat_all       = np.zeros([numTimeStep, len(quad.quat)])
    omega_all      = np.zeros([numTimeStep, len(quad.omega)])
    euler_all      = np.zeros([numTimeStep, len(quad.euler)])
    wMotor_all     = np.zeros([numTimeStep, len(quad.wMotor)])
    thr_all        = np.zeros([numTimeStep, len(quad.thr)])
    tor_all        = np.zeros([numTimeStep, len(quad.tor)])

    t_all[0]            = Ti
    s_all[0,:]          = quad.state
    pos_all[0,:]        = quad.pos
    vel_all[0,:]        = quad.vel
    quat_all[0,:]       = quad.quat
    omega_all[0,:]      = quad.omega
    euler_all[0,:]      = quad.euler
    wMotor_all[0,:]     = quad.wMotor
    thr_all[0,:]        = quad.thr
    tor_all[0,:]        = quad.tor

    # Run Simulation
    # ---------------------------
    # print("start simulation")
    t = Ti
    i = 1

    while round(t,3) < Tf:
        
        # controller

        thrus_signal = altitude_controller.getInput(altitude_setpoint, -quad.pos[2])
        thrus_signal +=ffHover

        quad_input = motor_input(thrus_signal, 0, 0, 0)
        print(quad.pos[2], thrus_signal)
        # time step simulation
        t = quad_sim(t, Ts, quad, quad_input, wind)
        
        # print("{:.3f}".format(t))
        t_all[i]             = t
        s_all[i,:]           = quad.state
        pos_all[i,:]         = quad.pos
        vel_all[i,:]         = quad.vel
        quat_all[i,:]        = quad.quat
        omega_all[i,:]       = quad.omega
        euler_all[i,:]       = quad.euler
        wMotor_all[i,:]      = quad.wMotor
        thr_all[i,:]         = quad.thr
        tor_all[i,:]         = quad.tor
        
        # print(quad.wMotor)
        i += 1
    
    end_time = time.time()






    # View Results
    # ---------------------------
    params = quad.params
    numFrames = 8


    x = pos_all[:,0]
    y = pos_all[:,1]
    z = pos_all[:,2]

    fig = plt.figure()
    ax = p3.Axes3D(fig,auto_add_to_figure=False)
    fig.add_axes(ax)
    line1, = ax.plot([], [], [], lw=2, color='red')
    line2, = ax.plot([], [], [], lw=2, color='blue')
    line3, = ax.plot([], [], [], '--', lw=1, color='blue')

    # Setting the axes properties
    extraEachSide = 0.5
    maxRange = 0.5*np.array([x.max()-x.min(), y.max()-y.min(), z.max()-z.min()]).max() + extraEachSide
    mid_x = 0.5*(x.max()+x.min())
    mid_y = 0.5*(y.max()+y.min())
    mid_z = 0.5*(z.max()+z.min())
    
    ax.set_xlim3d([mid_x-maxRange, mid_x+maxRange])
    ax.set_xlabel('X')
    if (config.orient == "NED"):
        ax.set_ylim3d([mid_y+maxRange, mid_y-maxRange])
    elif (config.orient == "ENU"):
        ax.set_ylim3d([mid_y-maxRange, mid_y+maxRange])
    ax.set_ylabel('Y')
    ax.set_zlim3d([mid_z-maxRange, mid_z+maxRange])
    ax.set_zlabel('Altitude')

    titleTime = ax.text2D(0.05, 0.95, "", transform=ax.transAxes)

    trajType = ''
    yawTrajType = ''

    titleType1 = ax.text2D(0.95, 0.95, trajType, transform=ax.transAxes, horizontalalignment='right')
    titleType2 = ax.text2D(0.95, 0.91, 'Yaw: '+ yawTrajType, transform=ax.transAxes, horizontalalignment='right')   
    
    ax.scatter(0, 0, 1, color='green', alpha=1, marker = 'o', s = 25)

    def updateLines(i):

        time = t_all[i*numFrames]
        pos = pos_all[i*numFrames]
        x = pos[0]
        y = pos[1]
        z = pos[2]

        x_from0 = pos_all[0:i*numFrames,0]
        y_from0 = pos_all[0:i*numFrames,1]
        z_from0 = pos_all[0:i*numFrames,2]
    
        dxm = params["dxm"]
        dym = params["dym"]
        dzm = params["dzm"]
        
        quat = quat_all[i*numFrames]
    
        if (config.orient == "NED"):
            z = -z
            z_from0 = -z_from0
            quat = np.array([quat[0], -quat[1], -quat[2], quat[3]])
    
        R = utils.quat2Dcm(quat)    
        motorPoints = np.array([[dxm, -dym, dzm], [0, 0, 0], [dxm, dym, dzm], [-dxm, dym, dzm], [0, 0, 0], [-dxm, -dym, dzm]])
        motorPoints = np.dot(R, np.transpose(motorPoints))
        motorPoints[0,:] += x 
        motorPoints[1,:] += y 
        motorPoints[2,:] += z 
        
        line1.set_data(motorPoints[0,0:3], motorPoints[1,0:3])
        line1.set_3d_properties(motorPoints[2,0:3])
        line2.set_data(motorPoints[0,3:6], motorPoints[1,3:6])
        line2.set_3d_properties(motorPoints[2,3:6])
        line3.set_data(x_from0, y_from0)
        line3.set_3d_properties(z_from0)
        titleTime.set_text(u"Time = {:.2f} s".format(time))
        
        return line1, line2


    def ini_plot():

        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(-1, 1)

        line1.set_data(np.empty([1]), np.empty([1]))
        line1.set_3d_properties(np.empty([1]))
        line2.set_data(np.empty([1]), np.empty([1]))
        line2.set_3d_properties(np.empty([1]))
        line3.set_data(np.empty([1]), np.empty([1]))
        line3.set_3d_properties(np.empty([1]))

        return line1, line2, line3

        
    # Creating the Animation object

    # plotting angle
    baba, angle_plot = plt.subplots()
    angle_plot.plot(t_all, -pos_all[:,2], label='Roll')

    line_ani = animation.FuncAnimation(fig, updateLines, init_func=ini_plot, frames=len(t_all[0:-2:numFrames]), interval=(Ts*1000*numFrames), blit=False)
    plt.show()