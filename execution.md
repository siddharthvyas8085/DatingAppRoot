# DatingApp --- Execution Plan

## 1. Project Vision

DatingApp is a serious, long-term dating application being built for the
Indian market.

The goal is not to build a learning/demo project. The first version
should be a focused, reliable MVP that can be tested with real users,
while keeping the architecture clean enough to evolve into a larger
product later.

The initial product flow is:

``` text
Register / Login
      ↓
Create Profile
      ↓
Set Dating Preferences
      ↓
Discover Profiles
      ↓
Like / Pass
      ↓
Mutual Like
      ↓
Match
      ↓
Chat
      ↓
AI Message Suggestions
```

Safety is part of the core product:

``` text
Block
Report
Unmatch
```

These should be included before external beta testing.

------------------------------------------------------------------------

# 2. Product Philosophy

The product should focus on:

-   Simple onboarding
-   Useful profiles
-   Preference-based discovery
-   Mutual matching
-   Meaningful conversations
-   Safety and authenticity
-   AI assistance where it adds genuine value
-   Indian user context
-   Low infrastructure cost during early development
-   Ability to scale later without rewriting the entire application

Potential future differentiators are hypotheses, not assumptions:

-   More intentional dating
-   Better compatibility
-   Conversation assistance
-   Reduced swipe fatigue
-   Better safety/authenticity mechanisms
-   Indian cultural/contextual support

These should eventually be validated through real user behavior rather
than being treated as proven advantages.

------------------------------------------------------------------------

# 3. Current Technology Stack

## Mobile

``` text
React Native
Expo
TypeScript
```

Development currently uses Expo Web.

Current mobile project:

``` text
DatingApp/mobile/
```

Important:

``` text
mobile/src/app/
```

is the application route directory.

Do not create or migrate to `mobile/app/` unless there is an explicit
architectural reason.

------------------------------------------------------------------------

## Backend

``` text
Python
FastAPI
Pydantic
JWT
```

Current backend:

``` text
DatingApp/backend/
```

------------------------------------------------------------------------

## Database / Backend Platform

Target:

``` text
Supabase
PostgreSQL
Supabase Auth
Supabase Storage
Row Level Security
```

Supabase has already been created manually.

Existing database tables:

``` text
profiles
preferences
likes
matches
messages
```

RLS has already been configured.

------------------------------------------------------------------------

## AI

AI functionality will be introduced behind a service abstraction.

The application should not tightly couple the entire product to one LLM
provider.

Future architecture should allow providers/models to be changed without
rewriting the application.

------------------------------------------------------------------------

## Version Control

``` text
Git
GitHub
```

------------------------------------------------------------------------

# 4. Important Architecture Decision

During early development, a CSV repository was intentionally used to
simplify development while the application architecture was being
established.

The current temporary architecture was:

``` text
Mobile
   ↓
FastAPI
   ↓
Services
   ↓
CSV Repository
   ↓
CSV files
```

The final architecture should be:

``` text
Mobile
   ↓
FastAPI
   ↓
Services
   ↓
Repository abstraction
   ↓
Supabase
   ↓
PostgreSQL
```

The CSV implementation is temporary and must not remain the production
persistence layer.

The migration to Supabase is a required milestone before external beta
launch.

------------------------------------------------------------------------

# 5. Critical Supabase Authentication Decision

Supabase already has:

``` text
auth.users
```

The existing `profiles` table is designed as:

``` sql
profiles.id
    ↓
references auth.users(id)
```

Therefore we should NOT create a separate `public.users` table merely to
reproduce `users.csv`.

Authentication should ultimately move from:

``` text
Custom users.csv
+
Custom password hashing
+
Custom JWT
```

to:

``` text
Supabase Auth
```

The target relationship is:

``` text
Supabase Auth
    ↓
auth.users
    ↓
profiles
```

This should be handled carefully because the existing application
currently uses custom JWT authentication.

------------------------------------------------------------------------

# 6. Current Project Structure

Current high-level structure:

``` text
DatingApp/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   └── profile.py
│   │   ├── core/
│   │   │   ├── security.py
│   │   │   └── dependencies.py
│   │   ├── models/
│   │   ├── repositories/
│   │   │   └── csv_repository.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   └── profile.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   └── profile_service.py
│   │   └── main.py
│   ├── data/
│   │   ├── users.csv
│   │   ├── profiles.csv
│   │   ├── preferences.csv
│   │   ├── likes.csv
│   │   ├── matches.csv
│   │   └── messages.csv
│   ├── tests/
│   ├── .env
│   ├── .env.example
│   └── requirements.txt
│
├── mobile/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── constants/
│   │   ├── services/
│   │   └── types/
│   ├── assets/
│   ├── package.json
│   └── tsconfig.json
│
└── docs/
```

Codex must inspect the actual repository before modifying this
structure.

Do not blindly recreate files that already exist.

------------------------------------------------------------------------

# 7. Features Already Implemented

The following functionality has already been built and manually tested:

## Foundation

-   FastAPI application
-   Health endpoint
-   React Native + Expo mobile application
-   Mobile → backend connectivity
-   CORS configuration
-   Environment configuration
-   Git project structure

## Authentication

Current implementation includes:

-   Registration
-   Password hashing
-   Login
-   JWT access token
-   Protected endpoints
-   `/auth/me`
-   Invalid-password handling
-   Duplicate-email handling

## Profile

Current implementation includes:

-   Create profile
-   Get own profile
-   Update own profile
-   JWT-protected profile endpoints
-   Basic profile fields

Profile fields currently include:

``` text
name
date_of_birth
gender
bio
occupation
city
profile_image_url
created_at
updated_at
```

------------------------------------------------------------------------

# 8. Existing Supabase Schema

The existing Supabase database contains:

``` text
profiles
preferences
likes
matches
messages
```

The intended relationships are:

``` text
auth.users
    │
    └── profiles
          │
          ├── preferences
          ├── likes
          ├── matches
          └── messages
```

Existing indexes have been created for important lookup fields.

RLS has also been enabled.

Before production/beta, RLS policies must be reviewed carefully rather
than assuming that the initial development policies are
production-ready.

For example, profile visibility currently needs a future security review
to ensure that only intended public profile fields are exposed.

------------------------------------------------------------------------

# 9. Development Phases

## Phase 0 --- Foundation

Status:

``` text
COMPLETED
```

Includes:

-   Project structure
-   FastAPI
-   Expo
-   Git
-   Environment configuration
-   Backend/mobile connection

------------------------------------------------------------------------

## Phase 1 --- Authentication

Status:

``` text
FUNCTIONALLY COMPLETED
MIGRATION TO SUPABASE AUTH PENDING
```

Current:

``` text
Custom authentication
CSV users
Custom JWT
```

Target:

``` text
Supabase Auth
auth.users
Supabase access token
```

------------------------------------------------------------------------

## Phase 2 --- Profile

Status:

``` text
FUNCTIONALLY COMPLETED
SUPABASE MIGRATION PENDING
```

------------------------------------------------------------------------

## Phase 3 --- Dating Preferences

Next feature after persistence/auth migration is stabilized.

Expected fields:

``` text
preferred_gender
min_age
max_age
city
relationship_intent
```

Expected API:

``` text
GET /preferences/me
PUT /preferences/me
```

Validation should include:

-   sensible age limits
-   minimum age
-   maximum age
-   min_age \<= max_age
-   authenticated user ownership

------------------------------------------------------------------------

## Phase 4 --- Discovery

Users should see profiles based on their preferences.

Initial discovery should be simple.

Potential filters:

``` text
gender
age
city
relationship intent
```

The current user's own profile should not appear.

Already-liked / already-passed profiles should eventually be handled
appropriately.

Do not build advanced recommendation ML yet.

------------------------------------------------------------------------

## Phase 5 --- Like / Pass

Implement:

``` text
Like
Pass
```

Like should be stored.

A mutual like should create a match.

Important rules:

``` text
User cannot like themselves.
Duplicate likes must be prevented.
A match should not be duplicated.
```

The database constraints and service-layer checks should work together.

------------------------------------------------------------------------

## Phase 6 --- Match

When:

``` text
User A likes User B
+
User B likes User A
```

create:

``` text
Match
```

Users should be able to retrieve their matches.

------------------------------------------------------------------------

## Phase 7 --- Chat

Implement:

``` text
Match
   ↓
Conversation
   ↓
Messages
```

Initially:

-   text messages only
-   match-based authorization
-   sender validation
-   message ordering
-   basic pagination if needed

Do not introduce unnecessary real-time complexity until the basic chat
flow works.

------------------------------------------------------------------------

## Phase 8 --- AI Message Suggestions

AI should be added after normal chat works.

Possible functionality:

``` text
User opens conversation
       ↓
AI analyzes conversation context
       ↓
Suggests several possible replies
```

AI should suggest rather than automatically send messages.

AI provider integration should be isolated behind a service interface.

------------------------------------------------------------------------

## Phase 9 --- Safety

Before beta:

``` text
Block
Report
Unmatch
```

Expected behavior:

### Block

A blocked user should no longer be discoverable/interactable according
to the product rules.

### Report

Store:

``` text
reporter
reported user
reason
timestamp
status
```

### Unmatch

Remove/disable the match relationship while preserving appropriate
audit/history behavior.

Safety logic must be server-side.

------------------------------------------------------------------------

## Phase 10 --- Basic Admin

Only build what is necessary initially.

Possible capabilities:

``` text
View reports
Review reported users
Take moderation action
View basic user/account status
```

Do not build a large admin dashboard initially.

------------------------------------------------------------------------

## Phase 11 --- Testing

Create automated tests for:

``` text
Authentication
Profiles
Preferences
Discovery
Likes
Matches
Chat
Safety
Authorization
Validation
```

Include positive and negative test cases.

Important security cases:

``` text
Unauthenticated request
Invalid JWT
Expired JWT
Accessing another user's profile
Updating another user's data
Creating a like as another user
Sending a message outside a match
```

------------------------------------------------------------------------

## Phase 12 --- Beta

Before external beta:

``` text
Internal testing
      ↓
5–10 trusted users
      ↓
25 users
      ↓
50 users
      ↓
100 users
```

Track:

``` text
Registration completion
Profile completion
Profiles viewed
Likes sent
Matches created
First message sent
Conversation continuation
Reports
Blocks
Unmatches
```

------------------------------------------------------------------------

# 10. Supabase Migration Plan

This is the immediate technical priority before continuing too far with
feature development.

## Step A --- Supabase Auth

Replace:

``` text
users.csv
custom password hashing
custom JWT
```

with:

``` text
Supabase Auth
```

Requirements:

-   Registration through Supabase Auth
-   Login through Supabase Auth
-   Access token handling
-   FastAPI token verification
-   Current-user dependency
-   Preserve existing API behavior where practical
-   Do not expose service-role credentials to mobile

------------------------------------------------------------------------

## Step B --- Supabase Profile Repository

Replace CSV profile persistence with:

``` text
Supabase profiles table
```

Keep the service/API contract stable where possible.

------------------------------------------------------------------------

## Step C --- Preferences Repository

Move preferences to:

``` text
Supabase preferences
```

------------------------------------------------------------------------

## Step D --- Likes Repository

Move likes to:

``` text
Supabase likes
```

------------------------------------------------------------------------

## Step E --- Matches Repository

Move matches to:

``` text
Supabase matches
```

Review match creation authorization/RLS carefully.

------------------------------------------------------------------------

## Step F --- Messages Repository

Move messages to:

``` text
Supabase messages
```

Review match-based message authorization carefully.

------------------------------------------------------------------------

## Step G --- Remove CSV Dependency

Only after successful migration and tests:

``` text
csv_repository.py
data/*.csv
```

can be deprecated/removed.

Do not delete CSV files before migration is verified.

------------------------------------------------------------------------

# 11. Repository Design Principle

Keep the layers separated:

``` text
API
 ↓
Service
 ↓
Repository
 ↓
Database
```

Business logic should primarily live in services.

Database-specific logic should live in repositories.

API routes should remain thin.

This will make future changes easier, including:

``` text
Supabase
→ another database
→ caching
→ background jobs
→ scaling
```

without rewriting the entire application.

------------------------------------------------------------------------

# 12. Coding Rules for Codex

Before changing anything:

1.  Inspect the existing repository.
2.  Understand the current implementation.
3.  Identify affected files.
4.  Preserve working functionality.
5.  Avoid unnecessary rewrites.
6.  Do not introduce new architecture unless required.
7.  Follow the existing project structure.
8.  Reuse existing services/schemas where appropriate.
9.  Do not duplicate functionality.
10. Do not silently delete working code.
11. Do not remove tests.
12. Add/update tests for every meaningful backend change.
13. Run the relevant tests after changes.
14. Report failures clearly.
15. Keep secrets out of source code.

------------------------------------------------------------------------

# 13. Security Rules

Never commit:

``` text
.env
Supabase service-role key
JWT secrets
API keys
LLM keys
```

The mobile application must never contain a Supabase service-role key.

Public/anon credentials must still be protected through correct RLS and
server-side authorization.

Do not trust:

``` text
user_id
sender_id
liker_id
```

from arbitrary client input when the authenticated identity can be
obtained from the token.

The backend should derive ownership from the authenticated user wherever
possible.

------------------------------------------------------------------------

# 14. Testing Strategy

Every feature should follow:

``` text
Implement
   ↓
Unit test
   ↓
API test
   ↓
Manual Swagger test
   ↓
Mobile integration test
   ↓
Edge-case test
```

Do not move to the next major feature if a previous feature is broken.

------------------------------------------------------------------------

# 15. Database Rules

Use database constraints wherever appropriate.

Examples:

``` text
No self-like
No duplicate like
Valid age range
Foreign keys
Required fields
Unique constraints
```

Application validation and database constraints should complement each
other.

------------------------------------------------------------------------

# 16. What We Should NOT Build Yet

Avoid premature complexity.

Do not build initially:

``` text
Advanced recommendation ML
Microservices
Kubernetes
Complex payment system
Video calling
Live streaming
Stories
Large-scale notification infrastructure
Complex subscription system
Large admin platform
Advanced analytics platform
Complex matching algorithms
```

These can be introduced after product validation.

------------------------------------------------------------------------

# 17. AI Roadmap

AI should initially solve specific user problems.

Possible future stages:

### Stage 1

AI message suggestions.

### Stage 2

Conversation-aware suggestions.

### Stage 3

Profile improvement assistance.

### Stage 4

Compatibility insights.

### Stage 5

Personalized recommendations.

Advanced recommendation ML should only be introduced after enough
behavioral data exists.

------------------------------------------------------------------------

# 18. Product Monetization --- Later

The first objective is product validation, not immediate monetization.

Possible future monetization ideas:

``` text
Premium analysis/report
Premium AI features
Profile enhancement
Additional discovery features
Subscription
```

Pricing and monetization should be validated later.

Do not allow monetization architecture to complicate the MVP.

------------------------------------------------------------------------

# 19. Cost Philosophy

Initial development should remain low-cost/free wherever practical.

Prefer:

``` text
Supabase free tier
GitHub
Expo
FastAPI
Python
Low-cost/free AI APIs during development
```

Move to paid infrastructure only when actual usage requires it.

Do not prematurely optimize for massive scale.

But avoid architecture that creates unnecessary migration pain later.

------------------------------------------------------------------------

# 20. Immediate Execution Order

The immediate execution order is:

``` text
1. Inspect current codebase
        ↓
2. Migrate authentication to Supabase Auth
        ↓
3. Migrate profiles from CSV → Supabase
        ↓
4. Run authentication/profile regression tests
        ↓
5. Migrate preferences
        ↓
6. Test preferences
        ↓
7. Build discovery
        ↓
8. Build like/pass
        ↓
9. Build match
        ↓
10. Build chat
        ↓
11. Add AI message suggestions
        ↓
12. Add block/report/unmatch
        ↓
13. Basic admin
        ↓
14. Full automated testing
        ↓
15. Internal beta
```

------------------------------------------------------------------------

# 21. Codex Execution Protocol

We will give Codex focused prompts rather than one giant implementation
request.

Each prompt should contain:

``` text
Context
Objective
Current architecture
Files to inspect
Required changes
Constraints
Testing requirements
Expected output
```

Codex should work incrementally.

After each major task:

``` text
Review changes
Run tests
Fix failures
Confirm behavior
Commit
```

Then proceed to the next task.

Do not ask Codex to implement the entire dating application in one
prompt.

------------------------------------------------------------------------

# 22. Prompt Sequence

The initial Codex prompts should be approximately:

``` text
PROMPT 01
Repository audit and architecture verification

PROMPT 02
Supabase Auth migration

PROMPT 03
Profile migration to Supabase

PROMPT 04
Authentication + profile regression testing

PROMPT 05
Dating Preferences

PROMPT 06
Discovery

PROMPT 07
Like / Pass

PROMPT 08
Match

PROMPT 09
Chat

PROMPT 10
AI Message Suggestions

PROMPT 11
Block / Report / Unmatch

PROMPT 12
Basic Admin

PROMPT 13
Full backend testing

PROMPT 14
Mobile integration testing

PROMPT 15
Beta-readiness audit
```

The exact number of prompts can change after Codex inspects the
repository.

------------------------------------------------------------------------

# 23. Important Rule for This Project

The application should evolve in small, verified steps.

The priority is:

``` text
Correctness
    ↓
Security
    ↓
Maintainability
    ↓
User experience
    ↓
Performance
    ↓
Scale
```

Do not sacrifice working functionality merely to introduce a more
advanced architecture.

------------------------------------------------------------------------

# 24. Current Status

At the point this document is created:

``` text
Foundation                  DONE
FastAPI                     DONE
Expo Mobile                 DONE
Backend connection          DONE
CSV Repository              DONE (temporary)
Registration                DONE
Login                       DONE
JWT authentication         DONE (temporary)
Protected /auth/me           DONE
Profile CRUD                DONE (temporary CSV)
Supabase project            DONE
Supabase tables             DONE
Supabase RLS                DONE
Supabase environment        CONFIGURED
Supabase migration          NEXT
Dating Preferences           NEXT AFTER MIGRATION
Discovery                   PENDING
Like / Pass                 PENDING
Match                       PENDING
Chat                        PENDING
AI Suggestions              PENDING
Block / Report / Unmatch    PENDING
Admin                       PENDING
Automated full testing     PENDING
Beta                        PENDING
```

------------------------------------------------------------------------

# 25. Final Target Architecture

The intended MVP architecture is:

``` text
                         ┌──────────────────────┐
                         │   React Native/Expo  │
                         │      Mobile App      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │      REST API        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Services        │
                         │ Business Logic       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Repository       │
                         │  Data Access Layer   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                 ┌────────────────────────────────────┐
                 │             SUPABASE                │
                 │                                    │
                 │  Auth                              │
                 │  PostgreSQL                        │
                 │  RLS                               │
                 │  Storage                           │
                 │                                    │
                 │  profiles                          │
                 │  preferences                       │
                 │  likes                             │
                 │  matches                           │
                 │  messages                          │
                 └────────────────────────────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    AI Service Layer  │
                         │   LLM providers      │
                         └──────────────────────┘
```

This document is the master execution reference for the DatingApp
project.

Codex prompts should use this document as the overall project context,
while each individual prompt should remain narrowly scoped to one
implementation task.
