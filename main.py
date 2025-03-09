import os
import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Label, Entry, Button, filedialog, StringVar, messagebox, ttk

def download_pdfs(url, folder):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links that end with .pdf
        pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
        total_pdfs = len(pdf_links)

        if total_pdfs == 0:
            messagebox.showinfo("No PDFs Found", "No PDF files found at the provided URL.")
            return

        # Update the progress bar
        progress_bar['maximum'] = total_pdfs
        progress_bar['value'] = 0

        # Download each PDF
        for pdf_link in pdf_links:
            if not pdf_link.startswith('http'):
                pdf_link = requests.compat.urljoin(url, pdf_link)  # Handle relative URLs
            
            # Get the PDF response and its size
            pdf_response = requests.get(pdf_link, stream=True)
            pdf_response.raise_for_status()  # Check for request errors

            pdf_name = os.path.basename(pdf_link)
            pdf_size = len(pdf_response.content)  # Get the size of the PDF in bytes

            # Update the label with the current PDF name and size
            current_pdf_label.config(text=f"Downloading: {pdf_name} ({pdf_size / 1024:.2f} KB)")

            with open(os.path.join(folder, pdf_name), 'wb') as pdf_file:
                pdf_file.write(pdf_response.content)

            # Update the progress bar
            progress_bar['value'] += 1
            root.update_idletasks()  # Update the GUI

        messagebox.showinfo("Success", f"Downloaded {total_pdfs} PDF(s) to {folder}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

def start_download():
    url = url_entry.get()
    folder = folder_var.get()
    if url and folder:
        download_pdfs(url, folder)
    else:
        messagebox.showwarning("Input Error", "Please enter a valid URL and select a folder.")

# GUI setup
root = Tk()
root.title("PDF Downloader")

folder_var = StringVar()

Label(root, text="Enter Website URL:").pack(pady=5)
url_entry = Entry(root, width=50)
url_entry.pack(pady=5)

Button(root, text="Select Folder", command=select_folder).pack(pady=5)
Label(root, textvariable=folder_var).pack(pady=5)

Button(root, text="Download PDFs", command=start_download).pack(pady=20)

# Label for current PDF name and size
current_pdf_label = Label(root, text="")
current_pdf_label.pack(pady=5)

# Progress bar
progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
progress_bar.pack(pady=20)

root.mainloop()

