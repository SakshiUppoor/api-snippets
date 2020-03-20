from datetime import datetime, timedelta
import hashlib
import requests
import time
from .credentials import api_key, api_secret


def make_request(contestId):
    base_url = "https://codeforces.com/api/"
    method = "contest.standings"

    # UNIX Timestamp
    time_str = str(int(time.time()))

    # Genrating Hash
    hash_str = "123456/" + method + "?apiKey=" + api_key + \
        "&contestId=" + contestId + "&time=" + time_str + "#" + api_secret
    result = hashlib.sha512(hash_str.encode())
    hash = result.hexdigest()

    # Making Request
    url = base_url + method + "/?contestId=" + \
        contestId + "&apiKey=" + api_key + "&time=" + time_str + "&apiSig=123456" + hash

    return requests.get(url).json()


def get_standing(handle, contestId):
    response = make_request(contestId)
    rows = response["result"]["rows"]
    for row in rows:
        for h in row["party"]["members"]:
            if h["handle"] == handle:
                return row
