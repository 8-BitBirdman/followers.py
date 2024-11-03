import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
import os

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        process_files(folder_path)

def process_files(folder_path):
    # Define the paths to following.html and followers_1.html
    following_path = os.path.join(folder_path, "following.html")
    followers_path = os.path.join(folder_path, "followers_1.html")
    
    if not os.path.exists(following_path) or not os.path.exists(followers_path):
        messagebox.showerror("Error", "Required files not found in the selected folder.")
        return
    
    # Parse the HTML files to extract the list of followers and following
    following_list = extract_usernames(following_path)
    followers_list = extract_usernames(followers_path)
    
    # Find non-followers
    non_followers = following_list - followers_list
    
    # Display non-followers
    display_non_followers(non_followers)

def extract_usernames(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        
        # Adjust this based on HTML structure - example for extracting links with usernames
        usernames = set(tag.text.strip() for tag in soup.find_all("a", href=True))
        
    return usernames

def display_non_followers(non_followers):
    result_window = tk.Toplevel(root)
    result_window.title("Non-Followers")
    
    if non_followers:
        result_text = "\n".join(non_followers)
    else:
        result_text = "Everyone follows you back!"
    
    text_widget = tk.Text(result_window, wrap="word", width=50, height=20)
    text_widget.insert("1.0", result_text)
    text_widget.config(state="disabled")  # Make text read-only
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)

# Set up the main application window
root = tk.Tk()
root.title("Non-Followers Finder")

# Add a button to select the folder
select_button = tk.Button(root, text="Select Folder", command=select_folder)
select_button.pack(pady=20)

# Run the application
root.geometry("300x150")
root.mainloop()
