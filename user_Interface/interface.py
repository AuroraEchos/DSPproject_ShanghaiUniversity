import os
import time
import webbrowser
import audio_plot
import audio_play
import email_send
import audio_record
import tkinter as tk
import tkinter.filedialog
from pydub import AudioSegment
from tkinter import colorchooser
from ttkbootstrap import Style

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


import sys
current_path = os.path.dirname(os.path.abspath(__file__))
parent_dir1 = os.path.dirname(current_path)
sys.path.append(parent_dir1)


import Denoise.denoise
import Denoise.add_noise
import Denoise.noise_plot
import Separation.merge
import Separation.separation
import Separation.separation_plot
import Recognition.content_recognition
import Recognition.character_recognition_Voiceprint
import Recognition.character_recognition_Deeplearning




class CustomLabel(tk.Label):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.label_bg_color = self.cget("bg")

class WindowManager:
    def __init__(self, root):
        self.root = root
        self.global_bg_color = "white"
        self.intensity=tk.IntVar(value=1)

    def change_background_color(self):
        colorvalue = tk.colorchooser.askcolor(initialcolor=self.global_bg_color)[1]
        self.global_bg_color = colorvalue
        self.update_background_color(self.root)

    def update_background_color(self, window):
        window.config(bg=self.global_bg_color)
        for widget in window.winfo_children():
            if isinstance(widget, tk.Toplevel):
                self.update_background_color(widget)

    def audio_information(self, audio_file_path):
        audio = AudioSegment.from_file(audio_file_path)
        duration_s = len(audio) / 1000
        sample_rate = audio.frame_rate
        sample_width = audio.sample_width * 8
        channels = audio.channels
        return duration_s, sample_rate, sample_width, channels
    
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    global icon_path
    icon_path = os.path.join(desktop_path, "Dsp", "user_Interface", "icon", "001.ico")


    #bug提交界面
    def bug_submission_interface(self):
        bug_submission_interface=tk.Toplevel()
        bug_submission_interface.geometry("400x200")
        bug_submission_interface.resizable(0, 0)
        bug_submission_interface.configure(bg="white")
        bug_submission_interface.title("Bug-提交")

        def submit_button_clicked():
            user_email = a1.get()
            user_feedback = a2.get("1.0", "end-1c")
            email_send.send_email(user_email, user_feedback)
            success_message = "已提交成功，感谢您的宝贵建议！！"
            a2.insert("end", "\n\n" + success_message)
            a2.insert("end", " 😄😄😄") 

        a0=ttk.Button(bug_submission_interface,text="您的邮箱",bootstyle=(INFO, OUTLINE))
        a0.place(x=20,y=10)
        a1=tk.Entry(bug_submission_interface, text="", bg='white',  width=30, relief="sunken")
        a1.place(x=100,y=14)
        a2=tk.Text(bug_submission_interface,bg='white', width=29,height=6,relief="sunken")
        a2.place(x=100,y=44)


        a3=ttk.Button(bug_submission_interface,text="提交",bootstyle=(INFO, OUTLINE),command=lambda:[submit_button_clicked()])
        a3.place(x=340,y=160)

    #成员识别界面-声纹识别
    def characterrecognitionVoiceprint_interface(self):
        characterrecognitionVoiceprint_interface=tk.Tk()
        characterrecognitionVoiceprint_interface.geometry("400x250")
        characterrecognitionVoiceprint_interface.configure(bg="white")
        characterrecognitionVoiceprint_interface.resizable(0, 0)
        characterrecognitionVoiceprint_interface.title("成员识别-声纹识别")
        characterrecognitionVoiceprint_interface.iconbitmap(default=icon_path)

        def return_to_Deeplearning_Voiceprintopintions_interface():
            characterrecognitionVoiceprint_interface.destroy()
            self.Deeplearning_Voiceprintopintions_interface()

        def choose_file_characterrecognition():
            global characterrecognitionVoiceprint_filepath
            characterrecognitionVoiceprint_filepath=tkinter.filedialog.askopenfilename()
            m1.config(state="normal")
            m1.delete(0,tk.END)
            m1.insert(0,characterrecognitionVoiceprint_filepath)
            m1.config(state="readonly")
            

        def text_get():
            m3.insert(tk.END, "请等待...")
            characterrecognitionVoiceprint_interface.update() 
            result=Recognition.character_recognition_Voiceprint.predicted(characterrecognitionVoiceprint_filepath)
            m3.delete(1.0,tk.END)
            m3.insert(tk.END, result)
        
        m0=ttk.Button(characterrecognitionVoiceprint_interface,text="选择音频",bootstyle=(INFO, OUTLINE),command=lambda:[choose_file_characterrecognition()])
        m0.place(x=30,y=20)
        m1=tk.Entry(characterrecognitionVoiceprint_interface,text="", bg='white', width=30, relief="sunken")
        m1.place(x=120,y=24) 
        m2=ttk.Button(characterrecognitionVoiceprint_interface,text="成员识别",bootstyle=(INFO, OUTLINE),command=lambda:[text_get()])
        m2.place(x=30,y=63)
        m3=tk.Text(characterrecognitionVoiceprint_interface,bg='white', width=29,height=8,relief="sunken")
        m3.place(x=120,y=64)


        characterrecognitionVoiceprint_interface.protocol('WM_DELETE_WINDOW',return_to_Deeplearning_Voiceprintopintions_interface)

    #成员识别界面-神经网络
    def characterrecognitionDeeplearning_interface(self):
        characterrecognitionDeeplearning_interface=tk.Tk()
        characterrecognitionDeeplearning_interface.geometry("400x250")
        characterrecognitionDeeplearning_interface.configure(bg="white")
        characterrecognitionDeeplearning_interface.resizable(0, 0)
        characterrecognitionDeeplearning_interface.title("成员识别-神经网络")
        characterrecognitionDeeplearning_interface.iconbitmap(default=icon_path)

        def return_to_Deeplearning_Voiceprintopintions_interface():
            characterrecognitionDeeplearning_interface.destroy()
            self.Deeplearning_Voiceprintopintions_interface()

        def choose_file_characterrecognition():
            global characterrecognitionDeeplearning_filepath
            characterrecognitionDeeplearning_filepath=tkinter.filedialog.askopenfilename()
            m1.config(state="normal")
            m1.delete(0,tk.END)
            m1.insert(0,characterrecognitionDeeplearning_filepath)
            m1.config(state="readonly")
            

        def text_get():
            m3.insert(tk.END, "请等待...")
            characterrecognitionDeeplearning_interface.update() 
            result=Recognition.character_recognition_Deeplearning.newaudio_process(characterrecognitionDeeplearning_filepath)
            m3.delete(1.0,tk.END)
            m3.insert(tk.END, result)
        
        m0=ttk.Button(characterrecognitionDeeplearning_interface,text="选择音频",bootstyle=(INFO, OUTLINE),command=lambda:[choose_file_characterrecognition()])
        m0.place(x=30,y=20)
        m1=tk.Entry(characterrecognitionDeeplearning_interface,text="", bg='white', width=30, relief="sunken")
        m1.place(x=120,y=24) 
        m2=ttk.Button(characterrecognitionDeeplearning_interface,text="成员识别",bootstyle=(INFO, OUTLINE),command=lambda:[text_get()])
        m2.place(x=30,y=63)
        m3=tk.Text(characterrecognitionDeeplearning_interface,bg='white', width=29,height=8,relief="sunken")
        m3.place(x=120,y=64)


        characterrecognitionDeeplearning_interface.protocol('WM_DELETE_WINDOW',return_to_Deeplearning_Voiceprintopintions_interface)

    #成员识别选择界面
    def Deeplearning_Voiceprintopintions_interface(self):
        Deeplearning_Voiceprintopintions_interface=tk.Tk()
        Deeplearning_Voiceprintopintions_interface.geometry("300x100")
        Deeplearning_Voiceprintopintions_interface.configure(bg="white")
        Deeplearning_Voiceprintopintions_interface.resizable(0, 0)
        Deeplearning_Voiceprintopintions_interface.title("识别")
        Deeplearning_Voiceprintopintions_interface.iconbitmap(default=icon_path)

        def return_to_content_characteropintions_interface():
            Deeplearning_Voiceprintopintions_interface.destroy()
            self.content_characteropintions_interface()

        t0=ttk.Button(Deeplearning_Voiceprintopintions_interface,text="神经网络", bootstyle=(INFO, OUTLINE),command=lambda:[Deeplearning_Voiceprintopintions_interface.withdraw(),self.characterrecognitionDeeplearning_interface()])
        t0.place(x=15,y=30)
        t1=ttk.Button(Deeplearning_Voiceprintopintions_interface,text="声纹识别", bootstyle=(INFO, OUTLINE),command=lambda:[Deeplearning_Voiceprintopintions_interface.withdraw(),self.characterrecognitionVoiceprint_interface()])
        t1.place(x=195,y=30)
        lable=tk.Label(Deeplearning_Voiceprintopintions_interface,text="or",bg="white")
        lable.place(x=140,y=33)

        Deeplearning_Voiceprintopintions_interface.protocol('WM_DELETE_WINDOW',return_to_content_characteropintions_interface)

    #内容识别界面
    def contentrecognition_interface(self):
        contentrecognition_interface=tk.Toplevel()
        contentrecognition_interface.geometry("400x250")
        contentrecognition_interface.configure(bg="white")
        contentrecognition_interface.resizable(0, 0)
        contentrecognition_interface.title("内容识别")
        contentrecognition_interface.iconbitmap(default=icon_path)

        def return_to_content_characteropintions_interface():
            contentrecognition_interface.destroy()
            self.content_characteropintions_interface()


        def choose_file_contentrecognition():
            global contentrecognition_filepath
            contentrecognition_filepath=tkinter.filedialog.askopenfilename()
            j1.config(state="normal")
            j1.delete(0,tk.END)
            j1.insert(0,contentrecognition_filepath)
            j1.config(state="readonly")
            
        def text_get():
            j5.insert(tk.END, "请等待...")
            contentrecognition_interface.update() 
            result=Recognition.content_recognition.text_output(file_path=contentrecognition_filepath)
            j5.delete(1.0,tk.END)
            j5.insert(tk.END, result)

        
        j0=ttk.Button(contentrecognition_interface,text="选择音频",bootstyle=(INFO, OUTLINE),command=lambda:[choose_file_contentrecognition()])
        j0.place(x=30,y=20)
        j1=tk.Entry(contentrecognition_interface,text="", bg='white', width=30, relief="sunken")
        j1.place(x=110,y=24)
        j4=ttk.Button(contentrecognition_interface,text="内容识别",bootstyle=(INFO, OUTLINE),command=lambda:[text_get()])
        j4.place(x=30,y=63)
        j5=tk.Text(contentrecognition_interface,bg='white', width=29,height=8,relief="sunken")
        j5.place(x=110,y=64)


        contentrecognition_interface.protocol('WM_DELETE_WINDOW',return_to_content_characteropintions_interface)

    #语音识别选择界面
    def content_characteropintions_interface(self):
        content_characteropintions_interface=tk.Tk()
        content_characteropintions_interface.geometry("300x100")
        content_characteropintions_interface.configure(bg="white")
        content_characteropintions_interface.resizable(0, 0)
        content_characteropintions_interface.title("识别")
        content_characteropintions_interface.iconbitmap(default=icon_path)

        i0=ttk.Button(content_characteropintions_interface,text="成员识别", bootstyle=(INFO, OUTLINE),command=lambda:[content_characteropintions_interface.withdraw(),self.Deeplearning_Voiceprintopintions_interface()])
        i0.place(x=15,y=30)
        i1=ttk.Button(content_characteropintions_interface,text="内容识别", bootstyle=(INFO, OUTLINE),command=lambda:[content_characteropintions_interface.withdraw(),self.contentrecognition_interface()])
        i1.place(x=195,y=30)
        lable=tk.Label(content_characteropintions_interface,text="or",bg="white")
        lable.place(x=140,y=33)

    #语音与音乐分离
    def music_separation_interface(self):
        music_separation_interface=tk.Tk()
        music_separation_interface.geometry("500x300")
        music_separation_interface.resizable(0, 0)
        music_separation_interface.configure(bg=self.global_bg_color)
        music_separation_interface.title("语音与音乐分离")
        music_separation_interface.iconbitmap(default=icon_path)
        
        def return_to_options_interface():
            music_separation_interface.destroy()
            self.voice_musicoptions_interface()
        
        def choose_file_speechsepararionmusic(index):
            global speechsepararionmusic_filepath_0
            global speechsepararionmusic_filepath_1
            if index == 0:
                speechsepararionmusic_filepath_0 = tkinter.filedialog.askopenfilename()
                file_path_lable_0.config(state="normal")
                file_path_lable_0.delete(0, tk.END)
                file_path_lable_0.insert(0, speechsepararionmusic_filepath_0)
                file_path_lable_0.config(state="readonly")
            elif index == 1:
                speechsepararionmusic_filepath_1 = tkinter.filedialog.askopenfilename()
                file_path_lable_1.config(state="normal")
                file_path_lable_1.delete(0, tk.END)
                file_path_lable_1.insert(0, speechsepararionmusic_filepath_1)
                file_path_lable_1.config(state="readonly")

        def out_file_speechsepararionmusic(index):
            if index == 0:
                time.sleep(2)
                out_file_path_lable_0.config(state="normal")
                out_file_path_lable_0.delete(0, tk.END)
                desktop_path = os.path.expanduser('~') + '\\Desktop\\'
                filename_mixed = 'mixed.wav'
                outpath_mixed = desktop_path + filename_mixed
                out_file_path_lable_0.insert(0, outpath_mixed)
                out_file_path_lable_0.config(state="readonly")
            elif index == 1:
                time.sleep(1)
                out_file_path_lable_1.config(state="normal")
                out_file_path_lable_1.delete(0, tk.END)
                desktop_path = os.path.expanduser('~') + '\\Desktop\\'
                filename_recovered_1 = 'recovered_1.wav'
                outpath_recovered_1 = desktop_path + filename_recovered_1
                out_file_path_lable_1.insert(0, outpath_recovered_1)
                out_file_path_lable_1.config(state="readonly")
            elif index == 2:
                time.sleep(1)
                out_file_path_lable_2.config(state="normal")
                out_file_path_lable_2.delete(0, tk.END)
                desktop_path = os.path.expanduser('~') + '\\Desktop\\'
                filename_recovered_2 = 'recovered_2.wav'
                outpath_recovered_2 = desktop_path + filename_recovered_2
                out_file_path_lable_2.insert(0, outpath_recovered_2)
                out_file_path_lable_2.config(state="readonly")
        
        k0=ttk.Button(music_separation_interface,text="语音",bootstyle=(INFO, OUTLINE),command=lambda:[choose_file_speechsepararionmusic(0)])
        k0.place(x=50,y=20)
        file_path_lable_0=tk.Entry(music_separation_interface, text="", bg='white',  width=30, relief="sunken")
        file_path_lable_0.place(x=140,y=24)
        k1=ttk.Button(music_separation_interface,text="音乐",bootstyle=(INFO, OUTLINE),command=lambda:[choose_file_speechsepararionmusic(1)])
        k1.place(x=50,y=55)
        file_path_lable_1=tk.Entry(music_separation_interface, text="", bg='white',  width=30, relief="sunken")
        file_path_lable_1.place(x=140,y=59)
        k2=ttk.Button(music_separation_interface,text="混合音频",bootstyle=(INFO, OUTLINE),command=lambda:[Separation.merge.merge_files(file_1=speechsepararionmusic_filepath_0,file_2=speechsepararionmusic_filepath_1),out_file_speechsepararionmusic(0)])
        k2.place(x=50,y=120)
        out_file_path_lable_0=tk.Entry(music_separation_interface, text="", bg='white',  width=30, relief="sunken")
        out_file_path_lable_0.place(x=140,y=124)
        k3=ttk.Button(music_separation_interface,text="分离音频",bootstyle=(INFO, OUTLINE),command=lambda:[Separation.separation.audio_separation(file_1=speechsepararionmusic_filepath_0,file_2=speechsepararionmusic_filepath_1),out_file_speechsepararionmusic(1),out_file_speechsepararionmusic(2)])
        k3.place(x=50,y=160)
        out_file_path_lable_1=tk.Entry(music_separation_interface, text="", bg='white',  width=30, relief="sunken")
        out_file_path_lable_1.place(x=140,y=164)
        out_file_path_lable_2=tk.Entry(music_separation_interface, text="", bg='white',  width=30, relief="sunken")
        out_file_path_lable_2.place(x=140,y=194)
        k4=ttk.Button(music_separation_interface,text="分离可视化",bootstyle=(INFO, OUTLINE),command=lambda:[Separation.separation_plot.show_audio_separation_results(file_1=speechsepararionmusic_filepath_0,file_2=speechsepararionmusic_filepath_1)])
        k4.place(x=50,y=235)

        music_separation_interface.protocol('WM_DELETE_WINDOW',return_to_options_interface)
    
    #语音与语音分离
    def voice_separation_interface(self):
        voice_separation_interface=tk.Tk()
        voice_separation_interface.geometry("500x300")
        voice_separation_interface.resizable(0, 0)
        voice_separation_interface.configure(bg=self.global_bg_color)
        voice_separation_interface.title("语音与语音分离")
        voice_separation_interface.iconbitmap(default=icon_path)

        def return_to_options_interface():
            voice_separation_interface.destroy()
            self.voice_musicoptions_interface()
        
        def choose_file_speechsepararionvoice(index):
            global speechsepararionvoice_filepath_0
            global speechsepararionvoice_filepath_1
            if index == 0:
                speechsepararionvoice_filepath_0 = tkinter.filedialog.askopenfilename()
                file_path_lable_0.config(state="normal")
                file_path_lable_0.delete(0, tk.END)
                file_path_lable_0.insert(0, speechsepararionvoice_filepath_0)
                file_path_lable_0.config(state="readonly")
            elif index == 1:
                speechsepararionvoice_filepath_1 = tkinter.filedialog.askopenfilename()
                file_path_lable_1.config(state="normal")
                file_path_lable_1.delete(0, tk.END)
                file_path_lable_1.insert(0, speechsepararionvoice_filepath_1)
                file_path_lable_1.config(state="readonly")

        def out_file_speechsepararionvoice(index):
            if index == 0:
                time.sleep(2)
                out_file_path_lable_0.config(state="normal")
                out_file_path_lable_0.delete(0, tk.END)
                desktop_path = os.path.expanduser('~') + '\\Desktop\\'
                filename_mixed = 'mixed.wav'
                outpath_mixed = desktop_path + filename_mixed
                out_file_path_lable_0.insert(0, outpath_mixed)
                out_file_path_lable_0.config(state="readonly")
            elif index == 1:
                time.sleep(1)
                out_file_path_lable_1.config(state="normal")
                out_file_path_lable_1.delete(0, tk.END)
                desktop_path = os.path.expanduser('~') + '\\Desktop\\'
                filename_recovered_1 = 'recovered_1.wav'
                outpath_recovered_1 = desktop_path + filename_recovered_1
                out_file_path_lable_1.insert(0, outpath_recovered_1)
                out_file_path_lable_1.config(state="readonly")
            elif index == 2:
                time.sleep(1)
                out_file_path_lable_2.config(state="normal")
                out_file_path_lable_2.delete(0, tk.END)
                desktop_path = os.path.expanduser('~') + '\\Desktop\\'
                filename_recovered_2 = 'recovered_2.wav'
                outpath_recovered_2 = desktop_path + filename_recovered_2
                out_file_path_lable_2.insert(0, outpath_recovered_2)
                out_file_path_lable_2.config(state="readonly")
            

        k0=ttk.Button(voice_separation_interface,text="音频 1",bootstyle=(INFO, OUTLINE),command=lambda:[choose_file_speechsepararionvoice(0)])
        k0.place(x=50,y=20)
        file_path_lable_0=tk.Entry(voice_separation_interface, text="", bg='white',  width=30, relief="sunken")
        file_path_lable_0.place(x=140,y=24)
        k1=ttk.Button(voice_separation_interface,text="音频 2",bootstyle=(INFO, OUTLINE),command=lambda:[choose_file_speechsepararionvoice(1)])
        k1.place(x=50,y=55)
        file_path_lable_1=tk.Entry(voice_separation_interface, text="", bg='white',  width=30, relief="sunken")
        file_path_lable_1.place(x=140,y=59)
        k2=ttk.Button(voice_separation_interface,text="混合音频",bootstyle=(INFO, OUTLINE),command=lambda:[Separation.merge.merge_files(file_1=speechsepararionvoice_filepath_0,file_2=speechsepararionvoice_filepath_1),out_file_speechsepararionvoice(0)])
        k2.place(x=50,y=120)
        out_file_path_lable_0=tk.Entry(voice_separation_interface, text="", bg='white',  width=30, relief="sunken")
        out_file_path_lable_0.place(x=140,y=124)
        k3=ttk.Button(voice_separation_interface,text="分离音频",bootstyle=(INFO, OUTLINE),command=lambda:[Separation.separation.audio_separation(file_1=speechsepararionvoice_filepath_0,file_2=speechsepararionvoice_filepath_1),out_file_speechsepararionvoice(1),out_file_speechsepararionvoice(2)])
        k3.place(x=50,y=160)
        out_file_path_lable_1=tk.Entry(voice_separation_interface, text="", bg='white',  width=30, relief="sunken")
        out_file_path_lable_1.place(x=140,y=164)
        out_file_path_lable_2=tk.Entry(voice_separation_interface, text="", bg='white',  width=30, relief="sunken")
        out_file_path_lable_2.place(x=140,y=194)
        k4=ttk.Button(voice_separation_interface,text="分离可视化",bootstyle=(INFO, OUTLINE),command=lambda:[Separation.separation_plot.show_audio_separation_results(file_1=speechsepararionvoice_filepath_0,file_2=speechsepararionvoice_filepath_1)])
        k4.place(x=50,y=235)

        
        voice_separation_interface.protocol('WM_DELETE_WINDOW',return_to_options_interface)

    #语音分离选择界面
    def voice_musicoptions_interface(self):
        voice_musicoptions_interface=tk.Tk()
        voice_musicoptions_interface.geometry("300x100")
        voice_musicoptions_interface.configure(bg="white")
        voice_musicoptions_interface.resizable(0, 0)
        voice_musicoptions_interface.title("分离")
        voice_musicoptions_interface.iconbitmap(default=icon_path)

        g0=ttk.Button(voice_musicoptions_interface,text="语音与语音分离", bootstyle=(INFO, OUTLINE),command=lambda:[voice_musicoptions_interface.withdraw(),self.voice_separation_interface()])
        g0.place(x=15,y=30)
        g1=ttk.Button(voice_musicoptions_interface,text="语音与音乐分离", bootstyle=(INFO, OUTLINE),command=lambda:[voice_musicoptions_interface.withdraw(),self.music_separation_interface()])
        g1.place(x=195,y=30)
        lable=tk.Label(voice_musicoptions_interface,text="or",bg="white")
        lable.place(x=145,y=33)

    #语音加噪界面
    def add_noise_interface(self):
        add_noise_interface=tk.Toplevel(self.root)
        add_noise_interface.geometry("400x200")
        add_noise_interface.configure(bg="white")
        add_noise_interface.resizable(0, 0)
        add_noise_interface.title("加噪")
        add_noise_interface.iconbitmap(default=icon_path)

        def return_to_add_denoiseoptions_interface():
            add_noise_interface.destroy()
            self.add_denoiseoptions_interface()


        def choose_file_addnoise(event):
            global addnoise_filepath
            addnoise_filepath = tkinter.filedialog.askopenfilename()
            h3.config(state="normal")
            h3.delete(0, tk.END)
            h3.insert(0, addnoise_filepath)
            h3.config(state="readonly")

        
        def save_and_add_noise():
            intensity = self.intensity.get()
            desktop_path = os.path.expanduser('~') + '\\Desktop\\'
            filename = 'noise_audio.wav'
            output_wav_loc = desktop_path + filename
            choose_wav_loc=addnoise_filepath
            Denoise.add_noise.save_noiseadd_file(choose_wav_loc,intensity)
            h7.delete(0,tk.END)
            time.sleep(2)
            h7.insert(0,output_wav_loc)

        h2=tk.Label(add_noise_interface,text="选择音频:",bg="white",font=("黑体",11))
        h2.place(x=60,y=10)
        h3=tk.Entry(add_noise_interface, text="", bg='white', width=21, relief="sunken")
        h3.place(x=160,y=10)
        h4=tk.Label(add_noise_interface,text="噪声强度:",bg="white",font=("黑体",11))
        h4.place(x=60,y=50)
        h5=tk.Spinbox(add_noise_interface,from_=1,to=10,increment=1,width=20,bg="white",textvariable=self.intensity)
        h5.place(x=160,y=50)
        h6=tk.Label(add_noise_interface,text="保存路径:",bg="white",font=("黑体",11))
        h6.place(x=60,y=90)
        h7=tk.Entry(add_noise_interface, text="", bg='white', width=21, relief="sunken")
        h7.place(x=160,y=90)
        h8=ttk.Button(add_noise_interface,text="确认",bootstyle=(INFO, OUTLINE),command=lambda:[save_and_add_noise()])
        h8.place(x=50,y=150)
        h9=ttk.Button(add_noise_interface,text="返回",bootstyle=(INFO, OUTLINE),command=lambda:[return_to_add_denoiseoptions_interface()])
        h9.place(x=320,y=150) 
        add_noise_interface.protocol('WM_DELETE_WINDOW',return_to_add_denoiseoptions_interface)   

        h2.bind("<Button-1>",choose_file_addnoise)

    #语音降噪界面
    def speechDenoise_interface(self):
        noise_reduction_window = tk.Tk()
        noise_reduction_window.geometry("600x400")
        noise_reduction_window.resizable(0, 0)
        noise_reduction_window.configure(bg=self.global_bg_color)
        noise_reduction_window.title("数字音效处理器——语音降噪")
        noise_reduction_window.iconbitmap(default=icon_path)

        def return_to_add_denoiseoptions_interface():
            noise_reduction_window.destroy()
            self.add_denoiseoptions_interface()

        def choose_file_speechdenoise():
            global reducenoise_filepath
            reducenoise_filepath = tkinter.filedialog.askopenfilename()
            file_path_label.config(state="normal")
            file_path_label.delete(0,tk.END)
            file_path_label.insert(0,reducenoise_filepath)
            file_path_label.config(state="readonly")
            # 调用audio_information函数并显示结果
            duration, sample_rate, sample_width, channels = self.audio_information(reducenoise_filepath)
            result_label.config(text=f"时长：{duration:.2f} 秒\n 采样频率：{sample_rate} Hz\n 采样位数：{sample_width} 位\n通道数：{channels} 通道")

        def out_file_speechdenoise():
            global outputdenoise_filepath
            desktop_path = os.path.expanduser('~') + '\\Desktop\\'
            filename = 'denoised_audio.wav'
            outputdenoise_filepath = desktop_path + filename
            save_path_label.delete(0,tk.END)
            time.sleep(2)
            save_path_label.insert(0,outputdenoise_filepath)


        c0 = ttk.Button(noise_reduction_window, text="语音输入", width=15, bootstyle=(INFO, OUTLINE))
        c0.place(x=20, y=40)
        choose_file_button = ttk.Button(noise_reduction_window, text="📁",  bootstyle=(INFO, OUTLINE), command=choose_file_speechdenoise)
        choose_file_button.place(x=360, y=40)
        file_path_label = tk.Entry(noise_reduction_window, text="", bg='white',  width=30, relief="sunken")
        file_path_label.place(x=140, y=43)
        c1 = ttk.Button(noise_reduction_window, text="音频可视化", width=15, bootstyle=(INFO, OUTLINE),command=lambda:[audio_plot.plot_waveforms(reducenoise_filepath)])
        c1.place(x=20, y=90)
        c2 = ttk.Button(noise_reduction_window, text="▶",  width=2, bootstyle=(INFO, OUTLINE),command=lambda:[audio_play.audio_play(reducenoise_filepath)])
        c2.place(x=480, y=40)
        c4 = ttk.Button(noise_reduction_window, text="降噪", width=15, bootstyle=(INFO, OUTLINE),command=lambda:[Denoise.denoise.denoise(reducenoise_filepath),out_file_speechdenoise()])
        c4.place(x=20, y=170)
        c5 = ttk.Button(noise_reduction_window, text="降噪可视化", width=15, bootstyle=(INFO, OUTLINE),command=lambda:[Denoise.noise_plot.denoise_plot()])
        c5.place(x=20, y=260)
        c6 = ttk.Button(noise_reduction_window, text="保存目录", width=15, bootstyle=(INFO, OUTLINE))
        c6.place(x=20, y=310)
        save_path_label = tk.Entry(noise_reduction_window, text="", bg='white',  width=30, relief="sunken")
        save_path_label.place(x=140, y=315)
        c7 = ttk.Button(noise_reduction_window, text="▶",  width=2, bootstyle=(INFO, OUTLINE),command=lambda:[audio_play.audio_play(outputdenoise_filepath)])
        c7.place(x=480, y=310)
        

        result_label = tk.Label(noise_reduction_window, text="", bg='white', width=20, height=5, relief="sunken", anchor="w")
        result_label.place(x=400, y=140)

        noise_reduction_window.protocol('WM_DELETE_WINDOW',return_to_add_denoiseoptions_interface)   

    #语音降噪选择界面
    def add_denoiseoptions_interface(self):
        add_denoiseoptions_interface=tk.Tk()
        add_denoiseoptions_interface.geometry("300x100")
        add_denoiseoptions_interface.configure(bg="white")
        add_denoiseoptions_interface.resizable(0, 0)
        add_denoiseoptions_interface.title("分离")
        add_denoiseoptions_interface.iconbitmap(default=icon_path)

        g0=ttk.Button(add_denoiseoptions_interface,text="加噪", bootstyle=(INFO, OUTLINE),command=lambda:[add_denoiseoptions_interface.withdraw(),self.add_noise_interface()])
        g0.place(x=15,y=30)
        g1=ttk.Button(add_denoiseoptions_interface,text="降噪", bootstyle=(INFO, OUTLINE),command=lambda:[add_denoiseoptions_interface.withdraw(),self.speechDenoise_interface()])
        g1.place(x=195,y=30)
        lable=tk.Label(add_denoiseoptions_interface,text="or",bg="white")
        lable.place(x=140,y=33)

    #功能选择界面
    def secondary_interface(self):
        secondary_window = tk.Toplevel(self.root)
        secondary_window.geometry("600x400")
        secondary_window.resizable(0, 0)
        secondary_window.configure(bg=self.global_bg_color)
        secondary_window.iconbitmap(default=icon_path)
        secondary_window.title("数字音效处理器")

        def return_to_primary_interface():
            secondary_window.destroy()
            self.root.deiconify()

        global logo_image
        logo_image = None
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "icon", "logo.png")
        if logo_image is None:
            logo_image = tk.PhotoImage(file=image_path)

        b0=ttk.Button(secondary_window, width=15, text="语音录制",bootstyle=(INFO, OUTLINE),command=lambda:[audio_record.recording_interface()])
        b0.place(x=100,y=90)
        b1 = ttk.Button(secondary_window, width=15, text="语音降噪", bootstyle=(INFO, OUTLINE),command=lambda: [self.add_denoiseoptions_interface()])
        b1.place(x=100, y=140)
        b2 = ttk.Button(secondary_window, width=15, text="语音分离", bootstyle=(INFO, OUTLINE),command=lambda:[self.voice_musicoptions_interface()])
        b2.place(x=100,y=190)
        b4 = ttk.Button(secondary_window, width=15, text="语音识别", bootstyle=(INFO, OUTLINE),command=lambda:[self.content_characteropintions_interface()])
        b4.place(x=100, y=240)
        b6 = ttk.Label(secondary_window, image=logo_image)
        b6.place(x=300, y=45)

        secondary_window.protocol('WM_DELETE_WINDOW',return_to_primary_interface) 

    #主界面界面
    def primary_interface(self):
        #Style()
        #Style(theme='journal')

        self.root.geometry("600x400")
        self.root.resizable(0, 0)
        self.root.configure(bg=self.global_bg_color)
        self.root.title("数字音效处理器")
        self.root.iconbitmap(default=icon_path)
        self.labels = []

        def change_background_color(event):
            self.change_background_color()
            for label in self.labels:
                label.config(bg=self.global_bg_color)
        
        def open_local_html(event):
            webbrowser.open("Description\\description.html")

        def open_bug_submission_interface(event):
            self.bug_submission_interface()

        self.root.bind("<Button-3>", change_background_color)

        a0 = tk.Label(self.root, text="Digital Signal Processing", font=("Courier", 20), fg="blue", bg="white")
        a0.pack()
        self.labels.append(a0)
        a1 = ttk.Button(self.root, text="开始", bootstyle=(INFO, OUTLINE),command=lambda: [self.root.withdraw(), self.secondary_interface()])
        a1.pack(fill="x", padx=240, pady=(200, 20))
        a2 = ttk.Button(self.root, text="退出", bootstyle=(INFO, OUTLINE),command=self.root.quit)
        a2.pack(fill="x", padx=240)

        a3=tk.Label(self.root,text="Copyright ShanghaiUniversity ALL Right Reserved---bug submission",bg="white")
        a3.pack(side="bottom")
        self.labels.append(a3)
        a3.bind("<Button-1>",open_bug_submission_interface)
        a4= tk.Label(self.root, text="Read Me",bg="white")
        a4.pack(side="bottom")
        self.labels.append(a4)
        a4.bind("<Button-1>", open_local_html)


def run():
    root = tk.Tk()
    manager = WindowManager(root) 
    manager.primary_interface()
    root.mainloop()


