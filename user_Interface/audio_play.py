import wave
import pyaudio
import tkinter as tk
import time

class AudioPlayer:
    def audioPlayer_interface(self, file_path):
        self.window = tk.Tk()
        self.window.title("播放")
        self.window.geometry("200x100")
        self.window.resizable(0, 0)
        self.window.configure(bg="white")
        self.window.iconbitmap("user_Interface\\icon\\001.ico")

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.playing = False
        self.current_frame = 0
        self.start_time = None  # 用于记录播放开始的时间

        self.wave_file = wave.open(file_path, 'rb')
        self.play_button = tk.Button(self.window, text="▶", height=1, width=2, activebackground='blue', command=self.toggle_play)
        self.play_button.place(x=60, y=10)
        self.stop_button = tk.Button(self.window, text="⏺", height=1, activebackground='blue', command=self.stop_play)
        self.stop_button.place(x=120, y=10)

        self.time_label = tk.Label(self.window, text="00:00", bg="white")
        self.time_label.place(x=82, y=60)
        self.window.mainloop()

    def toggle_play(self):
        if not self.playing:
            if not self.stream:
                self.stream = self.audio.open(
                    format=self.audio.get_format_from_width(self.wave_file.getsampwidth()),
                    channels=self.wave_file.getnchannels(),
                    rate=self.wave_file.getframerate(),
                    output=True
                )
                if self.current_frame == self.wave_file.getnframes():
                    # 如果当前帧数等于音频总帧数，说明音频已经播放完，重新开始计数
                    self.current_frame = 0
                    self.start_time = time.time()
                else:
                    # 如果没有播放完，从当前位置开始播放
                    self.start_time = time.time() - (self.current_frame / self.wave_file.getframerate())
                self.playing = True
                self.play_button.config(text="❚❚")
                self.play_audio()
        else:
            self.playing = False
            self.play_button.config(text="▶")
            self.pause_audio()

    def play_audio(self):
        if self.stream and self.playing:
            self.wave_file.setpos(self.current_frame)
            data = self.wave_file.readframes(1024)
            if data:
                self.stream.write(data)
                self.current_frame += 1024
                elapsed_time = time.time() - self.start_time  # 计算已经播放的时间
                self.update_time(elapsed_time)
                self.window.after(10, self.play_audio)
            else:
                self.stop_play()

    def pause_audio(self):
        if self.stream and self.playing:
            self.stream.stop_stream()

    def stop_play(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.playing = False
        self.play_button.config(text="▶")

    def update_time(self, elapsed_time):
        seconds = int(elapsed_time)
        milliseconds = int((elapsed_time - seconds) * 1000)
        time_str = f"{seconds:02}.{milliseconds:03}"
        self.time_label.config(text=time_str)

def audio_play(file_path):
    audio_player = AudioPlayer()
    audio_player.audioPlayer_interface(file_path=file_path)

