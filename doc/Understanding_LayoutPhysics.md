# Understandng Graph Layouts and Physics

References:
1. [Disable Physic Layout](https://stackoverflow.com/questions/74108243/pyvis-is-there-a-way-to-disable-physics-without-losing-graphs-layout
)

## What are `Layout` and `Physics`

The`pyvis` is an interactive graph network service that provides the ability zoom (in/out) and click on nodes.  When I got to 300+ nodes the graph was bouncing constantly and did not settle.  This was 

A network graph is a visual representation of data (nodes) that shows the relationship between two or more nodes.  It is best to think of nodes as `objects` and its data. 

The `physics` of a graph is about algorithms and dynamics of the visual representation.  Like real world physics `graph physic` seeks to reflect best visualization. 



It helps to understand and interpret physical phenomena by showing how quantities like position, velocity, or acceleration change over time. 

## Background on Physics 
(source: mostly from google AI search)

### Visual Representation:
- Graphs use lines, curves, and points to display data, making it easier to see trends and relationships. 
Variables:
- A graph typically shows the relationship between an independent variable (usually plotted on the x-axis) and a dependent variable (plotted on the y-axis). 
Types of Graphs in Physics:
- Position-time graphs: Show how the position of an object changes over time. The slope of the line represents the object's velocity. 
- Velocity-time graphs: Show how the velocity of an object changes over time. The slope of the line represents the object's acceleration. 
- Acceleration-time graphs: Show how the acceleration of an object changes over time. 

### Interpreting Graphs:
- Understanding the shape of the graph, the slope, and the position of the line can provide valuable information about the motion of an object. 

### Applications:
- Graphs are used in various areas of physics, including:
- Kinematics: Studying motion, including speed, velocity, and acceleration. 
- Waves: Analyzing sound waves, light waves, and other types of waves. 
- Electromagnetism: Understanding the behavior of electric and magnetic fields. 
- Thermodynamics: Visualizing the behavior of heat and energy. 

## `pyvis` - Controlling physics of node layout 

https://stackoverflow.com/questions/74108243/pyvis-is-there-a-way-to-disable-physics-without-losing-graphs-layout

1. add_node physics=False
1. add_edge physics=False
3. net.toggle_physics(False)
4. Network(options={"physics": {"enabled": False}})
      https://stackoverflow.com/questions/67548160/pyvis-graph-wont-stop-moving
5. Robust: The problem is that toggle_physics(False) doesn't allow the generated html to initially group the nodes out using a physics based algorithm like force Atlas 2based. So what we really want to do is disable physics right after the G.show_buttons(filter_=['physics'])  and immediately toggling physics off, but a more robust solution would be editing the html itself so that physics is automatically turned off after everything has loaded. This can be done by calling the following function:


#### Example1 
````
nt.write_html('nx.html')
add_physics_stop_to_html("nx.html")


for node in net.get_nodes():
  net.get_node(node)['x']=pos[node][0]
  net.get_node(node)['y']=-pos[node][1] #the minus is needed here to respect networkx y-axis convention 
  net.get_node(node)['physics']=False
  net.get_node(node)['label']=str(node) #set the node label as a string so that it can be displayed
````

#### Example 2
````
net = Network()
net.from_nx(G)

for node in net.get_nodes():
  net.get_node(node)['physics']=False
  net.get_node(node)['label']=str(node)
````

### Example 3
net.toggle_physics(False)

