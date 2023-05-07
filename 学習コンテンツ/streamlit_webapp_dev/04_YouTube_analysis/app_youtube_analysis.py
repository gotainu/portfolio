from apiclient.discovery import build
import json
import pandas as pd
import streamlit as st

with open('secret.json') as f:
    secret = json.load(f)

DEVELOPER_KEY = secret['KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)

def video_search(youtube, q='hamster', max_results=50):
    # q = 'Python'
    # max_results = 50
    response = youtube.search().list(
        q=q,
        # idは不要なので削除
        part="snippet",
        #視聴回数が多い順に取得
        order='viewCount',
        # ビデオ形式のみ取得    
        type='video',
        maxResults=max_results,
    #     # 必要なデータを絞り込み    
    #     fields='items(id(videoId), snippet(channelId, title, description, channelTitle))'
    ).execute()

    items_id = []
    items = response['items']
    for item in items:
        item_id = {}
        item_id['video_id'] = item['id']['videoId']
        item_id['channel_id'] = item['snippet']['channelId']
        items_id.append(item_id)
    df_video = pd.DataFrame(items_id)
    return df_video

def get_results(df_video, threshold=50000):
#     df_video = video_search(youtube, q='Python 自動化', max_results=30)
    channel_ids = df_video['channel_id'].unique().tolist()


    subscriber_list = youtube.channels().list(
        id=','.join(channel_ids),
        part='statistics',
        # 必要なデータを絞り込み
        fields='items(id,statistics(subscriberCount))'
    ).execute()

    subscribers = []
    for item in subscriber_list['items']:
        subscriber = {}
        if len(item['statistics']) > 0:
            subscriber['channel_id'] = item['id']
            subscriber['subscriber_count'] = int(item['statistics']['subscriberCount'])
        else:
            subscriber['channel_id'] = item['id']
        subscribers.append(subscriber)

    df_subscribers = pd.DataFrame(subscribers)

    df = pd.merge(left=df_video, right=df_subscribers, on='channel_id')
    df_extracted = df[df['subscriber_count'] < threshold]

    video_ids = df_extracted['video_id'].tolist()
    videos_list = youtube.videos().list(
                id=','.join(video_ids),
                part='snippet,contentDetails,statistics',
                fields='items(id,snippet(title,publishedAt),contentDetails(duration),statistics(viewCount))'
            ).execute()

    videos_info = []

    items = videos_list['items']
    for item in items:
        video_info = {}
        video_info['video_id'] = item['id']
        video_info['title'] = item['snippet']['title']
        video_info['view_count'] = item['statistics']['viewCount']
        videos_info.append(video_info)

    df_videos_info = pd.DataFrame(videos_info)

    try:
        results = pd.merge(left=df_extracted, right=df_videos_info, on='video_id')
        #     カラム並び替え
        results = results.loc[:, ['video_id', 'title', 'view_count', 'subscriber_count', 'channel_id']]
    except:
        results = pd.DataFrame()

    return results

# 以下、Streamlit部分

st.title('🐹用のYouTube分析アプリ')

st.sidebar.write("""
## クエリとしきい値の設定""")
st.sidebar.write("""
### クエリの入力""")
query = st.sidebar.text_input('検索ワードを入力してください🐹', 'hamster')

st.sidebar.write("""
### 閾値の設定""")
threshold = st.sidebar.slider("登録者数の閾値", 100, 10


0000, 10000)

st.markdown('### 選択中のパラメータ')
st.markdown(f"""
- 検索クエリ: {query}
- 登録者数の閾値: {threshold}
""")

df_video = video_search(youtube, q=query, max_results=50)
results = get_results(df_video, threshold=threshold)

st.write("### 分析結果", results)
st.write("### 動画再生")

video_id = st.text_input('動画IDを入力してください')
url = f"https://youtu.be/{video_id}"
video_field = st.empty()
video_field.write('こちらに動画が表示されます')

if st.button('ビデオ表示'):
    if len(video_id) > 0:
        try:
            video_field.video(url)
        except:
            st.error(
                """
                **おっと！何かエラーが起きているようです。** :(
            """
            )
