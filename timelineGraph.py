'''
'''
from graph import graphVis
from timeline import events
from colors import graphColors
import re

class timelineGraph(graphVis):
    
    def __init__(self, **kwargs):
        ''' 
        Graph services for timelines

        timelineGraph(timeliine = events(FN="path")[, prefix='Church'])

        Initialise
        self.evDict : all events in timelne
        self.t2Dict : tier2 nodes,  Events linked to all t2
        self.tl - empty timeline to use services
        '''
        super().__init__(**kwargs)

        # Default Prefix
        self.prefix = kwargs.get('prefix', 'Church')
        
        #timeline obj is required
        tl = kwargs['timeline']

        # graph object acts like a timeline object but focuses on graphing
        # Every event has a unique ID (enumerated by the set of evDict)
        self.evDict = {}
        prfxList = []
        for evID, (kw,desc) in enumerate(tl.evDict.items()):
            prfx = self._kw2prfx(kw)
            prfxList.append(prfx)
            
            self.evDict[(evID, tl.evDt(kw))] = (kw,desc) 

        # Timeline services
        self.tl = events(FN=None)
        self._initMillenium()
        self._initPrefix()
        self.cmDict = self.cg.list2cmDict('rainbow', self.prfxDict.keys())


        # Create tier2 nodes : prefix dict with unique ID for each prefix
        # FIXME: Smarter - allow tier2 prefix to be Prefix or custom
        d = {t2:(n,{}) for n,t2 in enumerate(set(self.milDict.keys()))}
        self.t2Dict = self.sortT2Dict(d)
        
        #self.importGraph()

    def _initPrefix(self):
        cr = graphColors()

        # find all prefixes in the evDict
        prfxSet = set([self._kw2prfx(kw) for kw,desc in self.values()])

        
        self.prfxDict = {p:n for n,p in enumerate(prfxSet)}
        return
        
    def _initMillenium(self):
        '''
        Return millenium dict of node names
            - each millenium node ('Mil(#0000)') containing it's own timeline evDict

        self.milDict[yr2Mil] = {}
        '''
        
        # Build prefix list
        try:
            yList = [yr for n,yr in self.evDict.keys()]
            mnYr = min(yList)
            mxYr = max(yList)
        except:
            self.milDict = {}
            return
        
        # Milleniums
        mnMil = 1000*(int(mnYr/1000)-1)
        mxMil = 1000*(int(mxYr/1000)+1)
        #print("Debug 74 milDict start", mnMil, mxMil)
        #print("debug 74", [m for m in range(mnMil, mxMil, 1000)])

        # Initialize Empty Millenium Dict
        mDict = {}
        for m in range(mnMil, mxMil, 1000):
            kw = self._yr2Mil(str(m))
            mDict[kw] = {} 
        self.milDict = mDict
        #print("Debug 80 milDict from:to", mnMil, mxMil)
        #print("Debug 80 milDict end", mDict)

        return

    def _nodeNm(self, evID, yr): return f"{evID}_{yr}"
    def _nodeLabel(self, evID, yr): return f"{yr}"

    # Manage Prefix
    def _kw2prfx(self, kw):
        '''
        Extract "prefix:" from event keyword (abstract line)
        Return 1st prefix (' xxx:  ') in keyword (event abstract line)
        '''
        p = r' (\w+:) '
        mList = re.split(p, kw)
        if mList is None : 
            # default prefix
            return self.prefix
        for m in mList:
            w = m.strip()
            if w[-1] == ':':
                return w[0:-1]

    def _kw2Mil(self,kw):
        return self._yr2Mil(self.tl.evDt(kw))

    def _yr2Mil(self,yr):
        yr = int(yr)
        #if yr < 0 : 
        return f"Mil({1000*int((yr/1000))})" 
        #return f"Mil({1000*int((yr/1000)-1)})" 
        #return f"Mil({1000*int((yr/1000))})"

            
    def _tier2ID(self, kw): 
        # FIXME : make smarter to allow Prefix: and custom tier2
        yr = self.tl.evDt(kw)
        return self._yr2Mil(yr)

    def sortT2Dict(self, t2Dict):
        p = r'^Mil\((.*)\)$'
        d = {}
        for k in t2Dict.keys():
            d[k] = int([m for m in re.split(p, k)][1])
        d = dict(sorted(d.items(), key=lambda item: item[1]))
        return {k:t2Dict[k] for k in d.keys()}


    def _prfx2Size(self, n, prfx, **kwargs):
        # FIXME: determine size based on Tier2 timeline
        # node size is dependent on net.barnes_hut settings.  
        scale = 5
        d = {'Period': 12,
             'Church': 8, 'Judeo': 8, 'Muslim': 8,
             'Roman': 5, 'Greek': 5, 
             'Evolution': 3, 
              }
        if 'Mil' in n : sz = 15
        elif n == 'Events' : sz = 20
        elif prfx in d.keys(): sz = d[prfx]
        else: sz = 3
        #print("147 size", sz, n, prfx)
        return sz * scale
        
    def _importGraphTop(self, **kwargs):
        '''
        Add nodes and top 2 tier edges: 

        Events :  top of network
        tier2 : can be Milleniums or PrefixSet or customClassification

        Add tier2 nodes into prfxDict 
        '''
        G = self.gObj()
        nStart = 'Events'
        
        ## FIXME: delete -- nPrev = prefix if prefix is not None else 'Events'
        G.add_node(nStart, 
                   size=self._prfx2Size(nStart,nStart), 
                   title=f"Start of Timeline",
                   label='Start',
                   prefix='tier1',
                   color=self.cmDict['tier1'],
                   value = 1000)
        
        nPrev = nStart
        for n in self.t2Dict.keys():
            G.add_node(n, size=self._prfx2Size(n, n), 
                       title=f"Events_{n}",
                       label=f"Events_{n}",
                       prefix='tier2',
                       color = self.cmDict['tier2'],
                       value=1001)
            G.add_edge(nPrev,n)
            self.prfxDict[n] = 100
            
            nPrev = n

        self.prfxDict[nStart] = 1000
        
        
        
    def importGraph(self, **kwargs):

        gc = graphColors()
        cmDict = self.cmDict
        
            
        G = self.gObj()
        # FIXME: legend nodes to not display
        self.addLegend(G, cmDict)
        self._importGraphTop()
        
        #G.add_nodes(['Events'], size=[2, 4, 6], title=["n1", "n2", "n3"])

        # Intiale previous state per tier2 timeline; track the last node added to build sequential timeline
        prevDict = {k:k for k in self.t2Dict.keys()}
        
        for (evID,yr),(kw,desc) in self.evDict.items():
            # determine prefix of event
            nT2 = self._tier2ID(kw)
            prfx = self._kw2prfx(kw)

            # Associate with top graph tree - usually millenium
            kwT2 = self._kw2Mil(kw)  # form "Mil(YYYY)"
            nID, t2Dict = self.t2Dict[kwT2]
            if False:
                try: 
                    (evID_p, yr_p),(kw,desc) = list(t2Dict.items())[-1]
                    nPrev = self._tier2ID(kw)
                except:
                    # Link to Head of Millenium
                    nPrev = self._tier2ID(kw)

            nPrev = prevDict[kwT2]
            
            # Fill in tier2 timeline
            #     event node info into tier 2 timeline
            t2Dict[(evID,yr)] = (kw,desc)

            #---- Now Graph
            # Node name
            n = self._nodeNm(evID,yr)
            if type(n) != str :
                print("Warning non str nodeNm", type(n), n, evID, yr, kw)
                n = str(n)

            #print("161 - Add node/edge", f"{nPrev} : {n}")

            
            G.add_node(n, 
                       size=self._prfx2Size(n, prfx),      # size of node
                       title=str(f"{kw}\n{desc}"),   # display on hover 
                       label=yr,                     # text to display
                       prefix=prfx,
                       color=self.cmDict[prfx],      # node color, based on prefix
                       value=evID,                   # enumerate)
            )
            G.add_edge(nPrev,n)
            prevDict[kwT2] = n

        # Link edge from last event per Mil back to start
        # FIXME: error on draw, linking back to T2 violates directed graPH, NEED 
        for t2, (t2ID,evDict) in self.t2Dict.items():
            n = len(evDict)
            if n != 0 : 
                (evID, yr) = list(evDict.keys())[-1]
                nm = f"{evID}-{yr}"
                #G.add_edge(nm, t2)
                


    


    def keys(self): return self.evDict.keys()
    def items(self): return self.evDict.items()
    def values(self): return self.evDict.values()   
    
    def iterEvents(self):
        self._keys = list(self.evDict.keys())  # Store keys to iterate
        self._index = 0
        return self

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._keys):
            key = self._keys[self._index]
            self._index += 1
            return key, self.evDict[key] # Return key-value pair
        else:
            raise StopIteration

    def _reprNodes(self):
        tx = ''
        G = self.gObj()
        if G is not None:
            tx += f"\n--- Nodes({len(G.nodes)})/Edges({len(G.edges)})\n"
            for nm,n in self.G.nodes(data=True):
                tx += f"===> {nm}, {n}\n"
        return tx
        

    def __repr__(self):

        tx = "timelineGraph Object\n"

        try:
            tx += "\n--- evDict"
            tx += f"events: {len(self.evDict)}\n"
        except: pass
            
        try:
            tx += "\n--- prfxDict"
            tx += f"{self.prfxDict}\n"
        except: pass
        
        try:
            tx += "\n--- t2Dict\n"
            d = {nm:len(l) for nm,l in self.t2Dict.items()}
            tx += f"{d}\n"
        except: pass
            
        try:
            tx += "\n--- cmDict\n"
            tx += f"{self.cmDict}\n"
        except: pass
            
        G = self.gObj()
        if G is not None:
            tx += f"\n--- Graph: Nodes({len(G.nodes)})/Edges({len(G.edges)})\n"

        return tx
