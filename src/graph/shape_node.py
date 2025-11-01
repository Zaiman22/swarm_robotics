import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np



class Swarm:
    def __init__(self,x,y,z,angle = 0):
        # actual node 
        # minimum node in a swarm is 1
        self.node_instance = []
        # this is node shape
        self.node_count = 0
        # swarm shape rotaion
        self.pos = np.array([x,y,z],dtype=np.float32)
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

    def updateTargetShape(self, target=None):
        if target is None:
            target = self.target_shape
        else:
            self.target_shape = target

        if target not in self.avail_shape:
            raise ValueError(
                f"The target shape '{target}' is not available. Choose from {list(self.avail_shape.keys())}."
            )

        if target == "square":
            a = self.avail_shape["square"]["a"]
            px, py, pz = self.pos
            theta = getattr(self, "angle", 0)  # rotation angle (in radians)

            cos_t = math.cos(theta)
            sin_t = math.sin(theta)

            # Local square coordinates centered at origin
            local_coords = [
                ( a/2,  a/2, 0),
                (-a/2,  a/2, 0),
                ( a/2, -a/2, 0),
                (-a/2, -a/2, 0)
            ]

            # Apply rotation and translation
            square_coords = [
                (
                    px + cos_t * x - sin_t * y,  # X'
                    py + sin_t * x + cos_t * y,  # Y'
                    pz + z                       # Z' (unchanged)
                )
                for (x, y, z) in local_coords
            ]

            square_connections = [
                [1, 2],
                [0, 3],
                [0, 3],
                [1, 2]
            ]

            if self.shape_node_count != 4:
                # (Re)create square shape nodes
                self.shape_node_instance = []
                self.shape_node_count = 0
                for i, (x, y, z) in enumerate(square_coords):
                    shape_node = self.Node(i, x, y, z, square_connections[i])
                    self.shape_node_instance.append(shape_node)
                    self.shape_node_count += 1
            else:
                # Update existing nodes
                for i in range(4):
                    self.shape_node_instance[i].x = square_coords[i][0]
                    self.shape_node_instance[i].y = square_coords[i][1]
                    self.shape_node_instance[i].z = square_coords[i][2]
                    self.shape_node_instance[i].connection = square_connections[i]
        self.updateNode()



    def changeAngle(self,angle):
        self.angle = angle
        self.updateTargetShape()

    def changePosition(self,pos):
        self.pos = pos
        self.updateTargetShape()



    def updateNode(self):
        if self.target_shape == "square":
            # Corners of the square (already defined in shape_node_instance)
            corners = self.shape_node_instance
            sides = [
                (corners[0], corners[1]),  # top
                (corners[1], corners[3]),  # left
                (corners[3], corners[2]),  # bottom
                (corners[2], corners[0])   # right
            ]

            if self.node_count <= 4:
                # If only 4 nodes, just match corners
                for i in range(self.node_count):
                    self.node_instance[i].x = corners[i].x
                    self.node_instance[i].y = corners[i].y
                    self.node_instance[i].z = corners[i].z
                return

            # Compute how many in-between nodes per side
            extra_nodes = self.node_count - 4
            node_per_side = extra_nodes // 4
            remainder = extra_nodes % 4

            node_index = 0
            # Place corner nodes
            for i in range(4):
                self.node_instance[node_index].x = corners[i].x
                self.node_instance[node_index].y = corners[i].y
                self.node_instance[node_index].z = corners[i].z
                node_index += 1

            # Place in-between nodes
            for side_index, (start, end) in enumerate(sides):
                num_between = node_per_side + (1 if side_index < remainder else 0)
                for j in range(num_between):
                    t = (j + 1) / (num_between + 1)
                    x = start.x + t * (end.x - start.x)
                    y = start.y + t * (end.y - start.y)
                    z = start.z + t * (end.z - start.z)

                    if node_index < len(self.node_instance):
                        self.node_instance[node_index].x = x
                        self.node_instance[node_index].y = y
                        self.node_instance[node_index].z = z
                        node_index += 1


    def createNode(self,x,y,z):
        node = self.Node(self.node_count,x,y,z)
        self.node_instance.append(node)
        self.node_count += 1







    



# visualization
if __name__ == "__main__":
    matplotlib.use('TkAgg')  # or Qt5Agg if available
    ax = plt.figure().add_subplot(projection='3d')

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
    swarm1.avail_shape["square"]["a"] = 2
    swarm1.updateTargetShape()


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