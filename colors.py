'''
Color services for pyvis - main goal is to color event nodes based on event Prefix
https://matplotlib.org/stable/users/explain/colors/colormaps.html

'''
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib import colormaps
import numpy as np

# Examples
cList = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                      'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                      'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

cmaps = {}

gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

class graphColors(object):
    def __init__(self, **kwargs):
        pass

    def list(self):
        return list(colormaps)
        #plot_color_gradients('Sequential', cList

    def list2cmDict(self, cmName, kList):
        '''
        convert list of keywords to dict  cm[kw] = '#3b528b'

        returns cmDict
        '''
        # Get a colormap
        #cmap = plt.cm.get_cmap('viridis')
        cmap = colormaps[cmName]
        
        # Sample colors from the colormap
        num_colors = len(kList)
        colors = cmap(np.linspace(0, 1, num_colors))
        
        # Convert to hex
        return {kw:v for kw,v in zip(kList, [matplotlib.colors.to_hex(color) for color in colors])}


    def plot_color_gradients(self, category, cmap_list):
        # Create figure and adjust figure height to number of colormaps
        nrows = len(cmap_list)
        figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22
        fig, axs = plt.subplots(nrows=nrows + 1, figsize=(6.4, figh))
        fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh,
                            left=0.2, right=0.99)
        axs[0].set_title(f'{category} colormaps', fontsize=14)
    
        for ax, name in zip(axs, cmap_list):
            ax.imshow(gradient, aspect='auto', cmap=colormaps[name])
            ax.text(-0.01, 0.5, name, va='center', ha='right', fontsize=10,
                    transform=ax.transAxes)
    
        # Turn off *all* ticks & spines, not just the ones with colormaps.
        for ax in axs:
            ax.set_axis_off()
    
        # Save colormap list for later.
        cmaps[category] = cmap_list

    def displayMaps(self, cmList=None):
        if cmList is None:
            cmList = self.list()
        c.plot_color_gradients('Perceptually Uniform Sequential', cmList)
