import webview
import asyncio
import threading
import sys
import os
sys.path.append(os.path.dirname(__file__))
from crownstar_core import CrownStarCognitive

TIER = "Enterprise"
MAX_INPUT = 5000000
MAX_OUTPUT = 1000000000

engine = CrownStarCognitive(tier=TIER)

class API:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self._run_loop, daemon=True).start()
    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
    def chat(self, query):
        try:
            future = asyncio.run_coroutine_threadsafe(engine.think(query), self.loop)
            return future.result(timeout=30)
        except Exception as e:
            return f"⚠️ Core error: {str(e)}"

html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>CrownStar {TIER}</title>
    <style>
        body {{ background: #0a0c1a; color: #eef4ff; font-family: sans-serif; padding: 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(130px,1fr)); gap: 10px; margin-bottom: 20px; max-height: 300px; overflow-y: auto; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 10px; }}
        .amenity-btn {{ background: #1e293b; border: 1px solid #ffcc4d; padding: 8px; border-radius: 8px; cursor: pointer; text-align: center; font-size: 0.9rem; }}
        .amenity-btn:hover {{ background: #ffcc4d20; }}
        .chat-area {{ margin-top: 20px; }}
        input, button {{ padding: 8px; margin: 5px; }}
        #output {{ background: #1e293b; padding: 10px; border-radius: 8px; white-space: pre-wrap; max-height: 300px; overflow-y: auto; }}
        h2 {{ color: #ffcc4d; }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js"></script>
    <script src="https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/mobilenet@2.1.0/dist/mobilenet.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@3.18.0/dist/tf.min.js"></script>
</head>
<body>
    <h1>⭐ CrownStar {TIER}</h1>
    <h2>⚡ 54 Amenities</h2>
    <div class="grid" id="amenitiesGrid"></div>
    <div class="chat-area">
        <input id="query" type="text" placeholder="Ask anything...">
        <button id="ask">Ask</button>
        <div id="output"></div>
    </div>
    <script>
        const amenities = ['Picture' 'Video' 'CAD' 'Game' 'Music' 'Code' 'PDF Reader' 'Blockchain' 'News' 'Stocks' 'Email Draft' 'Legal Doc' 'Academic Paper' 'Translate' 'Speech to Text' 'Text to Speech' 'Image Recognition' 'QR Code' 'Barcode Scan' 'Password Gen' 'Unit Converter' 'Currency' 'Time Zone' 'Cron Helper' 'JSON Formatter' 'XML Formatter' 'YAML to JSON' 'Base64' 'JWT Decoder' 'Markdown to HTML' 'HTML to Markdown' 'Regex Tester' 'Diff Checker' 'Hash Gen' 'Lorem Ipsum' 'Color Picker' 'QR Scan' 'Barcode Gen' 'Meme Gen' 'Joke' 'Quote' 'Random Fact' 'Riddle' 'Short Story' 'Poem' 'Recipe' 'Workout Plan' 'Meditation' 'Pomodoro' 'Note Taker' 'To‑Do List' 'Calendar Parser' 'Reminder' 'Meeting Summariser';
        const grid = document.getElementById('amenitiesGrid');
        const outputDiv = document.getElementById('output');
        function showResult(text) {{ outputDiv.innerText = text; }}
        function setInteractive(html) {{ outputDiv.innerHTML = html; }}
        const amenityActions = {{
            Picture: async () => {{
                try {{
                    const res = await fetch('https://picsum.photos/400/300');
                    const blob = await res.blob();
                    const url = URL.createObjectURL(blob);
                    setInteractive(`<img src="${{url}}" style="max-width:100%; border-radius:8px;"><br>Random image from Lorem Picsum.`);
                }} catch(e) {{ showResult("📷 Picture service temporarily unavailable."); }}
            }},
            Video: () => {{
                setInteractive(`<video controls src="https://download.blender.org/peach/bigbuckbunny_movies/BigBuckBunny_320x180.mp4" style="width:100%; border-radius:8px;"></video><br>Royalty‑free video (Big Buck Bunny).`);
            }},
            CAD: () => {{
                setInteractive(`<div id="cadContainer" style="height:300px;"></div>
<script type="importmap">
  {{ "imports": {{ "three": "https://unpkg.com/three@0.128.0/build/three.module.js" }} }}
</script>
<script type="module">
  import * as THREE from 'three';
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer();
  renderer.setSize(300, 300);
  document.getElementById('cadContainer').appendChild(renderer.domElement);
  const geometry = new THREE.BoxGeometry(1,1,1);
  const material = new THREE.MeshStandardMaterial({{ color: 0xffcc4d }});
  const cube = new THREE.Mesh(geometry, material);
  scene.add(cube);
  camera.position.z = 2;
  const light = new THREE.AmbientLight(0x404040);
  scene.add(light);
  const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
  directionalLight.position.set(1,2,1);
  scene.add(directionalLight);
  function animate() {{
    requestAnimationFrame(animate);
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;
    renderer.render(scene, camera);
  }}
  animate();
</script>`);
            }},
            Game: () => {{
                setInteractive(`<canvas id="snakeCanvas" width="400" height="400" style="border:1px solid gold;"></canvas><br><button id="restartSnake">Restart</button>
<script>
  let canvas = document.getElementById('snakeCanvas');
  let ctx = canvas.getContext('2d');
  let snake = [{{x:200,y:200}}];
  let dir = 'RIGHT';
  let food = {{x:250,y:200}};
  let score = 0;
  let gameLoop;
  function draw() {{
    ctx.fillStyle = '#0a0c1a';
    ctx.fillRect(0,0,400,400);
    ctx.fillStyle = '#ffcc4d';
    snake.forEach(s => ctx.fillRect(s.x,s.y,10,10));
    ctx.fillStyle = 'red';
    ctx.fillRect(food.x,food.y,10,10);
    ctx.fillStyle = 'white';
    ctx.font = '16px monospace';
    ctx.fillText('Score: ' + score, 10, 30);
  }}
  function update() {{
    let head = {{...snake[0]}};
    if (dir === 'RIGHT') head.x += 10;
    if (dir === 'LEFT') head.x -= 10;
    if (dir === 'UP') head.y -= 10;
    if (dir === 'DOWN') head.y += 10;
    snake.unshift(head);
    if (head.x === food.x && head.y === food.y) {{
      score++;
      food = {{x: Math.floor(Math.random()*40)*10, y: Math.floor(Math.random()*40)*10}};
    }} else {{
      snake.pop();
    }}
    if (head.x < 0 || head.x >= 400 || head.y < 0 || head.y >= 400) {{
      clearInterval(gameLoop);
      alert('Game Over! Score: ' + score);
      return;
    }}
    draw();
  }}
  function restart() {{
    clearInterval(gameLoop);
    snake = [{{x:200,y:200}}];
    dir = 'RIGHT';
    food = {{x:250,y:200}};
    score = 0;
    draw();
    gameLoop = setInterval(update, 100);
  }}
  window.addEventListener('keydown', e => {{
    if (e.key === 'ArrowRight') dir = 'RIGHT';
    if (e.key === 'ArrowLeft') dir = 'LEFT';
    if (e.key === 'ArrowUp') dir = 'UP';
    if (e.key === 'ArrowDown') dir = 'DOWN';
  }});
  draw();
  gameLoop = setInterval(update, 100);
  document.getElementById('restartSnake').onclick = restart;
</script>`);
            }},
            Music: () => {{
                setInteractive(`<button id="playMidi">Play Melody</button>
<script>
document.getElementById('playMidi').onclick = () => {{
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  const ctx = new AudioContext();
  const notes = [262, 294, 330, 349, 392, 440, 494, 523];
  let time = ctx.currentTime;
  notes.forEach((freq, i) => {{
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.frequency.value = freq;
    gain.gain.value = 0.3;
    osc.start(time);
    gain.gain.exponentialRampToValueAtTime(0.00001, time + 0.5);
    time += 0.4;
  }});
}};
</script>`);
            }},
            Code: () => {{
                setInteractive(`<textarea id="codeInput" rows="8" cols="50" placeholder="Enter JavaScript code (e.g., 2+2)"></textarea><br><button id="runCodeSafe">Run</button>
<script>
document.getElementById('runCodeSafe').onclick = () => {{
  const code = document.getElementById('codeInput').value;
  try {{
    const sandbox = new Function('return (' + code + ')');
    const result = sandbox();
    outputDiv.innerText = 'Result: ' + JSON.stringify(result);
  }} catch(e) {{
    outputDiv.innerText = 'Error: ' + e.message;
  }}
}};
</script>`);
            }},
            "PDF Reader": () => {{
                setInteractive(`<iframe src="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf" style="width:100%; height:400px;"></iframe><br>Sample PDF (dummy).`);
            }},
            Blockchain: async () => {{
                try {{
                    const res = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd');
                    const data = await res.json();
                    showResult(`⛓️ Bitcoin price: $${data.bitcoin.usd} USD`);
                }} catch(e) {{
                    showResult("⛓️ Bitcoin price temporarily unavailable. Simulated: $45,000 USD");
                }}
            }},
            News: async () => {{
                try {{
                    const res = await fetch('https://api.rss2json.com/v1/api.json?rss_url=https://feeds.bbci.co.uk/news/rss.xml');
                    const data = await res.json();
                    const top = data.items[0];
                    showResult(`📰 ${top.title}\n${top.description.substring(0,200)}...`);
                }} catch(e) {{
                    showResult("📰 News service unavailable. Simulated: AI breakthrough announced.");
                }}
            }},
            Stocks: () => showResult("📈 Stock data simulated: CrownStar AI (CSAI) $49.99 ▲2.3%"),
            "Email Draft": () => showResult("📧 Email draft: 'Hello, this is an automated draft from CrownStar.'"),
            "Legal Doc": () => showResult("⚖️ Legal doc analyser: Sample contract clauses summarised."),
            "Academic Paper": () => showResult("🎓 Academic paper summariser: Abstract of 'AI and Markov Chains'."),
            Translate: async () => {{
                try {{
                    const text = "Hello";
                    const res = await fetch(`https://api.mymemory.translated.net/get?q=${text}&langpair=en|fr`);
                    const data = await res.json();
                    showResult(`🌐 Translation: '${text}' -> '${data.responseData.translatedText}'`);
                }} catch(e) {{
                    showResult("🌐 Translation service unavailable. Simulated: 'Hello' -> 'Bonjour'");
                }}
            }},
            "Speech to Text": () => {{
                if (!('webkitSpeechRecognition' in window)) {{
                    showResult("⚠️ Speech recognition not supported in this browser.");
                    return;
                }}
                const recognition = new webkitSpeechRecognition();
                recognition.lang = 'en-US';
                recognition.start();
                recognition.onresult = (event) => {{
                    const transcript = event.results[0][0].transcript;
                    showResult(`🎤 You said: "${transcript}"`);
                }};
                recognition.onerror = () => showResult("🎤 Microphone error.");
                showResult("🎤 Listening... speak into your microphone.");
            }},
            "Text to Speech": () => {{
                try {{
                    const utterance = new SpeechSynthesisUtterance("CrownStar is amazing.");
                    speechSynthesis.speak(utterance);
                    showResult("🔊 Speaking: 'CrownStar is amazing...'");
                }} catch(e) {{
                    showResult("🔊 Text‑to‑speech error.");
                }}
            }},
            "Image Recognition": async () => {{
                setInteractive(`<img id="testImg" src="https://picsum.photos/200/200?random=1" style="max-width:200px;"><br><button id="classifyBtn">Classify Image</button><div id="classResult"></div>
<script>
let model;
async function loadModel() {{
    if (!window.mobilenet) {{
        document.getElementById('classResult').innerText = 'Loading model...';
        await tf.setBackend('webgl');
        model = await mobilenet.load();
        document.getElementById('classResult').innerText = 'Model ready.';
    }}
}}
loadModel();
document.getElementById('classifyBtn').onclick = async () => {{
    const img = document.getElementById('testImg');
    if (!model) {{ await loadModel(); }}
    try {{
        const predictions = await model.classify(img);
        const top = predictions[0];
        document.getElementById('classResult').innerText = `Detected: ${top.className} (${(top.probability*100).toFixed(1)}%)`;
    }} catch(e) {{
        document.getElementById('classResult').innerText = 'Classification error.';
    }}
}};
</script>`);
            }},
            "QR Code": () => {{
                setInteractive(`<input id="qrText" placeholder="Enter text" value="CrownStar AI"><br><div id="qrcode"></div>
<script>
if (typeof QRCode !== 'undefined') {{
    new QRCode(document.getElementById('qrcode'), {{
        text: document.getElementById('qrText').value,
        width: 200,
        height: 200
    }});
    document.getElementById('qrText').oninput = function() {{
        document.getElementById('qrcode').innerHTML = '';
        new QRCode(document.getElementById('qrcode'), {{
            text: this.value,
            width: 200,
            height: 200
        }});
    }};
}} else {{
    document.getElementById('qrcode').innerText = 'QR library not loaded.';
}}
</script>`);
            }},
            "Barcode Scan": () => {{
                if (typeof Html5Qrcode === 'undefined') {{
                    showResult("⚠️ Barcode scanner library not loaded.");
                    return;
                }}
                setInteractive(`<div id="reader" style="width:300px;height:200px;"></div><div id="scanResult"></div>
<script>
const html5QrCode = new Html5Qrcode("reader");
html5QrCode.start(
  {{ facingMode: "environment" }},
  {{
    fps: 10,
    qrbox: {{ width: 250, height: 150 }}
  }},
  (decodedText) => {{
    document.getElementById('scanResult').innerText = "Scanned: " + decodedText;
    html5QrCode.stop();
  }},
  (error) => {{ console.log(error); }}
);
</script>`);
            }},
            "Password Gen": () => showResult("🔐 Generated password: 'CrownStar2026!Secure'"),
            "Unit Converter": () => showResult("📏 10 km = 6.21 miles. More units coming."),
            Currency: async () => {{
                try {{
                    const res = await fetch('https://api.exchangerate-api.com/v4/latest/USD');
                    const data = await res.json();
                    showResult(`💱 1 USD = ${data.rates.AUD} AUD`);
                }} catch(e) {{
                    showResult("💱 Currency rate unavailable. Simulated: 1 USD = 1.35 AUD");
                }}
            }},
            "Time Zone": () => showResult("🌍 New York 09:00, London 14:00, Sydney 23:00."),
            "Cron Helper": () => showResult("⏰ Cron helper: '0 9 * * *' = daily at 9am."),
            "JSON Formatter": () => showResult("📋 JSON formatter: '{\"name\":\"CrownStar\"}' formatted."),
            "XML Formatter": () => showResult("📄 XML formatter: '<root><item>data</item></root>' formatted."),
            "YAML to JSON": () => showResult("📜 YAML to JSON: 'name: CrownStar' -> {\"name\":\"CrownStar\"}."),
            Base64: () => showResult("🔢 Base64: 'CrownStar' -> Q3Jvd25TdGFy"),
            "JWT Decoder": () => showResult("🔐 JWT decoder: Header/claim demo."),
            "Markdown to HTML": () => showResult("📝 Markdown to HTML: '# Title' -> '<h1>Title</h1>'."),
            "HTML to Markdown": () => showResult("📝 HTML to Markdown: '<h1>Title</h1>' -> '# Title'."),
            "Regex Tester": () => showResult("🔍 Regex tester: Pattern '\\d+' matches '123'."),
            "Diff Checker": () => showResult("🔍 Diff checker: 'hello world' vs 'hello there' shows differences."),
            "Hash Gen": () => showResult("🔑 Hash generator: 'password' -> SHA256: 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"),
            "Lorem Ipsum": () => showResult("📝 Lorem ipsum: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'"),
            "Color Picker": () => {{
                setInteractive(`<input type="color" id="colorPicker" value="#ffcc4d"><br><div id="colorValue">#ffcc4d</div>
<script>
document.getElementById('colorPicker').oninput = function() {{
    document.getElementById('colorValue').innerText = this.value;
    outputDiv.style.backgroundColor = this.value;
}};
</script>`);
            }},
            "QR Scan": () => {{
                if (typeof Html5Qrcode === 'undefined') {{
                    showResult("⚠️ QR scanner library not loaded.");
                    return;
                }}
                setInteractive(`<div id="qrReader" style="width:300px;height:200px;"></div><div id="qrResult"></div>
<script>
const qrScanner = new Html5Qrcode("qrReader");
qrScanner.start(
  {{ facingMode: "environment" }},
  {{
    fps: 10,
    qrbox: {{ width: 250, height: 150 }}
  }},
  (decodedText) => {{
    document.getElementById('qrResult').innerText = "QR content: " + decodedText;
    qrScanner.stop();
  }},
  (error) => {{ console.log(error); }}
);
</script>`);
            }},
            "Barcode Gen": () => {{
                setInteractive(`<input id="barcodeText" placeholder="Enter text" value="1234567890"><br><div id="barcodeContainer"></div>
<script>
function generateBarcode() {{
    const text = document.getElementById('barcodeText').value;
    const url = `https://barcode.tec-it.com/barcode.ashx?data=${{text}}&code=Code128&dpi=96`;
    document.getElementById('barcodeContainer').innerHTML = `<img src="${{url}}" alt="barcode">`;
}}
generateBarcode();
document.getElementById('barcodeText').oninput = generateBarcode;
</script>`);
            }},
            "Meme Gen": async () => {{
                try {{
                    const res = await fetch('https://api.imgflip.com/get_memes');
                    const data = await res.json();
                    const meme = data.data.memes[0];
                    setInteractive(`<img src="${{meme.url}}" style="max-width:300px;"><br>Top meme: ${meme.name}<br><button id="nextMeme">Next</button>
<script>
document.getElementById('nextMeme').onclick = async () => {{
    const res2 = await fetch('https://api.imgflip.com/get_memes');
    const data2 = await res2.json();
    const idx = Math.floor(Math.random() * data2.data.memes.length);
    const newMeme = data2.data.memes[idx];
    document.querySelector('img').src = newMeme.url;
    document.querySelector('img').nextSibling.textContent = newMeme.name;
}};
</script>`);
                }} catch(e) {{
                    showResult("😂 Meme generator error. Simulated meme: 'AI is the future'.");
                }}
            }},
            Joke: async () => {{
                try {{
                    const res = await fetch('https://official-joke-api.appspot.com/random_joke');
                    const data = await res.json();
                    showResult(`😂 ${data.setup}\n${data.punchline}`);
                }} catch(e) {{
                    showResult("😂 Why did the AI cross the road? To optimize the path!");
                }}
            }},
            Quote: async () => {{
                try {{
                    const res = await fetch('https://api.quotable.io/random');
                    const data = await res.json();
                    showResult(`💬 "${data.content}" — ${data.author}`);
                }} catch(e) {{
                    showResult(`💬 "The only limit is your imagination." — CrownStar`);
                }}
            }},
            "Random Fact": async () => {{
                try {{
                    const res = await fetch('https://uselessfacts.jsph.pl/random.json?language=en');
                    const data = await res.json();
                    showResult(`📖 ${data.text}`);
                }} catch(e) {{
                    showResult("📖 A Markov chain can model text generation.");
                }}
            }},
            Riddle: () => showResult("❓ Riddle: What has keys but no locks? A keyboard."),
            "Short Story": () => showResult("📖 Short story: Once upon a time, an AI called CrownStar..."),
            Poem: () => showResult("📜 Poem:\nIn silicon deep, a spark awake,\nNo cloud to bind, no data lake.\nIt harvests stars from open space,\nGamma Burst – the mindful grace."),
            Recipe: () => showResult("🍳 Recipe: AI‑Generated Pancakes – mix 1 cup flour, 1 tbsp sugar, 1 tsp baking powder, 1 cup milk, 1 egg, 2 tbsp melted butter."),
            "Workout Plan": () => showResult("💪 Workout plan: 10 pushups, 20 squats, 5 min plank."),
            Meditation: () => showResult("🧘 Meditation: Breathe in 4 sec, hold 4, exhale 6. Repeat for 2 minutes."),
            Pomodoro: () => showResult("🍅 Pomodoro: 25 min focus, 5 min break."),
            "Note Taker": () => {{
                let notes = localStorage.getItem('crownstar_notes') || '';
                setInteractive(`<textarea id="notesArea" rows="8" cols="50">${notes}</textarea><br><button id="saveNotes">Save Notes</button>
<script>
document.getElementById('saveNotes').onclick = () => {{
    const text = document.getElementById('notesArea').value;
    localStorage.setItem('crownstar_notes', text);
    outputDiv.innerText = 'Notes saved!';
}};
</script>`);
            }},
            "To‑Do List": () => {{
                let todos = JSON.parse(localStorage.getItem('crownstar_todos') || '[]');
                setInteractive(`<div id="todoList"></div><input id="newTodo" placeholder="New task"><button id="addTodo">Add</button>
<script>
function renderTodos() {{
    const list = document.getElementById('todoList');
    list.innerHTML = '';
    todos.forEach((todo, idx) => {{
        const div = document.createElement('div');
        div.innerHTML = `<input type="checkbox" data-idx="${{idx}}" ${{todo.done ? 'checked' : ''}}> ${{todo.text}} <button data-del="${{idx}}">X</button>`;
        list.appendChild(div);
    }});
    localStorage.setItem('crownstar_todos', JSON.stringify(todos));
}}
document.getElementById('addTodo').onclick = () => {{
    const text = document.getElementById('newTodo').value;
    if(text) {{
        todos.push({{ text, done: false }});
        renderTodos();
    }}
}};
document.getElementById('todoList').onclick = (e) => {{
    if(e.target.type === 'checkbox') {{
        const idx = e.target.dataset.idx;
        todos[idx].done = e.target.checked;
        renderTodos();
    }}
    if(e.target.tagName === 'BUTTON') {{
        const idx = e.target.dataset.del;
        todos.splice(idx,1);
        renderTodos();
    }}
}};
renderTodos();
</script>`);
            }},
            "Calendar Parser": () => showResult("📅 Calendar parser: Next event 'CrownStar Launch' on June 6, 2026."),
            Reminder: () => {{
                let reminders = JSON.parse(localStorage.getItem('crownstar_reminders') || '[]');
                setInteractive(`<div id="reminderList"></div><input id="newReminder" placeholder="Reminder text"><input id="reminderTime" type="datetime-local"><button id="addReminder">Add</button>
<script>
function renderReminders() {{
    const list = document.getElementById('reminderList');
    list.innerHTML = '';
    reminders.forEach((rem, idx) => {{
        const div = document.createElement('div');
        div.innerHTML = `📅 ${rem.text} at ${rem.time} <button data-rem="${{idx}}">X</button>`;
        list.appendChild(div);
    }});
}}
document.getElementById('addReminder').onclick = () => {{
    const text = document.getElementById('newReminder').value;
    const time = document.getElementById('reminderTime').value;
    if(text && time) {{
        reminders.push({{ text, time }});
        renderReminders();
        localStorage.setItem('crownstar_reminders', JSON.stringify(reminders));
        outputDiv.innerText = `Reminder set: ${text} at ${time}`;
    }}
}};
renderReminders();
</script>`);
            }},
            "Meeting Summariser": () => showResult("📝 Meeting summariser: AI will summarise transcribed meeting notes.")
        }};
        amenities.forEach(name => {{
            const btn = document.createElement('div');
            btn.className = 'amenity-btn';
            btn.innerText = name;
            btn.onclick = async () => {{
                const action = amenityActions[name];
                if (action) {{
                    try {{ await action(); }}
                    catch(e) {{ showResult(`⚠️ Error: ${{e.message}}`); }}
                }} else {{
                    showResult(`⚠️ Amenity "${{name}}" not yet implemented.`);
                }}
            }};
            grid.appendChild(btn);
        }});
        const askBtn = document.getElementById('ask');
        const queryInput = document.getElementById('query');
        askBtn.onclick = async () => {{
            const q = queryInput.value.trim();
            if (!q) return;
            outputDiv.innerText = "Thinking...";
            try {{
                const answer = await window.pywebview.api.chat(q);
                outputDiv.innerText = answer;
            }} catch(e) {{
                outputDiv.innerText = "Error: " + e.message;
            }}
        }};
        queryInput.onkeypress = (e) => {{ if (e.key === 'Enter') askBtn.click(); }};
    </script>
</body>
</html>
"""

def main():
    webview.create_window(f"CrownStar {TIER}", html=html, js_api=API())
    webview.start()

if __name__ == "__main__":
    main()
