import base64
import os

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
mp3_path = os.path.join(STATIC_DIR, "dijkstra_voiceover_hindi.mp3")
html_path = os.path.join(STATIC_DIR, "video_player.html")

if os.path.exists(mp3_path) and os.path.exists(html_path):
    mp3_data = open(mp3_path, "rb").read()
    b64_audio = base64.b64encode(mp3_data).decode("utf-8")
    data_uri = f"data:audio/mp3;base64,{b64_audio}"

    html = open(html_path, "r", encoding="utf-8").read()
    if 'src="dijkstra_voiceover_hindi.mp3"' in html:
        html = html.replace('src="dijkstra_voiceover_hindi.mp3"', f'src="{data_uri}"')
        open(html_path, "w", encoding="utf-8").write(html)
        print(f"Embedded base64 audio into {html_path} successfully! New size: {len(html)} bytes")
    else:
        print("Audio tag already replaced or different pattern.")
else:
    print("Files not found.")
