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
- SecureStore authentication token storage
- Guest mode with offline review queue
- Local voice recording/playback

## Run locally

```powershell
cd C:\Users\abdel\Documents\GitHub\JUBA_LISAN\mobile
npm install
Copy-Item .env.example .env.local
```

Edit `.env.local` and set the FastAPI address:

```text
EXPO_PUBLIC_API_URL=http://YOUR-PC-IP:8000
```

For Android Emulator, `http://10.0.2.2:8000` can be used when FastAPI is running on the development PC. For a physical Android/iPhone on the same Wi-Fi, use the Windows host LAN IPv4 address instead of `localhost`.

Start the app:

```powershell
npm start
```

Expo loads `EXPO_PUBLIC_*` variables from local `.env` files during development.

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

## EAS environments

The EAS profiles explicitly use `development`, `preview`, and `production` environments. Configure the public API endpoint on EAS rather than committing a production URL into source code:

```powershell
eas env:set --name EXPO_PUBLIC_API_URL --value https://YOUR-API-DOMAIN --environment development --visibility plaintext
eas env:set --name EXPO_PUBLIC_API_URL --value https://YOUR-API-DOMAIN --environment preview --visibility plaintext
eas env:set --name EXPO_PUBLIC_API_URL --value https://YOUR-API-DOMAIN --environment production --visibility plaintext
```

Verify the production value:

```powershell
eas env:list --environment production
```

`EXPO_PUBLIC_API_URL` is embedded in the client bundle, so it must never contain secrets.

## EAS builds

Preview APK for internal Android testing:

```powershell
npx eas build --platform android --profile preview
```

Production Android AAB for Google Play:

```powershell
npx eas build --platform android --profile production
```

Production iOS build:

```powershell
npx eas build --platform ios --profile production
```

The Android package and iOS bundle identifier are `com.jubalisan.app`.

## API architecture

The mobile client reuses the existing FastAPI contracts instead of duplicating business logic. The current shell reads the authenticated user and progress summary from `/api/auth/me` and `/api/progress/summary`.

The mobile code is structured as a native product foundation so future releases can add offline lessons, real-time voice/STT/TTS, push notifications, downloads, and deeper adaptive-learning flows without replacing the UI architecture.
