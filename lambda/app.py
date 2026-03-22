import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
import json
import urllib.request
import urllib.parse
import boto3
import os
from datetime import datetime

API_KEY = os.environ["YOUTUBE_API_KEY"]

BASE_URL = "https://www.googleapis.com/youtube/v3"
BUCKET_NAME = "data-raw-youtube-061039776564-us-east-1-an"

s3 = boto3.client("s3")


def http_get(url, params):
    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"

    with urllib.request.urlopen(full_url) as response:
        return json.loads(response.read())


def buscar_videos(query, max_results=5):

    url = f"{BASE_URL}/search"

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": API_KEY
    }

    data = http_get(url, params)

    videos = []

    for item in data.get("items", []):
        videos.append({
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"]
        })

    return videos


def pegar_estatisticas(video_id):

    url = f"{BASE_URL}/videos"

    params = {
        "part": "statistics",
        "id": video_id,
        "key": API_KEY
    }

    data = http_get(url, params)

    stats = data["items"][0]["statistics"]

    return {
        "views": stats.get("viewCount"),
        "likes": stats.get("likeCount"),
        "comments": stats.get("commentCount")
    }


def pegar_comentarios(video_id, max_results=5):

    url = f"{BASE_URL}/commentThreads"

    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": max_results,
        "textFormat": "plainText",
        "key": API_KEY
    }

    data = http_get(url, params)

    comentarios = []

    for item in data.get("items", []):
        snippet = item["snippet"]["topLevelComment"]["snippet"]

        comentarios.append({
            "autor": snippet["authorDisplayName"],
            "texto": snippet["textDisplay"]
        })

    return comentarios


def lambda_handler(event, context):

    marca = "Itau"

    print(f"Buscando vídeos sobre {marca}")

    videos = buscar_videos(marca)

    resultado_final = []

    for video in videos:

        video_id = video["video_id"]

        stats = pegar_estatisticas(video_id)

        comentarios = pegar_comentarios(video_id)

        resultado_final.append({
            "video": video,
            "estatisticas": stats,
            "comentarios": comentarios
        })

    data_hoje = datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")

    file_name = f"youtube-data/itau-{data_hoje}.json"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=json.dumps(resultado_final, ensure_ascii=False),
        ContentType="application/json"
    )

 

    print("Arquivo salvo no S3:", file_name)

    return {
        "statusCode": 200,
        "body": json.dumps("Dados coletados com sucesso!")
    }