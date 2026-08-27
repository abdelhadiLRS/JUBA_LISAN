# JUBA LISAN Mobile

Native Android/iOS client foundation for JUBA LISAN, built with Expo + React Native and connected to the existing FastAPI API.

## Current experience

- Premium light mobile visual system
- Home learning dashboard with streak, XP, vocabulary and accuracy
- Personalized learning path
- AI conversation surface with tutor prompt and waveform UI
- Smart review surface
- Progress and skill-growth view
- Bottom navigation designed for one-hand use
- Shared account/progress data with the web backend

## Run locally

```powershell
cd C:\Users\abdel\Documents\GitHub\JUBA_LISAN\mobile
npm install
$env:EXPO_PUBLIC_API_URL="http://10.0.2.2:8000"
npm start
```

For a physical Android/iPhone on the same Wi-Fi, replace the URL with the Windows host LAN address, for example `http://192.168.1.20:8000`.

## Android

```powershell
npm run android
```

## iOS

```bash
npm run ios
```

## Type check

```powershell
npm run typecheck
```

## EAS builds

```powershell
npx eas login
npx eas build:configure
npx eas build --platform android --profile preview
npx eas build --platform ios --profile preview
```

Production builds:

```powershell
npx eas build --platform android --profile production
npx eas build --platform ios --profile production
```

## API architecture

The mobile client reuses the existing FastAPI contracts instead of duplicating business logic. The current shell reads the authenticated user and progress summary from `/api/auth/me` and `/api/progress/summary`.

The mobile code is intentionally structured as a native product foundation so future releases can add offline lessons, real-time voice/STT/TTS, push notifications, downloads, and deeper adaptive-learning flows without replacing the UI architecture.
