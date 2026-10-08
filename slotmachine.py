from flask import Flask, jsonify, render_template_string
from datetime import datetime
import random

app = Flask(__name__)

# ============================================================
# SETTINGS
# ============================================================

SYMBOLS = ["🍒", "💎", "7", "🍋", "🍊"]

# Normal symbol weights (Higher = more common)
# These keep jackpots rare and mathematically balanced.
SYMBOL_WEIGHTS = {
    "🍒": 28,
    "🍋": 25,
    "🍊": 25,
    "💎": 12,
    "7": 10,
}

# Jackpot multipliers
JACKPOTS = {
    "🍒": ("CHERRY JACKPOT", 4),
    "💎": ("DIAMOND JACKPOT", 8),
    "7": ("SEVEN JACKPOT", 10),
    "🍋": ("LEMON JACKPOT", 2),
    "🍊": ("ORANGE JACKPOT", 2),
}

DOUBLE_MULTIPLIER = 1.5

# In-memory event feed.
jackpot_feed = []


# ============================================================
# RANDOM SYMBOL
# ============================================================

def random_symbol():
    symbols = list(SYMBOL_WEIGHTS.keys())
    weights = list(SYMBOL_WEIGHTS.values())

    # FIXED: Extract index 0 to get the raw symbol string instead of a list object
    return random.choices(
        symbols,
        weights=weights,
        k=1
    )[0]


# ============================================================
# SERVER-SIDE SPIN
# ============================================================

def create_spin_result():
    """
    Generates three individual symbols completely independently.
    The server controls the result entirely.
    """
    return [
        random_symbol(),
        random_symbol(),
        random_symbol()
    ]


# ============================================================
# DETERMINE RESULT
# ============================================================

def evaluate_spin(result):
    a, b, c = result

    # Three of a kind
    if a == b == c:
        name, multiplier = JACKPOTS[a]
        return {
            "type": "jackpot",
            "name": name,
            "multiplier": multiplier,
            "message": f"{name} — {multiplier}×"
        }

    # Two of a kind
    if a == b or a == c or b == c:
        return {
            "type": "double",
            "name": "DOUBLE MATCH",
            "multiplier": DOUBLE_MULTIPLIER,
            "message": f"DOUBLE MATCH — {DOUBLE_MULTIPLIER}×"
        }

    # Nothing
    return {
        "type": "nothing",
        "name": "",
        "multiplier": 0,
        "message": "NOTHING... THE MACHINE STARES BACK."
    }


# ============================================================
# ADD EVENT TO FEED
# ============================================================

def add_feed_event(result):
    event = {
        "name": result["name"],
        "multiplier": result["multiplier"],
        "time": datetime.now().isoformat()
    }
    jackpot_feed.insert(0, event)
    del jackpot_feed[50:]


# ============================================================
# FLASK ROUTES
# ============================================================

@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/spin", methods=["POST"])
def spin():
    result_reels = create_spin_result()
    evaluation = evaluate_spin(result_reels)
    
    if evaluation["type"] != "nothing":
        add_feed_event(evaluation)
        
    return jsonify({
        "reels": result_reels,
        "outcome": evaluation
    })


@app.route("/feed", methods=["GET"])
def get_feed():
    return jsonify(jackpot_feed)


# ============================================================
# HTML & FRONTEND UI
# ============================================================

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>THE NIGHT SHIFT — SLOT MACHINE</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Georgia, "Times New Roman", serif;
            background: radial-gradient(circle at center, #241522 0%, #110b12 45%, #040405 100%);
            color: #d0c6ca;
            overflow: hidden;
            position: relative;
        }

        /* CRT Scanlines Overlay */
        body::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 100;
            background: repeating-linear-gradient(
                0deg,
                rgba(255,255,255,0.018),
                rgba(255,255,255,0.018) 1px,
                transparent 1px,
                transparent 4px
            );
            opacity: 0.45;
        }

        /* Dark Vignette Edges */
        body::after {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 99;
            box-shadow: inset 0 0 180px rgba(0,0,0,0.95);
        }

        .machine {
            width: min(92vw, 650px);
            padding: 30px;
            border-radius: 30px;
            background: linear-gradient(145deg, #2d182b, #190c18);
            box-shadow: 
                0 0 30px rgba(184, 0, 116, 0.25),
                inset 0 0 15px rgba(255, 255, 255, 0.05);
            border: 4px solid #42263f;
            text-align: center;
            z-index: 10;
        }

        .title {
            font-size: clamp(24px, 6vw, 42px);
            font-weight: 900;
            letter-spacing: 4px;
            color: #fff;
            text-shadow: 0 0 15px rgba(255,255,255,0.5);
            margin-bottom: 18px;
        }

        .reels {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            padding: 20px;
            background: #090609;
            border: 4px solid #1c0e1a;
            border-radius: 18px;
            box-shadow: inset 0 0 25px #000;
        }

        .reel {
            height: 145px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            border-radius: 12px;
            background: linear-gradient(#1f141e, #140d14);
            border: 3px solid #331b2f;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
            color: #fff;
            font-size: clamp(50px, 11vw, 75px);
            user-select: none;
            transition: transform 0.1s ease;
        }

        .reel.spinning {
            animation: shake 0.08s infinite;
        }

        @keyframes shake {
            0% { transform: translateY(-3px); }
            50% { transform: translateY(3px); }
            100% { transform: translateY(-3px); }
        }

        .controls {
            margin-top: 25px;
        }

        #spinButton {
            width: 85%;
            padding: 18px;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            font-size: 22px;
            font-weight: bold;
            letter-spacing: 2px;
            color: white;
            background: linear-gradient(#9c27b0, #673ab7);
            border: 2px solid #ba68c8;
            box-shadow: 0 5px 0 #4a148c, 0 0 20px rgba(156, 39, 176, 0.4);
            transition: 0.1s;
        }

        #spinButton:hover:not(:disabled) {
            filter: brightness(1.15);
        }

        #spinButton:active:not(:disabled) {
            transform: translateY(4px);
            box-shadow: 0 1px 0 #4a148c, 0 0 15px rgba(156, 39, 176, 0.4);
        }

        #spinButton:disabled {
            cursor: not-allowed;
            opacity: 0.4;
        }

        .result {
            min-height: 45px;
            margin-top: 20px;
            font-size: 20px;
            font-weight: bold;
            letter-spacing: 1px;
        }

        .win {
            color: #ffeb3b;
            animation: winFlash 0.3s infinite alternate;
        }

        @keyframes winFlash {
            from { transform: scale(1); filter: brightness(1); }
            to { transform: scale(1.05); filter: brightness(1.4); }
        }
    </style>
</head>
<body>

    <div class="machine">
        <div class="title">THE NIGHT SHIFT</div>
        
        <div class="reels">
            <div class="reel" id="reel1">🍒</div>
            <div class="reel" id="reel2">7</div>
            <div class="reel" id="reel3">💎</div>
        </div>

        <div class="controls">
            <button id="spinButton">PULL LEVER</button>
        </div>

        <div class="result" id="resultMessage">READY FOR SPIN...</div>
    </div>

    <script>
        const spinButton = document.getElementById('spinButton');
        const reelelements = [
            document.getElementById('reel1'),
            document.getElementById('reel2'),
            document.getElementById('reel3')
        ];
        const resultMessage = document.getElementById('resultMessage');

        spinButton.addEventListener('click', async () => {
            spinButton.disabled = true;
            resultMessage.classList.remove('win');
            resultMessage.innerText = "SPINNING...";
            
            reelelements.forEach(reel => reel.classList.add('spinning'));

            try {
                const response = await fetch('/spin', { method: 'POST' });
                const data = await response.json();

                setTimeout(() => {
                    reelelements.forEach((reel, index) => {
                        reel.classList.remove('spinning');
                        reel.innerText = data.reels[index];
                    });

                    resultMessage.innerText = data.outcome.message;
                    if (data.outcome.type !== 'nothing') {
                        resultMessage.classList.add('win');
                    }
                    spinButton.disabled = false;
                }, 900);

            } catch (error) {
