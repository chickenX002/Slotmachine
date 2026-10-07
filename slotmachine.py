from flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)

LEADERBOARD_FILE = "leaderboard.json"

# Imaginary free-play multipliers
MULTIPLIERS = {
    "🍒": 4,
    "💎": 8,
    "7️⃣": 10,
    "🍋": 2,
    "🍊": 2
}

ALLOWED_JACKPOTS = {200, 400, 800, 1000}


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []

    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return []


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Midnight Pizzeria - Haunted Slots</title>

<style>

* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    min-height: 100%;
}

body {
    min-height: 100vh;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    color: white;

    background:
        radial-gradient(
            circle at 50% 20%,
            #39123f 0%,
            #170b1c 35%,
            #050507 80%
        );

    overflow-x: hidden;
}

/* Scanline effect */

body::before {
    content: "";

    position: fixed;
    inset: 0;

    pointer-events: none;

    background:
        repeating-linear-gradient(
            0deg,
            rgba(255,255,255,0.025) 0px,
            rgba(255,255,255,0.025) 1px,
            transparent 1px,
            transparent 4px
        );

    z-index: 1000;
}

/* Moving red security scan */

.scanline {
    position: fixed;

    left: 0;
    right: 0;

    height: 2px;

    background: rgba(255,0,0,0.15);

    box-shadow:
        0 0 10px red;

    pointer-events: none;

    z-index: 1001;

    animation: scan 5s linear infinite;
}

@keyframes scan {

    from {
        top: 0;
    }

    to {
        top: 100vh;
    }

}

/* Header */

header {
    text-align: center;

    padding:
        25px
        15px
        10px;
}

.warning {
    color: #ff3535;

    font-size: 12px;

    font-weight: 900;

    letter-spacing: 5px;

    text-shadow:
        0 0 12px red;
}

h1 {
    margin: 8px 0;

    font-size:
        clamp(
            30px,
            8vw,
            60px
        );

    color: #ffc928;

    text-shadow:
        3px 3px 0 #4c0808,
        0 0 20px #ff6a00;
}

.subtitle {
    color: #aaa;

    font-size: 14px;

    letter-spacing: 1px;
}

/* Main layout */

.layout {

    width: min(
        1200px,
        96vw
    );

    margin:
        15px
        auto
        50px;

    display: grid;

    grid-template-columns:
        minmax(0, 1.5fr)
        minmax(280px, .8fr);

    gap: 20px;
}

/* Panels */

.panel {

    background:
        linear-gradient(
            145deg,
            #1a111c,
            #08070a
        );

    border:
        2px solid #55171e;

    border-radius: 18px;

    box-shadow:
        0 0 30px rgba(0,0,0,.8),
        inset 0 0 25px rgba(255,0,0,.04);
}

/* Slot machine */

.machine {
    padding: 20px;
}

.machine-header {

    display: flex;

    justify-content:
        space-between;

    align-items: center;

    margin-bottom: 15px;
}

.machine-label {

    color: #ff3b3b;

    font-size: 12px;

    font-weight: 900;

    letter-spacing: 2px;
}

.status {

    color: #55ff7c;

    font-size: 11px;

    font-weight: bold;
}

/* Reels */

.reels {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 12px;

    padding: 14px;

    background: #020202;

    border:
        4px solid #351117;

    border-radius: 15px;

    box-shadow:
        inset 0 0 40px #000;
}

.reel {

    height:
        clamp(
            120px,
            20vw,
            190px
        );

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        linear-gradient(
            #ffffff,
            #cfcfcf
        );

    color: #111;

    font-size:
        clamp(
            55px,
            10vw,
            95px
        );

    border:
        5px solid #292929;

    border-radius: 12px;

    box-shadow:
        inset 0 0 25px rgba(0,0,0,.5),
        0 0 10px rgba(255,255,255,.1);

    overflow: hidden;

    user-select: none;
}

.reel.spinning {

    animation:
        shake .07s infinite;
}

@keyframes shake {

    0% {
        transform:
            translateY(-3px);
    }

    50% {
        transform:
            translateY(3px);
    }

    100% {
        transform:
            translateY(-3px);
    }

}

/* Controls */

.controls {

    margin-top: 20px;

    text-align: center;
}

.player-row {

    display: flex;

    margin-bottom: 10px;
}

input {

    width: 100%;

    padding: 14px;

    border-radius: 10px;

    border:
        1px solid #73323a;

    background: #0b090d;

    color: white;

    font-size: 16px;

    outline: none;
}

input:focus {

    border-color:
        #ff3838;

    box-shadow:
        0 0 10px
        rgba(255,0,0,.2);
}

/* Spin button */

#spinButton {

    width: 90%;

    padding: 18px;

    border: 3px solid #ffabab;

    border-radius: 50px;

    background:
        linear-gradient(
            #ef3038,
            #85080c
        );

    color: white;

    font-size: 25px;

    font-weight: 900;

    letter-spacing: 3px;

    box-shadow:
        0 7px 0 #3b0306,
        0 0 25px
        rgba(255,0,0,.35);

    cursor: pointer;

    transition:
        transform .1s,
        filter .1s;
}

#spinButton:hover {

    filter:
        brightness(1.2);
}

#spinButton:active {

    transform:
        translateY(5px);

    box-shadow:
        0 2px 0 #3b0306;
}

#spinButton:disabled {

    opacity: .5;

    cursor:
        not-allowed;
}

/* Result */

.result {

    min-height: 50px;

    padding-top: 16px;

    font-size: 21px;

    font-weight: 900;
}

.win {

    color: #ffd43b;

    animation:
        jackpotFlash
        .25s
        infinite
        alternate;
}

@keyframes jackpotFlash {

    from {
        transform:
            scale(1);

        text-shadow:
            0 0 8px
            #ff7b00;
    }

    to {
        transform:
            scale(1.08);

        text-shadow:
            0 0 25px
            white;
    }

}

/* Side panels */

.side {

    display: flex;

    flex-direction: column;

    gap: 18px;
}

.box {

    padding: 18px;
}

.box h2 {

    margin:
        0 0 12px;

    color: #f3c44d;

    font-size: 18px;
}

/* Paytable */

.paytable {

    width: 100%;

    border-collapse:
        collapse;
}

.paytable td {

    padding: 9px 4px;

    border-bottom:
        1px solid #2b2025;
}

.paytable td:last-child {

    text-align: right;

    color: #58ff7c;

    font-weight: 900;
}

/* Leaderboard */

.leaderboard {

    max-height:
        400px;

    overflow-y: auto;
}

.leader {

    display: grid;

    grid-template-columns:
        35px
        1fr
        auto;

    gap: 8px;

    align-items: center;

    padding: 11px 4px;

    border-bottom:
        1px solid #2b2025;
}

.rank {

    color: #ffc400;

    font-weight: 900;
}

.score {

    color: #59ff7e;

    font-weight: 900;
}

.small {

    color: #777;

    font-size: 11px;
}

.empty {

    color: #777;

    padding: 10px 0;
}

/* Falling pumpkins / coins */

.falling {

    position: fixed;

    top: -40px;

    z-index: 999;

    pointer-events: none;

    font-size: 28px;

    animation:
        fall 1.6s
        linear forwards;
}

@keyframes fall {

    from {

        transform:
            translateY(0)
            rotate(0deg);

        opacity: 1;
    }

    to {

        transform:
            translateY(110vh)
            rotate(720deg);

        opacity: 0;
    }

}

/* Event information */

.event-info {

    color: #aaa;

    font-size: 12px;

    line-height: 1.6;
}

.event-info strong {

    color: #ff4747;
}

/* Mobile */

@media (max-width: 800px) {

    .layout {

        grid-template-columns:
            1fr;
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

        font-size: 55px;
    }

    #spinButton {

        width: 100%;

        font-size: 20px;
    }

}

</style>

</head>

<body>

<div class="scanline"></div>

<header>

    <div class="warning">
        ⚠ NIGHT SHIFT TERMINAL ⚠
    </div>

    <h1>
        🎃 MIDNIGHT PIZZERIA 🎃
    </h1>

    <div class="subtitle">
        HAUNTED ANIMATRONIC SLOT MACHINE
        • FREE PLAY
    </div>

</header>


<div class="layout">


<!-- MACHINE -->

<main class="panel machine">

    <div class="machine-header">

        <div class="machine-label">
            UNIT #13 — ARCADE TERMINAL
        </div>

        <div class="status">
            ● ONLINE
        </div>

    </div>


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


    <div class="controls">

        <div class="player-row">

            <input
                id="playerName"
                maxlength="20"
                placeholder="Enter player name"
                autocomplete="off"
            >

        </div>


        <button
            id="spinButton"
            onclick="spin()"
        >
            SPIN 🎰
        </button>


        <div
            id="result"
            class="result"
        >
            Enter your name and survive the night...
        </div>

    </div>

</main>


<!-- SIDE -->

<aside class="side">


<!-- PAYTABLE -->

<section class="panel box">

    <h2>
        🎃 PAYTABLE
    </h2>

    <table class="paytable">

        <tr>
            <td>🍒 🍒 🍒</td>
            <td>4×</td>
        </tr>

        <tr>
            <td>💎 💎 💎</td>
            <td>8×</td>
        </tr>

        <tr>
            <td>7️⃣ 7️⃣ 7️⃣</td>
            <td>10×</td>
        </tr>

        <tr>
            <td>🍋 🍋 🍋</td>
            <td>2×</td>
        </tr>

        <tr>
            <td>🍊 🍊 🍊</td>
            <td>2×</td>
        </tr>

    </table>


    <div
        class="small"
        style="margin-top:10px"
    >
        Base jackpot:
        100 imaginary points
    </div>

</section>


<!-- LEADERBOARD -->

<section class="panel box">

    <h2>
        🏆 BIGGEST JACKPOTS
    </h2>

    <div
        id="leaderboard"
        class="leaderboard"
    >

        <div class="empty">
            Loading...
        </div>

    </div>

</section>


<!-- INFO -->

<section class="panel box event-info">

    <strong>
        ⚠ EVENT MODE
    </strong>

    <br>
    <br>

    This machine uses imaginary points only.
    There are no deposits, purchases,
    cash prizes, or real-money wagers.

    <br>
    <br>

    <strong>
        SPACEBAR
    </strong>

    can also be used to spin.

</section>


</aside>

</div>


<script>

/* ================================
   SLOT MACHINE JAVASCRIPT
================================ */


const symbols = [
    "🍒",
    "🍋",
    "🍊",
    "🍉",
    "⭐",
    "💎",
    "7️⃣"
];


const reels = [

    document.getElementById("reel1"),

    document.getElementById("reel2"),

    document.getElementById("reel3")

];


const button =
    document.getElementById("spinButton");


const result =
    document.getElementById("result");


const playerName =
    document.getElementById("playerName");


let spinning = false;

let audioContext = null;


/* Multipliers */

const multipliers = {

    "🍒": 4,

    "💎": 8,

    "7️⃣": 10,

    "🍋": 2,

    "🍊": 2

};


/* ================================
   AUDIO
================================ */


function getAudio() {

    if (!audioContext) {

        const AudioContext =
            window.AudioContext ||
            window.webkitAudioContext;

        if (AudioContext) {

            audioContext =
                new AudioContext();

        }

    }


    if (
        audioContext &&
        audioContext.state === "suspended"
    ) {

        audioContext.resume();

    }


    return audioContext;
}


function beep(
    frequency,
    duration,
    type = "square",
    volume = 0.04
) {

    const ctx = getAudio();

    if (!ctx) {
        return;
    }


    const oscillator =
        ctx.createOscillator();


    const gain =
        ctx.createGain();


    oscillator.type =
        type;


    oscillator.frequency.value =
        frequency;


    gain.gain.setValueAtTime(
        volume,
        ctx.currentTime
    );


    gain.gain.exponentialRampToValueAtTime(
        0.001,
        ctx.currentTime + duration
    );


    oscillator.connect(gain);

    gain.connect(ctx.destination);


    oscillator.start();


    oscillator.stop(
        ctx.currentTime + duration
    );

}


/* ================================
   RANDOM SYMBOL
================================ */


function randomSymbol() {

    return symbols[
        Math.floor(
            Math.random() *
            symbols.length
        )
    ];

}


/* ================================
   REEL ANIMATION
================================ */


function animateReel(
    reel,
    duration
) {

    return new Promise(resolve => {

        reel.classList.add(
            "spinning"
        );


        const interval =
            setInterval(() => {

                reel.textContent =
                    randomSymbol();

                beep(
                    100 +
                    Math.random() * 80,
                    0.025,
                    "square",
                    0.012
                );

            }, 70);


        setTimeout(() => {

            clearInterval(interval);


            reel.textContent =
                randomSymbol();


            reel.classList.remove(
                "spinning"
            );


            beep(
                320,
                0.08,
                "square",
                0.05
            );


            resolve();

        }, duration);

    });

}


/* ================================
   WIN SOUND
================================ */


function winSound(big) {

    const notes = big

        ? [
            392,
            523,
            659,
            784,
            1046,
            1318
        ]

        : [
            523,
            659,
            784,
            1046
        ];


    notes.forEach(
        (note, index) => {

            setTimeout(
                () => {

                    beep(
                        note,
                        0.18,
                        "triangle",
                        0.07
                    );

                },
                index * 120
            );

        }
    );

}


/* ================================
   JACKPOT EFFECT
================================ */


function jackpotEffect() {

    for (
        let i = 0;
        i < 35;
        i++
    ) {

        const item =
            document.createElement(
                "div"
            );


        item.className =
            "falling";


        item.textContent =
            Math.random() > 0.5
                ? "🎃"
                : "🪙";


        item.style.left =
            Math.random() *
            100 +
            "vw";


        item.style.animationDelay =
            Math.random() *
            0.5 +
            "s";


        document.body.appendChild(
            item
        );


        setTimeout(
            () => item.remove(),
            2200
        );

    }

}


/* ================================
   SPIN
================================ */


async function spin() {

    if (spinning) {
        return;
    }


    const player =
        playerName.value.trim();


    if (!player) {

        result.textContent =
            "Enter a player name first...";

        playerName.focus();

        return;

    }


    spinning = true;

    button.disabled = true;


    result.classList.remove(
        "win"
    );


    result.textContent =
        "The animatronic is watching...";


    getAudio();


    beep(
        130,
        0.12,
        "sawtooth",
        0.06
    );


    /* Three reels stop separately */

    const reel1 =
        animateReel(
            reels[0],
            1200
        );


    const reel2 =
        animateReel(
            reels[1],
            1800
        );


    const reel3 =
        animateReel(
            reels[2],
            2400
        );


    await Promise.all([
        reel1,
        reel2,
        reel3
    ]);


    const values =
        reels.map(
            reel =>
                reel.textContent
        );


    await checkResult(
        player,
        values
    );


    spinning = false;

    button.disabled = false;

}


/* ================================
   RESULT
================================ */


async function checkResult(
    player,
    values
) {

    const [
        a,
        b,
        c
    ] = values;


    /* JACKPOT */

    if (
        a === b &&
        b === c &&
        multipliers[a]
    ) {

        const multiplier =
            multipliers[a];


        const jackpot =
            100 * multiplier;


        result.classList.add(
            "win"
        );


        if (a === "7️⃣") {

            result.textContent =
                "💀 10× MEGA JACKPOT — " +
                jackpot +
                " POINTS! 💀";

        }

        else if (a === "💎") {

            result.textContent =
                "💎 8× DIAMOND JACKPOT — " +
                jackpot +
                " POINTS! 💎";

        }

        else if (a === "🍒") {

            result.textContent =
                "🍒 4× CHERRY JACKPOT — " +
                jackpot +
                " POINTS! 🍒";

        }

        else {

            result.textContent =
                a +
                " " +
                a +
                " " +
                a +
                " — " +
                multiplier +
                "× JACKPOT — " +
                jackpot +
                " POINTS!";

        }


        winSound(
            multiplier >= 8
        );


        jackpotEffect();


        /* Send jackpot to server */

        try {

            await fetch(
                "/api/score",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        name:
                            player,

                        score:
                            jackpot,

                        combination:
                            values.join(" ")

                    })

                }
            );

        }

        catch (error) {

            console.error(
                error
            );

        }


        loadLeaderboard();

    }


    /* TWO MATCHING SYMBOLS */

    else if (
        a === b ||
        b === c ||
        a === c
    ) {

        result.textContent =
            "👁 Something is watching...";


        beep(
            180,
            0.3,
            "sawtooth",
            0.05
        );

    }


    /* NOTHING */

    else {

        result.textContent =
            "Nothing but static... 🎃";

    }

}


/* ================================
   LEADERBOARD
================================ */


async function loadLeaderboard() {

    try {

        const response =
            await fetch(
                "/api/leaderboard"
            );


        const data =
            await response.json();


        const board =
            document.getElementById(
                "leaderboard"
            );


        if (!data.length) {

            board.innerHTML =
                '<div class="empty">' +
                'No jackpots yet. Be the first!' +
                '</div>';

            return;

        }


        board.innerHTML =
            data.map(
                (item, index) => `

                    <div class="leader">

                        <div class="rank">
                            #${index + 1}
                        </div>

                        <div>

                            <b>
                                ${escapeHtml(item.name)}
                            </b>

                            <div class="small">
                                ${escapeHtml(item.combination)}
                            </div>

                        </div>

                        <div class="score">
                            ${item.score}
                        </div>

                    </div>

                `
            ).join("");

    }

    catch (error) {

        document.getElementById(
            "leaderboard"
        ).innerHTML =
            '<div class="empty">' +
            'Leaderboard unavailable.' +
            '</div>';

    }

}


/* Prevent HTML injection in names */

function escapeHtml(value) {

    return String(value)

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );

}


/* ================================
   SPACEBAR SPIN
================================ */


document.addEventListener(
    "keydown",
    event => {

        if (
            event.code ===
            "Space"
        ) {

            event.preventDefault();


            if (!spinning) {

                spin();

            }

        }

    }
);


/* Load leaderboard */

loadLeaderboard();


/* Refresh leaderboard
   for multiple event machines */

setInterval(
    loadLeaderboard,
    3000
);

</script>

</body>

</html>
"""


# ==========================================
# WEB ROUTES
# ==========================================


@app.route("/")
def home():

    return render_template_string(
        HTML
    )


@app.route(
    "/api/leaderboard",
    methods=["GET"]
)
def get_leaderboard():

    data = load_leaderboard()

    data.sort(
        key=lambda item:
            item.get("score", 0),
        reverse=True
    )

    return jsonify(
        data[:50]
    )


@app.route(
    "/api/score",
    methods=["POST"]
)
def add_score():

    payload = (
        request.get_json(
            silent=True
        )
        or {}
    )


    name = str(
        payload.get(
            "name",
            "Player"
        )
    ).strip()[:20]


    combination = str(
        payload.get(
            "combination",
            ""
        )
    )[:50]


    try:

        score = int(
            payload.get(
                "score",
                0
            )
        )

    except (
        ValueError,
        TypeError
    ):

        score = 0


    # Server-side validation.
    # Only legitimate jackpot values
    # can enter the leaderboard.

    if (
        not name
        or score not in ALLOWED_JACKPOTS
    ):

        return jsonify(
            {
                "ok": False,
                "error":
                    "Invalid jackpot"
            }
        ), 400


    data =
        load_leaderboard()


    data.append(
        {
            "name": name,
            "score": score,
            "combination": combination,
            "time":
                datetime.now()
                .isoformat(
                    timespec="seconds"
                )
        }
    )


    data.sort(
        key=lambda item:
            item.get(
                "score",
                0
            ),
        reverse=True
    )


    # Keep only the top 50.

    data = data[:50]


    save_leaderboard(
        data
    )


    return jsonify(
        {
            "ok": True
        }
    )


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    print()
    print(
        "=========================================="
    )
    print(
        "     MIDNIGHT PIZZERIA - HAUNTED SLOTS"
    )
    print(
        "=========================================="
    )
    print()
    print(
        "Open in your browser:"
    )
    print(
        "http://127.0.0.1:5000"
    )
    print()
    print(
        "Leaderboard file:"
    )
    print(
        "leaderboard.json"
    )
    print()
    print(
        "Press CTRL+C to stop."
    )
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )