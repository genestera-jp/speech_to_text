# Speech to Textプログラム  
Sox(Sound exchange)を使ってパソコンの音を録音し保存します。  
そのファイルを使ってIBMのWatsonによりテキストに変換します。  

## 環境  
SoX(Sound exchange)がインストールされていること  
IBMクラウドのspeech to textのID、パスワードを取得していること  

## 使い方  
speech_textmain_v1.pyを実行します。  
なお、speech_text2.pyは同じフォルダ（階層）に入れてください。  
また、speech_text2の  
user='ユーザー名'  
pswd='パスワード'  
を自分のものに変えてください。  
  
仕様：  
録音開始ボタンで録音開始します。  
録音停止ボタンで録音を終了します。  
Speech to Textボタンでテキストに変換します。  
ファイルメニューのテキスト保存でテキストを保存します。  
ファイルメニューの保存先変更でファイルの保存先を変更します。  
ファイルメニューの再生で録音したものを再生します。  
ファイルメニューの終了でプログラムを終了します。  
言語選択メニューでテキスト変換する言語を指定します。  
  
  
## 関連情報  
1. [音声を録音してみる](http://blog1.tela.daa.jp/?eid=142/ "孤独なコンピュータ")　　


