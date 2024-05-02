from PIL import Image, ImageTk, ImageFont, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox

image_path = None
watermark_text = ""
current_image = None  # Global variable to store the loaded image


def watermark(font):
    global image_path
    global watermark_text
    global current_image
    if image_path is None:
        messagebox.showerror("Error", "No image loaded.")
        return

    # Create an image object from the file path
    image = Image.open(image_path)
    # Resize the image to fit the frame
    image.thumbnail((500, 500))

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Define the font and size for the watermark text
    text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Calculate the position to center the text on the image
    image_width, image_height = image.size
    x = (image_width - text_width) // 2
    y = (image_height - text_height) // 2

    # Draw the text on the image
    draw.text((x, y), watermark_text, fill=(255, 255, 255, 128), font=font)

    # Update the current image with the watermarked image
    current_image = image.copy()

    # Convert the image to PhotoImage for display
    photo = ImageTk.PhotoImage(image)
    img_label.config(image=photo)
    img_label.image = photo  # Keep a reference to avoid garbage collection

    return photo


def open_img_file():
    global image_path
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=(("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")))
    if image_path:
        load_image(image_path)


def save_img_file():
    global current_image
    global image_path
    if image_path is None:
        messagebox.showerror("Error", "No image loaded.")
        return

    file_path = filedialog.asksaveasfilename(
        title="Save Data",
        filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")],
        defaultextension=".jpg"
    )
    if file_path:
        try:
            with open(file_path, "wb") as file:
                current_image.save(file, "JPEG")  # Save the current image as JPEG format
            messagebox.showinfo("Save Successful", "Data saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving data: {str(e)}")


def apply_text():
    global watermark_text
    global current_image
    watermark_text = watermark_text_entry.get("1.0", tk.END).strip()
    if watermark_text:
        font = ImageFont.truetype("arial.ttf", 30)
        watermark(font)
    else:
        messagebox.showwarning("Warning", "Please enter text for watermark.")


def load_image(file_path):
    global current_image
    image = Image.open(file_path)
    image.thumbnail((500, 500))  # Resize the image to fit the frame
    current_image = image.copy()  # Store the loaded image
    photo = ImageTk.PhotoImage(image)
    img_label.config(image=photo)
    img_label.image = photo  # Keep a reference to avoid garbage collection


window = tk.Tk()
window.title("Watermark App")
window.geometry('900x600')

img_frame = tk.Frame(window, width=500, height=500)
img_frame.grid(row=1, column=2, rowspan=5, padx=10)

title_label = tk.Label(text="Custom Text Watermark App", font=("Ariel", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

img_select_button = tk.Button(text='Select Image', command=open_img_file)
img_select_button.grid(row=1, column=0, padx=5, pady=5)

empty_label = tk.Label(text="")
empty_label.grid(row=1, column=1)

watermark_text_entry = tk.Text(window, height=15, width=15)
watermark_text_entry.grid(row=2, column=0, padx=5, pady=5)

apply_text_button = tk.Button(text="Apply", command=apply_text)
apply_text_button.grid(row=3, column=0, padx=5, pady=5)

save_img_button = tk.Button(text='Save Image', command=save_img_file)
save_img_button.grid(row=4, column=0, padx=5, pady=5)

img_label = tk.Label(img_frame)
img_label.pack()

window.mainloop()
