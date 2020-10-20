import os
import random
import Tkinter as tk, ttk
from PIL import Image, ImageTk
from playsound import playsound

WINDOW_TITLE = "My Closet"
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 220
IMG_WIDTH = 250
IMG_HEIGHT = 250
SOUND_EFFECT_FILE_PATH = 'assets/yes-2.wav'

# store all the tops into a file
ALL_TOPS = [str("Tops/") + file for file in os.listdir("Tops/") if not file.startswith('.')]
ALL_BOTTOMS = [str("Bottoms/") + file for file in os.listdir("Bottoms/") if not file.startswith('.')]
# store all bottoms in a file

class closet:
    def __init__(self,root):
        self.root = root

        # show tops
        self.top_images = ALL_TOPS
        #show bottoms
        self.bottom_images = ALL_BOTTOMS

        # create and add first top img onto Frame
        self.top_image_path = self.top_images[0]
        self.tops_frame = tk.Frame(self.root)
        self.top_image_label = self.create_photo(self.top_image_path, self.tops_frame)
        # create and add first bottom img onto Frame
        self.bottom_image_path = self.bottom_images[0]
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_image_label = self.create_photo(self.bottom_image_path, self.bottom_frame)

        # add top to  pack
        self.top_image_label.pack(side=tk.TOP)
        # add bottom to  pack
        self.bottom_image_label.pack(side=tk.TOP)

        self.create_background()

    def create_background(self):
        self.root.title(WINDOW_TITLE)
        self.root.geometry('{0}x{1}'.format(WINDOW_WIDTH, WINDOW_HEIGHT))

        # add buttons
        self.create_buttons()
        # add clothes
        self.tops_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.bottom_frame.pack(fill=tk.BOTH, expand=tk.YES)

    def create_buttons(self):
        create_outfit_button = ttk.Button(self.tops_frame, text="Create Outfit", command=self.create_outfit)
        create_outfit_button.pack(side=tk.LEFT)

        top_prev_but = ttk.Button(self.tops_frame, text="Prev", command=self.get_prev_top)
        top_prev_but.pack(side=tk.LEFT)

        top_next_but = ttk.Button(self.tops_frame, text="Next", command=self.get_next_top)
        top_next_but.pack(side=tk.RIGHT)

        # now for bottoms
        bottom_prev_but = ttk.Button(self.bottom_frame, text="Prev", command=self.get_prev_bottom)
        bottom_prev_but.pack(side=tk.LEFT)

        bottom_next_but = ttk.Button(self.bottom_frame, text="Next", command=self.get_next_bottom)
        bottom_next_but.pack(side=tk.RIGHT)

    def create_photo(self, image, frame):
        image_file = Image.open(image)
        image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
        tk_photo = ImageTk.PhotoImage(image_resized)
        image_label = tk.Label(frame, image=tk_photo, anchor=tk.CENTER)
        image_label.image = tk_photo

        return image_label

    def update_image(self, new_image_path, image_label):
        image_file = Image.open(new_image_path)
        image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
        tk_photo = ImageTk.PhotoImage(image_resized)

        # update based on img label
        image_label.configure(image=tk_photo)
        image_label.image = tk_photo

    # general function to move prev and next
    def _get_next_item(self, current_item, category, increment=True):
        item_index = category.index(current_item)
        final_index = len(category) - 1
        next_index = 0

        #edge cases !!
        if increment and item_index == final_index:
            # go back to beginning
            next_index = 0
        elif not increment and item_index==0:
            next_index = final_index
        else:
            increment = 1 if increment else -1
            next_index = item_index+increment

        next_image = category[next_index]

        # reset and update img based on next_img_path
        if current_item in self.top_images:
            image_label = self.top_image_label
            self.tops_image_path = next_image
        else:
            image_label = self.bottom_image_label
            self.bottom_image_path = next_image

        self.update_image(next_image, image_label)

    def get_next_top(self):
        self._get_next_item(self.top_image_path, self.top_images)

    def get_prev_top(self):
        self._get_next_item(self.top_image_path, self.top_images, increment=False)

    def get_next_bottom(self):
        self._get_next_item(self.bottom_image_path, self.bottom_images)

    def get_prev_bottom(self):
        self._get_next_item(self.bottom_image_path, self.bottom_images, increment=False)

    def create_outfit(self):
        # randomly select an outfit
        new_top_index = random.randint(0, len(self.top_images) - 1)
        new_bottom_index = random.randint(0, len(self.bottom_images) - 1)

        # add the clothes onto the screen
        self.update_image(self.top_images[new_top_index], self.top_image_label)
        self.update_image(self.bottom_images[new_bottom_index], self.bottom_image_label)

        playsound(SOUND_EFFECT_FILE_PATH)


root = tk.Tk()
main = closet(root)
root.mainloop()