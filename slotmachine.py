from flask import Flask, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# ============================================================
# GAME SETTINGS
# ============================================================

SYMBOLS = ["🍒", "💎", "7", "🍋", "🍊"]

JACKPOTS = {
    "🍒": ("CHERRY JACKPOT", 4),
    "💎": ("DIAMOND JACKPOT", 8),
    "7": ("SEVEN JACKPOT", 10),
    "🍋": ("LEMON JACKPOT", 2),
    "🍊": ("ORANGE JACKPOT", 2),
}

# This is intentionally NOT saved anywhere.
# Restarting the server clears the feed.
jackpot_feed = []


# ============================================================
# PAGE
# ============================================================

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>THE NIGHT SHIFT</title>

<style>

/* =========================================================
   GENERAL
   ========================================================= */

* {
    box-sizing: border-box;
}

html {
    min-height: 100%;
}

body {
    margin: 0;
    min-height: 100vh;
    background:
        radial-gradient(
            ellipse at 50% 15%,
            #24142b 0%,
            #100b13 42%,
            #050507 100%
        );
    color: #ddd;
    font-family: Georgia, "Times New Roman", serif;
    overflow-x: hidden;
}

/* Old CRT scanlines */
body::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 100;
    pointer-events: none;

    background:
        repeating-linear-gradient(
            to bottom,
            rgba(255,255,255,0.018) 0px,
            rgba(255,255,255,0.018) 1px,
            transparent 1px,
            transparent 4px
        );

    opacity: 0.45;
}

/* Slight old-screen vignette */
body::after {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 99;

    box-shadow:
        inset 0 0 180px rgba(0,0,0,0.95);
}

/* =========================================================
   BACKGROUND DECORATION
   ========================================================= */

.wall {
    position: fixed;
    inset: 0;
    pointer-events: none;
    opacity: 0.28;

    background-image:
        radial-gradient(
            circle at 15% 30%,
            #4d263f 0px,
            transparent 2px
        ),
        radial-gradient(
            circle at 78% 65%,
            #542b42 0px,
            transparent 2px
        ),
        radial-gradient(
            circle at 45% 85%,
            #34202e 0px,
            transparent 2px
        );

    background-size: 140px 120px, 190px 170px, 220px 190px;
}

/* =========================================================
   MAIN WRAPPER
   ========================================================= */

.page {
    width: min(1200px, 94%);
    margin: auto;
    padding: 25px 0 60px;
    position: relative;
    z-index: 2;
}

/* =========================================================
   HEADER
   ========================================================= */

.header {
    text-align: center;
    margin-bottom: 24px;
}

.header-small {
    color: #76656f;
    letter-spacing: 6px;
    font-size: 11px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.title {
    margin: 0;

    font-family:
        Impact,
        Haettenschweiler,
        "Arial Narrow Bold",
        sans-serif;

    font-size: clamp(42px, 8vw, 82px);
    letter-spacing: 5px;
    color: #b9b0b5;

    text-shadow:
        3px 3px 0 #171217,
        5px 5px 0 #080608,
        0 0 15px rgba(255,60,50,0.13);

    transform: rotate(-1deg);
}

.subtitle {
    margin-top: 5px;
    color: #765c68;
    font-size: 12px;
    letter-spacing: 4px;
    text-transform: uppercase;
}

/* =========================================================
   CABINET
   ========================================================= */

.machine {
    position: relative;

    background:
        linear-gradient(
            90deg,
            #09090b,
            #171216 9%,
            #100d11 50%,
            #181216 91%,
            #080809
        );

    border: 5px solid #080709;
    border-radius: 22px;

    padding: 26px;

    box-shadow:
        0 25px 55px rgba(0,0,0,0.8),
        inset 0 0 0 2px #32242c,
        inset 0 0 35px rgba(0,0,0,0.9);

    max-width: 900px;
    margin: auto;
}

/* Cabinet screws */

.machine::before,
.machine::after {
    content: "";
    position: absolute;

    width: 11px;
    height: 11px;

    border-radius: 50%;
    background: #332d30;

    border: 2px solid #0a090a;

    box-shadow:
        inset 1px 1px 2px #777,
        0 1px 2px #000;
}

.machine::before {
    top: 12px;
    left: 13px;
}

.machine::after {
    top: 12px;
    right: 13px;
}

/* =========================================================
   WARNING STRIP
   ========================================================= */

.warning {
    background:
        repeating-linear-gradient(
            -45deg,
            #181315 0px,
            #181315 10px,
            #302127 10px,
            #302127 20px
        );

    border: 1px solid #4b343d;

    padding: 7px;

    text-align: center;

    color: #a8838e;

    font-family: Arial, sans-serif;
    font-size: 10px;
    letter-spacing: 3px;

    margin-bottom: 20px;
}

/* =========================================================
   MACHINE SIGN
   ========================================================= */

.machine-sign {
    text-align: center;
    margin-bottom: 20px;
}

.machine-sign span {
    display: inline-block;

    color: #d7c8ce;

    font-family:
        Impact,
        Haettenschweiler,
        sans-serif;

    font-size: 25px;
    letter-spacing: 4px;

    border-top: 2px solid #3b2a31;
    border-bottom: 2px solid #3b2a31;

    padding: 6px 35px;

    text-shadow: 0 0 10px rgba(255,255,255,0.12);
}

/* =========================================================
   REELS
   ========================================================= */

.reel-frame {
    background: #050506;

    border: 8px solid #0a090a;

    border-radius: 12px;

    padding: 13px;

    box-shadow:
        inset 0 0 0 2px #31242b,
        inset 0 0 30px #000,
        0 8px 20px rgba(0,0,0,0.8);
}

.reels {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
}

.reel {
    height: 190px;

    display: flex;
    justify-content: center;
    align-items: center;

    background:
        linear-gradient(
            90deg,
            #08080a,
            #17151a,
            #09090a
        );

    border: 3px solid #211c20;

    border-radius: 8px;

    overflow: hidden;

    font-family: Arial, sans-serif;
    font-size: clamp(65px, 11vw, 105px);

    text-shadow:
        0 0 12px rgba(255,255,255,0.18);

    box-shadow:
        inset 0 0 30px #000;
}

/* Reel spinning effect */

.reel.spinning {
    animation:
        reelShake 0.07s infinite linear;
}

@keyframes reelShake {

    0% {
        transform: translateY(-2px);
    }

    50% {
        transform: translateY(2px);
    }

    100% {
        transform: translateY(-2px);
    }
}

/* =========================================================
   BUTTON
   ========================================================= */

.controls {
    text-align: center;
    margin-top: 24px;
}

.spin-button {
    position: relative;

    border: 4px solid #260f18;

    border-radius: 50%;

    width: 125px;
    height: 125px;

    cursor: pointer;

    background:
        radial-gradient(
            circle at 35% 30%,
            #ff6b5e,
            #bd241e 40%,
            #68100e 75%,
            #280808
        );

    color: #f7d9d4;

    font-family:
        Impact,
        Haettenschweiler,
        sans-serif;

    font-size: 23px;
    letter-spacing: 2px;

    box-shadow:
        0 9px 0 #180506,
        0 12px 25px rgba(0,0,0,0.8),
        0 0 25px rgba(180,20,20,0.16);

    transition:
        transform 0.08s,
        filter 0.15s;
}

.spin-button:hover {
    filter: brightness(1.15);
}

.spin-button:active {
    transform: translateY(8px);
    box-shadow:
        0 2px 0 #180506,
        0 5px 15px rgba(0,0,0,0.8);
}

.spin-button:disabled {
    cursor: not-allowed;
    filter: grayscale(0.6);
    opacity: 0.6;
}

/* =========================================================
   RESULT
   ========================================================= */

.result {
    min-height: 40px;

    text-align: center;

    margin-top: 20px;

    font-family:
        Impact,
        Haettenschweiler,
        sans-serif;

    font-size: 25px;
    letter-spacing: 2px;

    color: #75646b;
}

.result.win {
    color: #d6b66b;

    text-shadow:
        0 0 8px rgba(255,180,70,0.3);

    animation: resultFlicker 0.15s 4;
}

@keyframes resultFlicker {

    0%, 100% {
        opacity: 1;
    }

    50% {
        opacity: 0.3;
    }
}

/* =========================================================
   LOWER AREA
   ========================================================= */

.lower {
    display: grid;
    grid-template-columns: 1fr 1.2fr;
    gap: 22px;

    margin-top: 24px;
}

/* =========================================================
   PANELS
   ========================================================= */

.panel {
    background:
        linear-gradient(
            145deg,
            #141014,
            #0b090c
        );

    border: 2px solid #2a2027;

    box-shadow:
        inset 0 0 25px rgba(0,0,0,0.75),
        0 10px 30px rgba(0,0,0,0.45);

    padding: 20px;

    position: relative;
}

.panel-title {
    margin: 0 0 15px;

    font-family:
        Impact,
        Haettenschweiler,
        sans-serif;

    color: #a9959e;

    font-size: 23px;

    letter-spacing: 3px;

    border-bottom: 1px solid #352931;

    padding-bottom: 10px;
}

/* =========================================================
   PAYTABLE
   ========================================================= */

.pay-row {
    display: flex;
    justify-content: space-between;
    align-items: center;

    padding: 11px 4px;

    border-bottom: 1px dotted #30262c;

    color: #81737a;

    font-family: Arial, sans-serif;
}

.pay-symbol {
    font-size: 22px;
}

.pay-name {
    flex: 1;
    margin-left: 10px;
}

.pay-value {
    color: #c9a86a;
    font-weight: bold;
}

/* =========================================================
   JACKPOT FEED
   ========================================================= */

.feed {
    max-height: 360px;
    overflow-y: auto;
    padding-right: 5px;
}

/* Scrollbar */

.feed::-webkit-scrollbar {
    width: 5px;
}

.feed::-webkit-scrollbar-track {
    background: #090809;
}

.feed::-webkit-scrollbar-thumb {
    background: #392932;
}

.feed-item {
    padding: 13px 10px;

    border-left: 3px solid #4a252e;

    margin-bottom: 8px;

    background:
        linear-gradient(
            90deg,
            rgba(90,35,45,0.12),
            transparent
        );

    animation: feedAppear 0.35s ease-out;
}

@keyframes feedAppear {

    from {
        opacity: 0;
        transform: translateX(-8px);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.feed-name {
    font-family:
        Impact,
        Haettenschweiler,
        sans-serif;

    letter-spacing: 2px;

    color: #bcaab1;

    font-size: 17px;
}

.feed-time {
    color: #5f5359;

    font-family: Arial, sans-serif;

    font-size: 11px;

    margin-top: 3px;
}

.feed-empty {
    text-align: center;

    color: #4e454a;

    font-family: Arial, sans-serif;

    font-size: 12px;

    padding: 35px 10px;

    letter-spacing: 2px;
}

/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    text-align: center;

    margin-top: 20px;

    color: #40383d;

    font-family: Arial, sans-serif;

    font-size: 9px;

    letter-spacing: 3px;
}

/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 760px) {

    .machine {
        padding: 15px;
    }

    .reels {
        gap: 7px;
    }

    .reel {
        height: 135px;
    }

    .lower {
        grid-template-columns: 1fr;
    }

    .spin-button {
        width: 110px;
        height: 110px;
    }
}

</style>
</head>

<body>

<div class="wall"></div>

<div class="page">

    <header class="header">

        <div class="header-small">
            HALLOWEEN NIGHT SHIFT • MACHINE 03
        </div>

        <h1 class="title">
            THE NIGHT SHIFT
        </h1>

        <div class="subtitle">
            DO NOT PLAY AFTER MIDNIGHT
        </div>

    </header>


    <!-- =====================================================
         SLOT MACHINE
         ===================================================== -->

    <main class="machine">

        <div class="warning">
            WARNING — DO NOT OPEN CABINET — POWER MUST REMAIN ON
        </div>

        <div class="machine-sign">
            <span>HAUNTED JACKPOT</span>
        </div>


        <div class="reel-frame">

            <div class="reels">

                <div class="reel" id="reel1">🍒</div>

                <div class="reel" id="reel2">💎</div>

                <div class="reel" id="reel3">7</div>

            </div>

        </div>


        <div class="controls">

            <button
                class="spin-button"
                id="spinButton"
                onclick="spin()"
            >
                SPIN
            </button>

        </div>


        <div class="result" id="result">
            INSERT COURAGE
        </div>

    </main>


    <!-- =====================================================
         PAYTABLE + FEED
         ===================================================== -->

    <section class="lower">


        <div class="panel">

            <h2 class="panel-title">
                PAYTABLE
            </h2>


            <div class="pay-row">

                <span class="pay-symbol">🍒 🍒 🍒</span>

                <span class="pay-name">
                    CHERRY
                </span>

                <span class="pay-value">
                    4×
                </span>

            </div>


            <div class="pay-row">

                <span class="pay-symbol">💎 💎 💎</span>

                <span class="pay-name">
                    DIAMOND
                </span>

                <span class="pay-value">
                    8×
                </span>

            </div>


            <div class="pay-row">

                <span class="pay-symbol">7 7 7</span>

                <span class="pay-name">
                    SEVEN
                </span>

                <span class="pay-value">
                    10×
                </span>

            </div>


            <div class="pay-row">

                <span class="pay-symbol">🍋 🍋 🍋</span>

                <span class="pay-name">
                    LEMON
                </span>

                <span class="pay-value">
                    2×
                </span>

            </div>


            <div class="pay-row">

                <span class="pay-symbol">🍊 🍊 🍊</span>

                <span class="pay-name">
                    ORANGE
                </span>

                <span class="pay-value">
                    2×
                </span>

            </div>


            <div class="pay-row">

                <span class="pay-symbol">🍒 🍒</span>

                <span class="pay-name">
                    DOUBLE MATCH
                </span>

                <span class="pay-value">
                    1.5×
                </span>

            </div>

        </div>


        <div class="panel">

            <h2 class="panel-title">
                JACKPOT FEED
            </h2>

            <div
                class="feed"
                id="feed"
            >
                <div class="feed-empty">
                    NO JACKPOTS YET...
                    <br><br>
                    THE MACHINE IS WAITING.
                </div>
            </div>

        </div>

    </section>


    <footer class="footer">
        PROPERTY OF THE NIGHT SHIFT • FREE PLAY MACHINE
    </footer>

</div>


<script>

/* =========================================================
   GAME DATA
   ========================================================= */

const symbols = [
    "🍒",
    "💎",
    "7",
    "🍋",
    "🍊"
];

const jackpotNames = {
    "🍒": "CHERRY JACKPOT",
    "💎": "DIAMOND JACKPOT",
    "7": "SEVEN JACKPOT",
    "🍋": "LEMON JACKPOT",
    "🍊": "ORANGE JACKPOT"
};

const jackpotMultipliers = {
    "🍒": 4,
    "💎": 8,
    "7": 10,
    "🍋": 2,
    "🍊": 2
};

let spinning = false;


/* =========================================================
   RANDOM SYMBOL
   ========================================================= */

function randomSymbol() {

    const index =
        Math.floor(Math.random() * symbols.length);

    return symbols[index];
}


/* =========================================================
   WAIT
   ========================================================= */

function wait(milliseconds) {

    return new Promise(resolve => {

        setTimeout(resolve, milliseconds);

    });
}


/* =========================================================
   SPIN ONE REEL
   ========================================================= */

async function spinReel(reel, duration) {

    reel.classList.add("spinning");

    const start = Date.now();

    while (Date.now() - start < duration) {

        reel.textContent = randomSymbol();

        await wait(70);
    }

    reel.classList.remove("spinning");

    const finalSymbol = randomSymbol();

    reel.textContent = finalSymbol;

    return finalSymbol;
}


/* =========================================================
   MAIN SPIN
   ========================================================= */

async function spin() {

    if (spinning) {
        return;
    }

    spinning = true;

    const button =
        document.getElementById("spinButton");

    const result =
        document.getElementById("result");

    button.disabled = true;

    result.className = "result";

    result.textContent =
        "SOMETHING IS WATCHING...";


    const reel1 =
        document.getElementById("reel1");

    const reel2 =
        document.getElementById("reel2");

    const reel3 =
        document.getElementById("reel3");


    /*
     * The reels stop at different times.
     * This makes it feel much more like a physical machine.
     */

    const r1 = spinReel(reel1, 900);

    await wait(180);

    const r2 = spinReel(reel2, 1250);

    await wait(180);

    const r3 = spinReel(reel3, 1600);


    const results = await Promise.all([
        r1,
        r2,
        r3
    ]);


    const a = results[0];
    const b = results[1];
    const c = results[2];


    /* =====================================================
       THREE OF A KIND
       ===================================================== */

    if (a === b && b === c) {

        const name = jackpotNames[a];

        const multiplier =
            jackpotMultipliers[a];

        result.className =
            "result win";

        result.textContent =
            name + " — " +
            multiplier + "×";


        await addJackpot(
            name,
            multiplier,
            [a, b, c]
        );

    }


    /* =====================================================
       EXACTLY TWO MATCH
       ===================================================== */

    else if (
        a === b ||
        a === c ||
        b === c
    ) {

        result.className =
            "result win";

        result.textContent =
            "DOUBLE MATCH — 1.5×";


        await addJackpot(
            "DOUBLE MATCH — 1.5×",
            1.5,
            [a, b, c]
        );

    }


    /* =====================================================
       NOTHING
       ===================================================== */

    else {

        result.className =
            "result";

        result.textContent =
            "NOTHING. THE MACHINE STARES BACK.";

    }


    button.disabled = false;

    spinning = false;
}


/* =========================================================
   ADD JACKPOT TO SERVER FEED
   ========================================================= */

async function addJackpot(name, multiplier, combination) {

    try {

        await fetch("/api/jackpot", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                name: name,
                multiplier: multiplier,
                combination: combination
            })

        });

        await loadFeed();

    } catch (error) {

        console.error(
            "Could not add jackpot:",
            error
        );

    }
}


/* =========================================================
   LOAD FEED
   ========================================================= */

async function loadFeed() {

    try {

        const response =
            await fetch("/api/jackpots");

        const jackpots =
            await response.json();

        const feed =
            document.getElementById("feed");


        if (jackpots.length === 0) {

            feed.innerHTML = `
                <div class="feed-empty">
                    NO JACKPOTS YET...
                    <br><br>
                    THE MACHINE IS WAITING.
                </div>
            `;

            return;
        }


        feed.innerHTML = "";


        jackpots.forEach(jackpot => {

            const item =
                document.createElement("div");

            item.className =
                "feed-item";


            const title =
                document.createElement("div");

            title.className =
                "feed-name";

            title.textContent =
                jackpot.name;


            const time =
                document.createElement("div");

            time.className =
                "feed-time";

            time.textContent =
                timeAgo(jackpot.time);


            item.appendChild(title);

            item.appendChild(time);

            feed.appendChild(item);

        });

    } catch (error) {

        console.error(
            "Could not load jackpot feed:",
            error
        );

    }
}


/* =========================================================
   TIME AGO
   ========================================================= */

function timeAgo(timestamp) {

    const then =
        new Date(timestamp).getTime();

    const now =
        Date.now();

    const seconds =
        Math.max(
            0,
            Math.floor((now - then) / 1000)
        );


    if (seconds < 5) {
        return "just now";
    }


    if (seconds < 60) {

        return (
            seconds +
            " second" +
            (seconds === 1 ? "" : "s") +
            " ago"
        );

    }


    const minutes =
        Math.floor(seconds / 60);


    if (minutes < 60) {

        return (
            minutes +
            " minute" +
            (minutes === 1 ? "" : "s") +
            " ago"
        );

    }


    const hours =
        Math.floor(minutes / 60);


    if (hours < 24) {

        return (
            hours +
            " hour" +
            (hours === 1 ? "" : "s") +
            " ago"
        );

    }


    const days =
        Math.floor(hours / 24);


    return (
        days +
        " day" +
        (days === 1 ? "" : "s") +
        " ago"
    );
}


/* =========================================================
   UPDATE TIMES WITHOUT RELOADING EVERYTHING
   ========================================================= */

setInterval(() => {

    loadFeed();

}, 10000);


/* Initial feed */

loadFeed();

</script>

</body>
</html>
"""


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/api/jackpots", methods=["GET"])
def get_jackpots():

    # Newest first
    return jsonify(list(reversed(jackpot_feed)))


@app.route("/api/jackpot", methods=["POST"])
def add_jackpot():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False
        }), 400

    name = str(
        data.get("name", "UNKNOWN JACKPOT")
    )

    multiplier = data.get(
        "multiplier",
        1
    )

    combination = data.get(
        "combination",
        []
    )

    jackpot = {
        "name": name,
        "multiplier": multiplier,
        "combination": combination,
        "time": datetime.now().isoformat()
    }

    jackpot_feed.append(jackpot)

    # Keep the current event from becoming enormous
    # if the machine is used hundreds of times.
    if len(jackpot_feed) > 100:
        del jackpot_feed[:-100]

    return jsonify({
        "success": True
    })


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    print()
    print("==============================================")
    print("          THE NIGHT SHIFT")
    print("       HAUNTED SLOT MACHINE")
    print("==============================================")
    print()
    print("Open:")
    print("http://127.0.0.1:5000")
    print()
    print("Press CTRL+C to stop the machine.")
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )