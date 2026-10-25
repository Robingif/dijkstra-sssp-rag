import asyncio
import os
import edge_tts

HINDI_SCRIPT = """
नमस्ते और स्वागत है! आज हम कंप्यूटर साइंस के सबसे महत्वपूर्ण एल्गोरिदम में से एक - डाइक्स्ट्रा एल्गोरिदम (Dijkstra's Algorithm) को गहराई से समझेंगे। 

डाइक्स्ट्रा एल्गोरिदम एक सिंगल-सोर्स शॉर्टेस्ट पाथ एल्गोरिदम है। इसका मुख्य उद्देश्य किसी वेटेड ग्राफ में एक निश्चित सोर्स नोड से बाकी सभी वर्टिसेस तक का सबसे छोटा रास्ता खोजना है।

यह एल्गोरिदम ग्रीडी अप्रोच पर काम करता है। इसमें दो मुख्य सेट्स होते हैं: पहला, वे नोड्स जिनकी सबसे छोटी दूरी तय हो चुकी है, और दूसरा, वे नोड्स जो अभी प्रायोरिटी क्यू में पेंडिंग हैं।

हर कदम पर, एल्गोरिदम सबसे कम दूरी वाले नोड को चुनता है और उसके पड़ोसियों के लिए एज रिलैक्सेशन करता है। रिलैक्सेशन का सरल नियम है: यदि नोड यू के माध्यम से वी तक जाने की दूरी, वी की मौजूदा दूरी से कम है, तो वी की दूरी को तुरंत अपडेट कर दिया जाता है।

अगर हम इसके टाइम कॉम्प्लेक्सिटी की बात करें, तो एडजेसेंसी मैट्रिक्स के साथ यह ओ ऑफ वी स्क्वायर समय लेता है, जो डेंस ग्राफ्स के लिए उपयुक्त है। लेकिन अगर हम बाइनरी मिन-हीप या प्रायोरिटी क्यू का उपयोग करते हैं, तो समय घटकर ओ ऑफ वी प्लस ई लॉग वी हो जाता है, जो गूगल मैप्स और बड़े नेटवर्क्स के लिए अत्यंत तीव्र है।

एक महत्वपूर्ण बात याद रखें: डाइक्स्ट्रा एल्गोरिदम केवल नॉन-नेगेटिव एज वेट्स पर काम करता है। नेगेटिव वेट्स होने पर इसका ग्रीडी नियम टूट जाता है, और ऐसी स्थिति में हम बेलमैन-फोर्ड एल्गोरिदम का उपयोग करते हैं।

इंटरनेट के ओएसपीएफ रूटिंग प्रोटोकॉल से लेकर जीपीएस नेविगेशन तक, डाइक्स्ट्रा एल्गोरिदम आधुनिक नेटवर्किंग की रीढ़ है। धन्यवाद!
"""

ENGLISH_SUBTITLES = [
    (0, 8, "Welcome! Today we will explore one of the most fundamental graph algorithms: Dijkstra's Shortest Path Algorithm."),
    (8, 17, "Dijkstra's algorithm is a Single-Source Shortest Path (SSSP) algorithm designed to find the shortest route from a source to all other vertices."),
    (17, 27, "It operates on a greedy paradigm, maintaining a finalized Shortest Path Tree set alongside an unvisited Priority Queue."),
    (27, 40, "At each step, it extracts the minimum tentative distance node and relaxes outgoing edges: if d[u] + w(u,v) < d[v], distance to v is updated."),
    (40, 53, "For complexity: Adjacency Matrix takes O(V^2), while an Adjacency List with Min-Heap drops runtime to O((V + E) log V)."),
    (53, 65, "Crucial rule: Dijkstra strictly requires non-negative edge weights. For graphs with negative edges, use the Bellman-Ford algorithm."),
    (65, 75, "From OSPF internet routing to GPS navigation in Google Maps, Dijkstra's algorithm powers modern infrastructure. Thank you!")
]

async def generate_voiceover(output_mp3_path: str):
    voice = "hi-IN-MadhurNeural"
    print(f"Generating voice-over with {voice}...")
    communicate = edge_tts.Communicate(HINDI_SCRIPT.strip(), voice=voice, rate="+0%", pitch="+0Hz")
    await communicate.save(output_mp3_path)
    print(f"Voice-over generated successfully at: {output_mp3_path}")

def generate_video_player_html(output_html_path: str):
    """
    Creates an interactive HTML5 video & animation player with synchronized Hindi audio,
    live SVG step-by-step graph animation, and bilingual subtitles.
    """
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dijkstra's Algorithm — Animation & Voice-Over Player</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: system-ui, -apple-system, sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; }
        .player-card { max-width: 900px; margin: 0 auto; background: #1e293b; border: 1px solid #334155; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
        .player-header { padding: 16px 24px; background: #0f172a; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }
        .title { font-size: 16px; font-weight: 700; color: #38bdf8; display: flex; align-items: center; gap: 8px; }
        .lang-badge { background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; color: #10b981; font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 12px; }
        .canvas-area { background: #0b0f19; padding: 24px; display: flex; justify-content: center; align-items: center; min-height: 400px; position: relative; }
        .subtitle-box { background: rgba(15, 23, 42, 0.95); border-top: 1px solid #334155; padding: 14px 20px; text-align: center; min-height: 70px; display: flex; flex-direction: column; justify-content: center; }
        .sub-hindi { font-size: 15px; color: #f8fafc; font-weight: 600; margin-bottom: 4px; }
        .sub-english { font-size: 12px; color: #94a3b8; }
        .controls { padding: 16px 24px; background: #0f172a; border-top: 1px solid #334155; display: flex; align-items: center; gap: 16px; }
        .play-btn { background: #38bdf8; border: none; color: #0f172a; width: 44px; height: 44px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: bold; transition: transform 0.1s; }
        .play-btn:hover { transform: scale(1.05); background: #7dd3fc; }
        .progress-bar { flex: 1; height: 6px; background: #334155; border-radius: 3px; cursor: pointer; position: relative; }
        .progress-fill { height: 100%; background: #38bdf8; border-radius: 3px; width: 0%; }
        .time-display { font-family: monospace; font-size: 13px; color: #94a3b8; min-width: 90px; text-align: right; }
        audio { display: none; }
    </style>
</head>
<body>
    <div class="player-card">
        <div class="player-header">
            <div class="title">🎬 Dijkstra's Algorithm: Visual Animation & Voice-Over</div>
            <div class="lang-badge">🔊 Audio: Hindi (हिंदी) • Subtitles: Bilingual</div>
        </div>

        <div class="canvas-area" id="canvasContainer">
            <!-- Animated SVG will be injected here -->
            <svg id="graphSvg" width="100%" height="380" viewBox="0 0 760 380" style="background:#0b0f19;">
                <defs>
                    <filter id="nodeGlow" x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur stdDeviation="3" result="blur" />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>
                </defs>
                <!-- Edges -->
                <line id="e01" x1="120" y1="190" x2="280" y2="90" stroke="#334155" stroke-width="2" />
                <line id="e02" x1="120" y1="190" x2="280" y2="290" stroke="#334155" stroke-width="2" />
                <line id="e12" x1="280" y1="90" x2="280" y2="290" stroke="#334155" stroke-width="2" />
                <line id="e13" x1="280" y1="90" x2="480" y2="90" stroke="#334155" stroke-width="2" />
                <line id="e24" x1="280" y1="290" x2="480" y2="290" stroke="#334155" stroke-width="2" />
                <line id="e34" x1="480" y1="90" x2="480" y2="290" stroke="#334155" stroke-width="2" />
                <line id="e35" x1="480" y1="90" x2="640" y2="190" stroke="#334155" stroke-width="2" />
                <line id="e45" x1="480" y1="290" x2="640" y2="190" stroke="#334155" stroke-width="2" />

                <!-- Weights -->
                <text x="195" y="130" fill="#94a3b8" font-size="11" font-weight="bold">4</text>
                <text x="195" y="255" fill="#94a3b8" font-size="11" font-weight="bold">2</text>
                <text x="290" y="195" fill="#94a3b8" font-size="11" font-weight="bold">1</text>
                <text x="380" y="80" fill="#94a3b8" font-size="11" font-weight="bold">5</text>
                <text x="380" y="305" fill="#94a3b8" font-size="11" font-weight="bold">8</text>
                <text x="490" y="195" fill="#94a3b8" font-size="11" font-weight="bold">2</text>
                <text x="565" y="130" fill="#94a3b8" font-size="11" font-weight="bold">6</text>
                <text x="565" y="255" fill="#94a3b8" font-size="11" font-weight="bold">3</text>

                <!-- Nodes -->
                <g id="node0"><circle cx="120" cy="190" r="24" fill="#1e293b" stroke="#64748b" stroke-width="2"/><text x="120" y="196" fill="#fff" font-size="15" font-weight="bold" text-anchor="middle">A</text><text id="d0" x="120" y="155" fill="#38bdf8" font-size="11" font-weight="bold" text-anchor="middle">d=0</text></g>
                <g id="node1"><circle cx="280" cy="90" r="24" fill="#1e293b" stroke="#64748b" stroke-width="2"/><text x="280" y="96" fill="#fff" font-size="15" font-weight="bold" text-anchor="middle">B</text><text id="d1" x="280" y="55" fill="#94a3b8" font-size="11" font-weight="bold" text-anchor="middle">d=inf</text></g>
                <g id="node2"><circle cx="280" cy="290" r="24" fill="#1e293b" stroke="#64748b" stroke-width="2"/><text x="280" y="296" fill="#fff" font-size="15" font-weight="bold" text-anchor="middle">C</text><text id="d2" x="280" y="325" fill="#94a3b8" font-size="11" font-weight="bold" text-anchor="middle">d=inf</text></g>
                <g id="node3"><circle cx="480" cy="90" r="24" fill="#1e293b" stroke="#64748b" stroke-width="2"/><text x="480" y="96" fill="#fff" font-size="15" font-weight="bold" text-anchor="middle">D</text><text id="d3" x="480" y="55" fill="#94a3b8" font-size="11" font-weight="bold" text-anchor="middle">d=inf</text></g>
                <g id="node4"><circle cx="480" cy="290" r="24" fill="#1e293b" stroke="#64748b" stroke-width="2"/><text x="480" y="296" fill="#fff" font-size="15" font-weight="bold" text-anchor="middle">E</text><text id="d4" x="480" y="325" fill="#94a3b8" font-size="11" font-weight="bold" text-anchor="middle">d=inf</text></g>
                <g id="node5"><circle cx="640" cy="190" r="24" fill="#1e293b" stroke="#64748b" stroke-width="2"/><text x="640" y="196" fill="#fff" font-size="15" font-weight="bold" text-anchor="middle">F</text><text id="d5" x="640" y="155" fill="#94a3b8" font-size="11" font-weight="bold" text-anchor="middle">d=inf</text></g>
            </svg>
        </div>

        <div class="subtitle-box">
            <div class="sub-hindi" id="subHindi">डाइक्स्ट्रा एल्गोरिदम (Dijkstra's Algorithm) का एनिमेशन और वॉयस-ओवर शुरू करने के लिए प्ले दबाएं।</div>
            <div class="sub-english" id="subEnglish">Press play to begin the step-by-step animated walkthrough with Hindi voice-over.</div>
        </div>

        <div class="controls">
            <button class="play-btn" id="playBtn" onclick="togglePlay()">▶</button>
            <div class="progress-bar" id="progressBar" onclick="seek(event)">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <div class="time-display" id="timeDisplay">0:00 / 1:15</div>
            <audio id="audioPlayer" src="dijkstra_voiceover_hindi.mp3"></audio>
        </div>
    </div>

    <script>
        const audio = document.getElementById('audioPlayer');
        const playBtn = document.getElementById('playBtn');
        const progressFill = document.getElementById('progressFill');
        const timeDisplay = document.getElementById('timeDisplay');
        const subHindi = document.getElementById('subHindi');
        const subEnglish = document.getElementById('subEnglish');

        const cues = [
            {
                start: 0, end: 8,
                hindi: "नमस्ते और स्वागत है! आज हम डाइक्स्ट्रा एल्गोरिदम को गहराई से समझेंगे।",
                english: "Welcome! Today we will explore one of the most fundamental graph algorithms: Dijkstra's Algorithm.",
                state: () => { resetGraph(); }
            },
            {
                start: 8, end: 17,
                hindi: "डाइक्स्ट्रा एल्गोरिदम सिंगल-सोर्स शॉर्टेस्ट पाथ खोजता है नॉन-नेगेटिव वेटेड ग्राफ्स में।",
                english: "Dijkstra's algorithm finds shortest paths from a single source to all nodes in non-negative weighted graphs.",
                state: () => { setNode(0, '#f59e0b', 'd=0'); }
            },
            {
                start: 17, end: 27,
                hindi: "यह ग्रीडी अप्रोच पर काम करता है और मिन-डिस्टेंस नोड को चुनता है।",
                english: "It operates on a greedy paradigm, iteratively picking the vertex with minimum tentative distance.",
                state: () => { 
                    setNode(0, '#10b981', 'd=0');
                    setEdge('e02', '#f59e0b', 4);
                    setNode(2, '#38bdf8', 'd=2');
                    setEdge('e01', '#f59e0b', 4);
                    setNode(1, '#38bdf8', 'd=4');
                }
            },
            {
                start: 27, end: 40,
                hindi: "एज रिलैक्सेशन: यदि नोड C से होकर नया रास्ता छोटा है, तो दूरी अपडेट हो जाती है।",
                english: "Edge relaxation: when a path through node C offers a shorter distance, tentative distance is relaxed.",
                state: () => {
                    setNode(2, '#10b981', 'd=2');
                    setEdge('e12', '#10b981', 3);
                    setNode(1, '#38bdf8', 'd=3'); // 2 + 1 = 3 (better than 4!)
                    setEdge('e24', '#10b981', 3);
                    setNode(4, '#38bdf8', 'd=10');
                }
            },
            {
                start: 40, end: 53,
                hindi: "प्रायोरिटी क्यू (Min-Heap) के साथ टाइम कॉम्प्लेक्सिटी O((V + E) log V) हो जाती है।",
                english: "Using an Adjacency List and Min-Heap, the runtime drops to an optimal O((V + E) log V).",
                state: () => {
                    setNode(1, '#10b981', 'd=3');
                    setEdge('e13', '#10b981', 3);
                    setNode(3, '#38bdf8', 'd=8'); // 3 + 5 = 8
                    setNode(4, '#10b981', 'd=10');
                    setEdge('e34', '#10b981', 3);
                }
            },
            {
                start: 53, end: 65,
                hindi: "डाइक्स्ट्रा नेगेटिव वेट्स पर काम नहीं करता; नेगेटिव वेट्स के लिए बेलमैन-फोर्ड का प्रयोग करें।",
                english: "Dijkstra strictly requires non-negative weights; for graphs with negative weights, use Bellman-Ford.",
                state: () => {
                    setNode(3, '#10b981', 'd=8');
                    setEdge('e45', '#10b981', 4);
                    setNode(5, '#10b981', 'd=13'); // 10 + 3 = 13
                }
            },
            {
                start: 65, end: 85,
                hindi: "इंटरनेट OSPF रूटिंग और Google Maps GPS नेविगेशन तक, डाइक्स्ट्रा दुनिया को जोड़ता है!",
                english: "From OSPF internet routing to Google Maps navigation, Dijkstra's algorithm powers our connected world!",
                state: () => {
                    // Highlight final Shortest Path Tree (SPT)
                    ['node0','node1','node2','node3','node4','node5'].forEach(id => {
                        document.querySelector('#' + id + ' circle').setAttribute('fill', '#10b981');
                    });
                }
            }
        ];

        function resetGraph() {
            for (let i = 0; i <= 5; i++) {
                setNode(i, '#1e293b', i === 0 ? 'd=0' : 'd=inf');
            }
            ['e01','e02','e12','e13','e24','e34','e35','e45'].forEach(id => {
                document.getElementById(id).setAttribute('stroke', '#334155');
                document.getElementById(id).setAttribute('stroke-width', '2');
            });
        }

        function setNode(idx, color, text) {
            const circle = document.querySelector('#node' + idx + ' circle');
            const dText = document.getElementById('d' + idx);
            if (circle) circle.setAttribute('fill', color);
            if (dText) dText.textContent = text;
        }

        function setEdge(id, color, width) {
            const edge = document.getElementById(id);
            if (edge) {
                edge.setAttribute('stroke', color);
                edge.setAttribute('stroke-width', width);
            }
        }

        function togglePlay() {
            if (audio.paused) {
                audio.play();
                playBtn.textContent = '❚❚';
            } else {
                audio.pause();
                playBtn.textContent = '▶';
            }
        }

        audio.addEventListener('timeupdate', () => {
            const cur = audio.currentTime;
            const dur = audio.duration || 75;
            progressFill.style.width = (cur / dur * 100) + '%';
            
            const curM = Math.floor(cur / 60);
            const curS = Math.floor(cur % 60).toString().padStart(2, '0');
            const durM = Math.floor(dur / 60);
            const durS = Math.floor(dur % 60).toString().padStart(2, '0');
            timeDisplay.textContent = `${curM}:${curS} / ${durM}:${durS}`;

            // Check subtitle and state cues
            for (const cue of cues) {
                if (cur >= cue.start && cur < cue.end) {
                    subHindi.textContent = cue.hindi;
                    subEnglish.textContent = cue.english;
                    cue.state();
                    break;
                }
            }
        });

        audio.addEventListener('ended', () => {
            playBtn.textContent = '▶';
            progressFill.style.width = '100%';
        });

        function seek(e) {
            const rect = document.getElementById('progressBar').getBoundingClientRect();
            const clickPos = (e.clientX - rect.left) / rect.width;
            audio.currentTime = clickPos * (audio.duration || 75);
        }
    </script>
</body>
</html>
"""
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Video player HTML saved successfully at: {output_html_path}")

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    asyncio.run(generate_voiceover("static/dijkstra_voiceover_hindi.mp3"))
    generate_video_player_html("static/video_player.html")
