# questo file permette di selezionare una determinata area di una foto presente nella cartella delle immagini del
# dataset, in modo da poter salvare annotazioni relativamente a questa

import os
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
from generate_xml import write_xml

# costanti globali
img = None
tl_list = [] # lista top-left
br_list = [] # lista bottom-right
object_list = []

# costanti
image_folder = 'train_images' # cartella dove sono presenti le immagini del dataset
savedir = 'annotations' #cartella dove sono presenti le annotazioni relative alle immagini del dataset
obj1 = 'red_card'
obj2 = 'yellow_card'

# la funzione permette di selezionare una determinata area di una foto presente nella cartella train_images, in modo
# da poter salvare nelle annotazioni il contenuto della foto stessa in quella particolare posizione
def line_select_callback(clk, rls):
    global tl_list
    global br_list
    global object_list
    tl_list.append((int(clk.xdata), int(clk.ydata)))
    br_list.append((int(rls.xdata), int(rls.ydata)))


# settaggio listener
def onkeypress(event):
    global object_list
    global tl_list
    global br_list
    global img

    # se premo y setto l'oggetto cartellino giallo, se premo r setto l'oggetto cartellino rosso, se premo q chiudo la
    # foto, salvo le annotazioni e vado avanti
    if event.key == 'y':
        object_list.append(obj2)
    elif event.key == 'r':
        object_list.append(obj1)
    elif event.key == 'q':
        print(object_list)
        write_xml(image_folder, img, object_list, tl_list, br_list, savedir)
        tl_list = []
        br_list = []
        object_list = []
        img = None
        plt.close(event.canvas.figure)


def toggle_selector(event):
    toggle_selector.RS.set_active(True)

if __name__ == '__main__':
    # nella cartella delle immagini, le scorro una per una...
    for n, image_file in enumerate(os.scandir(image_folder)):
        # dopo che ho superato l'ultima precedentemente inserita (nel nostro caso la numero 354), permetto all'utente
        # di effettuare la selezione
        if n > 354:
            print(str(n - 353)+" - "+str(n))
            img = image_file
            fig, ax = plt.subplots(1, figsize=(10.5, 8))
            mngr = plt.get_current_fig_manager()
            mngr.window.setGeometry(400, 400, 2048, 1536)
            image = cv2.imread(image_file.path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            ax.imshow(image)

            toggle_selector.RS = RectangleSelector(
                ax, line_select_callback,
                drawtype='box', useblit=True,
                button=[1], minspanx=5, minspany=5,
                spancoords='pixels', interactive=True,
            )
            bbox = plt.connect('key_press_event', toggle_selector)
            key = plt.connect('key_press_event', onkeypress)
            plt.tight_layout()
            plt.show()
            #plt.close(fig)
