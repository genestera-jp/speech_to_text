import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.filedialog as flog
import sys,os.path
import subprocess
import wave
import speech_text2
import json

class Application(tk.Frame):
    def __init__(self, master=None,file_name='out.wav'):
        super().__init__(master)
        self.grid()
        self.create_widgets()
        master.title(u"Speech to Text アプリ")
        master.geometry("640x512")
        self.cmd = ""
        self.file_na = file_name
        self.p = None
        self.rec_flag = False
        master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.result = {}
        self.result_json = {}

    def create_widgets(self):
        #録音開始ボタン
        self.Button1 = tk.Button(text=u'録音開始ボタン',width=20,command=self.button_clickrec)
        self.Button1.grid(row=0,column=0,pady=20)
        #録音停止ボタン
        self.Button2 = tk.Button(text=u'録音停止ボタン',width=20,command=self.button_clickstop)
        self.Button2.grid(row=0,column=1,pady=5)
        #再生ボタン
        self.Button3 = tk.Button(text=u'再生ボタン',width=20,command=self.button_clickplay)
        self.Button3.grid(row=1,column=0,pady=5)
        #出力ファイル変更ボタン
        self.Button4 = tk.Button(text=u'出力ファイルの変更',width=20,command=self.button_clickfc)
        self.Button4.grid(row=1,column=1,pady=5)
        #スクロールテキスト
        self.Scrolltext1 = st.ScrolledText()
        self.Scrolltext1.grid(row=2,columnspan=2,padx=20,pady=20)
        #言語選択スピンボックスボタン
        self.v = ('ja-JP_BroadbandModel','en-US_BroadbandModel','en-GB_BroadbandModel')
        self.SpinBox1 = tk.Spinbox(value = self.v,width = 25,state = 'readonly')
        self.SpinBox1.grid(row=3,column=0,pady=10)
        #テキスト出力ボタン
        self.Button5 = tk.Button(text=u'テキスト出力',width=20,command=self.button_clicktx)
        self.Button5.grid(row=3,column=1,pady=10)

    #録音開始
    def button_clickrec(self):
        if self.rec_flag == False:
            self.cmd = "sox -t waveaudio -d "+ self.file_na
            self.p = subprocess.Popen(self.cmd.split())
            self.Scrolltext1.insert('end',u'録音を開始しました\n')
            self.rec_flag = True

    #録音停止
    def button_clickstop(self):
        if self.rec_flag == True:
            self.p.terminate()
            self.Scrolltext1.insert('end',u'録音を終了しました\n')
            try:
                self.p.wait(timeout=1)
                self.rec_flag = False
            except subprocess.TimeoutExpired:
                self.p.kill()
                self.rec_flag = False

    #再生
    def button_clickplay(self):
        if self.rec_flag == False:
            self.cmd = self.file_na + '\n'
            self.p = subprocess.call(self.cmd,shell=True)
            self.Scrolltext1.insert('end',u'再生を実行中。ファイル名：' + self.cmd)

    #出力ファイル名変更
    def button_clickfc(self):
        self.file_na = flog.asksaveasfilename()
        self.Scrolltext1.insert('end',u'出力ファイル名変更：' + self.file_na + '\n')

    #録音中に終了したときの処理
    def on_closing(self):
        self.button_clickstop()
        sys.exit()

    #テキスト変換処理
    def button_clicktx(self):
        lang_k = self.SpinBox1.get()
        speech_text2.text_json(self.file_na,lang_k)
        self.Scrolltext1.delete('1.0', 'end')
        with open("result.json","r") as f:
            self.result_json = json.load(f)
        for i in range(len(self.result_json["results"])):
            self.cmd = self.result_json["results"][i]["alternatives"][0]["transcript"]
            if lang_k == "ja-JP_BroadbandModel":
                self.cmd = self.cmd.replace(' ','')
            if lang_k == "en-US_BroadbandModel":
                self.cmd = self.cmd.replace('%HESITATION ','')
            self.Scrolltext1.insert('end',self.cmd + '\n')

#本体
if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root,file_name='out1.wav')
    app.mainloop()