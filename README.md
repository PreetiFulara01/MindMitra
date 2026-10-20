# MindMitra — Interactive Website + Web App

A hackathon MVP by **Team TriNova**. Includes the official MindMitra logo, public landing page, role-based student/young-professional dashboard, onboarding, mood check-ins, journal, dynamic charts, wellness activities, voice recording, support resources, and local demo mode.

## Start in Replit

1. Create a new **Node.js** Replit project, or import this project folder / GitHub repository.
2. Upload the files preserving the folder structure.
3. In the Shell run `npm install`.
4. Click **Run**, or execute `npm run dev`.
5. Open the Webview. Vite listens on `0.0.0.0` and uses port 5173 by default.

## Start in VS Code

Install Node.js 20+, then run:

```bash
npm install
npm run dev
```

Open the local URL shown in your terminal (usually `http://localhost:5173`).

## Demo walkthrough

1. Open the landing page and explore the scroll sections.
2. Click **Get started** → **Continue to demo**.
3. Choose **Student**, enter a name, and finish onboarding.
4. Go to **Settings** → **Load samples** to populate the mood chart with clearly labeled fictional records.
5. Make a new journal check-in and watch the dashboard and charts update immediately.
6. Switch to **Young professional** in Settings for a different dashboard and separate browser-local records.
7. Try voice recording (microphone permission needed, HTTPS or localhost), breathing exercises, guided reflection, and the support resources page.

## Optional FastAPI integration

The frontend is **fully usable in local demo mode** without a backend. To point to your existing Python backend, create a `.env` file from `.env.example`:

```env
VITE_API_BASE_URL=https://your-deployed-backend.example.com
```

Then restart Vite. In Settings, switch to Live backend mode to send check-ins to FastAPI, and on Support Resources use live TinyFish lookup. The frontend never calls TinyFish directly or contains an API key.

**Important limitations:** Your current FastAPI backend has no real account authentication or per-user isolation. Live backend mode should only be used with non-sensitive demonstration text. Public deployment requires a publicly reachable HTTPS backend with the appropriate CORS origin configured. Localhost on your laptop is not reachable by a publicly hosted Replit frontend.

## Technical notes

- React + Vite + Recharts + Lucide + CSS, no paid frontend APIs.
- Browser-local demo profiles and entries are saved in localStorage; this is not secure user authentication.
- MediaRecorder voice notes are session-only and not transcribed or classified.
- Mood suggestions are simple rules, not trained AI or medical diagnoses.
- TinyFish results appear only after a successful backend call; offline sample resources are explicitly labeled.
- Public landing photographs load from Unsplash and require an internet connection.
- Social media links without provided URLs are marked 'coming soon'.
- The official supplied MindMitra logo is in `public/mindmitra-logo.png`.

## Build

```bash
npm run build
```

Vite writes deployable frontend files to `dist/`.
