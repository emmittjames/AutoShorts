from tiktok_uploader.upload import upload_videos
from tiktok_uploader.auth import AuthBackend

videos = [
    {
        'video': 'example.mp4',
        'description': 'Video 1 is about ...'
    },
    """
    {
        'video': 'video1.mp4',
        'description': 'Video 2 is about ...'
    }
    """
]

auth = AuthBackend(cookies='cookies.txt')
failed_videos = upload_videos(videos=videos, auth=auth, comment=True)
# failed_videos = upload_videos(videos=videos, auth=auth, comment=True, stitch=True, duet=True)

for video in failed_videos: # each input video object which failed
    print(f"{video['video']} with description '{video['description']}' failed")
