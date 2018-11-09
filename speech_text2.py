from watson_developer_cloud import SpeechToTextV1
import sys,os.path
import json

def text_json(out_f="out1.mp3",lang_k="ja-JP_BroadbandModel"):
    user='ユーザー名'
    pswd='パスワード'
    audio_file = open(out_f, "rb")
    ext = os.path.splitext(out_f)[1][1:]
    cont_type = "audio/" + ext
    print (cont_type)
    lang = lang_k
    # ワトソンとの送信と受信
    stt = SpeechToTextV1(username=user, password=pswd)
    result_json = stt.recognize(
            audio=audio_file,
            content_type=cont_type,
            model=lang).get_result()
    # ファイルの保存
    with open("result.json","w") as f:
        json.dump(result_json,f,ensure_ascii=False,indent=2)
