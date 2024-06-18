import os
from tkinter import Tk, filedialog, Button, Label, messagebox
from PIL import Image, ImageFile

# Ensure full loading of truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

def resize_and_optimize_image(input_path, output_path, size=(800, 800), quality=85):

    try:
        # Open an image file
        with Image.open(input_path) as img:
            # Resize image to the specified size
            img = img.resize(size, Image.LANCZOS)

            # Convert to RGB if necessary
            if img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            
            # Save it back to disk with the specified quality 
            img.save(output_path, format='JPEG', quality=quality, optimize=True, progressive=True)
    except Exception as e:
        raise Exception(f"Error processing image {input_path}: {e}")

def choose_files():
    # Open file dialog to select multiple images
    file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if not file_paths:
        return
    
    # Get the path to the Documents folder
    documents_folder = os.path.join(os.path.expanduser('~'), 'Documents')

    # Create a new folder if it doesn't exist
    new_folder_path = os.path.join(documents_folder, 'new_folder')
    os.makedirs(new_folder_path, exist_ok=True)

    counter = 1
    for file_path in file_paths:
        try:
            output_path = os.path.join(new_folder_path, f"{counter}.jpg")
            resize_and_optimize_image(file_path, output_path)
            counter += 1
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process {file_path}: {e}")
            continue

    messagebox.showinfo("Success", "Images have been resized and optimized successfully. Check Documents/new_folder.")

def create_gui():
    root = Tk()
    root.title("Image Optimizer and Resizer")
    
    # Set background color
    root.configure(bg='light gray')

    label = Label(root, text="Select images to resize and optimize:")
    label.pack(pady=20)

    choose_button = Button(root, text="Choose Files", command=choose_files)
    choose_button.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
