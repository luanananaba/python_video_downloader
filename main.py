import tkinter
import customtkinter
import yt_dlp


"""
Para funcionar:

No terminal:
Windows -> pip install yt-dlp
Mac/Linux -> pip3 install yt-dlp

Vídeo em alta qualidade -> baixar ffmpeg -> https://ffmpeg.org/download.html
"""


def get_video_title(yt_link):
    ydl_opts = {}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(yt_link, download=False)

        return info_dict.get('title', 'Título não encontrado')


def on_progress(d):
    if d['status'] == 'downloading':
        total_size = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
        bytes_downloaded = d.get('downloaded_bytes', 0)
        percentage = bytes_downloaded / total_size * 100 if total_size else 0

        p_percentage.configure(text=f'{percentage:.2f}%')
        p_percentage.update()
        progress_bar.set(percentage / 100)


def start_download():
    try:
        yt_link = link.get()
        video_title = get_video_title(yt_link)

        title.configure(text=video_title, text_color='white')

        ydl_opts = {
            'progress_hooks': [on_progress],
            'outtmpl': 'videos/%(title)s.%(ext)s',
            'verbose': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_link])

        finish_label.configure(text='Download completo!', text_color='green')
        
    except Exception as e:
        finish_label.configure(text=f'Erro ao baixar: {str(e)}', text_color='red')
        title.configure(text='ERROR: Insira um link válido!')


# System Settings
customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('blue')


# App frame.
app = customtkinter.CTk()
app.geometry('1280x720')
app.title('Youtube Downloads Grátis 2026')


# Adding UI Elements
title = customtkinter.CTkLabel(app, text='Coloque um link do Youtube!')
title.pack(padx=10, pady=10)


# Link input.
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()


# Finished downloading.
finish_label = customtkinter.CTkLabel(app, text='')
finish_label.pack()


# Progress percentage.
p_percentage = customtkinter.CTkLabel(app, text='0%')
p_percentage.pack()

progress_bar = customtkinter.CTkProgressBar(app, width=400)
progress_bar.set(0)
progress_bar.pack(padx=10, pady=10)


# Download button.
download = customtkinter.CTkButton(app, text='Download', command=start_download)
download.pack(padx=10, pady=10)


# Run app.
app.mainloop()