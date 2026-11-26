import os
import pprint
import requests 




def get_song(title, artist):
    try:
        url = "https://lrclib.net/api/search"
        
        parpams = {
            'track_name' : title,
            'artist_name' : artist
        }

        response = requests.get(url, params=parpams, timeout=10)

        if response.status_code != 200:
            print(f"요청 실패 (상태 코드: {response.status_code})")

        data = response.json()

        results = []
        

        for song in data:
            s = {
                "제목": song["trackName"],
                "가수": song["artistName"],
                "가사": song["plainLyrics"]
            }
            results.append(s)
        return results

    except requests.exceptions.Timeout as e:
        print(f"서버 응답시간 초과: {e}")
    except requests.exceptions.RequestException as e:
        print(f"요청 중 오류 발생: {e}")
    except Exception as e:
        print(f"오류 발생: {e}")
