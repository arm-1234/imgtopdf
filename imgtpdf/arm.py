import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import threading

# Function to convert images to PDF
def convert_images_to_pdf(input_images, output_pdf):
    try:
        # Create a PDF document
        c = canvas.Canvas(output_pdf, pagesize=letter)

        # Iterate through input image files
        for img_path in input_images:
            if img_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                img = Image.open(img_path)

                # Adjust image size to fit the PDF page (you can customize this part)
                img_width, img_height = img.size
                pdf_width, pdf_height = letter
                scale = min(pdf_width / img_width, pdf_height / img_height)
                img_width *= scale
                img_height *= scale

                # Add the image to the PDF
                c.drawImage(img_path, 0, 0, width=img_width, height=img_height)
                c.showPage()  # Start a new page for the next image

        # Save the PDF file
        c.save()
        result_label.config(text=f'PDF "{output_pdf}" created successfully!')
    except Exception as e:
        result_label.config(text=f'Error: {str(e)}')

# Function to browse and select image files
def browse_images():
    file_paths = filedialog.askopenfilenames(title="Select Image Files", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    selected_files.config(text=", ".join(file_paths))

# Function to convert and download the PDF
def convert_and_download():
    input_images = selected_files.cget("text").split(", ")
    output_pdf = "output.pdf"  # Output PDF file name (customize this)

    if not input_images:
        messagebox.showerror("Error", "No image files selected.")
        return

    browse_button.config(state=tk.DISABLED)
    convert_button.config(state=tk.DISABLED)

    conversion_thread = threading.Thread(target=convert_images_to_pdf, args=(input_images, output_pdf))
    conversion_thread.start()

    def check_conversion_thread():
        if conversion_thread.is_alive():
            window.after(100, check_conversion_thread)
        else:
            browse_button.config(state=tk.NORMAL)
            convert_button.config(state=tk.NORMAL)

    check_conversion_thread()

# Create the main window
window = tk.Tk()
window.title("Image to PDF Converter")

# Create a label to display selected files
selected_files = tk.Label(window, text="No files selected.")
selected_files.pack()

# Create a button to browse for image files with some customizations
browse_button = tk.Button(window, text="Browse Images", command=browse_images, bg="lightblue", fg="black", font=("Arial", 12), relief="raised")
browse_button.pack()

# Create a button to convert and download the PDF with customizations
convert_button = tk.Button(window, text="Convert to PDF and Download", command=convert_and_download, bg="green", fg="white", font=("Arial", 12), relief="raised")
convert_button.pack()

# Create a label to display conversion result
result_label = tk.Label(window, text="")
result_label.pack()

# Run the GUI application
window.mainloop()
