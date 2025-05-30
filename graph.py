'''
Core services for managing a pyvis network graph

## physics of node layout controls the bounce in the edges

https://stackoverflow.com/questions/74108243/pyvis-is-there-a-way-to-disable-physics-without-losing-graphs-layout

1. add_node physics=False
1. add_edge physics=False
3. net.toggle_physics(False)
4. Network(options={"physics": {"enabled": False}})
      https://stackoverflow.com/questions/67548160/pyvis-graph-wont-stop-moving
5. Robust: The problem is that toggle_physics(False) doesn't allow the generated html to initially group the nodes out using a physics based algorithm like force Atlas 2based. So what we really want to do is disable physics right after the G.show_buttons(filter_=['physics'])  and immediately toggling physics off, but a more robust solution would be editing the html itself so that physics is automatically turned off after everything has loaded. This can be done by calling the following function:


# Example usage
nt.write_html('nx.html')
add_physics_stop_to_html("nx.html")


for node in net.get_nodes():
  net.get_node(node)['x']=pos[node][0]
  net.get_node(node)['y']=-pos[node][1] #the minus is needed here to respect networkx y-axis convention 
  net.get_node(node)['physics']=False
  net.get_node(node)['label']=str(node) #set the node label as a string so that it can be displayed

Example 2
net = Network()
net.from_nx(G)

for node in net.get_nodes():
  net.get_node(node)['physics']=False
  net.get_node(node)['label']=str(node)

net.toggle_physics(False)
'''
from pyvis.network import Network
from pyvis import network as net
import networkx as nx
import matplotlib.pyplot as plt
import re
from colors import graphColors

# Needed to show graph.html on jupyter frame
from IPython.display import display

class graphVis(object):
    def __init__(self, **kwargs):
        # Initialize pyvis Graph network

        w = kwargs.get('width',"100%")
        h = kwargs.get('height', "500px")
        pyOptions = kwargs.get('options', {})
        
        #net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        self.pvG = net.Network(height=h, width=w, 
                               notebook=True, 
                               cdn_resources='in_line',
                               **pyOptions)
        self._initNX(**kwargs)
        self.cg = graphColors()

    def _initNX(self, **kwargs):
        graphNum = kwargs.get('graphNum', 10)
        #g = nx.cycle_graph(10)
        #g = nx.complete_graph(5)
        
        g = kwargs.get('nxGraph', 'Graph')
        if g == 'cycle_graph' : self.G = nx.cycle_graph(graphNum)
        elif g == 'complete_graph' : self.G = nx.complete_graph(graphNum)
        else:
            # Empty Graph
            print("Use empty nx.Graph")
            self.G = nx.Graph()

    def draw(self, **kwargs):
        '''
        Default is to use pyvis to draw
        - import network from nx (self.g)
        '''
        # import NX network
        if len(self.G.nodes) > 0 : 
            print("draw: Import NX network")
            self.pvG.from_nx(self.G)
        
        # Get HTML filename
        gFN = self.FN(**kwargs)
        
        # Generate html with jscript interaction
        display(self.pvG.show(gFN))
        
        #display(IFrame(src=gFN, width=w, height=h))
        

    def FN(self, **kwargs):
        return kwargs.get('FN', "data/graphShow.html")

    def nx(self):
        return self.G

    def nxDraw(self, **kwargs):
        w = kwargs.get('width',15)
        h = kwargs.get('height',13)
        plt.figure(3,figsize=(w,h)) 
        nx.draw(self.G, with_labels=True)
        plt.show()

    def addLegend(self, G, cmDict, **kwargs):
        '''
        https://github.com/WestHealth/pyvis/issues/50

        Adds legend nodes (with colors) into G
        '''
        # Add Legend Nodes
        xstep = kwargs.get('xstep',0)
        ystep = kwargs.get('ystep',20)
        x = kwargs.get('x',-300)
        y = kwargs.get('y',-250)
        nList = []
        
        nNum = len(G.nodes)
        for nID,k in enumerate(cmDict.keys()):
            G.add_node(f"Legend_{nNum + nID}",**{
                    'group': nID, 
                    'label': k,
                    'size': 30, 
                    # 'fixed': True, # So that we can move the legend nodes around to arrange them better
                    'physics': False, 
                    'x': f'{x + nID*xstep}px', 
                    'y': f'{y + nID*ystep}px',
                    'shape': 'box', 
                    'widthConstraint': 80, 
                    'font': {'size': 10},
                    'color' : cmDict[k]
                })

    def add_physics_stop_to_html(self, filepath):
        '''
        https://stackoverflow.com/questions/68117561/pyvis-network-keeps-on-moving
        '''
        with open(filepath, 'r', encoding="utf-8") as file:
            content = file.read()
    
        # Search for the stabilizationIterationsDone event and insert the network.setOptions line
        pattern = r'(network.once\("stabilizationIterationsDone", function\(\) {)'
        replacement = r'\1\n\t\t\t\t\t\t  // Disable the physics after stabilization is done.\n\t\t\t\t\t\t  network.setOptions({ physics: false });'
    
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
        # Write the modified content back to the file
        with open(filepath, 'w', encoding="utf-8") as file:
            file.write(new_content)
