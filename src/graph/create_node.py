import math
import matplotlib
matplotlib.use('TkAgg')  # or Qt5Agg if available
import matplotlib.pyplot as plt
import numpy as np

ax = plt.figure().add_subplot(projection='3d')


class Swarm:
    def __init__(self,x,y,z,angle = 0):
        # actual node 
        # minimum node in a swarm is 1
        self.node_instance = []
        # this is node shape
        self.node_count = 0
        # swarm shape rotaion
        self.pos = np.array([x,y,z])
        self.angle = angle


        # target/shape node
        self.shape_node_count = 0
        self.shape_node_instance = []
        self.avail_shape = {
            # shape node, a is size
            "square":{"node":4,"a": 1},
        }
        self.target_shape = "square"
        self.updateTargetShape("square")




    class Node:
        def __init__(self,index,x,y,z, connection =None):
            self.index = index
            self.x = x
            self.y = y
            self.z = z
            self.connection = connection

    def updateTargetShape(self,target = None):
        if target == None:
            if (self.target_shape == "square"):
                pass
        if target not in self.avail_shape:
            raise ValueError(f"The target shape is not in the available target shape, consider choosing {self.avail_shape}")
        else:
            if (target == "square"):
                if (self.shape_node_count <4):
                    # restart
                    self.shape_node_count = 0
                    self.shape_node_instance = []
                    shape_node = self.Node(self.shape_node_count,self.pos[0],self.pos[1],self.pos[2],[1,2])
                    self.shape_node_instance.append(shape_node)
                    self.shape_node_count += 1
                    shape_node = self.Node(self.shape_node_count,self.pos[0]-self.avail_shape["square"]["a"],self.pos[1],self.pos[2],[0,3])
                    self.shape_node_instance.append(shape_node)
                    self.shape_node_count += 1
                    shape_node = self.Node(self.shape_node_count,self.pos[0],self.pos[1],self.pos[2]-self.avail_shape["square"]["a"],[0,3])
                    self.shape_node_instance.append(shape_node)
                    self.shape_node_count += 1
                    shape_node = self.Node(self.shape_node_count,self.pos[0]-self.avail_shape["square"]["a"],self.pos[1],self.pos[2]-self.avail_shape["square"]["a"],[1,2])
                    self.shape_node_instance.append(shape_node)
                    self.shape_node_count += 1



    def updateNode(self):
        if(self.target_shape == "square"):
            node_in_side = (self.node_count-1)//4
            side = 0 
            node_side_count = 0
            for i in range(self.node_count):
                if (i<4):
                    self.node_instance[i].x = self.shape_node_instance[i].x
                    self.node_instance[i].y = self.shape_node_instance[i].y
                    self.node_instance[i].z = self.shape_node_instance[i].z
                else:
                    if side <4:
                        if node_side_count < node_in_side:
                            self.node_instance[i].x = self.shape_node_instance[i].x
                            self.node_instance[i].y = self.shape_node_instance[i].y
                            self.node_instance[i].z = self.shape_node_instance[i].z
        

    def createNode(self,x,y,z):
        node = self.Node(self.node_count,x,y,z)
        self.node_instance.append(node)
        self.node_count += 1







    



# visualization

swarm1 = Swarm(0,0,0)
swarm1.createNode(2,2,2)
swarm1.createNode(2,2,2)
# swarm1.createNode(2,2,2)
# swarm1.createNode(2,2,2)
# swarm1.createNode(2,2,2)
swarm1.updateNode()


print(swarm1.shape_node_count)


# plot target shape

for idx,i in enumerate(swarm1.shape_node_instance):

    # plot vertex
    ax.scatter(i.x, i.y, i.z, zdir='y', c=f"C{idx}", label=f"target`:{idx}")

    # plot edges
    for conn_idx in i.connection:
        if conn_idx < len(swarm1.shape_node_instance):
            conn_node = swarm1.shape_node_instance[conn_idx]
            ax.plot(
                [i.x, conn_node.x],
                [i.z, conn_node.z],
                [i.y, conn_node.y],
                'k-', alpha=0.6
            )

# plot drone estimation


for idx,i in enumerate(swarm1.node_instance):

    # plot vertex
    ax.scatter(i.x, i.y, i.z, zdir='y', c=f"black", label=f"target`:{idx}")


ax.legend()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.view_init(elev=20., azim=-35, roll=0)
plt.show()