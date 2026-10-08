from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Haunted Jackpot</title>

<style>
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    width: 100%;
    min-height: 100%;
}

body {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    font-family: Arial, Helvetica, sans-serif;
    color: white;
    background:
        radial-gradient(circle at 50% 35%, #35104f 0%, #100817 45%, #030305 100%);
    overflow-x: hidden;
}

/* CRT EFFECT */

body::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 50;
    background:
        repeating-linear-gradient(
            to bottom,
            rgba(255,255,255,.025) 0px,
            rgba(255,255,255,.025) 1px,
            transparent 2px,
            transparent 4px
        );
}

/* VIGNETTE */

body::after {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 49;
    box-shadow:
        inset 0 0 180px rgba(0,0,0,.9);
}

/* MACHINE */

.machine {
    width: min(95vw, 850px);
    padding: 28px;
    border-radius: 30px;

    background:
        linear-gradient(
            145deg,
            #171717,
            #080808 55%,
            #151515
        );

    border: 5px solid #292929;

    box-shadow:
        0 0 0 3px #050505,
        0 0 30px rgba(255,0,50,.15),
        0 30px 70px rgba(0,0,0,.8),
        inset 0 0 40px rgba(0,0,0,.9);

    text-align: center;
    position: relative;
}

/* DECORATION */

.machine::before {
    content: "WARNING";
    position: absolute;
    top: 12px;
    left: 20px;
    font-size: 9px;
    letter-spacing: 4px;
    color: #8d8d8d;
    opacity: .5;
}

.machine::after {
    content: "PROPERTY OF THE NIGHT SHIFT";
    position: absolute;
    bottom: 10px;
    right: 20px;
    font-size: 8px;
    letter-spacing: 2px;
    color: #555;
}

/* TITLE */

.title {
    font-size: clamp(30px, 7vw, 60px);
    font-weight: 900;
    letter-spacing: 7px;
    margin-top: 12px;
    margin-bottom: 5px;

    color: #ddd;

    text-shadow:
        0 0 5px #fff,
        0 0 15px rgba(255,0,50,.6),
        0 4px 0 #111;
}

.subtitle {
    color: #666;
    font-size: 11px;
    letter-spacing: 5px;
    margin-bottom: 20px;
}

/* JACKPOT SIGN */

.jackpot {
    display: inline-block;
    padding: 9px 20px;
    margin-bottom: 20px;

    background: #080808;
    border: 2px solid #4c0b14;
    border-radius: 4px;

    color: #b21d32;
    font-weight: 900;
    letter-spacing: 3px;

    box-shadow:
        inset 0 0 15px #000,
        0 0 15px rgba(180,0,30,.15);
}

/* REELS */

.reels {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;

    padding: 18px;

    background:
        linear-gradient(#080808, #020202);

    border: 5px solid #222;
    border-radius: 10px;

    box-shadow:
        inset 0 0 35px #000,
        0 8px 20px rgba(0,0,0,.8);
}

.reel {
    height: 155px;

    display: flex;
    justify-content: center;
    align-items: center;

    overflow: hidden;

    background:
        linear-gradient(
            180deg,
            #e8e8e8,
            #ffffff 45%,
            #c8c8c8
        );

    border: 5px solid #111;
    border-radius: 7px;

    color: #111;

    font-size: clamp(55px, 12vw, 90px);

    user-select: none;

    box-shadow:
        inset 0 0 25px rgba(0,0,0,.5),
        0 0 10px rgba(255,255,255,.08);
}

.reel.spinning {
    animation: shake .08s infinite;
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

/* CONTROLS */

.controls {
    margin-top: 25px;
}

#spinButton {
    width: min(500px, 90%);
    padding: 20px;

    border: 4px solid #53101a;
    border-radius: 8px;

    cursor: pointer;

    font-size: 25px;
    font-weight: 900;
    letter-spacing: 4px;

    color: #eee;

    background:
        linear-gradient(
            #a41c2d,
            #510912
        );

    box-shadow:
        0 8px 0 #210307,
        0 0 25px rgba(180,0,30,.25);

    transition: .1s;
}

#spinButton:hover {
    filter: brightness(1.2);
}

#spinButton:active {
    transform: translateY(7px);

    box-shadow:
        0 1px 0 #210307,
        0 0 15px rgba(180,0,30,.4);
}

#spinButton:disabled {
    cursor: not-allowed;
    opacity: .5;
}

/* FULLSCREEN */

#fullscreenButton {
    margin-top: 15px;

    padding: 10px 20px;

    background: #0d0d0d;
    color: #aaa;

    border: 1px solid #333;
    border-radius: 4px;

    cursor: pointer;

    font-size: 12px;
    letter-spacing: 2px;
}

#fullscreenButton:hover {
    color: white;
    border-color: #777;
}

/* RESULT */

.result {
    min-height: 55px;

    margin-top: 20px;

    font-size: clamp(18px, 4vw, 28px);
    font-weight: 900;

    color: #aaa;

    text-shadow:
        0 0 10px currentColor;
}

.win {
    animation: winFlash .25s infinite alternate;
}

@keyframes winFlash {
    from {
        transform: scale(1);
        filter: brightness(1);
    }

    to {
        transform: scale(1.08);
        filter: brightness(1.6);
    }
}

/* FEED */

.feed {
    margin-top: 25px;

    background: #060606;

    border: 1px solid #222;
    border-radius: 8px;

    text-align: left;

    box-shadow:
        inset 0 0 20px #000;
}

.feedTitle {
    padding: 12px 15px;

    border-bottom: 1px solid #222;

    color: #777;

    font-size: 11px;
    font-weight: 900;

    letter-spacing: 3px;
}

.feedList {
    max-height: 190px;
    overflow-y: auto;
}

.feedItem {
    display: flex;
    justify-content: space-between;
    gap: 10px;

    padding: 10px 15px;

    border-bottom: 1px solid #151515;

    font-size: 13px;
}

.feedName {
    color: #bbb;
}

.feedTime {
    color: #555;
    white-space: nowrap;
}

.emptyFeed {
    padding: 18px;
    text-align: center;

    color: #444;

    font-size: 12px;
}

/* PAYTABLE */

.paytable {
    margin-top: 18px;

    padding: 15px;

    background: rgba(0,0,0,.45);

    border: 1px solid #202020;
    border-radius: 7px;

    color: #777;

    font-size: 12px;
    line-height: 1.8;
}

.paytable strong {
    color: #aaa;
}

/* COINS */

.coin {
    position: fixed;

    pointer-events: none;

    z-index: 100;

    font-size: 28px;

    animation:
        coinFall 1.4s linear forwards;
}

@keyframes coinFall {
    0% {
        transform:
            translateY(-30px)
            rotate(0deg);

        opacity: 1;
    }

    100% {
        transform:
            translateY(100vh)
            rotate(720deg);

        opacity: 0;
    }
}

/* RESPONSIVE */

@media (max-width: 600px) {

    body {
        padding: 8px;
    }

    .machine {
        padding: 15px;
    }

    .reels {
        gap: 7px;
        padding: 9px;
    }

    .reel {
        height: 110px;
        border-width: 3px;
    }

    #spinButton {
        font-size: 20px;
        padding: 16px;
    }
}

</style>
</head>

<body>

<div class="machine">

    <div class="title">
        HAUNTED JACKPOT
    </div>

    <div class="subtitle">
        NIGHT SHIFT // FREE PLAY
    </div>

    <div class="jackpot">
        INFINITE SPINS
    </div>

    <div class="reels">

        <div class="reel" id="reel1">🍒</div>

        <div class="reel" id="reel2">🍋</div>

        <div class="reel" id="reel3">🍊</div>

    </div>

    <div class="controls">

        <button id="spinButton" onclick="spin()">
            SPIN
        </button>

        <br>

        <button id="fullscreenButton"
                onclick="toggleFullscreen()">
            ⛶ FULL SCREEN
        </button>

        <div id="result" class="result">
            Good luck...
        </div>

    </div>

    <div class="paytable">

        <strong>PAYTABLE</strong><br>

        🍒 🍒 🍒 = 4×<br>
        💎 💎 💎 = 8×<br>
        7️⃣ 7️⃣ 7️⃣ = 10×<br>
        🍋 🍋 🍋 = 2×<br>
        🍊 🍊 🍊 = 2×<br>
        ANY EXACT DOUBLE = 1.5×

    </div>

    <div class="feed">

        <div class="feedTitle">
            JACKPOT / DOUBLE FEED
        </div>

        <div id="feedList" class="feedList">

            <div class="emptyFeed">
                No unusual activity detected...
            </div>

        </div>

    </div>

    <div class="credits">
        Free-play machine — no real money involved.
    </div>

</div>


<script>

/*
====================================================
ORIGINAL SYMBOL SYSTEM
====================================================

This is the symbol pool from your original code.

Keeping all 7 symbols makes matching considerably
harder than the 5-symbol version.
*/

const symbols = [

    "🍒",
    "🍋",
    "🍊",
    "🍉",
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


let spinning = false;


/*
====================================================
AUDIO
====================================================
*/

const AudioContext =
    window.AudioContext ||
    window.webkitAudioContext;

let audioContext = null;


function getAudio() {

    if (!audioContext) {

        audioContext =
            new AudioContext();

    }

    if (audioContext.state === "suspended") {

        audioContext.resume();

    }

    return audioContext;

}


function beep(
    frequency,
    duration,
    type = "square",
    volume = 0.06
) {

    const ctx = getAudio();

    const oscillator =
        ctx.createOscillator();

    const gain =
        ctx.createGain();


    oscillator.type = type;

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


/*
====================================================
SOUNDS
====================================================
*/

function spinSound() {

    beep(180, .05);

    setTimeout(
        () => beep(220, .05),
        80
    );

    setTimeout(
        () => beep(260, .05),
        160
    );

}


function stopSound() {

    beep(350, .08);

}


function doubleSound() {

    beep(
        440,
        .12,
        "sine",
        .07
    );

    setTimeout(
        () => beep(
            660,
            .18,
            "sine",
            .08
        ),
        100
    );

}


function winSound() {

    const notes = [

        523,
        659,
        784,
        1046,
        1318

    ];


    notes.forEach(
        (note, index) => {

            setTimeout(
                () => {

                    beep(
                        note,
                        .18,
                        "sine",
                        .08
                    );

                },
                index * 120
            );

        }
    );

}


function jackpotSound() {

    const notes = [

        523,
        659,
        784,
        1046,
        1318,
        1568

    ];


    notes.forEach(
        (note, index) => {

            setTimeout(
                () => {

                    beep(
                        note,
                        .25,
                        "triangle",
                        .1
                    );

                },
                index * 150
            );

        }
    );

}


/*
====================================================
ORIGINAL RANDOM SYMBOL FUNCTION
====================================================
*/

function randomSymbol() {

    return symbols[
        Math.floor(
            Math.random() *
            symbols.length
        )
    ];

}


/*
====================================================
COIN EFFECT
====================================================
*/

function makeCoins() {

    for (let i = 0; i < 35; i++) {

        const coin =
            document.createElement("div");

        coin.className = "coin";

        coin.textContent =
            Math.random() > .5
                ? "🪙"
                : "💰";


        coin.style.left =
            Math.random() * 100 + "vw";


        coin.style.top =
            (-Math.random() * 30) + "vh";


        coin.style.animationDelay =
            Math.random() * .5 + "s";


        document.body.appendChild(coin);


        setTimeout(
            () => coin.remove(),
            2000
        );

    }

}


/*
====================================================
JACKPOT / DOUBLE FEED
====================================================
*/

let feedEvents = [];


function addFeedEvent(name) {

    feedEvents.unshift({

        name: name,

        time: Date.now()

    });


    /*
     * Keep the feed from growing forever.
     */

    if (feedEvents.length > 50) {

        feedEvents.length = 50;

    }


    renderFeed();

}


function timeAgo(timestamp) {

    const seconds =
        Math.floor(
            (Date.now() - timestamp) / 1000
        );


    if (seconds < 5) {

        return "just now";

    }


    if (seconds < 60) {

        return seconds + " seconds ago";

    }


    const minutes =
        Math.floor(seconds / 60);


    if (minutes < 60) {

        return minutes + " minutes ago";

    }


    const hours =
        Math.floor(minutes / 60);


    return hours + " hours ago";

}


function renderFeed() {

    const feed =
        document.getElementById("feedList");


    if (feedEvents.length === 0) {

        feed.innerHTML = `
            <div class="emptyFeed">
                No unusual activity detected...
            </div>
        `;

        return;

    }


    feed.innerHTML =
        feedEvents.map(event => {

            return `

                <div class="feedItem">

                    <div class="feedName">
                        ${event.name}
                    </div>

                    <div class="feedTime">
                        ${timeAgo(event.time)}
                    </div>

                </div>

            `;

        }).join("");

}


/*
 * Update feed timestamps.
 */

setInterval(
    renderFeed,
    10000
);


/*
====================================================
ORIGINAL REEL ANIMATION SYSTEM
====================================================

65ms random symbol changes.

The reels stop at:

Reel 1 = 1300ms
Reel 2 = 1900ms
Reel 3 = 2500ms
*/

function animateReel(reel, duration) {

    return new Promise(resolve => {

        reel.classList.add("spinning");


        const interval =
            setInterval(() => {

                reel.textContent =
                    randomSymbol();

            }, 65);


        setTimeout(() => {

            clearInterval(interval);


            /*
             * IMPORTANT:
             *
             * The final symbol is selected
             * using the SAME original
             * randomSymbol() system.
             */

            reel.textContent =
                randomSymbol();


            reel.classList.remove(
                "spinning"
            );


            stopSound();


            resolve();

        }, duration);

    });

}


/*
====================================================
MAIN SPIN
====================================================
*/

async function spin() {

    if (spinning) {

        return;

    }


    spinning = true;

    button.disabled = true;


    result.classList.remove("win");

    result.textContent =
        "Spinning...";


    getAudio();

    spinSound();


    /*
     * Same original reel timing.
     */

    const reel1 =
        animateReel(
            reels[0],
            1300
        );


    const reel2 =
        animateReel(
            reels[1],
            1900
        );


    const reel3 =
        animateReel(
            reels[2],
            2500
        );


    await Promise.all([

        reel1,
        reel2,
        reel3

    ]);


    const values =
        reels.map(
            reel => reel.textContent
        );


    checkResult(values);


    spinning = false;

    button.disabled = false;

}


/*
====================================================
RESULT CHECK
====================================================
*/

function checkResult(values) {

    const [a, b, c] =
        values;


    /*
     * THREE OF A KIND
     */

    if (
        a === b &&
        b === c
    ) {

        result.classList.add("win");


        /*
         * 7 = 10x
         */

        if (a === "7️⃣") {

            result.textContent =
                "💀💀💀 MEGA JACKPOT — 10× 💀💀💀";


            addFeedEvent(
                "💀 MEGA JACKPOT — 10×"
            );


            jackpotSound();

            makeCoins();

        }


        /*
         * Diamond = 8x
         */

        else if (a === "💎") {

            result.textContent =
                "💎💎💎 DIAMOND JACKPOT — 8×";


            addFeedEvent(
                "💎 DIAMOND JACKPOT — 8×"
            );


            jackpotSound();

            makeCoins();

        }


        /*
         * Cherry = 4x
         */

        else if (a === "🍒") {

            result.textContent =
                "🍒🍒🍒 CHERRY JACKPOT — 4×";


            addFeedEvent(
                "🍒 CHERRY JACKPOT — 4×"
            );


            jackpotSound();

            makeCoins();

        }


        /*
         * Lemon = 2x
         */

        else if (a === "🍋") {

            result.textContent =
                "🍋🍋🍋 LEMON JACKPOT — 2×";


            addFeedEvent(
                "🍋 LEMON JACKPOT — 2×"
            );


            winSound();

            makeCoins();

        }


        /*
         * Orange = 2x
         */

        else if (a === "🍊") {

            result.textContent =
                "🍊🍊🍊 ORANGE JACKPOT — 2×";


            addFeedEvent(
                "🍊 ORANGE JACKPOT — 2×"
            );


            winSound();

            makeCoins();

        }


        /*
         * Other symbols
         */

        else if (a === "⭐") {

            result.textContent =
                "⭐⭐⭐ STAR JACKPOT";


            addFeedEvent(
                "⭐ STAR JACKPOT"
            );


            winSound();

            makeCoins();

        }


        else {

            result.textContent =
                "🍉🍉🍉 THREE OF A KIND";


            addFeedEvent(
                "🍉 THREE OF A KIND"
            );


            winSound();

        }


        return;

    }


    /*
     * EXACTLY TWO MATCH
     *
     * This is checked only after
     * confirming it wasn't a triple.
     */

    if (
        a === b ||
        b === c ||
        a === c
    ) {

        result.textContent =
            "⚠ DOUBLE MATCH — 1.5×";


        addFeedEvent(
            "⚠ DOUBLE MATCH — 1.5×"
        );


        doubleSound();


        return;

    }


    /*
     * NOTHING
     */

    result.textContent =
        "Nothing... try again.";

}


/*
====================================================
FULL SCREEN
====================================================
*/

async function toggleFullscreen() {

    const button =
        document.getElementById(
            "fullscreenButton"
        );


    if (!document.fullscreenElement) {

        try {

            await document.documentElement
                .requestFullscreen();


            button.textContent =
                "⛶ EXIT FULL SCREEN";

        }

        catch (error) {

            console.log(
                "Fullscreen unavailable",
                error
            );

        }

    }

    else {

        await document.exitFullscreen();

        button.textContent =
            "⛶ FULL SCREEN";

    }

}


/*
 * Keep button text correct if
 * fullscreen is exited with ESC.
 */

document.addEventListener(
    "fullscreenchange",
    () => {

        const button =
            document.getElementById(
                "fullscreenButton"
            );


        if (document.fullscreenElement) {

            button.textContent =
                "⛶ EXIT FULL SCREEN";

        }

        else {

            button.textContent =
                "⛶ FULL SCREEN";

        }

    }
);


/*
====================================================
SPACEBAR
====================================================
*/

document.addEventListener(
    "keydown",
    function(event) {

        if (
            event.code === "Space" &&
            !spinning
        ) {

            event.preventDefault();

            spin();

        }

    }
);

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


if __name__ == "__main__":

    print()
    print("==========================================")
    print("          HAUNTED JACKPOT")
    print("==========================================")
    print()
    print("Server running at:")
    print("http://127.0.0.1:5000")
    print()
    print("Press CTRL+C to stop the server.")
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
