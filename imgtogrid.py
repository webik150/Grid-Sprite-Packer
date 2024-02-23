import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter


class ImageResizerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Resizer")

        self.images = []
        self.selected_dimension = tk.StringVar()
        self.selected_dimension.set("128")  # Default dimension

        self.max_images_per_row = tk.IntVar()
        self.max_images_per_row.set(4)  # Default value

        self.padding_between_images = tk.IntVar()
        self.padding_between_images.set(0)  # Default value

        # UI elements
        self.select_images_button = tk.Button(self, text="Select Images", command=self.select_images)
        self.select_images_button.pack(pady=10)

        self.dimension_label = tk.Label(self, text="Select Dimension:")
        self.dimension_label.pack()

        self.dimension_options = tk.OptionMenu(self, self.selected_dimension, "128", "256", "512")
        self.dimension_options.pack()

        self.row_slider_label = tk.Label(self, text="Max Images per Row:")
        self.row_slider_label.pack()

        self.row_slider = tk.Scale(self, from_=1, to=20, orient=tk.HORIZONTAL, variable=self.max_images_per_row)
        self.row_slider.pack()

        self.padding_label = tk.Label(self, text="Padding between Images:")
        self.padding_label.pack()

        self.padding_slider = tk.Scale(self, from_=0, to=20, orient=tk.HORIZONTAL, variable=self.padding_between_images)
        self.padding_slider.pack()

        self.resize_button = tk.Button(self, text="Resize and Compose", command=self.resize_and_compose)
        self.resize_button.pack(pady=10)

        self.save_button = tk.Button(self, text="Save Composed Image", command=self.save_composed_image)
        self.save_button.pack(pady=10)

    def select_images(self):
        file_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("PNG Files", "*.png")])
        for file_path in file_paths:
            self.images.append(file_path)

    def resize_and_compose(self):
        if not self.images:
            return

        dimension = int(self.selected_dimension.get())
        max_images_per_row = self.max_images_per_row.get()
        padding = self.padding_between_images.get()

        resized_images = []
        max_width, max_height = dimension, dimension

        for image_path in self.images:
            image = Image.open(image_path)
            image.thumbnail((max_width, max_height), Image.LANCZOS)
            resized_images.append(image)

        # Calculate composed image dimensions
        composed_width = max_width * min(max_images_per_row, len(resized_images)) + padding * (min(max_images_per_row, len(resized_images)) - 1)
        num_rows = (len(resized_images) - 1) // max_images_per_row + 1
        composed_height = max_height * num_rows + padding * (num_rows - 1)

        # Create a new blank image with transparency
        composed_image = Image.new("RGBA", (composed_width, composed_height), (0, 0, 0, 0))

        # Paste resized images into the composed image with padding
        x_offset, y_offset = 0, 0
        for image in resized_images:
            composed_image.paste(image, (x_offset, y_offset))
            x_offset += max_width + padding  # Move x_offset and add horizontal padding
            if x_offset >= max_width * max_images_per_row + padding * (max_images_per_row - 1):
                x_offset = 0
                y_offset += max_height + padding  # Move y_offset and add vertical padding

        # Display composed image
        self.composed_image = composed_image
        self.composed_image.thumbnail((500, 500), Image.LANCZOS)
        self.rendered_composed_image = ImageTk.PhotoImage(self.composed_image)
        if hasattr(self, 'composed_image_label'):
            self.composed_image_label.destroy()
        self.composed_image_label = tk.Label(self, image=self.rendered_composed_image)
        self.composed_image_label.pack()

    def save_composed_image(self):
        if not hasattr(self, 'composed_image'):
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.composed_image.save(file_path)


if __name__ == "__main__":
    app = ImageResizerApp()
    app.mainloop()