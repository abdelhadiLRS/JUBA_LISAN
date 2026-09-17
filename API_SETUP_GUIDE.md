# 📡 دليل إعداد APIs - JUBA LISAN

هذا الدليل يشرح كيفية ربط خدمات الذكاء الاصطناعي الحقيقية بمشروع JUBA LISAN.

---

## 1️⃣ OpenAI API (للمدرس الذكي)

### الخطوات:

#### أ. الحصول على مفتاح API
1. اذهب إلى [OpenAI Platform](https://platform.openai.com/)
2. سجل الدخول أو أنشئ حساباً جديداً
3. اذهب إلى **API Keys** من القائمة الجانبية
4. انقر على **Create new secret key**
5. انسخ المفتاح (يبدأ بـ `sk-...`)

#### ب. اختيار النموذج المناسب
- **gpt-4o-mini**: موصى به - سريع واقتصادي وجيد للتعليم
- **gpt-4o**: أعلى جودة، أغلى ثمناً
- **gpt-3.5-turbo**: أرخص خيار، جودة مقبولة

#### ج. إضافة المفتاح للمشروع
```bash
cd /workspace/frontend
cp .env.local.example .env.local
```

ثم عدل ملف `.env.local`:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

#### د. اختبار الاتصال
```bash
curl http://localhost:3000/api/ai/tutor \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, I want to learn Arabic", "language": "ar"}'
```

---

## 2️⃣ Google Cloud Speech-to-Text (لتحليل النطق)

### الخطوات:

#### أ. إنشاء مشروع Google Cloud
1. اذهب إلى [Google Cloud Console](https://console.cloud.google.com/)
2. أنشئ مشروعاً جديداً أو اختر مشروعاً موجوداً
3. فعّل **Cloud Speech-to-Text API**:
   - اذهب إلى **APIs & Services > Library**
   - ابحث عن "Cloud Speech-to-Text API"
   - انقر على **Enable**

#### ب. إنشاء حساب خدمة (Service Account)
1. اذهب إلى **IAM & Admin > Service Accounts**
2. انقر على **Create Service Account**
3. اسم الحساب: `juba-lisan-speech`
4. امنحه الصلاحيات التالية:
   - **Cloud Speech-to-Text API User**
5. انقر على **Create and Continue** ثم **Done**

#### ج. إنشاء مفتاح JSON
1. انقر على حساب الخدمة الذي أنشأته
2. اذهب إلى تبويب **Keys**
3. انقر على **Add Key > Create new key**
4. اختر **JSON** كتنسيق
5. سيتم تنزيل الملف تلقائياً (مثلاً: `juba-lisan-speech-key.json`)

#### د. إضافة المفتاح للمشروع
انقل ملف المفتاح إلى مجلد المشروع:
```bash
mv ~/Downloads/juba-lisan-speech-key.json /workspace/frontend/google-cloud-key.json
```

#### هـ. تحديث ملف البيئة
في ملف `.env.local`:
```env
GOOGLE_APPLICATION_CREDENTIALS=./google-cloud-key.json
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_SPEECH_LANGUAGE_CODE=ar-SA
```

#### و. اختبار الاتصال
```bash
# تسجيل صوتي قصير (webm/opus) ثم إرساله
curl http://localhost:3000/api/ai/speech \
  -F "audio=@recording.webm" \
  -F "language=ar-SA"
```

---

## 3️⃣ تكلفة الخدمات المتوقعة

### OpenAI (شهرياً - لمستخدم نشط متوسط)
| النموذج | التكلفة لكل 1M Token | الاستخدام الشهري | التكلفة المتوقعة |
|---------|---------------------|-----------------|-----------------|
| gpt-4o-mini | $0.15 (input) / $0.60 (output) | ~500K tokens | ~$0.50 - $2 |
| gpt-4o | $2.50 (input) / $10 (output) | ~500K tokens | ~$5 - $15 |

### Google Speech-to-Text (شهرياً)
| الميزة | التكلفة | الاستخدام الشهري | التكلفة المتوقعة |
|--------|---------|-----------------|-----------------|
| Speech-to-Text (أقل من 60 دقيقة/شهر) | مجاني | 30 دقيقة | $0 |
| Speech-to-Text (60+ دقيقة/شهر) | $0.006/15 ثانية | 300 دقيقة | ~$12 |

**💰 التكلفة الإجمالية المتوقعة:** $2 - $20 شهرياً حسب الاستخدام

---

## 4️⃣ التحقق من الإعداد

### سكريبت اختبار شامل
أنشئ ملف `/workspace/frontend/scripts/test-apis.js`:

```javascript
// test-apis.js
const fetch = require('node-fetch');

async function testOpenAI() {
  console.log('🧪 Testing OpenAI API...');
  try {
    const response = await fetch('http://localhost:3000/api/ai/tutor', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: 'Hello, how are you?',
        language: 'en'
      })
    });
    const data = await response.json();
    if (data.response && !data.error) {
      console.log('✅ OpenAI API is working!');
      console.log('Response:', data.response.substring(0, 100) + '...');
    } else {
      console.log('❌ OpenAI API error:', data.error);
    }
  } catch (error) {
    console.log('❌ OpenAI API connection failed:', error.message);
  }
}

async function testGoogleSpeech() {
  console.log('\n🧪 Testing Google Speech API...');
  // Note: Requires actual audio file
  console.log('⚠️  Manual testing required for speech API');
  console.log('📝 Use the browser interface to record and test speech');
}

async function main() {
  console.log('🚀 Starting API tests...\n');
  await testOpenAI();
  await testGoogleSpeech();
  console.log('\n✅ Tests completed!');
}

main();
```

تشغيل الاختبار:
```bash
cd /workspace/frontend
node scripts/test-apis.js
```

---

## 5️⃣ استكشاف الأخطاء

### المشكلة: "OpenAI API key not configured"
**الحل:** تأكد من وجود ملف `.env.local` وبه المفتاح الصحيح

### المشكلة: "Unable to read credentials file"
**الحل:** 
- تحقق من مسار ملف `google-cloud-key.json`
- تأكد من وجود الصلاحية للقراءة: `chmod 600 google-cloud-key.json`

### المشكلة: "Quota exceeded"
**الحل:** 
- راجع استخدامك في [Google Cloud Quotas](https://console.cloud.google.com/apis/api/speech.googleapis.com/quotas)
- قد تحتاج لربط بطاقة ائتمان لزيادة الحد

### المشكلة: "Rate limit exceeded" (OpenAI)
**الحل:** 
- راجع حدود الاستخدام في [OpenAI Dashboard](https://platform.openai.com/account/limits)
- قد تحتاج لترقية الخطة أو انتظار إعادة تعيين العداد

---

## 6️⃣ نصائح للأداء والتكلفة

### تقليل التكلفة
1. استخدم `gpt-4o-mini` بدلاً من `gpt-4o` للمحادثات اليومية
2. احفظ المحادثات الشائعة في قاعدة البيانات لإعادة استخدامها
3. حدد طول الردود بـ `max_tokens: 300`
4. استخدم caching للردود المتكررة

### تحسين الأداء
1. استخدم Streaming للردود الطويلة
2. نفذ Retry logic مع exponential backoff
3. أضف Timeout للطلبات (30 ثانية كحد أقصى)
4. استخدم CDN للAssets الثابتة

### الأمان
1. ⚠️ **لا ترفع ملف `.env.local` إلى Git**
2. ⚠️ **لا تشارك مفاتيح API علناً**
3. استخدم Rate Limiting لمنع إساءة الاستخدام
4. راقع الاستخدام بشكل دوري

---

## 7️⃣ الانتقال للإنتاج (Production)

### متغيرات بيئة الإنتاج
```env
# Production .env
OPENAI_API_KEY=sk-prod-key-here
GOOGLE_APPLICATION_CREDENTIALS=/secure/path/prod-key.json
BACKEND_URL=https://api.jubalisan.com
DATABASE_URL=postgresql://prod-db-connection
NODE_ENV=production
```

### توصيات النشر
1. استخدم **Vercel** أو **AWS Lambda** للـ Frontend
2. خزّن المفاتيح في **Secrets Manager** (AWS/GCP/Azure)
3. فعّل **HTTPS** إلزامياً
4. أضف **CORS headers** مناسبة
5. راقع الأداء مع **Sentry** أو **Datadog**

---

## 📞 الدعم

إذا واجهت أي مشاكل:
1. راجع السجلات (Logs): `docker logs juba-frontend`
2. تحقق من حالة الخدمات:
   - [OpenAI Status](https://status.openai.com/)
   - [Google Cloud Status](https://status.cloud.google.com/)
3. افتح Issue في مستودع المشروع

---

**آخر تحديث:** {{DATE}}  
**الإصدار:** 1.0.0
