import numpy as np

class Graph:
    def __init__(self,num_nodes):
        self.size= num_nodes
        self.g=np.zeros(shape=(self.size,self.size),dtype=np.int32)
        self.rg=np.zeros(shape=(self.size,self.size),dtype=np.int32)

    def add_edge(self,u,v,c):
        """
        adds a directed edge from u to v with capacity c
        :param u: int
        source vertex
        :param v: int
        destination vertex
        :param c: int
        capactity
        :return: None
        """
        self.g[u][v]=c
        self.rg[u][v] = c

    def get_numVertices(self):
        return self.size

    def residual_breadthFirstSearch(self,src ,dst):
        """
        Checks if there is a path in the residual graph from src to dst, and returns a boolean indicating the result
        :param src: int
            source vertice
        :param dst: int
            destination vertice
        :return: boolean, array
            Whether there is a path from stc to dst, and a list containing the path.
        """
        path=[-1]*self.size
        queue=[]
        queue.append(src)
        visited= [0]*self.size

        while len(queue)>0:
            u = queue.pop(0)
            for v, capacity in enumerate(self.rg[u]):
                if visited[v] == 0 and capacity > 0:
                    queue.append(v)
                    visited[v] = 1
                    path[v] = u
                    if v == dst:
                        return True, path

        return False, path

    def FordFulkerson(self, src, dst):
        """
        return the maximum -flow from src to dst in the graph using ForfFulkerson's algorthim
        :param src: int
            source vertice
        :param dst: int
            sink vertice
        :return: int
            The maximul-flow from src to dst
        """

        maxflow = 0
        still_a_path, path= self.residual_breadthFirstSearch(src,dst)
        while still_a_path:

            smallestPathflow= 2000000000
            s = dst
            while s != src:
                smallestPathflow = min(smallestPathflow, self.rg[path[s]][s])
                s = path[s]

            maxflow += smallestPathflow
            v = dst
            while (v != src):
                u = path[v]
                self.rg[u][v] -= smallestPathflow
                self.rg[v][u] += smallestPathflow
                v = path[v]
                
            still_a_path, path = self.residual_breadthFirstSearch(src, dst)

        return maxflow

