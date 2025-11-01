import matplotlib.pyplot as plt
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation



from shape_node import Swarm


a = 0

if __name__ == "__main__":
    matplotlib.use('TkAgg')  # or Qt5Agg if available
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')


    # initiating swarm object
    swarm1 = Swarm(0,0,0)
    swarm1.createNode(2,2,2)
    swarm1.createNode(2,2,2)
    swarm1.createNode(2,2,2)
    swarm1.createNode(2,2,2)
    swarm1.createNode(2,2,2)
    swarm1.createNode(2,2,2)
    swarm1.createNode(2,2,2)
    swarm1.createNode(2,2,2)
    swarm1.createNode(2,2,2)
    swarm1.createNode(2,2,2)
    swarm1.createNode(2,2,2)
    swarm1.createNode(2,2,2)
    swarm1.createNode(2,2,2)
    swarm1.createNode(2,2,2)
    swarm1.avail_shape["square"]["a"] = 1
    swarm1.updateTargetShape()

    # --- Initialization function ---
    def init():
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(-1, 1)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        return []

    # --- Update function ---
    def update(frame):
        global a
        ax.cla()  # clear the axes each frame
        swarm1.changePosition(np.array([a,0,0]))
        a += 0.01
        
        # swarm1.pos[0] += 0.1
        # print(type(swarm1.pos[0]))
        # --- plot target shape ---
        for idx, i in enumerate(swarm1.shape_node_instance):
            ax.scatter(i.x, i.y, i.z, zdir='z', c=f"C{idx}")
            for conn_idx in i.connection:
                if conn_idx < len(swarm1.shape_node_instance):
                    conn_node = swarm1.shape_node_instance[conn_idx]
                    ax.plot(
                        [i.x, conn_node.x],
                        [i.y, conn_node.y],
                        [i.z, conn_node.z],
                        'k-', alpha=0.6
                    )
        # --- plot drone estimation ---
        for idx, i in enumerate(swarm1.node_instance):
            ax.scatter(i.x, i.y, i.z, c="black")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        # ax.set_xlim(swarm1.pos[0]-1,swarm1.pos[0]+1)
        ax.set_xlim(-1,1)
        ax.set_ylim(swarm1.pos[1]-1,swarm1.pos[1]+1)
        ax.set_zlim(swarm1.pos[2]-1,swarm1.pos[2]+1)
        ax.set_title(f"Frame {frame}")

        return []

    # --- Animate ---
    anim = FuncAnimation(fig, update, frames=100, init_func=init, interval=10, blit=False)

    plt.show()
