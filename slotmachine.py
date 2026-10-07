from flask import Flask, jsonify, render_template_string
from datetime import datetime
import random

app = Flask(__name__)

# ============================================================
# SETTINGS
# ============================================================

SYMBOLS = ["🍒", "💎", "7", "🍋", "🍊"]

# Normal symbol weights.
# Higher = more common.
#
# These are intentionally NOT equal.
# The machine should not constantly produce matches.
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
# Nothing is saved to disk.
jackpot_feed = []


# ============================================================
# RANDOM SYMBOL
# ============================================================

def random_symbol():
    symbols = list(SYMBOL_WEIGHTS.keys())
    weights = list(SYMBOL_WEIGHTS.values())

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
    The server generates the three symbols.

    The browser never decides the result.
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

    # --------------------------------------------------------
    # THREE OF A KIND
    # --------------------------------------------------------

    if a == b == c:

        name, multiplier = JACKPOTS[a]

        return {
            "type": "jackpot",
            "name": name,
            "multiplier": multiplier,
            "message": f"{name} — {multiplier}×"
        }

    # --------------------------------------------------------
    # TWO OF A KIND
    # --------------------------------------------------------

    if a == b or a == c or b == c:

        return {
            "type": "double",
            "name": "DOUBLE MATCH",
            "multiplier": DOUBLE_MULTIPLIER,
            "message": "DOUBLE MATCH — 1.5×"
        }

    # --------------------------------------------------------
    # NOTHING
    # --------------------------------------------------------

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

    # Keep only the most recent 50 events.
    del jackpot_feed[50:]


# ============================================================
# HTML
# ============================================================

HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>THE NIGHT SHIFT</title>


<style>

/* =========================================================
   BASE
   ========================================================= */

* {
    box-sizing: border-box;
}

html,
body {
    margin: 0;
    min-height: 100%;
}

body {

    background:
        radial-gradient(
            ellipse at 50% 0%,
            #241522 0%,
            #110b12 42%,
            #040405 100%
        );

    color: #d0c6ca;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    overflow-x: hidden;
}


/* CRT scanlines */

body::before {

    content: "";

    position: fixed;

    inset: 0;

    pointer-events: none;

    z-index: 100;

    background:
        repeating-linear-gradient(
            0deg,
            rgba(255,255,255,0.018),
            rgba(255,255,255,0.018) 1px,
            transparent 1px,
            transparent 4px
        );

    opacity: 0.45;
}


/* dark edges */

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
   PAGE
   ========================================================= */

.page {

    width: min(1150px, 94%);

    margin: auto;

    padding:
        25px
        0
        60px;

    position: relative;

    z-index: 2;
}


/* =========================================================
   HEADER
   ========================================================= */

.header {

    text-align: center;

    margin-bottom: 25px;
}

.header-small {

    color: #695963;

    font-family: Arial, sans-serif;

    font-size: 10px;

    letter-spacing: 6px;

    margin-bottom: 8px;
}

.title {

    margin: 0;

    font-family:
        Impact,
        Haettenschweiler,
        "Arial Narrow Bold",
        sans-serif;

    font-size:
        clamp(42px, 8vw, 80px);

    letter-spacing: 5px;

    color: #bcb2b7;

    text-shadow:
        4px 4px 0 #0b090b,
        0 0 18px rgba(150,30,40,0.2);

    transform: rotate(-1deg);
}

.subtitle {

    margin-top: 7px;

    color: #69545f;

    font-family: Arial, sans-serif;

    font-size: 10px;

    letter-spacing: 4px;
}


/* =========================================================
   MACHINE
   ========================================================= */

.machine {

    max-width: 900px;

    margin: auto;

    padding: 26px;

    background:
        linear-gradient(
            90deg,
            #09090a,
            #171216 10%,
            #100d11 50%,
            #171216 90%,
            #080809
        );

    border:
        5px solid #070608;

    border-radius: 22px;

    box-shadow:
        0 30px 60px rgba(0,0,0,0.8),
        inset 0 0 0 2px #30232a,
        inset 0 0 35px rgba(0,0,0,0.9);

    position: relative;
}


/* screws */

.machine::before,
.machine::after {

    content: "";

    position: absolute;

    top: 12px;

    width: 11px;

    height: 11px;

    border-radius: 50%;

    background: #312c2e;

    border: 2px solid #080708;

    box-shadow:
        inset 1px 1px 2px #777;
}

.machine::before {
    left: 13px;
}

.machine::after {
    right: 13px;
}


/* =========================================================
   WARNING
   ========================================================= */

.warning {

    padding: 8px;

    margin-bottom: 20px;

    text-align: center;

    background:
        repeating-linear-gradient(
            -45deg,
            #171215 0px,
            #171215 10px,
            #2a1c22 10px,
            #2a1c22 20px
        );

    border: 1px solid #453039;

    color: #94757f;

    font-family: Arial, sans-serif;

    font-size: 9px;

    letter-spacing: 3px;
}


/* =========================================================
   SIGN
   ========================================================= */

.machine-sign {

    text-align: center;

    margin-bottom: 20px;
}

.machine-sign span {

    display: inline-block;

    padding:
        7px
        35px;

    border-top:
        2px solid #392a31;

    border-bottom:
        2px solid #392a31;

    color: #c9bec4;

    font-family:
        Impact,
        Haettenschweiler,
        sans-serif;

    font-size: 25px;

    letter-spacing: 4px;
}


/* =========================================================
   REELS
   ========================================================= */

.reel-frame {

    padding: 13px;

    background: #050506;

    border: 8px solid #090809;

    border-radius: 12px;

    box-shadow:
        inset 0 0 0 2px #30242a,
        inset 0 0 30px #000,
        0 8px 25px rgba(0,0,0,0.8);
}

.reels {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

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
            #18161b,
            #08080a
        );

    border: 3px solid #211c20;

    border-radius: 8px;

    font-family: Arial, sans-serif;

    font-size:
        clamp(65px, 11vw, 105px);

    box-shadow:
        inset 0 0 30px #000;

    user-select: none;
}

.reel.spinning {

    animation:
        shake 0.07s infinite linear;
}

@keyframes shake {

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

    margin-top: 25px;
}

.spin-button {

    width: 125px;

    height: 125px;

    border-radius: 50%;

    border: 4px solid #270c13;

    cursor: pointer;

    background:
        radial-gradient(
            circle at 35% 28%,
            #ff6c61,
            #c02520 42%,
            #68110f 75%,
            #270707
        );

    color: #f3d9d6;

    font-family:
        Impact,
        Haettenschweiler,
        sans-serif;

    font-size: 23px;

    letter-spacing: 2px;

    box-shadow:
        0 9px 0 #170405,
        0 12px 25px rgba(0,0,0,0.8);

    transition:
        transform 0.08s,
        filter 0.15s;
}

.spin-button:hover {

    filter: brightness(1.15);
}

.spin-button:active {

    transform:
        translateY(8px);

    box-shadow:
        0 2px 0 #170405;
}

.spin-button:disabled {

    cursor: not-allowed;

    filter: grayscale(0.7);

    opacity: 0.6;
}


/* =========================================================
   RESULT
   ========================================================= */

.result {

    min-height: 40px;

    margin-top: 20px;

    text-align: center;

    color: #655961;

    font-family:
        Impact,
        Haettenschweiler,
        sans-serif;

    font-size: 23px;

    letter-spacing: 2px;
}

.result.win {

    color: #d1ae68;

    text-shadow:
        0 0 12px rgba(255,180,70,0.25);

    animation:
        flicker 0.15s 5;
}

@keyframes flicker {

    0%,
    100% {
        opacity: 1;
    }

    50% {
        opacity: 0.25;
    }
}


/* =========================================================
   LOWER PANELS
   ========================================================= */

.lower {

    display: grid;

    grid-template-columns:
        1fr 1.2fr;

    gap: 22px;

    margin-top: 24px;
}

.panel {

    background:
        linear-gradient(
            145deg,
            #141014,
            #0a090c
        );

    border:
        2px solid #2a2027;

    padding: 20px;

    box-shadow:
        inset 0 0 25px rgba(0,0,0,0.75),
        0 10px 30px rgba(0,0,0,0.4);
}

.panel-title {

    margin:
        0
        0
        15px;

    padding-bottom: 10px;

    border-bottom:
        1px solid #352931;

    color: #a9959e;

    font-family:
        Impact,
        Haettenschweiler,
        sans-serif;

    font-size: 22px;

    letter-spacing: 3px;
}


/* =========================================================
   PAYTABLE
   ========================================================= */

.pay-row {

    display: flex;

    align-items: center;

    gap: 10px;

    padding: 11px 4px;

    border-bottom:
        1px dotted #30262c;

    font-family: Arial, sans-serif;

    color: #81737a;
}

.pay-symbol {

    min-width: 75px;

    font-size: 20px;
}

.pay-name {

    flex: 1;
}

.pay-value {

    color: #c7a664;

    font-weight: bold;
}


/* =========================================================
   JACKPOT FEED
   ========================================================= */

.feed {

    max-height: 365px;

    overflow-y: auto;
}

.feed::-webkit-scrollbar {

    width: 5px;
}

.feed::-webkit-scrollbar-track {

    background: #080708;
}

.feed::-webkit-scrollbar-thumb {

    background: #3c2931;
}

.feed-item {

    padding: 13px 10px;

    margin-bottom: 8px;

    border-left:
        3px solid #542630;

    background:
        linear-gradient(
            90deg,
            rgba(90,35,45,0.13),
            transparent
        );

    animation:
        appear 0.35s ease-out;
}

@keyframes appear {

    from {
        opacity: 0;
        transform: translateX(-10px);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.feed-name {

    color: #bcaab1;

    font-family:
        Impact,
        Haettenschweiler,
        sans-serif;

    font-size: 17px;

    letter-spacing: 2px;
}

.feed-time {

    margin-top: 3px;

    color: #5d5157;

    font-family: Arial, sans-serif;

    font-size: 11px;
}

.empty {

    text-align: center;

    padding: 40px 10px;

    color: #4c4449;

    font-family: Arial, sans-serif;

    font-size: 11px;

    letter-spacing: 2px;
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

<div class="page">


    <!-- HEADER -->

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


    <!-- MACHINE -->

    <main class="machine">

        <div class="warning">
            WARNING — DO NOT OPEN CABINET — POWER MUST REMAIN ON
        </div>


        <div class="machine-sign">
            <span>HAUNTED JACKPOT</span>
        </div>


        <div class="reel-frame">

            <div class="reels">

                <div
                    class="reel"
                    id="reel1"
                >
                    🍒
                </div>

                <div
                    class="reel"
                    id="reel2"
                >
                    🍋
                </div>

                <div
                    class="reel"
                    id="reel3"
                >
                    🍊
                </div>

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


        <div
            class="result"
            id="result"
        >
            THE MACHINE IS WAITING
        </div>

    </main>


    <!-- LOWER PANELS -->

    <section class="lower">


        <!-- PAYTABLE -->

        <div class="panel">

            <h2 class="panel-title">
                PAYTABLE
            </h2>


            <div class="pay-row">

                <span class="pay-symbol">
                    🍒 🍒 🍒
                </span>

                <span class="pay-name">
                    CHERRY
                </span>

                <span class="pay-value">
                    4×
                </span>

            </div>


            <div class="pay-row">

                <span class="pay-symbol">
                    💎 💎 💎
                </span>

                <span class="pay-name">
                    DIAMOND
                </span>

                <span class="pay-value">
                    8×
                </span>

            </div>


            <div class="pay-row">

                <span class="pay-symbol">
                    7 7 7
                </span>

                <span class="pay-name">
                    SEVEN
                </span>

                <span class="pay-value">
                    10×
                </span>

            </div>


            <div class="pay-row">

                <span class="pay-symbol">
                    🍋 🍋 🍋
                </span>

                <span class="pay-name">
                    LEMON
                </span>

                <span class="pay-value">
                    2×
                </span>

            </div>


            <div class="pay-row">

                <span class="pay-symbol">
                    🍊 🍊 🍊
                </span>

                <span class="pay-name">
                    ORANGE
                </span>

                <span class="pay-value">
                    2×
                </span>

            </div>


            <div class="pay-row">

                <span class="pay-symbol">
                    ANY TWO
                </span>

                <span class="pay-name">
                    DOUBLE MATCH
                </span>

                <span class="pay-value">
                    1.5×
                </span>

            </div>

        </div>


        <!-- FEED -->

        <div class="panel">

            <h2 class="panel-title">
                JACKPOT FEED
            </h2>

            <div
                class="feed"
                id="feed"
            >

                <div class="empty">

                    NO JACKPOTS YET...

                    <br><br>

                    THE MACHINE IS WAITING.

                </div>

            </div>

        </div>

    </section>


</div>


<script>

/* =========================================================
   FRONT-END
   ========================================================= */

let spinning = false;


/*
 * These symbols are only used for the visual animation.
 *
 * IMPORTANT:
 * The actual result comes from Python.
 */

const symbols = [
    "🍒",
    "💎",
    "7",
    "🍋",
    "🍊"
];


function wait(ms) {

    return new Promise(
        resolve => setTimeout(resolve, ms)
    );
}


/* =========================================================
   VISUAL REEL ANIMATION
   ========================================================= */

async function animateReel(element, duration) {

    element.classList.add("spinning");

    const start = Date.now();

    while (
        Date.now() - start < duration
    ) {

        const symbol =
            symbols[
                Math.floor(
                    Math.random() *
                    symbols.length
                )
            ];

        element.textContent = symbol;

        await wait(65);
    }

    element.classList.remove("spinning");
}


/* =========================================================
   SPIN
   ========================================================= */

async function spin() {

    if (spinning) {
        return;
    }

    spinning = true;

    const button =
        document.getElementById(
            "spinButton"
        );

    const resultText =
        document.getElementById(
            "result"
        );

    const reel1 =
        document.getElementById(
            "reel1"
        );

    const reel2 =
        document.getElementById(
            "reel2"
        );

    const reel3 =
        document.getElementById(
            "reel3"
        );


    button.disabled = true;

    resultText.className = "result";

    resultText.textContent =
        "THE REELS ARE TURNING...";


    /*
     * Start visual animations.
     */

    const animation1 =
        animateReel(reel1, 900);

    await wait(150);

    const animation2 =
        animateReel(reel2, 1200);

    await wait(150);

    const animation3 =
        animateReel(reel3, 1500);


    /*
     * ASK PYTHON FOR THE ACTUAL RESULT.
     */

    let serverResult;

    try {

        const response =
            await fetch(
                "/api/spin",
                {
                    method: "POST"
                }
            );

        serverResult =
            await response.json();

    } catch (error) {

        console.error(error);

        resultText.textContent =
            "THE MACHINE IS BROKEN.";

        button.disabled = false;

        spinning = false;

        return;
    }


    /*
     * Wait until the visual reels finish.
     */

    await Promise.all([
        animation1,
        animation2,
        animation3
    ]);


    /*
     * Show the REAL server result.
     */

    reel1.textContent =
        serverResult.result[0];

    reel2.textContent =
        serverResult.result[1];

    reel3.textContent =
        serverResult.result[2];


    /*
     * Show result message.
     */

    if (
        serverResult.type ===
        "jackpot"
    ) {

        resultText.className =
            "result win";

        resultText.textContent =
            serverResult.message;

    }

    else if (
        serverResult.type ===
        "double"
    ) {

        resultText.className =
            "result win";

        resultText.textContent =
            serverResult.message;

    }

    else {

        resultText.className =
            "result";

        resultText.textContent =
            serverResult.message;
    }


    /*
     * Refresh the feed.
     */

    await loadFeed();


    button.disabled = false;

    spinning = false;
}


/* =========================================================
   LOAD FEED
   ========================================================= */

async function loadFeed() {

    try {

        const response =
            await fetch(
                "/api/jackpots"
            );

        const events =
            await response.json();

        const feed =
            document.getElementById(
                "feed"
            );


        if (
            events.length === 0
        ) {

            feed.innerHTML = `
                <div class="empty">
                    NO JACKPOTS YET...
                    <br><br>
                    THE MACHINE IS WAITING.
                </div>
            `;

            return;
        }


        feed.innerHTML = "";


        events.forEach(event => {

            const item =
                document.createElement(
                    "div"
                );

            item.className =
                "feed-item";


            const name =
                document.createElement(
                    "div"
                );

            name.className =
                "feed-name";

            name.textContent =
                event.name;


            const time =
                document.createElement(
                    "div"
                );

            time.className =
                "feed-time";

            time.textContent =
                timeAgo(event.time);


            item.appendChild(name);

            item.appendChild(time);

            feed.appendChild(item);

        });

    } catch (error) {

        console.error(error);
    }
}


/* =========================================================
   TIME AGO
   ========================================================= */

function timeAgo(timestamp) {

    const time =
        new Date(timestamp)
            .getTime();

    const seconds =
        Math.floor(
            (Date.now() - time) /
            1000
        );


    if (seconds < 5) {
        return "just now";
    }


    if (seconds < 60) {

        return (
            seconds +
            " second" +
            (
                seconds === 1
                    ? ""
                    : "s"
            ) +
            " ago"
        );
    }


    const minutes =
        Math.floor(
            seconds / 60
        );


    if (minutes < 60) {

        return (
            minutes +
            " minute" +
            (
                minutes === 1
                    ? ""
                    : "s"
            ) +
            " ago"
        );
    }


    const hours =
        Math.floor(
            minutes / 60
        );


    if (hours < 24) {

        return (
            hours +
            " hour" +
            (
                hours === 1
                    ? ""
                    : "s"
            ) +
            " ago"
        );
    }


    const days =
        Math.floor(
            hours / 24
        );


    return (
        days +
        " day" +
        (
            days === 1
                ? ""
                : "s"
        ) +
        " ago"
    );
}


/* =========================================================
   KEEP TIMES UPDATED
   ========================================================= */

setInterval(
    loadFeed,
    5000
);


/* Initial load */

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


@app.route("/api/spin", methods=["POST"])
def spin():

    # Python decides the actual outcome.
    result = create_spin_result()

    # Work out whether it is a jackpot/double/nothing.
    outcome = evaluate_spin(result)

    # Only jackpots and doubles enter the feed.
    if outcome["type"] in ("jackpot", "double"):
        add_feed_event(outcome)

    return jsonify({
        "result": result,
        "type": outcome["type"],
        "message": outcome["message"],
        "multiplier": outcome["multiplier"]
    })


@app.route("/api/jackpots", methods=["GET"])
def get_jackpots():

    return jsonify(jackpot_feed)


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print()
    print("==============================================")
    print("             THE NIGHT SHIFT")
    print("          HAUNTED SLOT MACHINE")
    print("==============================================")
    print()
    print("Open in your browser:")
    print("http://127.0.0.1:5000")
    print()
    print("No database.")
    print("No JSON file.")
    print("No player names.")
    print("Jackpot feed resets when the server stops.")
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )