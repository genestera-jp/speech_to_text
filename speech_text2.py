from watson_developer_cloud import SpeechToTextV1
import json

def text_json(out_f="out1.wav",lang_k="ja-JP_BroadbandModel"):
    user='ユーザー名'
    pswd='パスワード'
    audio_file = open(out_f, "rb")
    cont_type = "audio/wav"
    lang = lang_k
    # ワトソンとの送信と受信
    stt = SpeechToTextV1(username=user, password=pswd)
    result_json = stt.recognize(audio=audio_file, content_type=cont_type, model=lang)
    # ファイルの保存
    with open("result.json","w") as f:
        json.dump(result_json,f,ensure_ascii=False,indent=2)
