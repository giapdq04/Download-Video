import yt_dlp
from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu, filedialog, Checkbutton, BooleanVar
from tkinter.ttk import Progressbar
import re

# Từ điển ánh xạ mã ngôn ngữ sang tên ngôn ngữ
language_map = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh": "Chinese",
    "vi": "Vietnamese"
}

def progress_hook(d):
    if d['status'] == 'downloading':
        # Loại bỏ các ký tự màu sắc ANSI
        percent_str = re.sub(r'\x1b\[[0-9;]*m', '', d['_percent_str']).strip().strip('%')
        percent = float(percent_str)
        progress_var.set(percent)
        root.update_idletasks()
    elif d['status'] == 'finished':
        progress_bar.pack_forget()
        download_button.pack()
        progress_var.set(0)

def download_video():
    link = url_entry.get()
    quality = quality_var.get()
    save_path = filedialog.askdirectory()  # Mở hộp thoại để chọn thư mục lưu
    if not save_path:
        return  # Nếu người dùng không chọn thư mục, thoát khỏi hàm

    format_map = {
        "2160p": "bestvideo[height<=2160]+bestaudio/best[height<=2160]",
        "1440p": "bestvideo[height<=1440]+bestaudio/best[height<=1440]",
        "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
        "240p": "bestvideo[height<=240]+bestaudio/best[height<=240]",
        "144p": "bestvideo[height<=144]+bestaudio/best[height<=144]",
    }
    ydl_opts = {
        'format': format_map.get(quality, "best"),
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',  # Đặt đường dẫn lưu video
        'merge_output_format': 'mp4',  # Đảm bảo định dạng đầu ra là MP4
        'progress_hooks': [progress_hook],  # Thêm hook để cập nhật tiến trình
    }

    if subtitle_var.get():
        subtitle_lang_name = subtitle_lang_var.get()
        subtitle_lang = list(language_map.keys())[list(language_map.values()).index(subtitle_lang_name)]
        ydl_opts['subtitleslangs'] = [subtitle_lang]
        ydl_opts['writesubtitles'] = True

        # Kiểm tra định dạng phụ đề có sẵn
        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(link, download=False)
            subs = info_dict.get('subtitles', {})
            if subtitle_lang in subs and any(fmt['ext'] == 'srt' for fmt in subs[subtitle_lang]):
                ydl_opts['subtitlesformat'] = 'srt'
            else:
                ydl_opts['subtitlesformat'] = 'vtt'

    download_button.pack_forget()
    progress_bar.pack()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

# GUI setup
root = Tk()
root.title("Video Downloader")

Label(root, text="Enter URL:").pack()
url_entry = Entry(root, width=50)
url_entry.pack()

Label(root, text="Select Quality:").pack()
quality_var = StringVar(root)
quality_var.set("1080p")  # default value
quality_options = ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]
OptionMenu(root, quality_var, *quality_options).pack()

subtitle_var = BooleanVar()
subtitle_checkbox = Checkbutton(root, text="Download Subtitles", variable=subtitle_var)
subtitle_checkbox.pack()

Label(root, text="Select Subtitle Language:").pack()
subtitle_lang_var = StringVar(root)
subtitle_lang_var.set("English")  # default value
subtitle_lang_options = list(language_map.values())
OptionMenu(root, subtitle_lang_var, *subtitle_lang_options).pack()

progress_var = StringVar()
progress_bar = Progressbar(root, orient="horizontal", length=300, mode="determinate", variable=progress_var)

download_button = Button(root, text="Download", command=download_video)
download_button.pack()

root.mainloop()