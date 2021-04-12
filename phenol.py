import networkx as NX
import pylab as P

def atomcolorsandsizes():
    """construct a dictionary to give different
       atoms a different color and size
       returns 2 dictionaries
    """
    
    atoms = {}

    atomcolors={}
    atomcolors['C']='#909090'
    atomcolors['O']='#FF0D0D'
    atomcolors['H']='#DDDDDD'
    
    atomsizes={}
    atomsizes['C']=1000
    atomsizes['O']=400
    atomsizes['H']=300
    return atomcolors, atomsizes

def readnodesfromfile(nodesfilename="", G=NX.Graph()):
    """ read the nodes from a file
        each line consists of a number and the atomtype
        separated by blank space.
        
        nodes are added to the graph G
        atomtypes to the list of atoms
       
        returns G and a dictionary of atoms
    """

    f=open(nodesfilename)
    lines = f.readlines()
    atoms={}
    f.close()
    for line in lines:
        [nr, atomtype] = line.split()
        if not atomtype in atoms.keys():
            atoms[atomtype] = []
        G.add_node(nr)
        atoms[atomtype].append(nr)
    return G, atoms



def readedgesfromfile(edgesfilename="", G=NX.Graph()):
    """ read the edges from a file
        each line consists of the 2 numbers of the nodes of the edge
  
        returns updated G
    """ 
        
    f=open(edgesfilename)
    lines = f.readlines()
    f.close()
    for line in lines:
        inds = line.split()
        G.add_edge(inds[0],inds[1])
    return G

def makegraphfromfile(nodesfilename="", edgesfilename=""):

    atomcolors, atomsizes=atomcolorsandsizes()
    G=NX.Graph()
    G, atoms=readnodesfromfile(nodesfilename=nodesfilename, G=G)
    G=readedgesfromfile(edgesfilename=edgesfilename, G=G)
    print("The nodes of G are:", list(G.nodes))
    print("The edges of G are:", list(G.edges))
    return G, atoms, atomcolors, atomsizes
    
    
def drawGraph(G=NX.Graph(), atoms={}, atomsizes={}, atomcolors={}, nriterations=100):
    """ - G is a graph, 
        - atoms a dictionary with as keys the atomtypes
          and as values a list of atom numbers of that atomtype
        - atomcolors is a dictionary of colors per atomtype
        - atomsizes is a dictionary of colors per atomtype
        - nriterations the number of iterations the layout
          algorithm should do
    """
    
    fig=P.figure()
    pos=NX.spring_layout(G, iterations=nriterations) 
    for atomtype in atoms.keys():
        NX.draw_networkx_nodes(G, pos, nodelist=atoms[atomtype],
                               node_color=atomcolors[atomtype],
                               node_size=atomsizes[atomtype])  
    NX.draw_networkx_edges(G,pos)

    labels = {}
    for node in G.nodes():
        labels[node] = node
    NX.draw_networkx_labels(G,pos,labels,font_color='black',
                            font_family='sans-serif')
    
    P.show()
        

if __name__=="__main__":
    G, atoms, atomcolors, atomsizes=makegraphfromfile('fenolnodes.txt', 'fenoledges.txt')
    drawGraph(G=G, atoms=atoms, atomcolors=atomcolors, atomsizes=atomsizes, nriterations=500)
    

