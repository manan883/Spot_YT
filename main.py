import tkinter as tk
from tkinter import messagebox
import re
from playlist import playlist
def run_playlist():
    playlist_link = playlist_link_entry.get()
    playlist_name_yt = playlist_name_yt_entry.get()
    if playlist_link and playlist_name_yt:
        # Extract playlist ID from the link
        match = re.search(r"playlist/(\w+)", playlist_link)
        if match:
            playlist_id = match.group(1)
            print(match)
            try:
                playlist(playlist_id, playlist_name_yt)
                messagebox.showinfo("Success", "Playlist created successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Invalid Spotify playlist link.")
    else:
        messagebox.showwarning("Input Error", "Please enter both Playlist Link and Playlist Name.")

root = tk.Tk()
root.title("Spotify to YouTube Playlist")

playlist_link_label = tk.Label(root, text="Spotify Playlist Link:")
playlist_link_label.pack()

playlist_link_entry = tk.Entry(root)
playlist_link_entry.pack()

playlist_name_yt_label = tk.Label(root, text="Playlist Name on YouTube:")
playlist_name_yt_label.pack()

playlist_name_yt_entry = tk.Entry(root)
playlist_name_yt_entry.pack()

run_button = tk.Button(root, text="Create Playlist", command=run_playlist)
run_button.pack()

root.mainloop()
