from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Infinite Slot Machine</title>

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
            font-family: Arial, Helvetica, sans-serif;
            background:
                radial-gradient(circle at center, #3b0764 0%, #17002b 45%, #050008 100%);
            color: white;
            overflow: hidden;
        }

        .machine {
            width: min(92vw, 650px);
            padding: 25px;
            border-radius: 30px;
            background: linear-gradient(145deg, #ffcf33, #b87500);
            box-shadow:
                0 0 20px #ffd700,
                0 0 60px rgba(255, 174, 0, 0.45),
                inset 0 0 15px rgba(255,255,255,.5);
            border: 6px solid #ffe98a;
            text-align: center;
        }

        .title {
            font-size: clamp(28px, 7vw, 48px);
            font-weight: 900;
            letter-spacing: 4px;
            color: #fff;
            text-shadow:
                0 3px 0 #a44d00,
                0 0 15px #fff;
            margin-bottom: 18px;
        }

        .jackpot {
            display: inline-block;
            padding: 8px 18px;
            margin-bottom: 18px;
            border-radius: 20px;
            background: #17001f;
            border: 2px solid #ffd700;
            color: #ffd700;
            font-weight: bold;
            box-shadow: inset 0 0 15px #000;
        }

        .reels {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            padding: 15px;
            background: #090909;
            border: 5px solid #3c2200;
            border-radius: 18px;
            box-shadow:
                inset 0 0 25px #000,
                0 5px 10px rgba(0,0,0,.5);
        }

        .reel {
            height: 145px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            border-radius: 12px;
            background: linear-gradient(#fff, #ddd);
            border: 4px solid #222;
            box-shadow:
                inset 0 0 20px rgba(0,0,0,.4),
                0 0 10px rgba(255,255,255,.25);
            color: #111;
            font-size: clamp(55px, 12vw, 85px);
            user-select: none;
        }

        .reel.spinning {
            animation: shake .08s infinite;
        }

        @keyframes shake {
            0% { transform: translateY(-2px); }
            50% { transform: translateY(2px); }
            100% { transform: translateY(-2px); }
        }

        .controls {
            margin-top: 20px;
        }

        #spinButton {
            width: 85%;
            padding: 18px;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            font-size: 25px;
            font-weight: 900;
            letter-spacing: 2px;
            color: white;
            background: linear-gradient(#ff4545, #a90000);
            border: 4px solid #ffb3b3;
            box-shadow:
                0 7px 0 #650000,
                0 0 25px rgba(255,0,0,.5);
            transition: .1s;
        }

        #spinButton:hover {
            transform: scale(1.03);
            filter: brightness(1.15);
        }

        #spinButton:active {
            transform: translateY(6px);
            box-shadow:
                0 1px 0 #650000,
                0 0 20px rgba(255,0,0,.5);
        }

        #spinButton:disabled {
            cursor: not-allowed;
            opacity: .6;
        }

        .result {
            min-height: 45px;
            margin-top: 18px;
            font-size: 25px;
            font-weight: 900;
            text-shadow: 0 0 10px currentColor;
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
                transform: scale(1.12);
                filter: brightness(1.6);
            }
        }

        .paytable {
            margin-top: 18px;
            padding: 12px;
            border-radius: 15px;
            background: rgba(0,0,0,.35);
            font-size: 14px;
            line-height: 1.8;
        }

        .credits {
            margin-top: 10px;
            font-size: 13px;
            opacity: .7;
        }

        .coin {
            position: fixed;
            pointer-events: none;
            font-size: 28px;
            animation: coinFall 1.2s linear forwards;
        }

        @keyframes coinFall {
            0% {
                transform: translateY(-30px) rotate(0deg);
                opacity: 1;
            }

            100% {
                transform: translateY(100vh) rotate(720deg);
                opacity: 0;
            }
        }

        @media (max-width: 500px) {
            .machine {
                padding: 15px;
            }

            .reel {
                height: 110px;
            }

            #spinButton {
                width: 95%;
                font-size: 20px;
            }
        }
    </style>
</head>

<body>

<div class="machine">

    <div class="title">🎰 JACKPOT 🎰</div>

    <div class="jackpot">
        INFINITE FREE SPINS
    </div>

    <div class="reels">
        <div class="reel" id="reel1">🍒</div>
        <div class="reel" id="reel2">🍋</div>
        <div class="reel" id="reel3">🍊</div>
    </div>

    <div class="controls">
        <button id="spinButton" onclick="spin()">
            SPIN 🎰
        </button>

        <div id="result" class="result">
            Good luck!
        </div>
    </div>

    <div class="paytable">
        🍒 🍒 🍒 = BIG WIN<br>
        💎 💎 💎 = JACKPOT<br>
        7️⃣ 7️⃣ 7️⃣ = MEGA WIN<br>
        🍋 🍋 🍋 = WIN<br>
        🍊 🍊 🍊 = WIN
    </div>

    <div class="credits">
        Free-play machine — no real money involved.
    </div>

</div>

<script>
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

    const button = document.getElementById("spinButton");
    const result = document.getElementById("result");

    let spinning = false;

    /*
     * Web Audio API
     * Creates the slot-machine sounds directly in the browser.
     */

    const AudioContext = window.AudioContext || window.webkitAudioContext;
    let audioContext = null;

    function getAudio() {
        if (!audioContext) {
            audioContext = new AudioContext();
        }

        if (audioContext.state === "suspended") {
            audioContext.resume();
        }

        return audioContext;
    }

    function beep(frequency, duration, type = "square", volume = 0.06) {
        const ctx = getAudio();

        const oscillator = ctx.createOscillator();
        const gain = ctx.createGain();

        oscillator.type = type;
        oscillator.frequency.value = frequency;

        gain.gain.setValueAtTime(volume, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(
            0.001,
            ctx.currentTime + duration
        );

        oscillator.connect(gain);
        gain.connect(ctx.destination);

        oscillator.start();
        oscillator.stop(ctx.currentTime + duration);
    }

    function spinSound() {
        beep(180, .05);
        setTimeout(() => beep(220, .05), 80);
        setTimeout(() => beep(260, .05), 160);
    }

    function stopSound() {
        beep(350, .08);
    }

    function winSound() {
        const notes = [
            523,
            659,
            784,
            1046,
            1318
        ];

        notes.forEach((note, index) => {
            setTimeout(() => {
                beep(note, .18, "sine", .08);
            }, index * 120);
        });
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

        notes.forEach((note, index) => {
            setTimeout(() => {
                beep(note, .25, "triangle", .1);
            }, index * 150);
        });
    }

    /*
     * Returns a random symbol.
     */

    function randomSymbol() {
        return symbols[Math.floor(Math.random() * symbols.length)];
    }

    /*
     * Creates falling coins during a big win.
     */

    function makeCoins() {

        for (let i = 0; i < 35; i++) {

            const coin = document.createElement("div");

            coin.className = "coin";
            coin.textContent = Math.random() > .5 ? "🪙" : "💰";

            coin.style.left =
                Math.random() * 100 + "vw";

            coin.style.top =
                (-Math.random() * 30) + "vh";

            coin.style.animationDelay =
                Math.random() * .5 + "s";

            document.body.appendChild(coin);

            setTimeout(() => {
                coin.remove();
            }, 2000);
        }
    }

    /*
     * Spin one reel.
     */

    function animateReel(reel, duration) {

        return new Promise(resolve => {

            reel.classList.add("spinning");

            const interval = setInterval(() => {
                reel.textContent = randomSymbol();
            }, 65);

            setTimeout(() => {

                clearInterval(interval);

                reel.textContent = randomSymbol();
                reel.classList.remove("spinning");

                stopSound();

                resolve();

            }, duration);
        });
    }

    /*
     * Main slot-machine function.
     */

    async function spin() {

        if (spinning) {
            return;
        }

        spinning = true;
        button.disabled = true;

        result.classList.remove("win");
        result.textContent = "Spinning...";

        getAudio();

        spinSound();

        /*
         * Each reel stops at a different time,
         * giving it the feel of a real slot machine.
         */

        const reel1 = animateReel(reels[0], 1300);
        const reel2 = animateReel(reels[1], 1900);
        const reel3 = animateReel(reels[2], 2500);

        await Promise.all([
            reel1,
            reel2,
            reel3
        ]);

        const values = reels.map(reel => reel.textContent);

        checkResult(values);

        spinning = false;
        button.disabled = false;
    }

    /*
     * Check the final combination.
     */

    function checkResult(values) {

        const [a, b, c] = values;

        if (a === b && b === c) {

            result.classList.add("win");

            if (a === "7️⃣") {

                result.textContent =
                    "💰💰💰 MEGA JACKPOT!!! 💰💰💰";

                jackpotSound();
                makeCoins();

            } else if (a === "💎") {

                result.textContent =
                    "💎💎💎 DIAMOND JACKPOT! 💎💎💎";

                jackpotSound();
                makeCoins();

            } else if (a === "⭐") {

                result.textContent =
                    "⭐⭐⭐ STAR WIN! ⭐⭐⭐";

                winSound();
                makeCoins();

            } else {

                result.textContent =
                    "🎉 THREE OF A KIND! 🎉";

                winSound();
            }

        } else if (a === b || b === c || a === c) {

            result.textContent =
                "✨ NICE COMBINATION! ✨";

            beep(500, .12, "sine", .07);

        } else {

            result.textContent =
                "Try again! 🎰";
        }
    }

    /*
     * Allow pressing SPACE to spin.
     */

    document.addEventListener("keydown", function(event) {

        if (event.code === "Space") {

            event.preventDefault();

            if (!spinning) {
                spin();
            }
        }
    });

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
    print("       INFINITE SLOT MACHINE")
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
