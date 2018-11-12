import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.filedialog as flog
import sys,os.path
import subprocess
import wave
import speech_text2
import json
import textwrap

class Application(tk.Frame):
    def __init__(self, master=None,file_name='out.wav'):
        super().__init__(master)
        self.grid()
        self.create_widgets()
        self.master.title(u"Speech to Text アプリ")
        self.master.geometry("640x512")
        self.master.configure(background = '#ccffcc')
        self.cmd = ""
        self.file_na = file_name
        self.p = None
        self.rec_flag = False
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.result = {}
        self.result_json = {}
        self.lang_k = ""
        self.v = ('ja-JP_BroadbandModel',
            'en-US_BroadbandModel',
            'en-GB_BroadbandModel',
            'fr-FR_BroadbandModel',
            'es-ES_BroadbandModel',
            'de-DE_BroadbandModel',
            'zh-CN_BroadbandModel',
            'ko-KR_BroadbandModel',
            )
        self.rec_time = 0    

    def create_widgets(self):
        #メニューバー
        self.menbar = tk.Menu(self.master)
        self.master.configure(menu = self.menbar)
        self.files = tk.Menu(self.menbar,tearoff = False)
        self.menbar.add_cascade(label=u"ファイル",underline=0,menu=self.files)
        self.files.add_command(label =u"テキスト保存",under = 0,command = self.data_save)
        self.files.add_command(label =u"保存先変更",under = 0,command = self.button_clickfc)
        self.files.add_command(label =u"ファイル再生",under = 0,command = self.button_clickplay)
        self.files.add_separator()
        self.files.add_command(label =u"プログラム終了",under = 0,command = self.on_closing)
        self.level = tk.IntVar()
        self.level.set(0)
        self.langs = tk.Menu(self.menbar,tearoff = False)
        self.menbar.add_cascade(label=u"言語選択",underline=0,menu=self.langs)
        self.langs.add_radiobutton(label =u'日本語', variable = self.level, value = 0, command = self.lang_change)
        self.langs.add_radiobutton(label =u'英語（米語）', variable = self.level, value = 1, command = self.lang_change)
        self.langs.add_radiobutton(label =u'英語', variable = self.level, value = 2, command = self.lang_change)
        self.langs.add_radiobutton(label =u'フランス語', variable = self.level, value = 3, command = self.lang_change)
        self.langs.add_radiobutton(label =u'スペイン語', variable = self.level, value = 4, command = self.lang_change)
        self.langs.add_radiobutton(label =u'ドイツ語', variable = self.level, value = 5, command = self.lang_change)
        self.langs.add_radiobutton(label =u'中国語', variable = self.level, value = 6, command = self.lang_change)
        self.langs.add_radiobutton(label =u'韓国語', variable = self.level, value = 7, command = self.lang_change)
        #録音開始ボタン
        self.Button1 = tk.Button(text=u'録音開始ボタン',width=20,command=self.button_clickrec)
        self.Button1.grid(row=0,column=0,pady=20)
        #録音停止ボタン
        self.Button2 = tk.Button(text=u'録音停止ボタン',width=20,command=self.button_clickstop)
        self.Button2.grid(row=0,column=1,pady=5)
        #スクロールテキスト
        self.Scrolltext1 = st.ScrolledText()
        self.Scrolltext1.grid(row=2,columnspan=2,padx=20,pady=20)
        #ラベル
        self.Label1 = tk.Label(text='ja-JP_BroadbandModel')
        self.Label1.grid(row=3,column=0,pady=10)
        #テキスト出力ボタン
        self.Button5 = tk.Button(text=u'Speech to Text',width=20,command=self.button_clicktx)
        self.Button5.grid(row=3,column=1,pady=10)

    #言語選択
    def lang_change(self):
        self.cmd = self.level.get()
        self.lang_k = self.v[self.cmd]
        self.Label1["text"] = self.lang_k

    #録音開始
    def button_clickrec(self):
        if self.rec_flag == False:
            self.Button1.configure(text=u'録音中',foreground ='#ff0000')
            self.cmd = "sox -t waveaudio -d "+ self.file_na
            self.p = subprocess.Popen(self.cmd.split())
            self.Scrolltext1.insert('end',u'録音しています　ファイル名：' + self.file_na + '\n')
            self.rec_flag = True
            self.timer()

    #録音停止
    def button_clickstop(self):
        if self.rec_flag == True:
            self.master.after_cancel(self.timer)
            self.Scrolltext1.insert('end','録音時間　{:0>2}:{:0>2}:{:0>2}'.format(self.rec_time//3600,self.rec_time//60,self.rec_time%60) + '\n')
            self.time = 0
            self.lang_change()
            self.p.terminate()
            self.Scrolltext1.insert('end',u'録音を終了しました\n')
            self.Button1.configure(text=u'録音開始ボタン',foreground ='#000000')
            try:
                self.p.wait(timeout=1)
                self.rec_flag = False
            except subprocess.TimeoutExpired:
                self.p.kill()
                self.rec_flag = False

    #タイマー
    def timer(self):
        if self.rec_flag == True:
            self.master.after(1000,self.timer)
            self.rec_time += 1
            self.Label1["text"] = '録音中　{:0>2}:{:0>2}:{:0>2}'.format(self.rec_time//3600,self.rec_time//60,self.rec_time%60)

    #再生
    def button_clickplay(self):
        if self.rec_flag == False:
            self.cmd = self.file_na + '\n'
            self.p = subprocess.call(self.cmd,shell=True)
            self.Scrolltext1.insert('end',u'再生を実行中。ファイル名：' + self.cmd + '\n')

    #出力ファイル名変更
    def button_clickfc(self):
        self.file_type = [('Wav Files', '.wav'), 
            ('MP3 files','.mp3'),
            ('Flac Files','.Flac')]
        self.file_save = flog.asksaveasfilename(filetypes = self.file_type)
        if self.file_save != '':
            self.file_na = self.file_save
            self.Scrolltext1.insert('end',u'出力ファイル名変更：' + self.file_na + '\n')

    #録音中に終了したときの処理
    def on_closing(self):
        self.button_clickstop()
        sys.exit()

    #テキスト変換処理
    def button_clicktx(self):
        self.cmd = self.level.get()
        self.lang_k = self.v[self.cmd]
        speech_text2.text_json(self.file_na,self.lang_k)
        with open("result.json","r") as f:
            self.result_json = json.load(f)
        self.Scrolltext1.delete('1.0', 'end')
        for i in range(len(self.result_json["results"])):
            self.cmd = self.result_json["results"][i]["alternatives"][0]["transcript"]
            if self.lang_k == "ja-JP_BroadbandModel":
                self.cmd = self.cmd.replace(' ','')
                self.cmd = textwrap.fill(self.cmd,40)
            if self.lang_k == "en-US_BroadbandModel":
                self.cmd = self.cmd.replace('%HESITATION ','')
                self.cmd = textwrap.fill(self.cmd,80)
            self.Scrolltext1.insert('end',self.cmd + '\n')

    #ファイル保存
    def data_save(self):
        self.file_type = [('Text Files', '.txt'),
            ('Dat Files','.dat'),
            ('Doc Files','.doc')]
        self.file_save = flog.asksaveasfilename(filetypes = self.file_type)
        if self.file_na != '':
            self.cmd = self.Scrolltext1.get('1.0','end')
            with open(self.file_save,mode='w',encoding='utf-8') as f:
                f.write(self.cmd)
                self.Scrolltext1.insert('end',u'ファイルに保存しました：' + self.file_save + '\n')

#本体
if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root,file_name='out1.mp3')
    app.mainloop()