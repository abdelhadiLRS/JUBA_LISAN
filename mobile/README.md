# JUBA LISAN Mobile

Cross-platform mobile client for Android and iOS, built with Expo and React Native.

## Current mobile experience

- JUBA LISAN branded authentication
- JWT login against the existing FastAPI backend
- Persistent mobile session token
- Personalized home dashboard
- Streak, XP, vocabulary and accuracy cards
- Today's learning mission
- AI Learning Coach surface
- Voice practice UI with microphone capture
- Smart review queue
- Profile and sign-out
- Shared backend progress endpoints so web and mobile can use the same account data

## Development

```bash
cd mobile
npm install
$env:EXPO_PUBLIC_API_URL="http://YOUR_SERVER:8000"
npm start
```

For an Android emulator, use `http://10.0.2.2:8000` when the API is running on the host machine. For a physical phone, use the host machine's LAN IP or your deployed HTTPS API URL.

Android:

```bash
npm run android
```

iOS (macOS + Xcode):

```bash
npm run ios
```

Type checking:

```bash
npm run typecheck
```

## Architecture

The mobile app intentionally reuses the existing FastAPI contracts instead of duplicating business logic. Authentication uses `/api/auth/login` and `/api/auth/me`; progress uses `/api/progress/summary`; the daily plan uses `/api/study-plan/today`.

The mobile UI is designed as a native learning product rather than a wrapped web page: large touch targets, safe-area layouts, bottom-friendly actions, focused learning cards, voice-first interaction, and a lightweight navigation stack.
