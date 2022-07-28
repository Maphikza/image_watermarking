"""
I did not have a very organised approach to this build, and I now know that it was the biggest source of my struggle.
In my next build I will plan better, If I were to do this again, I would have started with planning out the
functionality and the widgets I needed to pin down the functionality. From there, I would work on making it look pretty.

The difficulty with this project was caused by the fact that I was inefficient with my planning. I am not able to spend
more time on it for now. But, if I had more time; I would work on refactoring my code to simplify it. I would also
change the theme and fine-tune the user interface.
"""

from PIL import Image, ImageTk, ImageFont, ImageDraw
from tkinter import ttk, Tk, filedialog


# This class handles the uploading, watermarking and saving of the image once it has been watermarked.
class ImageProcessor:
    def __init__(self):
        self.filename = None
        self.watermark = None
        self.img = None
        self.files = [('png Files', '*.png*')]

    # This section deals with the uploading of the image and resizing it.
    def browse_files(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select Image",
                                                   filetypes=[("Image Files", "*.jpg*"), ("Image Files", "*.png*")])

        with Image.open(self.filename) as first_img:  # Uploads the image using the path from filedialog above.
            first_img = first_img.resize((400, 400))
        self.img = ImageTk.PhotoImage(first_img)
        image_display_label.config(image=self.img)  # Displaying the image
        image_display_label.grid(column=0, row=1)
        save_image_button.grid(column=0, row=0, sticky="N E", padx="5", pady="5")

    def add_watermark_txt(self):
        self.watermark = watermark_writing_entry.get()
        with Image.open(self.filename).convert("RGBA") as base:
            # make a blank image for the text, initialized to transparent text color
            txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

            # get a font
            fnt = ImageFont.truetype("OpenSans-Italic-VariableFont_wdth,wght.ttf", 200)
            # get a drawing context
            d = ImageDraw.Draw(txt)

            # draw text, full opacity
            d.text((txt.size[0] - 100, txt.size[1] - 100), self.watermark, font=fnt, fill=(255, 255, 255, 255),
                   anchor="rs")

            out = Image.alpha_composite(base, txt)
            out = out.resize((400, 400))
            out.save("watermark_img.png")
            final_img = ImageTk.PhotoImage(image=out)
            image_display_label.config(image=final_img)
            image_display_label.grid(column=0, row=1)
            save_image_button.config(command=self.save)

    # Saves the image in png format
    def save(self):
        file = filedialog.asksaveasfile(filetypes=self.files, defaultextension=".png", mode="wb")
        img_to_save = open("watermark_img.png", "rb").read()
        file.write(img_to_save)
        file.close()


process = ImageProcessor()  # Initializing my ImageProcessor class.

root = Tk()
root.title("Homemade Image Watermarker!")
root.minsize(500, 250)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

frame = ttk.Frame(root, padding="3 3 12 12")
frame.grid(column=0, row=0, sticky="N W E S")

exit_button = ttk.Button(root, text="Close App", padding="2", command=exit)
exit_button.grid(column=0, row=0, sticky="N W", padx="5", pady="5")

add_image_button = ttk.Button(root, text="Upload Image", padding=2, command=process.browse_files)
add_image_button.grid(column=0, row=0, padx="5", pady="5", sticky="N", columnspan=2)

save_image_button = ttk.Button(root, text="Save Image")

# Used a Label to display image. Canvas could have also worked.
image_display_label = ttk.Label(root, padding="5 0 0 5")
image_display_label.grid(column=0, row=1)

# label for watermark entry, watermark entry and button for adding watermark.
watermark_entry_label = ttk.Label(root, text="Watermark Text:")
watermark_entry_label.grid(column=0, row=2, sticky="W", padx="20")
watermark_writing_entry = ttk.Entry(root, width=30)
watermark_writing_entry.grid(column=0, row=2, columnspan=2)
add_watermark_button = ttk.Button(root, text="Add It", padding="2 0 0 2", command=process.add_watermark_txt)
add_watermark_button.grid(column=0, row=2, padx=20, pady=5, sticky="E")

root.mainloop()
