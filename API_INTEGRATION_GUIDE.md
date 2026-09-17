# JUBA LISAN - OpenAI & Google Speech API Integration

## 🔑 مفاتيح API المطلوبة

### 1. OpenAI API
- احصل على مفتاح من: https://platform.openai.com/api-keys
- أضفه في `.env.local`:
```
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### 2. Google Cloud Speech-to-Text
- اذهب إلى: https://console.cloud.google.com/
- أنشئ مشروعاً جديداً
- فعّل "Cloud Speech-to-Text API"
- أنشئ خدمة حساب (Service Account) وحمل ملف JSON
- أضف المسار في `.env.local`:
```
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/google-credentials.json
GOOGLE_PROJECT_ID=your-project-id
```

## 📦 التثبيت

```bash
# تثبيت مكتبات OpenAI
npm install openai

# تثبيت مكتبات Google Cloud
npm install @google-cloud/speech
```

## 🔧 الإعدادات

### ملف `.env.local` الكامل:
```env
# OpenAI
OPENAI_API_KEY=sk-...

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=./google-credentials.json
GOOGLE_PROJECT_ID=your-project-id

# Database (PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/juba_lisan

# NextAuth
NEXTAUTH_SECRET=your-secret-key-here
NEXTAUTH_URL=http://localhost:3000
```

## 🚀 الاستخدام

### AI Tutor API
```typescript
const response = await fetch('/api/ai/tutor', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'مرحباً، أريد ممارسة المحادثة',
    language: 'ar',
    level: 'intermediate'
  })
});
```

### Speech Analysis API
```typescript
const formData = new FormData();
formData.append('audio', audioBlob);
formData.append('language', 'ar-SA');

const response = await fetch('/api/ai/speech', {
  method: 'POST',
  body: formData
});
```

## ⚠️ ملاحظات مهمة

1. **الأمان**: لا تشارك مفاتيح API أبداً في الكود
2. **التكلفة**: راقب استخدامك لـ APIs المدفوعة
3. **Rate Limiting**: تم إعداد حدود للاستخدام في الكود
4. **Fallback**: يوجد وضع تجريبي بدون APIs حقيقية للتطوير

## 🧪 اختبار APIs

```bash
# اختبار AI Tutor
curl -X POST http://localhost:3000/api/ai/tutor \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "language": "en"}'

# اختبار Speech (يتطلب ملف صوتي)
curl -X POST http://localhost:3000/api/ai/speech \
  -F "audio=@test.wav" \
  -F "language=en-US"
```
