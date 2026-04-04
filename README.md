# OpenGuy

**Control a robot with plain English.**

OpenGuy converts natural language commands into structured robot actions — no robotics experience required. Type what you want the arm to do, and OpenGuy handles the rest.

> **Status:** MVP — AI parser live · Web UI ready · Hardware integration in progress

---

## Demo

```
Input   →  "go a bit forward"
Parsed  →  { "action": "move", "direction": "forward", "distance_cm": 5, "confidence": 0.92 }
Output  →  Moving forward 5 cm... ✓

Input   →  "turn slightly right"
Parsed  →  { "action": "rotate", "direction": "right", "angle_deg": 15, "confidence": 0.88 }
Output  →  Rotating right 15°... ✓

Input   →  "pick up the object"
Parsed  →  { "action": "grab", "confidence": 0.95 }
Output  →  Closing gripper... ✓
```

No need to memorise commands — click a suggestion and the robot responds instantly. After each command, suggestions update to show what makes sense to do next.

---

## What It Does

- Accepts natural language commands in plain English
- Parses them into structured JSON using an AI model (Groq / Llama 3.1)
- Scores each parsed command with a confidence value so ambiguous input is flagged
- Falls back to a regex-based parser when the AI is unavailable — the system keeps working offline
- Shows context-aware smart suggestions that update after every command
- Stores up to 8 recent commands in persistent history with one-click replay

---

## How It Works

**1. AI Parser**
Commands are sent to Llama 3.1 (via Groq's free API) with a structured system prompt. The model returns a clean JSON object — action, direction, distance, angle, and a confidence score. Vague phrasing like "a bit" or "slightly" is interpreted and estimated automatically.

**2. Regex Fallback**
If the AI is unreachable, the system switches to a regex-based parser. It handles common patterns reliably and marks results with a lower confidence score so you always know which path was taken.

**3. Smart Suggestions**
Five suggestions are shown below the input at all times. On load, they cover a broad range of actions. After each successful command, they update to reflect logical next steps — if you just grabbed an object, the suggestions shift to lift, move, release, and reposition. A shuffle button cycles in fresh options from the same context pool.

**4. Command History**
Every successful command is saved to `localStorage`. The history row sits between the suggestions and output, so past commands are always within reach. Each entry has two actions: tap the text to fill the input box, or hit the replay button to re-run immediately.

**5. Simulator**
The parsed command is passed to a simulator that describes the robot's response in plain text — motor engagement, force applied, confirmation. Ready to be swapped for real hardware output.

---

## Try It

**Web UI (no setup)**

Open `index.html` in any browser. Enter your [Groq API key](https://console.groq.com) once via the top-right menu — it saves locally. That's it.

**Run locally**

```bash
git clone https://github.com/NEHIRAAS/openguy.git
cd openguy
python main.py
```

Requirements: Python 3.8+, no external libraries.

---

## Project Structure

```
openguy/
├── index.html      # Web UI — single file, no build step
├── main.py         # CLI entry point
├── parser.py       # AI parser + regex fallback
└── simulator.py    # Simulates robot arm responses
```

Four files. Intentionally minimal. Every part is easy to read and easy to extend.

---

## Roadmap

- [x] AI-based natural language parser
- [x] Regex fallback with confidence scoring
- [x] Web UI (single-file, no setup)
- [x] Command history with persistent replay
- [x] Smart context-aware suggestions
- [ ] Serial/USB connection to real hardware
- [ ] Multi-step command chains ("pick up the block and move it left")
- [ ] WhatsApp / Telegram bot interface
- [ ] Voice input via browser microphone
- [ ] PyBullet physics simulation

Have an idea? [Open an issue](https://github.com/NEHIRAAS/openguy/issues) — suggestions are welcome.

---

## Contributing

OpenGuy is beginner-friendly. If you can write Python or basic HTML, you can contribute.

Good places to start: adding new command types to `parser.py`, expanding the suggestion bank in `index.html`, improving the AI system prompt for better accuracy on ambiguous input, writing tests for the `parse()` function, or connecting `simulator.py` to real serial hardware.

**How to contribute:**

1. Fork the repo
2. Create a branch: `git checkout -b your-feature`
3. Make your changes
4. Open a pull request with a short description

No contribution is too small.

---

## Support

If OpenGuy is useful to you, a star helps others find it.

[⭐ Star on GitHub](https://github.com/NEHIRAAS/openguy)

---

## License

MIT — free to use, modify, and distribute.

---

*Built by [@NEHIRAAS](https://github.com/NEHIRAAS)*
