import os
import wave
import tkinter
import pyaudio

def recording_function():#录音函数
    #获取录音时长
    duration=int(duration_var.get())
    #定义录音参数
    CHUNK=1024                          #每个缓存区的大小
    FORMAT=pyaudio.paInt16              #采样位数
    CHANNELS=1                          #单声道
    RATE=44100                          #采样率
    RECORD_SECONDS=duration             #录音时长
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    WAVE_OUTPUT_FILEMAME = os.path.join(desktop_path, "output.wav")   #输出文件
    #创建一个对象
    audio=pyaudio.PyAudio()

    #打开音频流
    stream=audio.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    #创建一个空列表用于储存录音数据
    frames=[]

    #录音
    for i in range(0,int(RATE/CHUNK*(RECORD_SECONDS+1))):
        data=stream.read(CHUNK)
        frames.append(data)

    #关闭音频流
    stream.stop_stream()
    stream.close()
    audio.terminate()

    #将录音数据保存为wav文件
    wave_file=wave.open(WAVE_OUTPUT_FILEMAME,'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

    #显示文件保存路径
    filepath_var.set(os.path.abspath(WAVE_OUTPUT_FILEMAME))


def recording_interface():
    window=tkinter.Toplevel()
    window['background']='white'
    window.title("录音程序")
    window.geometry("400x200")
    window.resizable(0,0)

    #添加录音时长输入框
    global duration_var
    duration_var=tkinter.StringVar(value="5")
    I0=tkinter.Button(window,text='录音时长设置')
    I0.place(x=50,y=20)
    I1=tkinter.Entry(window,textvariable=duration_var,justify='center')
    I1.place(x=150,y=24)

    #添加开始录音按钮
    I2=tkinter.Button(window,text="开始录音",command=recording_function,activebackground='blue')
    I2.place(x=50,y=70)
    I3=tkinter.Button(window,text="文件保存目录")
    I3.place(x=50,y=120)

    #添加文件保存路径标签
    global filepath_var
    filepath_var=tkinter.StringVar(value="")
    I4=tkinter.Entry(window,textvariable=filepath_var)
    I4.place(x=150,y=124)


    window.mainloop()
