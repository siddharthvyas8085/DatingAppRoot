# DatingApp — Remaining Codex Prompts

## Completed
# Prompt 1: Audit + stabilization
Implement only the mobile registration screen for the DatingApp.

Current stack:

* React Native
* Expo
* TypeScript
* `mobile/src/app`
* FastAPI backend already working
* CSV persistence remains the current backend storage

Requirements:

1. Create a clean, modern registration screen.
2. Fields:

   * Email
   * Password
   * Confirm Password
3. Client-side validation:

   * valid email
   * password minimum 8 characters
   * passwords must match
4. Add Register button.
5. Show useful validation/error messages.
6. Add a link/button for existing users to go to Login.
7. Keep the UI simple and mobile-friendly.
8. Do NOT change backend code.
9. Do NOT implement API integration yet.
10. Do NOT add Supabase.
11. Do NOT add unrelated features.

Use the existing project structure and navigation approach.

After implementation:

* run `npx tsc --noEmit`
* run `npm run lint`

Report only:

* files changed
* validation result
* TypeScript result
* lint result
* any remaining issue.

# Prompt 2: Backend Python environment
Implement only the mobile Login screen for the DatingApp.

Requirements:

1. Create `mobile/src/app/login.tsx`.
2. Fields:

   * Email
   * Password
3. Add basic validation:

   * valid email
   * password required
4. Add Login button.
5. Show local validation/error messages.
6. Add a link to Register.
7. Connect the existing Register screen's Login link to this screen.
8. Keep the existing design style consistent with Register.
9. Do NOT connect to the backend API yet.
10. Do NOT modify backend code.
11. Do NOT add Supabase.
12. Do not implement authentication/session storage yet.

After implementation run:

* `npx tsc --noEmit`
* `npm run lint`

Report only:

* files changed
* TypeScript result
* lint result
* any remaining issue.

# Prompt 3: Registration UI
Connect the existing mobile Register screen to the existing backend registration API.

Current state:

* Register UI is complete.
* Login UI is complete.
* Backend `/auth/register` already exists.
* CSV remains the current persistence layer.

Tasks:

1. Inspect the existing `mobile/src/services/api.ts`.
2. Add a registration API function for:
   `POST /auth/register`
3. Update `register.tsx` to call this API when Register is pressed.
4. Send:

   * email
   * password
5. Handle:

   * successful registration
   * duplicate email
   * validation/API errors
   * network/backend unavailable
6. Show a clear message to the user.
7. Do not implement login API yet.
8. Do not add authentication/session storage yet.
9. Do not modify backend code.
10. Do not add Supabase.
11. Reuse the existing API configuration and project structure.

After implementation run:

* `npx tsc --noEmit`
* `npm run lint`

Report only:

* files changed
* registration API result
* TypeScript result
* lint result
* any remaining issue.

# Prompt 4: Login UI
Connect the existing mobile Login screen to the existing backend login API.

Current state:

* Register UI + API integration are complete.
* Login UI is complete.
* Backend `POST /auth/login` already exists.
* CSV remains the current persistence layer.

Tasks:

1. Add a login API function using `POST /auth/login`.
2. Update `login.tsx` to call the API.
3. Send email and password.
4. Handle:

   * successful login
   * invalid credentials
   * validation/API errors
   * backend/network failure
5. On successful login, store the returned access token locally for this app session.
6. Do not build profile functionality yet.
7. Do not modify backend code.
8. Do not add Supabase.
9. Do not implement advanced authentication/session management yet.
10. Reuse the existing API configuration and project structure.

After implementation run:

* `npx tsc --noEmit`
* `npm run lint`

Report only:

* files changed
* login API result
* token storage approach
* TypeScript result
* lint result
* any remaining issue.

# Prompt 5: Registration API
Complete the mobile authentication flow using the EXISTING Register and Login screens and the EXISTING backend APIs.

Current state:

* Register UI is complete.
* Register API integration is complete.
* Login UI is complete.
* Backend `/auth/register`, `/auth/login`, and `/auth/me` already exist.
* CSV remains the current persistence layer.

Tasks:

1. Connect Login to `POST /auth/login`.
2. Handle successful login, invalid credentials, validation errors, and network errors.
3. Store the returned access token using an appropriate local mobile storage mechanism.
4. Create a small reusable authentication/session utility if needed.
5. Add an authenticated API helper that can send:
   `Authorization: Bearer <token>`
6. Verify the stored token by calling `/auth/me` after successful login.
7. Keep the user authenticated when navigating between screens.
8. Add logout functionality that clears the stored token.
9. Connect Register → Login and Login → Register navigation properly.
10. After successful login, navigate to the existing/main authenticated area instead of leaving the user on the Login screen.
11. If no authenticated home/profile screen exists yet, use the existing Home screen as the temporary destination.
12. Do NOT build profile functionality yet.
13. Do NOT modify backend authentication.
14. Do NOT add Supabase.
15. Do NOT add unrelated features.

Reuse the existing project structure and API configuration. Do not recreate functionality that already exists.

After implementation run:

* `npx tsc --noEmit`
* `npm run lint`

Report only:

* files changed
* authentication flow completed
* token storage approach
* logout result
* TypeScript result
* lint result
* any remaining issue.

# Prompt 6: Complete authentication flow
Build the authenticated Profile Setup flow.

Current state:

* Register and Login flows are complete.
* Authentication token is stored locally.
* `/auth/me` works.
* Backend profile APIs already exist:

  * `POST /profiles`
  * `GET /profiles/me`
  * `PUT /profiles/me`
* CSV remains the current persistence layer.

Tasks:

1. Create a mobile Profile Setup screen.
2. Fields:

   * Name
   * Date of birth
   * Gender
   * Bio
   * Occupation
   * City
   * Profile image URL
3. Use the authenticated API helper with the stored Bearer token.
4. Connect the screen to `POST /profiles`.
5. Validate required/appropriate fields on the mobile side.
6. Handle API and network errors clearly.
7. After successful profile creation, navigate to the authenticated home/discovery area.
8. Add `GET /profiles/me` support so the app can determine whether the user already has a profile.
9. If a profile already exists, do not force the user through profile creation again.
10. Add a simple Edit Profile flow using `PUT /profiles/me`.
11. Keep the UI consistent with the existing authentication screens.
12. Do NOT build discovery/matching yet.
13. Do NOT modify the backend profile implementation unless a genuine integration bug is found.
14. Do NOT add Supabase.
15. Do NOT add unrelated features.

After implementation run:

* `npx tsc --noEmit`
* `npm run lint`

Report only:

* files changed
* profile creation result
* profile retrieval/edit result
* TypeScript result
* lint result
* any remaining issue.


# Prompt 7: Profile setup/edit
Build the authenticated Preferences flow for the DatingApp.

Current state:

* Register, Login, authentication/session handling are complete.
* Profile creation, retrieval, and editing are complete.
* Backend preference APIs already exist.
* CSV remains the current persistence layer.

Tasks:

1. Create a mobile Preferences screen.
2. Fields:

   * Preferred gender
   * Minimum age
   * Maximum age
   * City
   * Relationship intent
3. Add client-side validation:

   * minimum age must not exceed maximum age
   * sensible age values
4. Connect the screen to the existing backend preference APIs.
5. Use the authenticated Bearer token.
6. Support both:

   * creating preferences
   * loading existing preferences
   * updating existing preferences
7. Show clear loading, success, and error states.
8. Add navigation from Profile Setup/Edit to Preferences.
9. After saving preferences, navigate to the main authenticated/discovery area.
10. Keep the UI consistent with the existing application.
11. Do NOT build discovery, likes, matching, or chat yet.
12. Do NOT modify backend code unless a genuine integration issue is found.
13. Do NOT add Supabase.
14. Do not recreate authentication or profile functionality.

After implementation run:

* `npx tsc --noEmit`
* `npm run lint`

Report only:

* files changed
* preference create/load/update result
* navigation result
* TypeScript result
* lint result
* any remaining issue.


## Current
- Prompt 8: Preferences flow

CSV remains the active persistence layer.
Supabase migration is the FINAL infrastructure phase.

## Rules for Codex
- Current repository is the source of truth.
- Do not repeat completed work.
- Combine related tasks.
- Keep prompts focused.
- Do not migrate to Supabase until the final phase.
- Do not replace CSV during feature development.
- Do not add unrelated features.
- Run TypeScript and lint after mobile work.

---

# Prompt 8 — Preferences Flow

Build the authenticated Preferences flow.

Tasks:
1. Create a mobile Preferences screen.
2. Fields:
   - Preferred gender
   - Minimum age
   - Maximum age
   - City
   - Relationship intent
3. Validate minimum age <= maximum age.
4. Connect to existing preference APIs using the Bearer token.
5. Support create, load, and update.
6. Add loading, success, and error states.
7. Add navigation from Profile Setup/Edit to Preferences.
8. After saving, navigate to the main authenticated/discovery area.
9. Keep existing UI style.
10. Do not build discovery, likes, matching, or chat yet.
11. Do not add Supabase.

Run:
- `npx tsc --noEmit`
- `npm run lint`

---

# Prompt 9 — Discovery Screen

Build the main Discovery screen using existing backend functionality.

Tasks:
1. Create a clean dating-app style Discovery screen.
2. Load candidate profiles.
3. Show profile image, name, age, city, occupation, and bio.
4. Add loading, empty, and error states.
5. Add Like and Pass UI actions.
6. Do not implement Like API integration yet.
7. Do not add recommendation ML.
8. Do not add Supabase.

Run TypeScript and lint.

---

# Prompt 10 — Like / Pass Flow

Connect Discovery to the existing Like backend functionality.

Tasks:
1. Inspect existing Like/matching APIs first.
2. Connect Like.
3. Connect Pass to candidate progression.
4. Prevent duplicate Like actions.
5. Handle API/network errors.
6. If a mutual Like creates a match, show a simple Match confirmation.
7. Remove the processed profile from Discovery.
8. Do not build the full Matches screen yet.
9. Do not modify unrelated backend functionality.
10. Do not add Supabase.

Run backend tests if backend code changes.
Run TypeScript and lint.

---

# Prompt 11 — Matches Screen

Build the authenticated Matches screen.

Tasks:
1. Use the existing matches API.
2. Display current matches.
3. Show profile image, name, and basic profile information.
4. Add loading, empty, and error states.
5. Selecting a match should navigate to Chat.
6. Add Matches to the main navigation.
7. Do not build chat messaging yet.
8. Do not add Supabase.

Run TypeScript and lint.

---

# Prompt 12 — Chat Flow

Implement basic one-to-one chat using the existing messages backend.

Tasks:
1. Build the Chat screen.
2. Load messages for the selected match.
3. Display messages by sender.
4. Add message input and Send button.
5. Send through the existing API.
6. Enforce match membership.
7. Handle loading, empty, and error states.
8. Refresh messages after sending.
9. Do not implement realtime/WebSockets yet.
10. Do not add AI message suggestions yet.
11. Do not add Supabase.

Run backend tests if backend code changes.
Run TypeScript and lint.

---

# Prompt 13 — Safety Features

Implement the basic safety functionality required before beta.

Tasks:
1. Add Block.
2. Add Report.
3. Add Unmatch.
4. Connect to existing backend safety functionality.
5. Add confirmation dialogs for destructive actions.
6. Remove blocked/unmatched users from relevant UI.
7. Preserve unrelated matches.
8. Show success/error messages.
9. Do not build an admin panel.
10. Do not add advanced moderation.
11. Do not add Supabase.

Run backend tests and mobile TypeScript/lint.

---

# Prompt 14 — Main App UX & Navigation Polish

Polish the complete current application without adding new product functionality.

Expected flow:

Welcome
→ Register/Login
→ Profile
→ Preferences
→ Discovery
→ Like/Pass
→ Match
→ Chat
→ Safety

Tasks:
1. Review navigation across all screens.
2. Fix broken/back navigation.
3. Add appropriate loading states.
4. Add consistent error states.
5. Add empty states.
6. Protect authenticated screens.
7. Prevent authenticated users from unnecessarily returning to Login/Register.
8. Add logout in the appropriate location.
9. Make spacing, typography, buttons, and forms consistent.
10. Test the complete user journey.
11. Do not add new product features.
12. Do not migrate to Supabase.

Run TypeScript and lint.

---

# Prompt 15 — Final Functional Testing & Beta Preparation

Perform focused end-to-end testing of the current DatingApp.

Test:

AUTH
- registration
- duplicate registration
- login
- invalid login
- logout
- authenticated access

PROFILE
- create
- load
- edit

PREFERENCES
- create
- load
- update
- invalid age range

DISCOVERY
- candidate loading
- like
- pass
- empty state

MATCHING
- mutual like
- match display

CHAT
- send/read message
- unauthorized match access

SAFETY
- block
- report
- unmatch
- unrelated matches preserved

Verify:
- backend pytest
- mobile TypeScript
- mobile lint
- no secrets committed
- .env remains ignored

Fix only genuine issues found.

Do not migrate to Supabase or add major features.

Final report:
- tests passed
- bugs fixed
- remaining issues
- beta blockers
- next development step

---

# FINAL PHASE — Supabase Migration

Only begin after functionality and UI are stable.

Migration order:

1. Supabase Auth
2. Profiles
3. Preferences
4. Likes
5. Matches
6. Messages
7. Remove/deprecate CSV persistence
8. Full regression testing

Do not start this phase early.
