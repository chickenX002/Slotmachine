from flask import Flask, render_template_string

app = Flask(__name__)


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
   RESET
   ========================================================= */

* {
    box-sizing: border-box;
}

html,
body {
    margin: 0;
    padding: 0;
    min-height: 100%;
}


/* =========================================================
   BODY
   ========================================================= */

body {

    background:
        radial-gradient(
            ellipse at 50% 15%,
            #28162b 0%,
            #120b14 38%,
            #050506 100%
        );

    color: #d1c5ca;

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
            to bottom,
            rgba(255,255,255,0.018) 0px,
            rgba(255,255,255,0.018) 1px,
            transparent 1px,
            transparent 4px
        );

    opacity: .5;
}


/* CRT vignette */

body::after {

    content: "";

    position: fixed;

    inset: 0;

    pointer-events: none;

    z-index: 99;

    box-shadow:
        inset 0 0 180px rgba(0,0,0,.95);
}


/* =========================================================
   BACKGROUND
   ========================================================= */

.background {

    position: fixed;

    inset: 0;

    pointer-events: none;

    overflow: hidden;

    z-index: 0;
}


/* Fake old wall stains */

.stain {

    position: absolute;

    border-radius: 50%;

    filter: blur(2px);

    opacity: .12;

    background: #6d3045;
}

.stain.one {

    width: 230px;
    height: 180px;

    top: 8%;
    left: 4%;
}

.stain.two {

    width: 300px;
    height: 200px;

    bottom: 5%;
    right: 4%;
}

.stain.three {

    width: 180px;
    height: 130px;

    top: 48%;
    right: 18%;
}


/* =========================================================
   PAGE
   ========================================================= */

.page {

    position: relative;

    z-index: 2;

    width: min(1180px, 94%);

    margin: auto;

    padding:
        25px
        0
        60px;
}


/* =========================================================
   HEADER
   ========================================================= */

.header {

    text-align: center;

    margin-bottom: 22px;
}

.header-small {

    color: #75616c;

    font-family: Arial, sans-serif;

    font-size: 10px;

    letter-spacing: 6px;

    margin-bottom: 7px;
}

.title {

    margin: 0;

    color: #bdb1b7;

    font-family:
        Impact,
        Haettenschweiler,
        "Arial Narrow Bold",
        sans-serif;

    font-size:
        clamp(43px, 8vw, 82px);

    letter-spacing: 5px;

    text-shadow:
        4px 4px 0 #0b090b,
        7px 7px 0 #050405,
        0 0 18px rgba(190,40,50,.16);

    transform: rotate(-1deg);
}

.subtitle {

    margin-top: 7px;

    color: #715967;

    font-family: Arial, sans-serif;

    font-size: 10px;

    letter-spacing: 4px;
}


/* =========================================================
   FULLSCREEN BUTTON
   ========================================================= */

.fullscreen-button {

    position: fixed;

    top: 16px;

    right: 16px;

    z-index: 150;

    padding:
        9px
        13px;

    border:
        1px solid #49333d;

    background:
        rgba(10,8,11,.88);

    color: #9e8a93;

    font-family: Arial, sans-serif;

    font-size: 11px;

    letter-spacing: 1px;

    cursor: pointer;

    box-shadow:
        0 4px 15px rgba(0,0,0,.5);

    transition:
        .15s;
}

.fullscreen-button:hover {

    color: #ddd;

    border-color: #75505e;

    background: #181017;
}


/* =========================================================
   MACHINE
   ========================================================= */

.machine {

    position: relative;

    max-width: 910px;

    margin: auto;

    padding: 26px;

    background:
        linear-gradient(
            90deg,
            #09090a 0%,
            #191317 9%,
            #100d11 50%,
            #191317 91%,
            #080809 100%
        );

    border:
        5px solid #070608;

    border-radius: 22px;

    box-shadow:
        0 30px 65px rgba(0,0,0,.85),
        inset 0 0 0 2px #33252d,
        inset 0 0 40px rgba(0,0,0,.95);
}


/* Machine screws */

.machine::before,
.machine::after {

    content: "";

    position: absolute;

    top: 12px;

    width: 11px;

    height: 11px;

    border-radius: 50%;

    background: #353033;

    border:
        2px solid #080708;

    box-shadow:
        inset 1px 1px 2px #777,
        0 1px 2px #000;
}

.machine::before {
    left: 13px;
}

.machine::after {
    right: 13px;
}


/* =========================================================
   WARNING STRIP
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
            #2b1c22 10px,
            #2b1c22 20px
        );

    border:
        1px solid #4b333d;

    color: #987782;

    font-family: Arial, sans-serif;

    font-size: 9px;

    letter-spacing: 3px;
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

    padding:
        7px
        38px;

    border-top:
        2px solid #3b2b32;

    border-bottom:
        2px solid #3b2b32;

    color: #c9bec3;

    font-family:
        Impact,
        Haettenschweiler,
        sans-serif;

    font-size: 25px;

    letter-spacing: 4px;

    text-shadow:
        0 0 10px rgba(255,255,255,.08);
}


/* =========================================================
   REEL AREA
   ========================================================= */

.reel-frame {

    padding: 13px;

    background: #050506;

    border:
        8px solid #090809;

    border-radius: 12px;

    box-shadow:
        inset 0 0 0 2px #30242a,
        inset 0 0 35px #000,
        0 9px 25px rgba(0,0,0,.8);
}

.reels {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 12px;
}


/* =========================================================
   REELS
   ========================================================= */

.reel {

    height: 190px;

    display: flex;

    align-items: center;

    justify-content: center;

    overflow: hidden;

    background:
        linear-gradient(
            90deg,
            #08080a,
            #1b181d,
            #08080a
        );

    border:
        3px solid #241e22;

    border-radius: 8px;

    font-family: Arial, sans-serif;

    font-size:
        clamp(65px, 11vw, 105px);

    text-shadow:
        0 0 12px rgba(255,255,255,.16);

    box-shadow:
        inset 0 0 30px #000;
}


/* Exact spinning style from original */

.reel.spinning {

    animation:
        reelShake .07s infinite linear;
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
   CONTROLS
   ========================================================= */

.controls {

    text-align: center;

    margin-top: 24px;
}


/* Spin button */

#spinButton {

    width: 125px;

    height: 125px;

    border-radius: 50%;

    border:
        4px solid #280d14;

    cursor: pointer;

    color: #f3d9d5;

    font-family:
        Impact,
        Haettenschweiler,
        sans-serif;

    font-size: 23px;

    letter-spacing: 2px;

    background:
        radial-gradient(
            circle at 35% 28%,
            #ff6b61,
            #bf251f 42%,
            #69100e 75%,
            #270707
        );

    box-shadow:
        0 9px 0 #170405,
        0 12px 25px rgba(0,0,0,.8),
        0 0 25px rgba(170,20,20,.15);

    transition:
        transform .08s,
        filter .15s;
}

#spinButton:hover {

    filter: brightness(1.15);
}

#spinButton:active {

    transform:
        translateY(8px);

    box-shadow:
        0 2px 0 #170405,
        0 5px 15px rgba(0,0,0,.8);
}

#spinButton:disabled {

    cursor: not-allowed;

    opacity: .55;

    filter: grayscale(.6);
}


/* =========================================================
   RESULT
   ========================================================= */

.result {

    min-height: 42px;

    margin-top: 20px;

    color: #685b62;

    font-family:
        Impact,
        Haettenschweiler,
        sans-serif;

    font-size: 24px;

    letter-spacing: 2px;
}

.result.win {

    color: #d4b36b;

    text-shadow:
        0 0 12px rgba(255,180,70,.3);

    animation:
        resultFlicker .15s 5;
}

@keyframes resultFlicker {

    0%,
    100% {
        opacity: 1;
    }

    50% {
        opacity: .25;
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

    padding: 20px;

    background:
        linear-gradient(
            145deg,
            #141014,
            #0a090c
        );

    border:
        2px solid #2a2027;

    box-shadow:
        inset 0 0 25px rgba(0,0,0,.75),
        0 10px 30px rgba(0,0,0,.4);
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

    padding:
        11px
        4px;

    border-bottom:
        1px dotted #30262c;

    color: #81737a;

    font-family: Arial, sans-serif;
}

.pay-symbol {

    min-width: 85px;

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

    padding-right: 4px;
}

.feed::-webkit-scrollbar {

    width: 5px;
}

.feed::-webkit-scrollbar-track {

    background: #080708;
}

.feed::-webkit-scrollbar-thumb {

    background: #3d2931;
}


/* Individual event */

.feed-item {

    padding:
        13px
        10px;

    margin-bottom: 8px;

    border-left:
        3px solid #552631;

    background:
        linear-gradient(
            90deg,
            rgba(90,35,45,.13),
            transparent
        );

    animation:
        feedAppear .3s ease-out;
}

@keyframes feedAppear {

    from {

        opacity: 0;

        transform:
            translateX(-10px);
    }

    to {

        opacity: 1;

        transform:
            translateX(0);
    }
}

.feed-name {

    color: #c0adb5;

    font-family:
        Impact,
        Haettenschweiler,
        sans-serif;

    font-size: 17px;

    letter-spacing: 2px;
}

.feed-time {

    margin-top: 3px;

    color: #5e5158;

    font-family: Arial, sans-serif;

    font-size: 11px;
}


/* Empty feed */

.feed-empty {

    padding:
        40px
        10px;

    text-align: center;

    color: #4d454a;

    font-family: Arial, sans-serif;

    font-size: 11px;

    letter-spacing: 2px;
}


/* =========================================================
   COINS / CELEBRATION
   ========================================================= */

.coin {

    position: fixed;

    z-index: 200;

    pointer-events: none;

    font-size: 28px;

    animation:
        coinFall 1.3s linear forwards;
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


/* =========================================================
   FOOTER
   ========================================================= */

.footer {

    margin-top: 20px;

    text-align: center;

    color: #40383d;

    font-family: Arial, sans-serif;

    font-size: 9px;

    letter-spacing: 3px;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 760px) {

    .page {
        width: 96%;
    }

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

    #spinButton {
        width: 110px;
        height: 110px;
    }

    .fullscreen-button {
        top: 8px;
        right: 8px;
    }
}

</style>

</head>


<body>


<!-- Background -->

<div class="background">

    <div class="stain one"></div>

    <div class="stain two"></div>

    <div class="stain three"></div>

</div>


<!-- Fullscreen -->

<button
    class="fullscreen-button"
    id="fullscreenButton"
    onclick="toggleFullscreen()"
>
    ⛶ FULL SCREEN
</button>


<div class="page">


    <!-- =====================================================
         HEADER
         ===================================================== -->

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

            <span>
                HAUNTED JACKPOT
            </span>

        </div>


        <!-- REELS -->

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


        <!-- SPIN -->

        <div class="controls">

            <button
                id="spinButton"
                onclick="spin()"
            >
                SPIN
            </button>


            <div
                id="result"
                class="result"
            >
                THE MACHINE IS WAITING
            </div>

        </div>


    </main>


    <!-- =====================================================
         PAYTABLE + FEED
         ===================================================== -->

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
                    7️⃣ 7️⃣ 7️⃣
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
                    ANY 2
                </span>

                <span class="pay-name">
                    DOUBLE MATCH
                </span>

                <span class="pay-value">
                    1.5×
                </span>

            </div>

        </div>


        <!-- JACKPOT FEED -->

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

                    <br>
                    <br>

                    THE MACHINE IS WAITING.

                </div>

            </div>

        </div>


    </section>


    <footer class="footer">

        FREE-PLAY HALLOWEEN MACHINE
        •
        NO REAL MONEY

    </footer>


</div>


<script>

/* =========================================================
   SYMBOLS
   ========================================================= */

/*
 * Same choosing approach as your original code.
 *
 * Every symbol has the same chance of being selected.
 */

const symbols = [

    "🍒",
    "💎",
    "7️⃣",
    "🍋",
    "🍊"

];


/* =========================================================
   ELEMENTS
   ========================================================= */

const reels = [

    document.getElementById("reel1"),

    document.getElementById("reel2"),

    document.getElementById("reel3")

];

const button =
    document.getElementById(
        "spinButton"
    );

const result =
    document.getElementById(
        "result"
    );

const feed =
    document.getElementById(
        "feed"
    );


let spinning = false;


/* =========================================================
   AUDIO
   ========================================================= */

const AudioContext =
    window.AudioContext ||
    window.webkitAudioContext;

let audioContext = null;


function getAudio() {

    if (!audioContext) {

        audioContext =
            new AudioContext();
    }


    if (
        audioContext.state ===
        "suspended"
    ) {

        audioContext.resume();
    }


    return audioContext;
}


function beep(
    frequency,
    duration,
    type = "square",
    volume = .06
) {

    const ctx =
        getAudio();


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
        .001,
        ctx.currentTime + duration
    );


    oscillator.connect(gain);

    gain.connect(
        ctx.destination
    );


    oscillator.start();

    oscillator.stop(
        ctx.currentTime + duration
    );
}


/* =========================================================
   SPIN SOUND
   ========================================================= */

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


/* =========================================================
   REEL STOP SOUND
   ========================================================= */

function stopSound() {

    beep(
        350,
        .08
    );
}


/* =========================================================
   NORMAL WIN SOUND
   ========================================================= */

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


/* =========================================================
   JACKPOT SOUND
   ========================================================= */

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


/* =========================================================
   RANDOM SYMBOL
   ========================================================= */

/*
 * This is the same random-symbol selection
 * method from your original code.
 */

function randomSymbol() {

    return symbols[
        Math.floor(
            Math.random() *
            symbols.length
        )
    ];
}


/* =========================================================
   COIN EFFECT
   ========================================================= */

function makeCoins() {

    for (
        let i = 0;
        i < 35;
        i++
    ) {

        const coin =
            document.createElement(
                "div"
            );


        coin.className =
            "coin";


        coin.textContent =
            Math.random() > .5
                ? "🪙"
                : "💰";


        coin.style.left =
            Math.random() *
            100 +
            "vw";


        coin.style.top =
            (-Math.random() * 30) +
            "vh";


        coin.style.animationDelay =
            Math.random() *
            .5 +
            "s";


        document.body.appendChild(
            coin
        );


        setTimeout(
            () => coin.remove(),
            2000
        );
    }
}


/* =========================================================
   ANIMATE ONE REEL
   ========================================================= */

/*
 * This keeps the original:
 *
 * - 65ms symbol changes
 * - randomSymbol()
 * - staggered stopping
 */

function animateReel(
    reel,
    duration
) {

    return new Promise(
        resolve => {

            reel.classList.add(
                "spinning"
            );


            const interval =
                setInterval(
                    () => {

                        reel.textContent =
                            randomSymbol();

                    },
                    65
                );


            setTimeout(
                () => {

                    clearInterval(
                        interval
                    );


                    /*
                     * Final symbol is also
                     * chosen with randomSymbol().
                     */

                    reel.textContent =
                        randomSymbol();


                    reel.classList.remove(
                        "spinning"
                    );


                    stopSound();


                    resolve();

                },
                duration
            );

        }
    );
}


/* =========================================================
   MAIN SPIN
   ========================================================= */

async function spin() {

    if (spinning) {
        return;
    }


    spinning = true;

    button.disabled = true;


    result.classList.remove(
        "win"
    );


    result.textContent =
        "SPINNING...";


    getAudio();

    spinSound();


    /*
     * ORIGINAL TIMING:
     *
     * Reel 1 = 1300ms
     * Reel 2 = 1900ms
     * Reel 3 = 2500ms
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


    /*
     * Read the final symbols.
     */

    const values =
        reels.map(
            reel =>
                reel.textContent
        );


    checkResult(
        values
    );


    spinning = false;

    button.disabled = false;
}


/* =========================================================
   CHECK RESULT
   ========================================================= */

function checkResult(
    values
) {

    const [
        a,
        b,
        c
    ] = values;


    /* =====================================================
       THREE OF A KIND
       ===================================================== */

    if (
        a === b &&
        b === c
    ) {

        result.classList.add(
            "win"
        );


        let jackpotName = "";
        let multiplier = 0;


        if (a === "🍒") {

            jackpotName =
                "🍒 CHERRY JACKPOT";

            multiplier = 4;

        }

        else if (a === "💎") {

            jackpotName =
                "💎 DIAMOND JACKPOT";

            multiplier = 8;

        }

        else if (a === "7️⃣") {

            jackpotName =
                "7️⃣ SEVEN JACKPOT";

            multiplier = 10;

        }

        else if (a === "🍋") {

            jackpotName =
                "🍋 LEMON JACKPOT";

            multiplier = 2;

        }

        else if (a === "🍊") {

            jackpotName =
                "🍊 ORANGE JACKPOT";

            multiplier = 2;

        }


        result.textContent =
            jackpotName +
            " — " +
            multiplier +
            "×";


        jackpotSound();

        makeCoins();


        /*
         * Add jackpot to feed.
         */

        addFeedEvent(
            jackpotName
        );


        return;
    }


    /* =====================================================
       EXACTLY TWO MATCH
       ===================================================== */

    if (
        a === b ||
        b === c ||
        a === c
    ) {

        result.classList.add(
            "win"
        );


        result.textContent =
            "DOUBLE MATCH — 1.5×";


        beep(
            500,
            .12,
            "sine",
            .07
        );


        /*
         * Add the double to feed.
         */

        addFeedEvent(
            "🎃 DOUBLE MATCH — 1.5×"
        );


        return;
    }


    /* =====================================================
       NO MATCH
       ===================================================== */

    result.textContent =
        "NOTHING... THE MACHINE STARES BACK.";
}


/* =========================================================
   JACKPOT FEED
   ========================================================= */

let feedEvents = [];


function addFeedEvent(
    name
) {

    feedEvents.unshift({

        name: name,

        time: Date.now()

    });


    /*
     * Keep the feed from becoming huge.
     */

    if (
        feedEvents.length > 50
    ) {

        feedEvents =
            feedEvents.slice(
                0,
                50
            );
    }


    renderFeed();
}


/* =========================================================
   TIME AGO
   ========================================================= */

function timeAgo(
    timestamp
) {

    const seconds =
        Math.floor(
            (Date.now() - timestamp) /
            1000
        );


    if (
        seconds < 5
    ) {

        return "just now";
    }


    if (
        seconds < 60
    ) {

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


    if (
        minutes < 60
    ) {

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


/* =========================================================
   RENDER FEED
   ========================================================= */

function renderFeed() {

    if (
        feedEvents.length === 0
    ) {

        feed.innerHTML = `

            <div class="feed-empty">

                NO JACKPOTS YET...

                <br>
                <br>

                THE MACHINE IS WAITING.

            </div>

        `;

        return;
    }


    feed.innerHTML = "";


    feedEvents.forEach(
        event => {

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
                timeAgo(
                    event.time
                );


            item.appendChild(
                name
            );


            item.appendChild(
                time
            );


            feed.appendChild(
                item
            );

        }
    );
}


/* =========================================================
   UPDATE FEED TIMES
   ========================================================= */

setInterval(
    renderFeed,
    5000
);


/* =========================================================
   FULLSCREEN
   ========================================================= */

async function toggleFullscreen() {

    const button =
        document.getElementById(
            "fullscreenButton"
        );


    /*
     * Enter fullscreen.
     */

    if (
        !document.fullscreenElement
    ) {

        try {

            await document.documentElement.requestFullscreen();

            button.textContent =
                "⛶ EXIT FULL SCREEN";

        }

        catch (error) {

            console.error(
                "Fullscreen failed:",
                error
            );

        }

    }

    /*
     * Exit fullscreen.
     */

    else {

        try {

            await document.exitFullscreen();

            button.textContent =
                "⛶ FULL SCREEN";

        }

        catch (error) {

            console.error(
                "Could not exit fullscreen:",
                error
            );
        }
    }
}


/* =========================================================
   KEEP BUTTON TEXT CORRECT
   ========================================================= */

document.addEventListener(
    "fullscreenchange",
    () => {

        const button =
            document.getElementById(
                "fullscreenButton"
            );


        if (
            document.fullscreenElement
        ) {

            button.textContent =
                "⛶ EXIT FULL SCREEN";

        }

        else {

            button.textContent =
                "⛶ FULL SCREEN";
        }

    }
);


/* =========================================================
   SPACEBAR = SPIN
   ========================================================= */

document.addEventListener(
    "keydown",
    event => {

        if (
            event.code === "Space"
        ) {

            event.preventDefault();


            if (!spinning) {

                spin();
            }
        }
    }
);


/* =========================================================
   INITIAL FEED
   ========================================================= */

renderFeed();

</script>

</body>

</html>
"""


# ============================================================
# FLASK ROUTE
# ============================================================

@app.route("/")
def home():

    return render_template_string(
        HTML
    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    print()
    print("==============================================")
    print("             THE NIGHT SHIFT")
    print("          HAUNTED SLOT MACHINE")
    print("==============================================")
    print()
    print("Open:")
    print("http://127.0.0.1:5000")
    print()
    print("Press CTRL+C to stop.")
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
