How to Run This Project
=======================

This repository contains a FastAPI backend and an Expo React Native mobile app. The instructions below explain how to clone the repository, install dependencies, run the backend locally, run the mobile app (web or device/emulator), and run tests. These steps are written for cross-platform use but include Windows-friendly commands where helpful.

Prerequisites
-------------
- Git (https://git-scm.com)
- Python 3.10+ and pip
- Node.js 18+ and npm or yarn
- Expo CLI (optional for native device/emulator): `npm install -g expo-cli` or use `npx expo`
- (Optional) Android Studio or Xcode for device emulators
- (Optional) A code editor such as VS Code

Quick start — clone + run both
--------------------------------
1. Clone the repo:

```bash
git clone <repo-url>
cd DatingApp
```

2. Backend: create a virtual environment, install dependencies, and run tests:

Windows (PowerShell):

```powershell
cd backend
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
python -m pytest -q
# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

macOS / Linux:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Notes:
- The backend serves HTTP APIs on port `8000` by default. If you need a different port, change the `--port` value.
- The CSV files in `backend/data/` are used for simple persistence in this project. Do not delete them unless you want to reset sample data.

3. Mobile (Expo): install dependencies and run the Expo app:

Open a new terminal, then:

```bash
cd mobile
npm install
# Type-check only (no emit)
npx tsc --noEmit
# Run linter
npm run lint
# Start Expo (web, device, or simulator)
npx expo start
```

Using Expo:
- After `npx expo start` you can open the app in a web browser (w), on a physical device using the Expo Go app (scan QR), or in an Android/iOS simulator if configured.
- The mobile app expects the backend running at the development host. By default, the mobile code calls relative API paths using the same host as the app; when using Expo web this will work automatically. For device/emulator you may need to set the backend host to your machine IP in `mobile/src/constants/config.ts` (or the environment / app config) so the device can reach your machine.

Running the full flow (suggested order)
--------------------------------------
1. Start the backend server (see backend step above).
2. Start the Expo server (`npx expo start`) and open the app on your preferred target (web or device).
3. Use the mobile app to register, login, complete profile/preferences, and try discovery/likes/matches/chat.

Running tests
-------------
- Backend tests:

```bash
cd backend
source .venv/bin/activate  # or Windows . .venv/Scripts/Activate.ps1
python -m pytest -q
```

- Mobile type-check and lint (no runtime tests included):

```bash
cd mobile
npx tsc --noEmit
npm run lint
```

GitHub / sharing notes
----------------------
- To push the project to GitHub:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-git-remote-url>
git push -u origin main
```

- When your friend clones the repo, they should follow these steps (from repo root):
  1. `cd backend` → create venv → install `requirements.txt` → run tests → `uvicorn app.main:app --reload`
  2. `cd mobile` → `npm install` → `npx expo start` → open app (web/device)

Troubleshooting
---------------
- If the mobile app cannot reach the backend from a device, replace localhost with your machine IP in `mobile/src/constants/config.ts` or the appropriate environment variable.
- If `python-jose` or other packages are missing, ensure `pip install -r requirements.txt` completed successfully.
- If port conflicts occur, change the `--port` for `uvicorn` and update the mobile config if needed.
- On Windows PowerShell, you may need to change the execution policy to run activation scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
. .venv/Scripts/Activate.ps1
```

Security / Data
---------------
- This project uses CSV files for simple local persistence under `backend/data/`. Do not use this storage method for production data.
- The mobile app stores the JWT token using Expo SecureStore on device; on web it uses a localStorage fallback. Treat tokens like credentials.

Further work
------------
- You can migrate the backend CSV repository to Supabase or another real database if you want production persistence.
- For real-time chat consider adding WebSocket support or a hosted real-time DB.

Contact
-------
If anything is unclear, share the exact error output and I can help troubleshoot.
