'''
Core services for managing a pyvis network graph


'''
from pyvis.network import Network
from pyvis import network as net
import networkx as nx
import matplotlib.pyplot as plt
import re
from colors import graphColors

# Needed to show graph.html on jupyter frame
from IPython.display import display

class graphAnchor(object):

    def __init__(self, tlG, **kwargs):
        '''
        Determine anchor points for UL (upper left), LL (lower left)
        UL default is (-2000, -2000
        UL can be overridden x= and y=
        '''
        
        # Add Legend Nodes
        self.xstep = kwargs.get('xstep',0)
        self.ystep = kwargs.get('ystep',100)

        w = tlG._n2int(tlG.w, 400)
        h = tlG._n2int(tlG.h, 500)


        xOrig = kwargs.get('x',-2000)
        yOrig = kwargs.get('y',-2000) 
        
        x = tlG._n2int(xOrig, w)
        y = tlG._n2int(yOrig, h)

        self.xUL = x
        self.yUL = y

        self.xLL = x
        self.yLL = 0
        print("Legend x,y", (w, h), (tlG.w, tlG.h), (xOrig, yOrig), f"UL({self.xUL}, {self.yUL})", f"LL({self.xLL}, {self.yLL})")


class graphVis(object):
    def __init__(self, **kwargs):
        # Initialize pyvis Graph network
        self._initNX(**kwargs)        
        self.cg = graphColors()
        self.w = kwargs.get('width',"100%")
        self.h = kwargs.get('height', "500px")
        self.a = graphAnchor(self, **kwargs)
        

    def _initVIS(self, **kwargs):

        visOptions = kwargs.get('visOptDict', {})
        
        #net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        self.pvG = net.Network(height=self.h, width=self.w, 
                               notebook=True, 
                               cdn_resources='in_line',
                               **visOptions)

    def _initNX(self, **kwargs):
        graphNum = kwargs.get('graphNum', 0)
        #g = nx.cycle_graph(10)
        #g = nx.complete_graph(5)

        # Select nx graph layout
        g = kwargs.get('nxG', None)
        
        if g == 'cycle_graph' : self.G = nx.cycle_graph(graphNum)
        elif g == 'complete_graph' : self.G = nx.complete_graph(graphNum)
        elif g == 'default' : 
            # Empty Graph
            print("Use empty nx.Graph")
            self.G = nx.Graph()
        else:
            self.G = None
            
            

    def draw_fromVIS(self, **kwargs):
        '''
        This was the initial draw function (w/in juypter) using pvvis network. 
        '''
        # Get HTML filename
        gFN = self.FN(**kwargs)
        
        # Generate html with jscript interaction
        display(self.pvG.show(gFN))
        
        #display(IFrame(src=gFN, width=w, height=h))

    def draw_fromNX(self, **kwargs):
        '''
        Default is to use pyvis to draw
        - import network from nx (self.g)

        REF: https://stackoverflow.com/questions/77754435/pyvis-and-networkx-how-to-make-nodes-different-color-based-on-source-or-target
        '''
        # Get HTML filename
        gFN = self.FN(**kwargs)

        # NOTE: assumes nx network
        cList = [n['color'] for nm,n in self.gObj().nodes(data=True)]

        #nx.draw(self.G, node_color=cList, with_labels=True)

        #net = Network(notebook=True, filter_menu=True, cdn_resources='remote')
        self._initVIS(**kwargs)
        
        # import NX network
        print("draw: Import NX network")
        self.pvG.from_nx(self.G)
        
        # Generate html with jscript interaction
        display(self.pvG.show(gFN))
        
        #display(IFrame(src=gFN, width=w, height=h))

    def draw(self, **kwargs):
        if self.G : 
            self.draw_fromNX(**kwargs)
            return
        self.draw_fromVIS(**kwargs)

    def gObj(self):
        if self.G is not None : return self.G
        if self.pvG is not None : return self.pvG
        return None

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

    def _n2int(self, n, dim):
        '''
        Convert numeric arg into int

        100    -> 100
        "80%"  -> w *80/100
        "100px" -> 100
        '''
        
        try:
            return int(n)
        except:
            pass
        if type(n) != str : 
            print("ERROR: bad number formation:", n)
            return None
        if n.strip()[0] == '-' : 
            n = int(n)
        elif '%' in n : 
            n = int(n.replace('%',''))/100 * int(dim)
            return n
        elif 'px' in n:
            n = int(n.replace('px',''))
            return n
        else:
            print("ERROR: unknown dimention format:", n)
            return None

    def addLegend(self, G, cmDict, **kwargs):
        '''
        https://github.com/WestHealth/pyvis/issues/50

        Adds legend nodes (with colors) into G
        
        '''
        # get anchor points for UL and LL, also xstep, ystep
        a = self.a
        
        nList = []
        nNum = len(G.nodes)
        for nID,k in enumerate(cmDict.keys()):
            G.add_node(f"Legend_{nNum + nID}",**{
                    'group': nID, 
                    'label': k,
                    'size': 30, 
                    # 'fixed': True, # So that we can move the legend nodes around to arrange them better
                    'physics': False, 
                    'x': f'{a.xUL + nID*a.xstep}px', 
                    'y': f'{a.yUL + nID*a.ystep}px',
                    'shape': 'box', 
                    'widthConstraint': 00, 
                    'font': {'size': 80},
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
