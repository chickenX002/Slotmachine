from pathlib import Path

code = r'''from flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "leaderboard.json"

# Imaginary/free-play multipliers
MULTIPLIERS = {
    "🍒": 4,
    "💎": 8,
    "7️⃣": 10,
    "🍋": 2,
    "🍊": 2,
}

SYMBOLS = ["🍒", "🍋", "🍊", "🍉", "⭐", "💎", "7️⃣"]


def load_leaderboard():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_leaderboard(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Midnight Pizzeria — Haunted Slots</title>

<style>
* { box-sizing: border-box; }

:root {
    --red: #d71920;
    --dark-red: #65060b;
    --gold: #ffc400;
    --green: #49ff7a;
    --purple: #8a2be2;
}

body {
    margin: 0;
    min-height: 100vh;
    color: #eee;
    font-family: Arial, Helvetica, sans-serif;
    background:
        radial-gradient(circle at 50% 30%, #32103f 0%, #100818 38%, #030305 80%);
    overflow-x: hidden;
}

body::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background:
        repeating-linear-gradient(
            0deg,
            rgba(255,255,255,.025) 0,
            rgba(255,255,255,.025) 1px,
            transparent 1px,
            transparent 4px
        );
    mix-blend-mode: screen;
}

header {
    text-align: center;
    padding: 25px 15px 5px;
}

.warning {
    color: #ff3333;
    font-weight: 900;
    letter-spacing: 5px;
    font-size: 12px;
    text-transform: uppercase;
    text-shadow: 0 0 12px red;
}

h1 {
    margin: 7px 0;
    font-size: clamp(30px, 8vw, 58px);
    color: #f4c542;
    text-shadow:
        3px 3px 0 #4b0505,
        0 0 18px #ff7b00;
}

.subtitle {
    color: #aaa;
    font-size: 14px;
}

.layout {
    width: min(1200px, 96vw);
    margin: 15px auto 40px;
    display: grid;
    grid-template-columns: minmax(0, 1.5fr) minmax(280px, .8fr);
    gap: 18px;
}

.panel {
    background: linear-gradient(145deg, #171019, #08070b);
    border: 2px solid #5a171c;
    border-radius: 18px;
    box-shadow:
        0 0 30px rgba(0,0,0,.8),
        inset 0 0 30px rgba(255,0,0,.04);
}

.machine {
    padding: 20px;
}

.machine-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    margin-bottom: 15px;
}

.machine-label {
    color: #ff3434;
    font-size: 13px;
    font-weight: 900;
    letter-spacing: 2px;
}

.status {
    color: #5cff83;
    font-size: 11px;
    font-weight: bold;
}

.reels {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    background: #020202;
    padding: 14px;
    border: 4px solid #301015;
    border-radius: 14px;
    box-shadow: inset 0 0 35px #000;
}

.reel {
    height: clamp(120px, 20vw, 190px);
    background: linear-gradient(#fff, #bdbdbd);
    border: 5px solid #292929;
    border-radius: 12px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: clamp(55px, 10vw, 95px);
    user-select: none;
    color: #111;
    overflow: hidden;
    box-shadow:
        inset 0 0 25px rgba(0,0,0,.5),
        0 0 10px rgba(255,255,255,.1);
}

.reel.spinning {
    animation: jitter .07s infinite;
}

@keyframes jitter {
    0% { transform: translateY(-3px); }
    50% { transform: translateY(3px); }
    100% { transform: translateY(-3px); }
}

.controls {
    margin-top: 18px;
    text-align: center;
}

.player-row {
    display: flex;
    gap: 8px;
    margin-bottom: 10px;
}

input {
    min-width: 0;
    flex: 1;
    padding: 13px;
    border-radius: 10px;
    border: 1px solid #71323a;
    background: #0b090d;
    color: white;
    outline: none;
}

input:focus {
    border-color: #ff3c3c;
}

button {
    cursor: pointer;
    font-weight: 900;
}

#spinButton {
    width: 90%;
    padding: 18px;
    border: 3px solid #ff9a9a;
    border-radius: 50px;
    background: linear-gradient(#ef3038, #8b080d);
    color: white;
    font-size: 25px;
    letter-spacing: 3px;
    box-shadow: 0 7px 0 #3c0306, 0 0 25px rgba(255,0,0,.3);
}

#spinButton:hover {
    filter: brightness(1.2);
}

#spinButton:active {
    transform: translateY(5px);
    box-shadow: 0 2px 0 #3c0306;
}

#spinButton:disabled {
    opacity: .5;
    cursor: not-allowed;
}

.result {
    min-height: 45px;
    padding-top: 16px;
    font-size: 22px;
    font-weight: 900;
}

.win {
    color: #ffd43b;
    animation: flash .25s infinite alternate;
}

@keyframes flash {
    from { transform: scale(1); text-shadow: 0 0 8px #ff8c00; }
    to { transform: scale(1.08); text-shadow: 0 0 25px #fff; }
}

.side {
    display: flex;
    flex-direction: column;
    gap: 18px;
}

.box {
    padding: 18px;
}

.box h2 {
    margin: 0 0 12px;
    color: #f3c44d;
    font-size: 18px;
}

.paytable {
    width: 100%;
    border-collapse: collapse;
}

.paytable td {
    padding: 8px 4px;
    border-bottom: 1px solid #2b2025;
}

.paytable td:last-child {
    text-align: right;
    color: #59ff7e;
    font-weight: bold;
}

.leaderboard {
    max-height: 400px;
    overflow-y: auto;
}

.leader {
    display: grid;
    grid-template-columns: 35px 1fr auto;
    gap: 8px;
    align-items: center;
    padding: 10px 4px;
    border-bottom: 1px solid #2b2025;
}

.rank {
    color: #ffb900;
    font-weight: 900;
}

.score {
    color: #5cff83;
    font-weight: 900;
}

.small {
    color: #888;
    font-size: 11px;
}

.warning-box {
    color: #bbb;
    font-size: 12px;
    line-height: 1.5;
}

.empty {
    color: #777;
    padding: 10px 0;
}

.eyes {
    position: fixed;
    right: 5vw;
    top: 8vh;
    font-size: 24px;
    opacity: .15;
    letter-spacing: 10px;
    pointer-events: none;
}

.scan {
    position: fixed;
    left: 0;
    right: 0;
    height: 2px;
    background: rgba(255,30,30,.12);
    pointer-events: none;
    animation: scan 5s linear infinite;
}

@keyframes scan {
    from { top: 0; }
    to { top: 100vh; }
}

@media (max-width: 800px) {
    .layout {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 500px) {
    .machine {
        padding: 12px;
    }

    .reels {
        gap: 6px;
        padding: 8px;
    }

    .reel {
        height: 105px;
    }

    #spinButton {
        width: 100%;
        font-size: 20px;
    }
}
</style>
</head>

<body>

<div class="eyes">● ●</div>
<div class="scan"></div>

<header>
    <div class="warning">⚠ NIGHT SHIFT TERMINAL ⚠</div>
    <h1>🎃 MIDNIGHT PIZZERIA 🎃</h1>
    <div class="subtitle">HAUNTED ANIMATRONIC SLOT MACHINE • FREE PLAY</div>
</header>

<div class="layout">

    <main class="panel machine">

        <div class="machine-top">
            <div class="machine-label">UNIT #13 — ARCADE TERMINAL</div>
            <div class="status">● ONLINE</div>
        </div>

        <div class="reels">
            <div class="reel" id="reel1">🍒</div>
            <div class="reel" id="reel2">🍋</div>
            <div class="reel" id="reel3">🍊</div>
        </div>

        <div class="controls">

            <div class="player-row">
                <input id="playerName" maxlength="20"
                       placeholder="Enter player name">
            </div>

            <button id="spinButton" onclick="spin()">
                SPIN 🎰
            </button>

            <div id="result" class="result">
                Insert your name and survive the night...
            </div>

        </div>

    </main>

    <aside class="side">

        <section class="panel box">
            <h2>🎃 PAYTABLE</h2>

            <table class="paytable">
                <tr><td>🍒 🍒 🍒</td><td>4×</td></tr>
                <tr><td>💎 💎 💎</td><td>8×</td></tr>
                <tr><td>7️⃣ 7️⃣ 7️⃣</td><td>10×</td></tr>
                <tr><td>🍋 🍋 🍋</td><td>2×</td></tr>
                <tr><td>🍊 🍊 🍊</td><td>2×</td></tr>
            </table>

            <div class="small" style="margin-top:10px">
                Base jackpot value: 100 imaginary points.
            </div>
        </section>

        <section class="panel box">
            <h2>🏆 BIGGEST JACKPOTS</h2>
            <div id="leaderboard" class="leaderboard">
                <div class="empty">Loading...</div>
            </div>
        </section>

        <section class="panel box warning-box">
            <b style="color:#ff4545">⚠ EVENT MODE</b><br><br>
            This machine uses imaginary points only.
            There are no purchases, deposits, cash prizes,
            or real-money wagers.
        </section>

    </aside>

</div>

<script>
const symbols = ["🍒", "🍋", "🍊", "🍉", "⭐", "💎", "7️⃣"];

const reels = [
    document.getElementById("reel1"),
    document.getElementById("reel2"),
    document.getElementById("reel3")
];

const button = document.getElementById("spinButton");
const result = document.getElementById("result");
const nameInput = document.getElementById("playerName");

let spinning = false;
let audioContext = null;

const multipliers = {
    "🍒": 4,
    "💎": 8,
    "7️⃣": 10,
    "🍋": 2,
    "🍊": 2
};

function audio() {
    if (!audioContext) {
        const AC = window.AudioContext || window.webkitAudioContext;
        if (AC) audioContext = new AC();
    }

    if (audioContext && audioContext.state === "suspended") {
        audioContext.resume();
    }

    return audioContext;
}

function beep(freq, duration, type="square", volume=.045) {
    const ctx = audio();
    if (!ctx) return;

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = type;
    osc.frequency.value = freq;

    gain.gain.setValueAtTime(volume, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(
        .001,
        ctx.currentTime + duration
    );

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start();
    osc.stop(ctx.currentTime + duration);
}

function randomSymbol() {
    return symbols[Math.floor(Math.random() * symbols.length)];
}

function animateReel(reel, duration) {
    return new Promise(resolve => {
        reel.classList.add("spinning");

        const interval = setInterval(() => {
            reel.textContent = randomSymbol();
            beep(100 + Math.random() * 80, .025, "square", .015);
        }, 75);

        setTimeout(() => {
            clearInterval(interval);
            reel.textContent = randomSymbol();
            reel.classList.remove("spinning");
            beep(320, .08, "square", .05);
            resolve();
        }, duration);
    });
}

function winSound(big=false) {
    const notes = big
        ? [392, 523, 659, 784, 1046, 1318]
        : [523, 659, 784, 1046];

    notes.forEach((n, i) => {
        setTimeout(() => beep(n, .18, "triangle", .07), i * 120);
    });
}

function coins() {
    for (let i = 0; i < 30; i++) {
        const c = document.createElement("div");
        c.textContent = Math.random() > .5 ? "🪙" : "🎃";
        c.style.position = "fixed";
        c.style.left = Math.random() * 100 + "vw";
        c.style.top = "-30px";
        c.style.zIndex = 999;
        c.style.fontSize = "25px";
        c.style.pointerEvents = "none";
        c.style.transition = "transform 1.5s linear, opacity 1.5s";

        document.body.appendChild(c);

        requestAnimationFrame(() => {
            c.style.transform =
                `translateY(${window.innerHeight + 80}px) rotate(${Math.random()*720}deg)`;
            c.style.opacity = "0";
        });

        setTimeout(() => c.remove(), 1800);
    }
}

async function spin() {
    if (spinning) return;

    let player = nameInput.value.trim();

    if (!player) {
        nameInput.focus();
        result.textContent = "Enter a player name first...";
        return;
    }

    spinning = true;
    button.disabled = true;
    result.classList.remove("win");
    result.textContent = "The animatronic is watching...";

    audio();

    beep(130, .12, "sawtooth", .06);

    const r1 = animateReel(reels[0], 1200);
    const r2 = animateReel(reels[1], 1800);
    const r3 = animateReel(reels[2], 2400);

    await Promise.all([r1, r2, r3]);

    const values = reels.map(r => r.textContent);

    checkResult(player, values);

    spinning = false;
    button.disabled = false;
}

async function checkResult(player, values) {
    const [a,b,c] = values;

    if (a === b && b === c && multipliers[a]) {

        const multiplier = multipliers[a];
        const jackpot = 100 * multiplier;

        result.classList.add("win");

        if (a === "7️⃣") {
            result.textContent =
                `💀 10× MEGA JACKPOT — ${jackpot} POINTS! 💀`;
        } else if (a === "💎") {
            result.textContent =
                `💎 8× DIAMOND JACKPOT — ${jackpot} POINTS! 💎`;
        } else if (a === "🍒") {
            result.textContent =
                `🍒 4× CHERRY JACKPOT — ${jackpot} POINTS! 🍒`;
        } else {
            result.textContent =
                `${a} ${a} ${a} — ${multiplier}× JACKPOT — ${jackpot} POINTS!`;
        }

        winSound(multiplier >= 8);
        coins();

        await fetch("/api/score", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                name: player,
                score: jackpot,
                combination: values.join(" ")
            })
        });

        loadLeaderboard();

    } else if (a === b || b === c || a === c) {

        result.textContent = "👁 Something is watching...";

        beep(180, .3, "sawtooth", .05);

    } else {

        result.textContent = "Nothing but static... 🎃";
    }
}

async function loadLeaderboard() {
    try {
        const response = await fetch("/api/leaderboard");
        const data = await response.json();

        const board = document.getElementById("leaderboard");

        if (!data.length) {
            board.innerHTML =
                '<div class="empty">No jackpots yet. Be the first.</div>';
            return;
        }

        board.innerHTML = data.map((item, index) => `
            <div class="leader">
                <div class="rank">#${index + 1}</div>
                <div>
                    <b>${escapeHtml(item.name)}</b>
                    <div class="small">${escapeHtml(item.combination)}</div>
                </div>
                <div class="score">${item.score}</div>
            </div>
        `).join("");

    } catch (e) {
        document.getElementById("leaderboard").innerHTML =
            '<div class="empty">Leaderboard unavailable.</div>';
    }
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

document.addEventListener("keydown", event => {
    if (event.code === "Space") {
        event.preventDefault();
        if (!spinning) spin();
    }
});

loadLeaderboard();
setInterval(loadLeaderboard, 3000);
</script>

</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/api/leaderboard")
def leaderboard():
    data = load_leaderboard()
    data.sort(key=lambda x: x.get("score", 0), reverse=True)
    return jsonify(data[:50])


@app.route("/api/score", methods=["POST"])
def add_score():
    payload = request.get_json(silent=True) or {}

    name = str(payload.get("name", "Player")).strip()[:20]
    combination = str(payload.get("combination", ""))[:50]

    try:
        score = int(payload.get("score", 0))
    except (ValueError, TypeError):
        score = 0

    # Only allow the server to store legitimate jackpot values.
    allowed_scores = {200, 400, 800, 1000}

    if not name or score not in allowed_scores:
        return jsonify({"ok": False}), 400

    data = load_leaderboard()

    data.append({
        "name": name,
        "score": score,
        "combination": combination,
        "time": datetime.now().isoformat(timespec="seconds")
    })

    data.sort(key=lambda x: x.get("score", 0), reverse=True)

    # Keep the 50 biggest jackpots.
    data = data[:50]

    save_leaderboard(data)

    return jsonify({"ok": True})


if __name__ == "__main__":
    print()
    print("==============================================")
    print("       MIDNIGHT PIZZERIA — HAUNTED SLOTS")
    print("==============================================")
    print()
    print("Open: http://127.0.0.1:5000")
    print("For another device on the same network,")
    print("use your computer's local IP address.")
    print()
    print("Leaderboard is saved to leaderboard.json")
    print("Press CTRL+C to stop.")
    print()

    app.run(host="0.0.0.0", port=5000, debug=False)
'''

requirements = "Flask>=3.0.0\n"

Path("/mnt/data/haunted_slot_machine.py").write_text(code, encoding="utf-8")
Path("/mnt/data/requirements.txt").write_text(requirements, encoding="utf-8")

print("Created:")
print("/mnt/data/haunted_slot_machine.py")
print("/mnt/data/requirements.txt")
