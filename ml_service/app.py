from ml_module import VideoTranslator

from fastapi import FastAPI
from starlette import status
from starlette.responses import Response


video_translator = VideoTranslator()
app = FastAPI()


@app.get("/process_video")
async def process_video(youtube_url: str):
    return_video_path, success = video_translator.process(youtube_url)
    if success:
        return Response(content=return_video_path, status_code=status.HTTP_200_OK)
    return Response(content="", status_code=status.HTTP_400_BAD_REQUEST)
