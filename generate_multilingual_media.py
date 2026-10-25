import asyncio
import os
import edge_tts
import imageio_ffmpeg
import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import re

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

ENGLISH_SCRIPT = """
Welcome to the comprehensive guide on Dijkstra's Shortest Path Algorithm!

Dijkstra's algorithm is a fundamental Single-Source Shortest Path algorithm designed to find the shortest route from a starting source vertex to all other vertices in a weighted graph.

It operates on a greedy paradigm, maintaining two distinct sets: finalized vertices whose shortest distance is proven, and tentative vertices stored in a Priority Queue.

At each step, it extracts the vertex with the minimum tentative distance and relaxes all its outgoing edges. Relaxation follows a strict rule: if the distance through vertex u to vertex v is smaller than the current tentative distance of v, we immediately update v's distance.

In terms of computational complexity, using an Adjacency Matrix takes O(V squared) time, which is well-suited for dense graphs. However, when implemented with an Adjacency List and a Binary Min-Heap, the runtime drops dramatically to O((V + E) log V), making it exceptionally fast for road networks and large-scale graphs.

A critical requirement: Dijkstra's algorithm strictly requires all edge weights to be non-negative. If any negative weights exist, the greedy choice invariant is violated, and we must instead use the Bellman-Ford algorithm.

From internet routing via the OSPF protocol to real-time GPS navigation in Google Maps, Dijkstra's algorithm remains the bedrock of modern networking and route planning. Thank you!
"""

HINDI_SCRIPT = """
नमस्ते और स्वागत है! आज हम कंप्यूटर साइंस के सबसे महत्वपूर्ण एल्गोरिदम में से एक - डाइक्स्ट्रा एल्गोरिदम को गहराई से समझेंगे।

डाइक्स्ट्रा एल्गोरिदम एक सिंगल-सोर्स शॉर्टेस्ट पाथ एल्गोरिदम है। इसका मुख्य उद्देश्य किसी वेटेड ग्राफ में एक निश्चित सोर्स नोड से बाकी सभी वर्टिसेस तक का सबसे छोटा रास्ता खोजना है।

यह एल्गोरिदम ग्रीडी अप्रोच पर काम करता है। इसमें दो मुख्य सेट्स होते हैं: पहला, वे नोड्स जिनकी सबसे छोटी दूरी तय हो चुकी है, और दूसरा, वे नोड्स जो अभी प्रायोरिटी क्यू में पेंडिंग हैं।

हर कदम पर, एल्गोरिदम सबसे कम दूरी वाले नोड को चुनता है और उसके पड़ोसियों के लिए एज रिलैक्सेशन करता है। रिलैक्सेशन का सरल नियम है: यदि नोड यू के माध्यम से वी तक जाने की दूरी, वी की मौजूदा दूरी से कम है, तो वी की दूरी को तुरंत अपडेट कर दिया जाता है।

अगर हम इसके टाइम कॉम्प्लेक्सिटी की बात करें, तो एडजेसेंसी मैट्रिक्स के साथ यह ओ ऑफ वी स्क्वायर समय लेता है, जो डेंस ग्राफ्स के लिए उपयुक्त है। लेकिन अगर हम बाइनरी मिन-हीप या प्रायोरिटी क्यू का उपयोग करते हैं, तो समय घटकर ओ ऑफ वी प्लस ई लॉग वी हो जाता है, जो गूगल मैप्स और बड़े नेटवर्क्स के लिए अत्यंत तीव्र है।

एक महत्वपूर्ण बात याद रखें: डाइक्स्ट्रा एल्गोरिदम केवल नॉन-नेगेटिव एज वेट्स पर काम करता है। नेगेटिव वेट्स होने पर इसका ग्रीडी नियम टूट जाता है, और ऐसी स्थिति में हम बेलमैन-फोर्ड एल्गोरिदम का उपयोग करते हैं।

इंटरनेट के ओएसपीएफ रूटिंग प्रोटोकॉल से लेकर जीपीएस नेविगेशन तक, डाइक्स्ट्रा एल्गोरिदम आधुनिक नेटवर्किंग की रीढ़ है। धन्यवाद!
"""

SUBTITLE_CUES = [
    {
        'start': 0.0, 'end': 8.0,
        'en': "Welcome to Dijkstra's Single-Source Shortest Path Algorithm (SSSP).",
        'hi': "डाइक्स्ट्रा सिंगल-सोर्स शॉर्टेस्ट पाथ एल्गोरिदम में आपका स्वागत है।",
        'step': 0, 'active_node': 0, 'relaxed_edge': None, 'spt': []
    },
    {
        'start': 8.0, 'end': 18.0,
        'en': "Initialization: Source node A set to distance 0, other nodes set to infinity.",
        'hi': "प्रारंभ: सोर्स नोड A की दूरी 0, और बाकी नोड्स की दूरी अनंत (infinity) रखी गई।",
        'step': 1, 'active_node': 0, 'relaxed_edge': None, 'spt': [0]
    },
    {
        'start': 18.0, 'end': 29.0,
        'en': "Greedy choice: Extract min node A (d=0). Relax outgoing edges A->B (4) and A->C (2).",
        'hi': "ग्रीडी चॉइस: न्यूनतम दूरी नोड A (d=0)। एज रिलैक्सेशन A->B (4) और A->C (2)।",
        'step': 2, 'active_node': 0, 'relaxed_edge': 'AC', 'spt': [0]
    },
    {
        'start': 29.0, 'end': 43.0,
        'en': "Node C has min dist 2. Relax C->B (2+1=3 < 4, updated!) and C->E (2+8=10).",
        'hi': "नोड C न्यूनतम दूरी 2 पर। रिलैक्स C->B (2+1=3 < 4, अपडेट!) और C->E (2+8=10)।",
        'step': 3, 'active_node': 2, 'relaxed_edge': 'CB', 'spt': [0, 2]
    },
    {
        'start': 43.0, 'end': 56.0,
        'en': "Node B has min dist 3. Relax B->D (3+5=8). Complexity with Min-Heap is O((V+E) log V).",
        'hi': "नोड B दूरी 3। रिलैक्स B->D (3+5=8)। बाइनरी मिन-हीप के साथ समय O((V+E) log V)।",
        'step': 4, 'active_node': 1, 'relaxed_edge': 'BD', 'spt': [0, 2, 1]
    },
    {
        'start': 56.0, 'end': 69.0,
        'en': "Crucial rule: Non-negative weights required! If negative edges exist, use Bellman-Ford.",
        'hi': "नियम: केवल नॉन-नेगेटिव एज वेट्स मान्य हैं! नेगेटिव वेट्स के लिए बेलमैन-फोर्ड इस्तेमाल करें।",
        'step': 5, 'active_node': 3, 'relaxed_edge': 'DF', 'spt': [0, 2, 1, 3]
    },
    {
        'start': 69.0, 'end': 85.0,
        'en': "Final Shortest Path Tree locked! Powers OSPF internet routing and Google Maps GPS.",
        'hi': "शॉर्टेस्ट पाथ ट्री पूरा हुआ! यह OSPF इंटरनेट रूटिंग और गूगल मैप्स GPS को चलाता है।",
        'step': 6, 'active_node': 5, 'relaxed_edge': None, 'spt': [0, 1, 2, 3, 4, 5]
    }
]

async def generate_speech_files():
    en_path = os.path.join(STATIC_DIR, "dijkstra_voiceover_english.mp3")
    hi_path = os.path.join(STATIC_DIR, "dijkstra_voiceover_hindi.mp3")
    
    print("[1/4] Generating English Neural Voice-over (en-US-ChristopherNeural)...")
    comm_en = edge_tts.Communicate(ENGLISH_SCRIPT.strip(), voice="en-US-ChristopherNeural", rate="+0%", pitch="+0Hz")
    await comm_en.save(en_path)
    print(f"      Saved: {en_path} ({os.path.getsize(en_path)} bytes)")

    print("[2/4] Generating Hindi Neural Voice-over (hi-IN-MadhurNeural)...")
    comm_hi = edge_tts.Communicate(HINDI_SCRIPT.strip(), voice="hi-IN-MadhurNeural", rate="+0%", pitch="+0Hz")
    await comm_hi.save(hi_path)
    print(f"      Saved: {hi_path} ({os.path.getsize(hi_path)} bytes)")

def draw_graph_frame(cue_idx: int, lang: str = "en") -> np.ndarray:
    cue = SUBTITLE_CUES[min(cue_idx, len(SUBTITLE_CUES) - 1)]
    
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
    fig.patch.set_facecolor('#0b0f19')
    ax.set_facecolor('#0b0f19')
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-0.5, 4.0)
    ax.axis('off')

    nodes = {
        0: {'name': 'A', 'pos': (1.0, 1.8), 'd': 'd=0' if cue['step'] >= 1 else 'd=inf'},
        1: {'name': 'B', 'pos': (2.5, 3.0), 'd': 'd=3' if cue['step'] >= 3 else ('d=4' if cue['step'] >= 2 else 'd=inf')},
        2: {'name': 'C', 'pos': (2.5, 0.6), 'd': 'd=2' if cue['step'] >= 2 else 'd=inf'},
        3: {'name': 'D', 'pos': (4.2, 3.0), 'd': 'd=8' if cue['step'] >= 4 else 'd=inf'},
        4: {'name': 'E', 'pos': (4.2, 0.6), 'd': 'd=10' if cue['step'] >= 3 else 'd=inf'},
        5: {'name': 'F', 'pos': (5.5, 1.8), 'd': 'd=14' if cue['step'] >= 5 else 'd=inf'}
    }

    edges = [
        (0, 1, 4, 'AB'),
        (0, 2, 2, 'AC'),
        (1, 2, 1, 'CB'),
        (1, 3, 5, 'BD'),
        (2, 4, 8, 'CE'),
        (3, 4, 2, 'DE'),
        (3, 5, 6, 'DF'),
        (4, 5, 7, 'EF'),
    ]

    for u, v, w, name in edges:
        p1, p2 = nodes[u]['pos'], nodes[v]['pos']
        is_relaxed = (cue['relaxed_edge'] == name)
        is_spt = (u in cue['spt'] and v in cue['spt'] and name in ['AC', 'CB', 'BD', 'DF', 'CE'])
        
        if is_spt:
            color = '#10b981'
            lw = 4.5
        elif is_relaxed:
            color = '#f59e0b'
            lw = 4.0
        else:
            color = '#334155'
            lw = 2.0

        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, linewidth=lw, zorder=1)
        
        mid_x = (p1[0] + p2[0]) / 2.0
        mid_y = (p1[1] + p2[1]) / 2.0
        offset_y = 0.12 if u != 1 or v != 2 else 0.0
        ax.text(mid_x, mid_y + offset_y, str(w), color='#38bdf8' if is_spt else '#94a3b8',
                fontsize=13, fontweight='bold', ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#0f172a', edgecolor=color, alpha=0.9), zorder=2)

    for idx, data in nodes.items():
        x, y = data['pos']
        in_spt = idx in cue['spt']
        is_active = (idx == cue['active_node'])
        
        if in_spt:
            facecolor = '#10b981'
            edgecolor = '#34d399'
        elif is_active:
            facecolor = '#f59e0b'
            edgecolor = '#fbbf24'
        else:
            facecolor = '#1e293b'
            edgecolor = '#475569'

        circle = patches.Circle((x, y), 0.28, facecolor=facecolor, edgecolor=edgecolor, linewidth=3, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, data['name'], color='#ffffff', fontsize=16, fontweight='bold', ha='center', va='center', zorder=4)
        ax.text(x, y - 0.42, data['d'], color='#38bdf8' if in_spt else '#94a3b8', fontsize=12, fontweight='bold', ha='center', va='center', zorder=4)

    title_text = "Dijkstra's Algorithm Walkthrough (Single-Source Shortest Path)"
    subtitle_text = "Source Node: A • Target: All Vertices • Greedy Invariant: w(u,v) >= 0"
    ax.text(3.0, 3.8, title_text, color='#38bdf8', fontsize=18, fontweight='bold', ha='center', va='top')
    ax.text(3.0, 3.52, subtitle_text, color='#94a3b8', fontsize=12, ha='center', va='top')

    sub_en = cue['en']
    sub_hi = cue['hi']
    primary_sub = sub_en if lang == 'en' else sub_hi
    sec_sub = sub_hi if lang == 'en' else sub_en

    rect = patches.Rectangle((-0.4, -0.45), 7.2, 0.75, facecolor='#0f172a', edgecolor='#334155', linewidth=1.5, zorder=5)
    ax.add_patch(rect)
    ax.text(3.1, -0.05, primary_sub, color='#f8fafc', fontsize=13, fontweight='bold', ha='center', va='center', zorder=6)
    ax.text(3.1, -0.30, sec_sub, color='#94a3b8', fontsize=11, ha='center', va='center', zorder=6)

    fig.canvas.draw()
    img = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (4,))[:, :, :3]
    plt.close(fig)
    return img

def create_mp4_video(lang: str = "en"):
    audio_fname = f"dijkstra_voiceover_{'english' if lang == 'en' else 'hindi'}.mp3"
    audio_path = os.path.join(STATIC_DIR, audio_fname)
    video_out = os.path.join(STATIC_DIR, f"dijkstra_walkthrough_{'english' if lang == 'en' else 'hindi'}.mp4")
    
    print(f"[3/4] Rendering frames for {lang.upper()} walkthrough MP4...")
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    fps = 2
    cmd_probe = [ffmpeg_exe, "-i", audio_path, "-f", "null", "-"]
    probe_res = subprocess.run(cmd_probe, stderr=subprocess.PIPE, text=True, errors='ignore')
    dur_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", probe_res.stderr)
    if dur_match:
        hours, mins, secs = dur_match.groups()
        total_duration = float(hours)*3600 + float(mins)*60 + float(secs)
    else:
        total_duration = 75.0

    print(f"      Audio duration: {total_duration:.2f} seconds")
    total_frames = int(total_duration * fps)

    cmd_ffmpeg = [
        ffmpeg_exe,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1280x720",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        video_out
    ]

    proc = subprocess.Popen(cmd_ffmpeg, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    current_cue_idx = 0
    for frame_i in range(total_frames):
        current_time = frame_i / fps
        while current_cue_idx < len(SUBTITLE_CUES) - 1 and current_time >= SUBTITLE_CUES[current_cue_idx + 1]["start"]:
            current_cue_idx += 1
        
        frame_rgb = draw_graph_frame(current_cue_idx, lang=lang)
        proc.stdin.write(frame_rgb.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"      Video created: {video_out} ({os.path.getsize(video_out)} bytes)")

def build_all():
    asyncio.run(generate_speech_files())
    create_mp4_video("en")
    create_mp4_video("hi")
    print("[4/4] All multilingual media assets successfully generated!")

if __name__ == "__main__":
    build_all()