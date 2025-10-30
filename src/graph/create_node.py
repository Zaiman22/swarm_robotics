import math
import matplotlib
matplotlib.use('TkAgg')  # or Qt5Agg if available
import matplotlib.pyplot as plt
import numpy as np

ax = plt.figure().add_subplot(projection='3d')


class Swarm:
    def __init__(self,x,y,size = 1):
        # minimum node in a swarm is 1
        self.node_instance = [0]
        self.count_node = 1
        # first index position
        self.pos = np.array((x,y))

        # length
        # 0 is null 
        self.length = np.zeros((1,1))


        # angle 
        # 0 is null
        self.angle = np.zeros((1,1))


        self.target_shape = "square"
        self.avail_shape = {
            "square":{"size": 1},
        }


    
    def updateNode(self):
        if self.target_shape == "square":
            # Define connection pattern for each new node
            connections = [
                [0],       # Node 2 connects to Node 1
                [0],       # Node 3 connects to Node 1
                [1, 2]     # Node 4 connects to Nodes 2 and 3
            ]

            # Only proceed if pattern exists
            if self.count_node < 4:
                n = self.count_node  # current matrix size
                conn = connections[self.count_node - 1]  # new node's connections

                # ✅ Add new column (incoming connections)
                new_col = np.zeros((n, 1), dtype=int)
                for i in conn:
                    new_col[i][0] = 1
                self.length = np.append(self.length, new_col, axis=1)

                # ✅ Add new row (outgoing connections)
                new_row = np.zeros((1, n + 1), dtype=int)
                for i in conn:
                    new_row[0][i] = 1
                self.length = np.append(self.length, new_row, axis=0)

                self.count_node += 1
            else:
                print("⚠️ Maximum defined connection pattern reached.")



                


    def updateTargetShape(self,target):
        if target not in self.avail_shape:
            raise ValueError(f"The target shape is not in the available target shape, consider choosing {self.avail_shape}")






    



# visualization

swarm1 = Swarm(0,0)
swarm1.updateNode()  # Step 2
swarm1.updateNode()  # Step 3
swarm1.updateNode()  # Step 4
swarm1.updateNode()  # Step 4

print(swarm1.node_instance)
print(swarm1.length)
print(swarm1.angle)
print(swarm1.count_node)


# for idx,i in enumerate(swarm1.node_instance):

#     # plot vertex
#     ax.scatter(i.x, i.y, i.z, zdir='y', c=f"C{idx}", label=i.name)
#     # plot edges


# ax.legend()
# ax.set_xlim(0, 1)
# ax.set_ylim(0, 1)
# ax.set_zlim(0, 1)
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# plt.show()