# MindMitra — Your Quiet Daily Companion

**A mental-wellness companion for students and young professionals**  
**Team TriNova | Kritical Hacks '26 | AI/ML Track**

MindMitra is a supportive web-app prototype designed to make everyday emotional check-ins approachable. It combines mood tracking, reflective journaling, simple wellness activities, trend visualizations, and a support-resource discovery interface. The project explores how live-web search through **TinyFish** can help users find relevant mental-health support information in their city.

> **Project status (20 October 2026):** The interactive frontend has been demonstrated in Replit using browser-local storage. A separate Python FastAPI backend and TinyFish Search API test are included in this repository. The public frontend-to-backend-to-TinyFish connection is **not yet completed or verified**. The Support Resources screen currently shows **clearly labeled sample links** when no live backend is configured. MindMitra is a hackathon MVP, not a clinical or production-ready service.

## The problem

Students and young professionals often experience stress, loneliness, academic pressure, and burnout, but may find it difficult to reflect on their emotions consistently or locate credible help when needed. MindMitra aims to offer a gentle daily entry point: understand how you feel, notice patterns, try small self-care actions, and discover where to seek additional support.

## What the prototype includes

| Feature | Current implementation |
| --- | --- |
| Landing page and onboarding | Interactive React interface with Student and Young Professional paths |
| Mood check-ins | Mood score (1–5), with optional sleep and energy inputs |
| Reflection journal | Write and review personal check-ins in browser-local demo mode |
| Mood dashboard and trends | Charts update from browser-local entries and optional clearly marked sample data |
| Self-care toolkit | Breathing and reflection activities |
| Voice notes | Browser MediaRecorder recording; **no speech transcription or AI voice-emotion detection** |
| Support Resources page | City-based search interface; sample resources shown until a live backend is configured |
| Backend API | FastAPI routes for check-ins, trends, health checks, and a TinyFish-powered support-resource lookup route |
| TinyFish Search | Separate API connectivity test and backend integration code; **not yet verified end-to-end in the deployed website** |

### Demonstration walkthrough

1. Open the MindMitra landing page and choose **Get started**.
2. Select **Student** or **Young Professional** and complete onboarding.
3. Record a mood check-in and a short journal reflection.
4. Explore the dashboard and trend charts; use **Settings → Load samples** if you want fictional demo history.
5. Explore breathing activities, guided reflection, and optional voice recording.
6. Visit **Support Resources**. Without a configured backend, the cards are **sample references, not live TinyFish search results**.
7. Demonstrate `tinyfish_test.py` separately to show the existing TinyFish Search API experiment, if the API key and credits are available.

## TinyFish: purpose, implementation, and status

**Why TinyFish?** Mental-health support information varies by location and may change. TinyFish Search is intended to help MindMitra retrieve current public support resources, rather than relying only on a hard-coded directory.

**Intended flow:**

```text
User selects city on Support Resources page
    → React frontend requests GET /support-resources?city=Delhi
    → FastAPI backend uses server-side TINYFISH_API_KEY
    → TinyFish Search API queries public mental-health resources
    → Backend returns a small set of search results
    → Frontend presents links for users to review
```

**What is implemented:**

- `tinyfish_test.py` makes a direct request to the TinyFish Search API for official Tele-MANAS information and prints the returned JSON. This test was previously run locally during development.
- `main.py` includes `GET /support-resources?city=Delhi`, which reads `TINYFISH_API_KEY` from environment variables, requests city-specific mental-health support results from TinyFish, and returns up to five results or an error.
- The frontend includes a support-resource page and a configuration hook for a public FastAPI URL.

**What is not yet complete:**

- The hosted frontend and FastAPI backend are not yet connected and tested as one public application.
- The Support Resources page therefore displays sample resources when the backend is unavailable.
- Search results have not been independently verified or medically endorsed. Source checking, freshness checks, and clear labeling are important future improvements.
- TinyFish Fetch and Web Agent workflows are **proposed extensions**, not implemented functionality in this MVP.

**Privacy boundary:** The TinyFish query is intended to contain the requested **city and public resource topic**, not personal journals or voice recordings. The API key must remain on the backend and must never be embedded in frontend code or committed to GitHub.

## Technology stack

- **Frontend:** React 19, Vite 6, JavaScript, CSS, Recharts, Lucide React
- **Backend:** Python, FastAPI, Uvicorn, Pydantic
- **Live-web exploration:** TinyFish Search API through `requests`
- **Prototype persistence:** Browser `localStorage` for frontend demo records; local JSON file for FastAPI check-ins
- **Development:** VS Code, Replit, GitHub

## Run locally

### Frontend

Install **Node.js 20+**, then run from the folder containing `package.json`, `index.html`, and the `src` directory:

```bash
npm install
npm run dev
```

Open the local address shown in the terminal (normally `http://localhost:5173`).

For a production build:

```bash
npm run build
```

Vite outputs static files to `dist/`.

**Repository layout note:** The Vite `index.html` references `/src/main.jsx`. The file must therefore exist at `src/main.jsx` (along with any imported assets) before `npm run build` can succeed. If files were uploaded to the GitHub repository root rather than their original folders, restore the original extracted website folder structure first. The Netlify deployment attempted on 20 October failed because `/src/main.jsx` could not be resolved; a public deployment should **not** be assumed working.

### Backend

Use Python 3.10+ and run from the directory containing `main.py` and `requirements.txt`:

```bash
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

Local API documentation: `http://127.0.0.1:8000/docs`

Available routes:

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/health` | API health check |
| POST | `/checkins` | Save a check-in with mood, journal, and optional sleep/energy |
| GET | `/checkins` | List locally stored check-ins |
| GET | `/trends` | Return count, average mood, and recent records |
| GET | `/support-resources?city=Delhi` | Query TinyFish Search API using the server-side API key |
| GET | `/resources?city=Delhi` | Legacy placeholder that explicitly returns `not_configured` |

Example check-in JSON:

```json
{
  "journal": "I felt stressed about deadlines today.",
  "mood": 2,
  "sleep_hours": 6.5,
  "energy": 3
}
```

### TinyFish configuration and test

Create a local `.env` file beside `main.py`:

```env
TINYFISH_API_KEY=your_actual_tinyfish_key
```

Then run:

```bash
python tinyfish_test.py
```

This test requires network access, a valid API key, and available TinyFish credits. A successful API response demonstrates **API connectivity**, not full website integration. **Never commit `.env` or real credentials.**

### Connecting frontend and backend later

Create the frontend `.env` file:

```env
VITE_API_BASE_URL=https://your-public-fastapi-backend.example.com
```

Restart Vite and use the app's Live backend option where supported. The backend must be publicly reachable over HTTPS, its CORS allowlist must include the frontend's actual origin, and the entire support-resource flow must be tested. **Do not place `TINYFISH_API_KEY` in a `VITE_` variable** because Vite exposes those values to the browser.

## Architecture and engineering decisions

```text
                  MINDMITRA FRONTEND
             React + Vite + Recharts
                        |
          +-------------+-------------+
          |                           |
   Local demo mode               Planned live mode
   browser localStorage          HTTPS requests
                                      |
                                FastAPI backend
                                      |
                         +------------+-----------+
                         |                        |
                   JSON check-ins           TinyFish Search
                   (demo only)              (city-based query)
```

- The frontend is intentionally usable without a running server, making the core wellness experience easy to demonstrate.
- Basic mood interpretation is **rule-based**, using mood values and a small keyword list. It is **not** a trained emotion-recognition model or a clinical assessment.
- The backend uses a local JSON file, which is suitable only for experimentation. It is not a secure multi-user data store.
- Voice recordings are session-only; they are not sent for speech recognition or sentiment classification.

## Privacy, safety, and limitations

MindMitra is a self-reflection prototype and **does not diagnose, treat, or replace mental-health professionals or emergency services**. Resource listings are informational and should be checked against official providers before reliance. The current backend has **no account authentication, per-user isolation, or production-grade protection for sensitive journal data**. Do not enter real sensitive personal information into the shared backend demo. Browser-local records are also not a substitute for secure accounts or encrypted medical records.

## What makes MindMitra different

MindMitra brings together a daily emotional check-in, accessible self-care tools, role-specific experiences, and a path toward location-relevant support discovery. Rather than presenting itself as a therapist, it is designed as a low-pressure companion that encourages reflection and helps users take the next small step toward support.

## Impact and future roadmap

**Intended users:** College students, early-career professionals, and campus wellness communities.

**Potential impact:** More consistent emotional self-awareness, earlier discovery of support options, and lower friction when seeking help.

**Next development priorities:**

1. Complete and test frontend → FastAPI → TinyFish integration.
2. Add verified-source labeling and regular freshness checks for support links.
3. Introduce secure authentication, encrypted storage, and proper per-user access controls.
4. Add multilingual support, accessibility improvements, and opt-in campus or counselor referrals.
5. Evaluate usability and usefulness with consent-based user feedback; do not claim clinical efficacy without evidence.

## Revenue model (proposal, not launched)

MindMitra's core daily mood check-ins and basic self-care tools should remain free. Potential sustainable funding options include:

- **Free individual tier:** Basic tracking, journaling, and support-resource discovery.
- **Optional premium tier (hypothesis: ₹99/month):** Expanded personal trend insights and customization, only after privacy and safety requirements are met.
- **Institutional partnerships:** Opt-in wellness programs for colleges and employers, with transparent pricing negotiated by institution size and **no sale of individual journal data**.

These prices are **illustrative assumptions**, not validated willingness-to-pay findings. Real pricing would require competitor research, user interviews, infrastructure cost estimates, and pilots. No revenue or customer traction is claimed.

## Team and event

**Team TriNova**  
- **Preeti Fulara** — Team Leader
- **Khushi** — Team Member
- **Diksha Thakur** — Team Member

Built for **Kritical Hacks '26**, AI/ML track.

## Repository and demonstration

**Source code:** https://github.com/PreetiFulara01/MindMitra

The video demo should show the working local frontend and describe the separate TinyFish API test accurately. A stable public website URL is not yet confirmed. Please evaluate the implemented prototype and documented development status rather than assuming that every planned feature is live.

---

*MindMitra — you don't have to do it alone.*
