import os
import json
import requests
import base64

def call_refresh_api(refreshtoken: str):
    """
    idTokenをリフレッシュするメソッド。

    Parameters
    ----------
    refreshtoken : str
        refreshtoken。ログイン後の画面からご確認いただけます。

    Returns
    -------
    resjson : dict
        新しいidtokenが格納されたAPIレスポンス(json形式)
    """
    headers = {"accept": "application/json"}
    data = {"refresh-token": refreshtoken}

    response = requests.post(
        "https://api.jpx-jquants.com/refresh", headers=headers, data=json.dumps(data)
    )

    resjson = json.loads(response.text)
    return resjson

def call_jquants_api(params: dict, idtoken: str, apitype: str, code: str = None):
    """
    J-QuantsのAPIを試すメソッド。

    Parameters
    ----------
    params : dict
        リクエストパラメータ。
    idtoken : str
        idTokenはログイン後の画面からご確認いただけます。
    apitype: str
        APIの種類。"news", "prices", "lists"などがあります。
    code: str
        銘柄を指定するAPIの場合に設定します。

    Returns
    -------
    resjson : dict
        APIレスポンス(json形式)
    """
    datefrom = params.get("datefrom", None)
    dateto = params.get("dateto", None)
    date = params.get("date", None)
    includedetails = params.get("includedetails", "false")
    keyword = params.get("keyword", None)
    headline = params.get("headline", None)
    paramcode = params.get("code", None)
    nexttoken = params.get("nextToken", None)
    scrollid = params.get("scrollId", None)
    headers = {"accept": "application/json", "Authorization": idtoken}
    data = {
        "from": datefrom,
        "to": dateto,
        "includeDetails": includedetails,
        "nextToken": nexttoken,
        "date": date,
        "keyword": keyword,
        "headline": headline,
        "code": paramcode,
        "scrollId": scrollid,
    }

    if code:
        code = "/" + code
        r = requests.get(
            "https://api.jpx-jquants.com/" + apitype + code,
            params=data,
            headers=headers,
        )
    else:
        r = requests.get(
            "https://api.jpx-jquants.com/" + apitype, params=data, headers=headers
        )
    resjson = json.loads(r.text)
    return resjson

