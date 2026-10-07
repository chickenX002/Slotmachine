from flask import Flask, request, jsonify, render_template_string
from pathlib import Path
from datetime import datetime
import json

app = Flask(__name__)

LEADERBOARD_FILE = Path("leaderboard.json")

# --------------------------------------------------
# PAYTABLE
# --------------------------------------------------

PAYOUTS = {
    "🍒": 4,
    "💎": 8,
    "7️⃣": 10,
    "🍋": 2,
    "🍊": 2,
}

SYMBOLS = ["🍒", "💎", "7️⃣", "🍋", "🍊"]


# --------------------------------------------------
# LEADERBOARD
# --------------------------------------------------

def load_leaderboard():
    if not LEADERBOARD_FILE.exists():
        return []

    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

    except (json.JSONDecodeError, OSError):
        pass

    return []


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


# --------------------------------------------------
# HTML
# --------------------------------------------------

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Midnight Pizzeria</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    min-height: 100vh;
    background:
        radial-gradient(circle at top, #35104d 0%, #130b1d 45%, #050509 100%);
    color: white;
    font-family: Arial, Helvetica, sans-serif;
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
            rgba(255,255,255,0.015) 0px,
            rgba(255,255,255,0.015) 1px,
            transparent 1px,
            transparent 4px
        );
}

.container {
    width: min(1100px, 94%);
    margin: auto;
    padding: 30px 0 50px;
}

.header {
    text-align: center;
    margin-bottom: 25px;
}

.header h1 {
    margin: 0;
    font-size: clamp(34px, 7vw, 70px);
    color: #ff315f;
    text-shadow:
        0 0 5px #ff315f,
        0 0 20px #ff315f,
        0 0 40px #8c1740;
    letter-spacing: 4px;
}

.header p {
    color: #bcb1c7;
    margin-top: 8px;
}

.panel {
    background: rgba(12, 9, 19, 0.93);
    border: 2px solid #6e234f;
    border-radius: 18px;
    box-shadow:
        0 0 20px rgba(255, 25, 100, 0.12),
        inset 0 0 30px rgba(0, 0, 0, 0.6);
    padding: 25px;
    margin-bottom: 25px;
}

.name-section {
    text-align: center;
}

.name-section label {
    display: block;
    color: #c9bdcf;
    margin-bottom: 8px;
}

#playerName {
    width: min(400px, 100%);
    padding: 13px 16px;
    border-radius: 10px;
    border: 1px solid #7f3561;
    background: #09070d;
    color: white;
    font-size: 18px;
    outline: none;
}

#playerName:focus {
    border-color: #ff315f;
    box-shadow: 0 0 12px rgba(255, 49, 95, 0.35);
}

.machine {
    max-width: 850px;
    margin: auto;
    padding: 25px;
    border-radius: 25px;
    border: 5px solid #481a35;
    background:
        linear-gradient(145deg, #32152b, #100b13);
    box-shadow:
        0 0 35px rgba(255, 30, 90, 0.2),
        inset 0 0 40px rgba(0, 0, 0, 0.8);
}

.machine-top {
    text-align: center;
    color: #ffcc44;
    font-size: 18px;
    font-weight: bold;
    letter-spacing: 3px;
    margin-bottom: 18px;
}

.slots {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    background: #050408;
    padding: 18px;
    border-radius: 18px;
    border: 3px solid #7b315c;
}

.reel {
    height: 160px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 14px;
    background:
        radial-gradient(circle, #29202d, #0b090e);
    border: 3px solid #4e3451;
    font-size: clamp(60px, 10vw, 100px);
    box-shadow:
        inset 0 0 30px #000,
        0 0 12px rgba(255,255,255,0.04);
    user-select: none;
}

.reel.spinning {
    animation: shake 0.08s infinite;
}

@keyframes shake {
    0% {
        transform: translateY(-3px);
    }

    50% {
        transform: translateY(3px);
    }

    100% {
        transform: translateY(-3px);
    }
}

.spin-area {
    text-align: center;
    margin-top: 22px;
}

#spinButton {
    border: none;
    border-radius: 14px;
    padding: 17px 55px;
    font-size: 25px;
    font-weight: bold;
    color: white;
    background: linear-gradient(180deg, #ff3765, #a30f42);
    cursor: pointer;
    box-shadow:
        0 6px 0 #5a0a27,
        0 0 25px rgba(255, 30, 90, 0.3);
    transition: transform 0.1s, filter 0.2s;
}

#spinButton:hover {
    filter: brightness(1.2);
}

#spinButton:active {
    transform: translateY(5px);
    box-shadow:
        0 1px 0 #5a0a27,
        0 0 20px rgba(255, 30, 90, 0.3);
}

#spinButton:disabled {
    cursor: not-allowed;
    filter: grayscale(0.7);
    opacity: 0.6;
}

.message {
    min-height: 35px;
    margin-top: 20px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
}

.win {
    color: #ffe36e;
    text-shadow: 0 0 15px #ffb300;
}

.lose {
    color: #aaa;
}

.jackpot {
    animation: jackpot 0.35s infinite alternate;
}

@keyframes jackpot {
    from {
        transform: scale(1);
    }

    to {
        transform: scale(1.08);
    }
}

.bottom-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 25px;
}

.panel h2 {
    margin-top: 0;
    color: #ff4d75;
    text-align: center;
}

.paytable {
    width: 100%;
    border-collapse: collapse;
}

.paytable th,
.paytable td {
    padding: 12px;
    border-bottom: 1px solid #302333;
    text-align: center;
}

.paytable th {
    color: #aaa0b1;
}

.multiplier {
    color: #ffd44d;
    font-weight: bold;
}

.leaderboard {
    width: 100%;
    border-collapse: collapse;
}

.leaderboard th,
.leaderboard td {
    padding: 10px;
    text-align: center;
    border-bottom: 1px solid #302333;
}

.leaderboard th {
    color: #aaa0b1;
}

.rank-1 {
    color: #ffd700;
}

.rank-2 {
    color: #c0c0c0;
}

.rank-3 {
    color: #cd7f32;
}

.empty {
    text-align: center;
    color: #777;
    padding: 25px;
}

.footer {
    text-align: center;
    color: #655b6a;
    margin-top: 25px;
    font-size: 13px;
}

@media (max-width: 700px) {

    .bottom-grid {
        grid-template-columns: 1fr;
    }

    .machine {
        padding: 15px;
    }

    .slots {
        gap: 8px;
        padding: 10px;
    }

    .reel {
        height: 120px;
    }

    #spinButton {
        width: 100%;
    }
}

</style>
</head>

<body>

<div class="container">

    <div class="header">
        <h1>MIDNIGHT PIZZERIA</h1>
        <p>Something is watching from behind the reels...</p>
    </div>

    <div class="panel name-section">

        <label for="playerName">
            Enter your player name
        </label>

        <input
            id="playerName"
            maxlength="20"
            placeholder="Your name..."
            autocomplete="off"
        >

    </div>

    <div class="machine">

        <div class="machine-top">
            ★ HAUNTED JACKPOT ★
        </div>

        <div class="slots">

            <div class="reel" id="reel1">🍒</div>
            <div class="reel" id="reel2">🍒</div>
            <div class="reel" id="reel3">🍒</div>

        </div>

        <div class="spin-area">

            <button id="spinButton">
                SPIN
            </button>

            <div class="message" id="message">
                Press SPIN to begin...
            </div>

        </div>

    </div>

    <div class="bottom-grid">

        <div class="panel">

            <h2>PAYTABLE</h2>

            <table class="paytable">

                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Reward</th>
                    </tr>
                </thead>

                <tbody>

                    <tr>
                        <td>🍒 🍒 🍒</td>
                        <td class="multiplier">4×</td>
                    </tr>

                    <tr>
                        <td>💎 💎 💎</td>
                        <td class="multiplier">8×</td>
                    </tr>

                    <tr>
                        <td>7️⃣ 7️⃣ 7️⃣</td>
                        <td class="multiplier">10×</td>
                    </tr>

                    <tr>
                        <td>🍋 🍋 🍋</td>
                        <td class="multiplier">2×</td>
                    </tr>

                    <tr>
                        <td>🍊 🍊 🍊</td>
                        <td class="multiplier">2×</td>
                    </tr>

                </tbody>

            </table>

            <p style="text-align:center;color:#777;">
                Free-play event machine — no real money.
            </p>

        </div>

        <div class="panel">

            <h2>🏆 BIGGEST JACKPOTS</h2>

            <div id="leaderboard">
                Loading...
            </div>

        </div>

    </div>

    <div class="footer">
        Midnight Pizzeria • Free Play
    </div>

</div>


<script>

const symbols = ["🍒", "💎", "7️⃣", "🍋", "🍊"];

const payouts = {
    "🍒": 4,
    "💎": 8,
    "7️⃣": 10,
    "🍋": 2,
    "🍊": 2
};

const reels = [
    document.getElementById("reel1"),
    document.getElementById("reel2"),
    document.getElementById("reel3")
];

const spinButton = document.getElementById("spinButton");
const message = document.getElementById("message");
const nameInput = document.getElementById("playerName");

let spinning = false;


function randomSymbol() {
    const index = Math.floor(Math.random() * symbols.length);
    return symbols[index];
}


function sleep(milliseconds) {
    return new Promise(resolve => {
        setTimeout(resolve, milliseconds);
    });
}


async function spinReel(reel, duration) {

    reel.classList.add("spinning");

    const start = Date.now();

    while (Date.now() - start < duration) {

        reel.textContent = randomSymbol();

        await sleep(75);
    }

    reel.classList.remove("spinning");

    const result = randomSymbol();
    reel.textContent = result;

    return result;
}


async function spin() {

    if (spinning) {
        return;
    }

    let playerName = nameInput.value.trim();

    if (!playerName) {
        playerName = "Anonymous";
    }

    spinning = true;
    spinButton.disabled = true;

    message.className = "message";
    message.textContent = "The machine is watching...";

    const results = await Promise.all([
        spinReel(reels[0], 1000),
        spinReel(reels[1], 1500),
        spinReel(reels[2], 2000)
    ]);

    const [a, b, c] = results;

    let score = 0;

    if (a === b && b === c) {

        const multiplier = payouts[a];

        score = multiplier * 100;

        message.className = "message win jackpot";

        message.textContent =
            "JACKPOT! " +
            a + " " + a + " " + a +
            " — " + multiplier + "× = " +
            score + " POINTS!";

        await saveScore(
            playerName,
            score,
            a + " " + a + " " + a
        );

    } else {

        message.className = "message lose";

        message.textContent =
            "No jackpot... Try again.";

    }

    await loadLeaderboard();

    spinning = false;
    spinButton.disabled = false;
}


async function saveScore(name, score, combination) {

    try {

        await fetch("/api/score", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                name: name,
                score: score,
                combination: combination
            })
        });

    } catch (error) {

        console.error("Could not save score:", error);

    }
}


async function loadLeaderboard() {

    const leaderboard = document.getElementById("leaderboard");

    try {

        const response = await fetch("/api/leaderboard");

        const data = await response.json();

        if (!data.length) {

            leaderboard.innerHTML =
                '<div class="empty">No jackpots yet...</div>';

            return;
        }

        let html = `
            <table class="leaderboard">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Player</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
        `;

        data.forEach((entry, index) => {

            let rankClass = "";

            if (index === 0) {
                rankClass = "rank-1";
            } else if (index === 1) {
                rankClass = "rank-2";
            } else if (index === 2) {
                rankClass = "rank-3";
            }

            html += `
                <tr class="${rankClass}">
                    <td>${index + 1}</td>
                    <td>${escapeHtml(entry.name)}</td>
                    <td>${entry.score}</td>
                </tr>
            `;
        });

        html += `
                </tbody>
            </table>
        `;

        leaderboard.innerHTML = html;

    } catch (error) {

        leaderboard.innerHTML =
            '<div class="empty">Leaderboard unavailable.</div>';

        console.error(error);
    }
}


function escapeHtml(value) {

    const div = document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}


spinButton.addEventListener("click", spin);

nameInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        spin();
    }

});


loadLeaderboard();

</script>

</body>
</html>
"""


# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/api/leaderboard", methods=["GET"])
def leaderboard():
    data = load_leaderboard()

    data.sort(
        key=lambda entry: entry.get("score", 0),
        reverse=True
    )

    return jsonify(data[:50])


@app.route("/api/score", methods=["POST"])
def add_score():

    request_data = request.get_json(silent=True)

    if not isinstance(request_data, dict):
        return jsonify({
            "success": False,
            "error": "Invalid request."
        }), 400

    name = str(request_data.get("name", "Anonymous")).strip()
    combination = str(
        request_data.get("combination", "")
    ).strip()

    try:
        score = int(request_data.get("score", 0))
    except (TypeError, ValueError):
        score = 0

    if not name:
        name = "Anonymous"

    name = name[:20]

    # Only allow legitimate jackpot values.
    if score not in [200, 400, 800, 1000]:
        return jsonify({
            "success": False,
            "error": "Invalid score."
        }), 400

    entry = {
        "name": name,
        "score": score,
        "combination": combination,
        "date": datetime.now().isoformat(timespec="seconds")
    }

    data = load_leaderboard()

    data.append(entry)

    data.sort(
        key=lambda item: item.get("score", 0),
        reverse=True
    )

    data = data[:50]

    save_leaderboard(data)

    return jsonify({
        "success": True
    })


# --------------------------------------------------
# START SERVER
# --------------------------------------------------

if __name__ == "__main__":

    print("")
    print("======================================")
    print("       MIDNIGHT PIZZERIA SLOTS")
    print("======================================")
    print("")
    print("Open this in your browser:")
    print("http://127.0.0.1:5000")
    print("")
    print("For another device on your network:")
    print("http://YOUR-PC-IP:5000")
    print("")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )