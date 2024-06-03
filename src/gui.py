import tkinter as tk
from tkinter import filedialog, font
from PIL import Image, ImageTk

from converter import convert, upscale, clean


class GUI(tk.Tk):
    def __init__(self, tmp_path: str = "../tmp"):
        super().__init__()
        self.title("Ganics || Home")
        self.geometry("640x480")
        self.resizable(False, False)
        self.file_path, self.final_file_path, self.option_var = "None", "None", "None"
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family='Helvetica')
        self.configure(bg="#3b3b3b")
        self.selected_image = None
        self.tmp = tmp_path  # path for temporary files

        # Defined recommendations for each style (based on my tests)
        self.recommendations = {
            "Vincent Van Gogh Art": "Use images with vibrant colours for best results",
            "Cartoon": "Use simple images with clear outlines for best results"
        }

        # Frame for buttons
        self.button_frame = tk.Frame(self, bg="#3b3b3b")
        self.button_frame.pack(pady=(15, 0))

        # Button that opens a file
        self.select_button = tk.Button(self.button_frame, text="Select PNG File", command=self.select_png_file,
                                       bg="lightblue")
        self.select_button.pack(side="left", padx=(0, 15))

        # Button that starts the style conversion
        self.convert_button = tk.Button(self.button_frame, text="Convert!", command=self.convert, bg="lightblue")
        self.convert_button.pack(side="left", padx=(15, 0))

        # Label for image state
        self.image_label = tk.Label(self, text="Selected image: None", bg="#3b3b3b", fg="white")
        self.image_label.pack(pady=(15, 0))

        # Label for style state
        self.style_label = tk.Label(self, text="Selected style: None", bg="#3b3b3b", fg="white")
        self.style_label.pack()

        # Label for bonus information
        self.info_layer = tk.Label(self, text="Recommendation: Select the style first!", bg="#3b3b3b", fg="white")
        self.info_layer.pack()

        # List of styles
        self.option_var = tk.StringVar()
        self.option_var.set("None")
        self.option1 = tk.Radiobutton(self, text="Vincent Van Gogh Art", variable=self.option_var,
                                      value="Vincent Van Gogh Art", command=self.update_style, bg="#3b3b3b",
                                      fg="white", activebackground="#3b3b3b", activeforeground="white",
                                      selectcolor="#3b3b3b", highlightbackground="#3b3b3b", highlightcolor="white",
                                      highlightthickness=2)
        self.option1.pack(pady=(15, 0))
        self.option2 = tk.Radiobutton(self, text="Cartoon", variable=self.option_var,
                                      value="Cartoon", command=self.update_style, bg="#3b3b3b", fg="white",
                                      activebackground="#3b3b3b", activeforeground="white",
                                      selectcolor="#3b3b3b", highlightbackground="#3b3b3b", highlightcolor="white",
                                      highlightthickness=2)
        self.option2.pack()

        # Canvas for image preview
        self.canvas = tk.Canvas(self, width=600, height=256, bg="#3b3b3b", highlightbackground="#3b3b3b")
        self.canvas.pack(pady=(20, 0))

    def convert(self):
        if self.file_path == "None":  # image not selected
            self.image_label.config(text="Select the image first!")
            return

        if self.option_var.get() == "None":  # style not selected
            self.style_label.config(text="Select the style first!")
            return

        self.style_label.config(text="Changing the style!")  # style conversion
        try:
            convert(self.file_path, self.option_var.get())
        except FileNotFoundError:
            self.image_label.config(text="Style model initialization failed!")
            self.style_label.config(text="Missing style '.weights.h5' file!")
            return

        self.final_file_path = f"""{self.file_path[0:-4]}_{
        "van_gogh" if self.option_var.get() == "Vincent Van Gogh Art" else "cartoon"}.png"""  # upscaling
        self.style_label.config(text="Upscaling the image!")
        try:
            upscale(self.final_file_path, original_img_path=self.file_path)
        except FileNotFoundError:
            self.image_label.config(text="Upscaling model initialization failed!")
            self.style_label.config(text="Missing PatchGAN '.weights.h5' file!")
            return

        self.image_label.config(text="Style conversion successful!")
        self.style_label.config(text=f"""Result saved at: {self.final_file_path}.png""")
        self.show_image_preview(self.tmp + "/conversion.png", resize_to_square=False)
        self.after(10000, self.quit)  # closes the program after 10 seconds
        clean()  # clears temporary files

    def select_png_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if self.file_path:
            self.image_label.config(text="Selected image: " + self.file_path)
            self.show_image_preview(self.file_path)

    def update_style(self):
        selected_option = self.option_var.get()
        self.style_label.config(text="Selected style: " + selected_option)
        self.info_layer.config(text=f"Recommendation: {self.recommendations[selected_option]}")

    def show_image_preview(self, image_path, resize_to_square: bool = True):
        image = Image.open(image_path)
        if resize_to_square:
            image = image.resize((256, 256))
        else:
            image = image.resize((image.width, image.height))
        self.selected_image = ImageTk.PhotoImage(image)
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        x = (canvas_width - image.width) / 2
        y = (canvas_height - image.height) / 2
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.selected_image)
