import numpy as np
import matplotlib.pyplot as plt

def plot(x2, y2, df, phis2, distance):
    def update_annot(ind):
        """
        Update the annotation based on the index
        """
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = f'{ind["ind"][0]+1}'
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.7)

    def hover(event):
        """
        Show annotation on hover
        """
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    # Make figure and set background color
    fig, ax = plt.subplots()
    ax.set_facecolor('#8FCF4C')
    # Plot grass
    ax.plot(x2, y2, color='darkgreen', linewidth=10, solid_capstyle='round')
    # Create lists to store text locations
    text_x = []
    text_y = []
    # Plot kerbs and gravel + add corner labels
    for i in df:
        corners = (x2[np.where(abs(phis2-i) < 0.1)], y2[np.where(abs(phis2-i) < 0.1)])
        ax.plot(corners[0], corners[1], color='grey', linewidth=10, solid_capstyle='round')
        ax.plot(corners[0], corners[1], color='white', linewidth=5.5, solid_capstyle='round')
        ax.plot(corners[0], corners[1], 'r:', linewidth=5.5)
        # Add corner numbers
        if len(corners[0]) > 0:
            xtext1, ytext1 = corners[0][int(len(corners[0])/2)], corners[1][int(len(corners[1])/2)]
            text_x.append(xtext1)
            text_y.append(ytext1)
    # For showing corner labels when hovering over them
    sc = ax.scatter(text_x, text_y, s=800, alpha=0.0)
    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="circle", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)
    fig.canvas.mpl_connect("motion_notify_event", hover)
    # Show track statistic box
    props = dict(boxstyle='round', facecolor='white', alpha=0.6)
    textstr = f' Track length: {round(distance,2)} \n Corners: {len(text_x)}'
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
    # Plot full track in black
    plt.plot(x2, y2, color='black', linewidth=4)
    plt.axis('equal')
    plt.show()

def plot_plain(x2, y2, df, phis2, distance):
    # -------------------------------------------------------------------
    # Fancy plot
    plt.figure()
    # Background color
    plt.rcParams['axes.facecolor'] = '#8FCF4C'
    # Kerbs, grass and gravel
    plt.plot(x2, y2, color='darkgreen', linewidth=10)
    for j, i in enumerate(df):
        corners = (x2[np.where(abs(phis2-i) < 0.1)], y2[np.where(abs(phis2-i) < 0.1)])
        plt.plot(corners[0], corners[1], color='grey', linewidth=10)
        plt.plot(corners[0], corners[1], color='white', linewidth=5.5)
        plt.plot(corners[0], corners[1], 'r:', linewidth=5.5)
    # Full track
    plt.plot(x2, y2, color='black', linewidth=4, label=f'length = {round(distance, 2)}')
    plt.axis('equal')
    plt.legend()
    plt.show()