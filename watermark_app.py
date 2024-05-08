from PIL import Image, ImageTk, ImageFont, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox, font
import os  # Import the os module to handle file paths
import tkinter.colorchooser as colorchooser


FONT_MAPPING = {"arial": "arial", "bahnschrift": "bahnschrift", "calibri": "calibri", "candara": "Candara",
                "centaur": "CENTAUR", "century": "CENTURY", "chiller": "CHILLER", "corbel": "corbel",
                "ebrima": "ebrima", "forte": "FORTE", "gabriola": "Gabriola", "gadugi": "gadugi",
                "georgia": "georgia", "gigi": "GIGI", "impact": "impact", "jokerman": "JOKERMAN",
                "mistral": "MISTRAL", "onyx": "ONYX", "papyrus": "PAPYRUS", "playbill": "PLAYBILL",
                "pristina": "PRISTINA", "ravie": "RAVIE", "stencil": "STENCIL", "sylfaen": "sylfaen",
                "tahoma": "tahoma", "verdana": "verdana",
                }

# Use lowercase font names for the font list
FONTS = [
    "arial", "bahnschrift", "calibri", "candara", "centaur", "century", "chiller",
    "corbel", "ebrima", "forte", "gabriola", "gadugi", "georgia", "gigi", "impact",
    "jokerman", "mistral", "onyx", "papyrus", "playbill", "pristina", "ravie",
    "stencil", "sylfaen", "tahoma", "verdana"
]


class WatermarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Watermark App")
        self.geometry('900x600')

        # Set dark color scheme
        self.configure(bg='#222831')  # Dark gray background for the window
        self.label_fg_color = '#76ABAE'  # Teal text color for labels
        self.button_bg_color = '#31363F'  # Dark gray background for buttons
        self.button_fg_color = '#EEEEEE'  # White text color for buttons
        self.text_bg_color = '#31363F'  # Dark gray background for text entry

        self.image_path = None
        self.watermark_text = ""
        self.current_image = None  # Global variable to store the loaded image

        self.font_options = font.families()  # Get all available fonts
        self.selected_font = tk.StringVar(value=FONTS[0])

        self.fonts_directory = os.path.join(os.getcwd(), 'fonts')
        # gets files out of the fonts directory and lists them
        self.font_file_list = self.get_font_file_list()

        self.font_size = 30  # Default font size
        self.font_opacity = 0.6  # Default Opacity
        self.selected_font_color = "#FFFFFF"  # Default font color (white)

        self.create_widgets()

    def get_font_file_list(self):
        font_files = os.listdir(self.fonts_directory)
        return font_files

    def create_widgets(self):
        self.img_frame = tk.Frame(self, width=500, height=500, bg=self.button_bg_color)
        self.img_frame.grid(row=1, column=2, rowspan=5, padx=10)

        self.title_label = tk.Label(self, text="Custom Text Watermark App", font=("Arial", 16, "bold"),
                                    bg=self['bg'], fg=self.label_fg_color)
        self.title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.img_select_button = tk.Button(self, text='Select Image', command=self.open_img_file,
                                           bg=self.button_bg_color, fg=self.button_fg_color)
        self.img_select_button.grid(row=1, column=0, padx=5, pady=5)

        self.empty_label = tk.Label(self, text="", bg=self['bg'])
        self.empty_label.grid(row=1, column=1)

        self.watermark_text_entry = tk.Text(self, height=15, width=15, bg=self.text_bg_color, fg=self.label_fg_color)
        self.watermark_text_entry.grid(row=2, column=0, padx=5, pady=5)

        self.apply_text_button = tk.Button(self, text="Apply", command=self.apply_text,
                                           bg=self.button_bg_color, fg=self.button_fg_color)
        self.apply_text_button.grid(row=3, column=0, padx=5, pady=5)

        self.save_img_button = tk.Button(self, text='Save Image', command=self.save_img_file,
                                         bg=self.button_bg_color, fg=self.button_fg_color)
        self.save_img_button.grid(row=4, column=0, padx=5, pady=5)

        self.font_label = tk.Label(self, text="Select Font:", bg=self['bg'], fg=self.label_fg_color)
        self.font_label.grid(row=5, column=0, padx=5, pady=5)

        self.font_menu = tk.OptionMenu(self, self.selected_font, *FONTS)
        self.font_menu.config(bg=self.button_bg_color, fg=self.button_fg_color)
        self.font_menu.grid(row=5, column=1, padx=5, pady=5)

        self.img_label = tk.Label(self.img_frame, bg=self.button_bg_color)
        self.img_label.pack()

        self.font_size_label = tk.Label(self, text="Font Size:", bg=self['bg'], fg=self.label_fg_color)
        self.font_size_label.grid(row=6, column=0, padx=5, pady=5)

        self.font_size_entry = tk.Entry(self, bg=self.text_bg_color, fg=self.label_fg_color)
        self.font_size_entry.grid(row=6, column=1, padx=5, pady=5)
        self.font_size_entry.insert(0, str(self.font_size))  # Set default font size in the entry

        self.font_opacity_label = tk.Label(self, text="Opacity:", bg=self['bg'], fg=self.label_fg_color)
        self.font_opacity_label.grid(row=7, column=0, padx=5, pady=5)

        self.font_opacity_entry = tk.Entry(self, bg=self.text_bg_color, fg=self.label_fg_color)
        self.font_opacity_entry.grid(row=7, column=1, padx=5, pady=5)
        self.font_opacity_entry.insert(0, str(self.font_opacity))  # Set default opacity in the entry

        self.font_color_label = tk.Label(self, text="Font Color:", bg=self['bg'], fg=self.label_fg_color)
        self.font_color_label.grid(row=8, column=0, padx=5, pady=5)

        self.font_color_button = tk.Button(self, text="Select Color", command=self.select_font_color,
                                           bg=self.button_bg_color, fg=self.button_fg_color)
        self.font_color_button.grid(row=8, column=1, padx=5, pady=5)

    def select_font_color(self):
        color = colorchooser.askcolor(title="Select Font Color")[1]  # Get the selected color
        if color:
            self.font_color_button.config(bg=color)  # Update the button color to show the color selected
            self.selected_font_color = color

    def watermark(self, selected_font):
        if self.image_path is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        try:
            font_size = int(self.font_size_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid font size. Please enter a valid integer.")
            return

        if font_size <= 0:
            messagebox.showerror("Error", "Font size must be greater than zero.")
            return

        chosen_font_name = FONT_MAPPING.get(selected_font.lower())
        print(f"Chosen font name: {chosen_font_name}")
        if chosen_font_name:
            try:
                chosen_font = ImageFont.truetype(chosen_font_name, font_size)
            except OSError:
                messagebox.showerror("Error", f"Font '{chosen_font_name}' not available.")
                return
        else:
            messagebox.showerror("Error", f"Font '{selected_font}' not supported.")
            return

        image = Image.open(self.image_path).convert("RGBA")  # Convert to RGBA mode
        image.thumbnail((500, 500))
        draw = ImageDraw.Draw(image)

        text_bbox = draw.textbbox((0, 0), self.watermark_text, font=chosen_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        image_width, image_height = image.size
        x = (image_width - text_width) // 2
        y = (image_height - text_height) // 2

        # Convert opacity value to alpha value (0-255)
        opacity = int(float(self.font_opacity_entry.get()) * 255)
        text_color = tuple(int(self.selected_font_color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)) + (opacity,)

        # Create a new image with the same size and format as the original image
        txt_img = Image.new("RGBA", image.size, (255, 255, 255, 0))
        txt_draw = ImageDraw.Draw(txt_img)

        # Draw the text on the new image with the adjusted alpha value
        txt_draw.text((x, y), self.watermark_text, fill=text_color, font=chosen_font)

        # Blend the text image with the original image using alpha compositing
        image = Image.alpha_composite(image, txt_img)

        self.current_image = image.copy()

        photo = ImageTk.PhotoImage(image)
        self.img_label.config(image=photo)
        self.img_label.image = photo

        return photo

    def open_img_file(self):
        self.image_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("JPEG files", "*.jpg *.jpeg"),
                       ("PNG Files", "*.png"),
                       ("GIF Files", "*.gif"),
                       ("Bitmap Files", "*.bmp"),
                       ("All files", "*.*")],
        )
        if self.image_path:
            self.load_image(self.image_path)

    def save_img_file(self):
        if self.image_path is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Data",
            filetypes=[("JPEG files", "*.jpg *.jpeg"),
                       ("All files", "*.*")],
            defaultextension=".jpg"
        )
        if file_path:
            try:
                with open(file_path, "wb") as file:
                    self.current_image.save(file, "JPEG")
                messagebox.showinfo("Save Successful", "Data saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving data: {str(e)}")

    def apply_text(self):
        self.watermark_text = self.watermark_text_entry.get("1.0", tk.END).strip()
        if self.watermark_text:
            selected_font_name = self.selected_font.get()
            print(f"applied font name: {selected_font_name}")
            try:
                new_font_size = int(self.font_size_entry.get())
                if new_font_size <= 0:
                    messagebox.showerror("Error", "Font size must be greater than zero")
                    return
                self.font_size = new_font_size

                # Print the opacity value
                opacity_value = self.font_opacity_entry.get()
                print(f"Opacity Value: {opacity_value}")

            except ValueError:
                messagebox.showerror("Error", "Invalid font size. Please enter a valid integer.")
                return

            if selected_font_name:
                try:
                    self.watermark(selected_font_name)
                except Exception as e:
                    print(str(e))
                    messagebox.showerror("Error", f"Font error: {str(e)}")
            else:
                messagebox.showwarning("Warning", "Selected font is not available.")
        else:
            messagebox.showwarning("Warning", "Please enter text for watermark.")

    def load_image(self, file_path):
        image = Image.open(file_path).convert("RGBA")  # Convert the image to RGBA mode
        image.thumbnail((500, 500))
        self.current_image = image.copy()
        photo = ImageTk.PhotoImage(image)
        self.img_label.config(image=photo)
        self.img_label.image = photo


if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()
