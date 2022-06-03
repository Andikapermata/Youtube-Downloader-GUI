from tkinter import *
from PIL import Image, ImageTk
import re, os, requests, shutil
from pytube import YouTube


#Referensi https://stackoverflow.com/a/49325719

class SampleApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Youtube Downloader")
        self.config(background="PaleGreen1")
        self.resizable(False, False)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class, **kwargs):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self, **kwargs)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.geometry("600x600")
        self.config(background="PaleGreen1")
        self.img = ImageTk.PhotoImage(Image.open("yt.png"))
        canvas = Canvas(self, width = 320, height = 320, bg="PaleGreen1")
        canvas.create_image(10, 10, anchor=NW, image=self.img) 
        canvas.pack()
        l = Label(self, text="Youtube Link : ", bg="salmon",font="SegoeUI 12")
        self.ent = Entry(self, width = 50, font="Arial 12")
        Button(self, pady = 3, padx = 5,text="Download Video",
                  command=lambda: self.getData("video")).pack(side=BOTTOM, fill = "both", pady = 7)
        Button(self, pady = 5, padx = 10, text="Download Audio",
                  command=lambda: self.getData("audio")).pack(side=BOTTOM, fill = "both", padx = 3, pady = 5)
        l.pack(side=LEFT, fill="both", pady=15, padx=15)
        self.ent.pack(side=LEFT, fill = "both", padx = 10, pady = 10)

    def getUrlInText(self,text):
        regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        datas = re.findall(regex, text)
        links = []
        for link in datas:
            if link not in links:
                links.append(link)
        return links

    def getData(self, ttype):
        links = self.getUrlInText(self.ent.get())
        if len(links) == 0:
            return self.master.switch_frame(FailedPage, error="Please input a valid link")
        if ttype == "video":
            if "video" not in os.listdir():
                os.mkdir("video")
            path = os.getcwd()+"\\video\\"
        else:
            if "audio" not in os.listdir():
                os.mkdir("audio")
            path = os.getcwd()+"\\audio\\"
        try:
            # cl = pafy.new(links[0])
            getVideo = YouTube(links[0])
            if ttype == "video":
                getVideo.streams.get_highest_resolution().download(path)
            else:
                getVideo.streams.get_audio_only().download(path)
            self.master.switch_frame(SuccessPage, path = path)
        except Exception as e:
            self.master.switch_frame(FailedPage, error = e)

    def saveFile(self,path, raw):
        with open(path, 'wb') as f:
            shutil.copyfileobj(raw, f)

    def downloadFileURL(self, fileUrl, saveAs):
        r = requests.get(fileUrl,stream=True)
        if r.status_code != 404:
            self.saveFile(saveAs,r.raw)
            return print("Download File Success ...")
        else:
            return print("Download file failure ...")

class SuccessPage(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master)
        master.geometry("500x250")
        path = kwargs.get("path")
        self.config(background="PaleGreen1")
        Label(self, text="Success Downloading").pack(side="top", fill="x", pady=10)
        Label(self, text=f"Download Path : {path}").pack(side="top", fill="x", pady=10)
        Button(self, pady = 5, padx = 10,text="Kembali ke halaman utama",
                  command=lambda: master.switch_frame(StartPage)).pack(side = BOTTOM)

class FailedPage(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master)
        error = kwargs.get("error")
        master.geometry("500x250")
        self.config(background="PaleGreen1")
        Label(self, text="Failed Download").pack(side="top", fill="x", pady=10)
        Label(self, text=f"Reason : {error}").pack(side="top", fill="x", pady=10)
        Button(self, pady = 5, padx = 10,text="Kembali ke halaman utama",
                  command=lambda: master.switch_frame(StartPage)).pack(side = BOTTOM)

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()