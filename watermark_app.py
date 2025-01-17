from PIL import Image, ImageTk, ImageFont, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox, font
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
        self.geometry('900x650')

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

        self.font_size = 50  # Default font size
        self.font_opacity = 0.6  # Default Opacity
        self.selected_font_color = "#FFFFFF"  # Default font color (white)

        # New properties for text position
        self.text_x = 0
        self.text_y = 0
        self.movement_increment = 10  # Default movement amount

        self.create_widgets()

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

        # Buttons for moving text
        self.move_up_button = tk.Button(self, text="Up", command=self.move_text_up,
                                        bg=self.button_bg_color, fg=self.button_fg_color)
        self.move_up_button.grid(row=9, column=0, padx=5, pady=5)

        self.move_down_button = tk.Button(self, text="Down", command=self.move_text_down,
                                          bg=self.button_bg_color, fg=self.button_fg_color)
        self.move_down_button.grid(row=9, column=1, padx=5, pady=5)

        self.move_left_button = tk.Button(self, text="Left", command=self.move_text_left,
                                          bg=self.button_bg_color, fg=self.button_fg_color)
        self.move_left_button.grid(row=9, column=2, padx=5, pady=5)

        self.move_right_button = tk.Button(self, text="Right", command=self.move_text_right,
                                           bg=self.button_bg_color, fg=self.button_fg_color)
        self.move_right_button.grid(row=9, column=3, padx=5, pady=5)

        self.move_increment_label = tk.Label(self, text="Movement Increment (pixels):",
                                             bg=self['bg'], fg=self.label_fg_color)
        self.move_increment_label.grid(row=10, column=0, padx=5, pady=5)

        self.move_increment_entry = tk.Entry(self, bg=self.text_bg_color, fg=self.label_fg_color)
        self.move_increment_entry.grid(row=10, column=1, padx=5, pady=5)
        self.move_increment_entry.insert(0, self.movement_increment)

        self.rotation_label = tk.Label(self, text="Rotation Angle:", bg=self['bg'], fg=self.label_fg_color)
        self.rotation_label.grid(row=11, column=0, padx=5, pady=5)

        self.rotation_entry = tk.Entry(self, bg=self.text_bg_color, fg=self.label_fg_color)
        self.rotation_entry.grid(row=11, column=1, padx=5, pady=5)
        self.rotation_entry.insert(0, 0)

        self.rotate_button = tk.Button(self, text="Rotate", command=self.rotate_clockwise,
                                          bg=self.button_bg_color, fg=self.button_fg_color)
        self.rotate_button.grid(row=11, column=2, padx=5, pady=5)

    def select_font_color(self):
        color = colorchooser.askcolor(title="Select Font Color")[1]  # Get the selected color
        if color:
            self.font_color_button.config(bg=color)  # Update the button color to show the color selected
            self.selected_font_color = color

    def watermark(self, selected_font, x, y, rotation_angle):
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

        # Calculate the final position based on the provided x and y coordinates
        x_final = x
        y_final = y

        # Convert opacity value to alpha value (0-255)
        opacity = int(float(self.font_opacity_entry.get()) * 255)
        text_color = tuple(int(self.selected_font_color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)) + (opacity,)

        # Create a new image with the same size and format as the original image
        txt_img = Image.new("RGBA", image.size, (255, 255, 255, 0))
        txt_draw = ImageDraw.Draw(txt_img)

        # Draw the text on the new image with the adjusted alpha value
        txt_draw.text((x_final, y_final), self.watermark_text, fill=text_color, font=chosen_font)
        rotated_txt_img = txt_img.rotate(rotation_angle, expand=True)  # Rotate the text image

        # Before compositing
        print("Image Size:", image.size, "Image Mode:", image.mode)
        print("Rotated Text Size:", rotated_txt_img.size, "Rotated Text Mode:", rotated_txt_img.mode)

        # Blend the text image with the original image using alpha compositing

        # Assuming rotated_txt_img is the rotated text image
        # Resize rotated_txt_img to match the size of image
        rotated_txt_img = rotated_txt_img.resize(image.size, Image.Resampling.LANCZOS)

        # Now perform alpha compositing with the resized rotated_txt_img
        image = Image.alpha_composite(image, rotated_txt_img)

        # After compositing
        print("Composited Image Size:", image.size, "Composited Image Mode:", image.mode)

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
                # Convert the image to RGB mode before saving as JPEG
                if self.current_image.mode == "RGBA":
                    rgb_image = self.current_image.convert("RGB")
                    rgb_image.save(file_path, "JPEG")
                else:
                    self.current_image.save(file_path, "JPEG")

                messagebox.showinfo("Save Successful", "Data saved successfully.")
            except Exception as e:
                print(f"Error: {str(e)}")
                messagebox.showerror("Error", f"An error occurred while saving data: {str(e)}")

    def apply_text(self):
        self.watermark_text = self.watermark_text_entry.get("1.0", tk.END).strip()
        if self.watermark_text:
            selected_font_name = self.selected_font.get()
            rotation_angle = self.rotation_entry.get()  # Get rotation angle from Entry field
            print(f"applied font name: {selected_font_name}")
            try:
                new_font_size = int(self.font_size_entry.get())
                if new_font_size <= 0:
                    messagebox.showerror("Error", "Font size must be greater than zero")
                    return
                self.font_size = new_font_size

                # Convert the rotation angle to integer
                rotation_angle = int(rotation_angle)

                # Print the opacity value
                opacity_value = self.font_opacity_entry.get()
                print(f"Opacity Value: {opacity_value}")
                print(f"X: {self.text_x},\nY: {self.text_y}")

            except ValueError:
                messagebox.showerror("Error", "Invalid font size. Please enter a valid integer.")
                return

            if selected_font_name:
                try:
                    self.watermark(selected_font_name, self.text_x, self.text_y, rotation_angle)
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

        # Get the dimensions of the loaded image
        image_width, image_height = image.size

        # Calculate the center of the image
        self.text_x = image_width // 2
        self.text_y = image_height // 2

    def move_text_up(self):
        # Move the text up by a certain amount and reapply the text.
        self.text_y -= int(self.move_increment_entry.get())  # Adjust the increment/decrement value as needed
        self.apply_text()

    def move_text_down(self):
        # Move the text down by a certain amount and reapply the text.
        self.text_y += int(self.move_increment_entry.get())  # Adjust the increment/decrement value as needed
        self.apply_text()

    def move_text_left(self):
        # Move the text left by a certain amount and reapply the text.
        self.text_x -= int(self.move_increment_entry.get())  # Adjust the increment/decrement value as needed
        self.apply_text()

    def move_text_right(self):
        # Move the text right by a certain amount and reapply the text.
        self.text_x += int(self.move_increment_entry.get())  # Adjust the increment/decrement value as needed
        self.apply_text()

    def rotate_clockwise(self):
        rotation_angle = self.rotation_entry.get()
        if rotation_angle:
            self.apply_text()

    def rotate_counterclockwise(self):
        rotation_angle = self.rotation_entry.get()
        if rotation_angle:
            self.apply_text()


if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()
