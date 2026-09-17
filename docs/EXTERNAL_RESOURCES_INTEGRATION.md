# JUBA LISAN External Educational Resources Integration

## نظرة عامة

تم دمج مصادر تعليمية خارجية قوية في منصة JUBA LISAN لتوسيع المحتوى التعليمي من المستوى A1 إلى C2 وفق معايير CEFR.

## المصادر المُدمجة

### 1. Tatoeba - جمل حقيقية مع ترجمات
**الموقع:** https://tatoeba.org

**ما يضيفه لـ JUBA LISAN:**
- جمل حقيقية مستخدمة في السياقات اليومية
- ترجمات متعددة اللغات (429 لغة)
- أمثلة عملية للكلمات والمفردات
- ملفات صوتية للنطق (متوفرة لبعض اللغات)

**الاستخدام:**
```python
from app.services.external_resources_service import ExternalResourcesService

service = ExternalResourcesService()

# البحث عن جمل تحتوي على كلمة معينة
sentences = service.tatoeba.search_sentences(
    query="hello",
    target_language="eng",
    translation_language="spa",
    limit=10
)

for sent in sentences:
    print(f"{sent.text} -> {sent.translations}")
```

**التخزين المؤقت:** يتم حفظ النتائج في `/tmp/juba_lisan_cache/tatoeba/`

---

### 2. CEFRLex - مفردات مصنفة حسب مستويات CEFR
**المستودع:** https://github.com/CEFRlex

**ما يضيفه لـ JUBA LISAN:**
- قوائم مفردات مرتبة حسب المستويات (A1, A2, B1, B2, C1, C2)
- توزيعات تكرار الكلمات
- معلومات عن جزء الكلام (noun, verb, adjective...)
- أمثلة استخدام لكل كلمة

**اللغات المدعومة:**
- الإنجليزية (EFLLex)
- الإسبانية (SVALex)
- الفرنسية (FLELex)
- الألمانية (DEFLex)
- الإيطالية (ITALLex)
- البرتغالية (PLELex)
- الهولندية (DutchLex)

**الاستخدام:**
```python
# الحصول على كلمات مستوى A1
words = service.cefrlex.get_words_by_level(
    language="en",
    cefr_level="A1",
    limit=50
)

for word in words:
    print(f"{word.word} - {word.definition} (Rank: {word.frequency_rank})")
```

**ملاحظة:** إذا لم تكن البيانات متاحة عن بعد، يستخدم النظام بيانات عينة مدمجة.

---

### 3. Mozilla Common Voice - بيانات صوتية
**الموقع:** https://commonvoice.mozilla.org

**ما يضيفه لـ JUBA LISAN:**
- ملفات صوتية حقيقية للنطق والاستماع
- أصوات متنوعة (أعمار، لهجات، جنس)
- نصوص مكتوبة مصاحبة للصوت
- مناسب لتمارين النطق والاستماع

**حجم البيانات:** 
- بعض مجموعات اللغات تصل إلى عدة جيجابايت
- التحميل عند الطلب لتجنب استهلاك المساحة

**الاستخدام:**
```python
# الحصول على معلومات مجموعة البيانات
info = service.common_voice.get_dataset_info("es")

# تحميل مقاطع صوتية محددة
clips = service.common_voice.download_clips(
    language="es",
    clip_ids=["clip1", "clip2"],
    progress_callback=lambda current, total: print(f"{current}/{total}")
)
```

---

### 4. MERLIN Corpus - نصوص المتعلمين
**الموقع:** https://merlin-corpus.github.io

**ما يضيفه لـ JUBA LISAN:**
- نصوص كتابية حقيقية كتبها متعلمو اللغة
- مصنفة حسب مستويات CEFR (A1-C1)
- تحليل الأخطاء الشائعة
- مفيد لإنشاء تمارين تصحيح وتصنيف

**اللغات المدعومة:**
- الألمانية (2,286 نصًا)
- الإيطالية
- التشيكية

**الاستخدام:**
```python
texts = service.merlin.get_texts_by_level(
    language="de",
    cefr_level="B1",
    limit=10
)

for text in texts:
    print(f"Level {text.cefr_level}: {text.text[:100]}...")
```

---

## التكامل مع المنهج الدراسي

### دمج جمل Tatoeba في الدروس

```python
from app.services.external_resources_service import integrate_tatoeba_sentences_into_curriculum

sentences = integrate_tatoeba_sentences_into_curriculum(
    target_language="en-GB",
    cefr_level="A1",
    unit_id="a1-unit-1"
)

# إضافة الجمل إلى درس القراءة/الاستماع
for sent in sentences:
    lesson_content.append({
        "type": "reading_listening",
        "text": sent["content"]["text"],
        "translation": sent["content"]["translations"],
        "audio": sent["content"]["audio_available"]
    })
```

### دمج مفردات CEFRLex

```python
from app.services.external_resources_service import integrate_cefr_vocabulary_into_sets

vocab_entries = integrate_cefr_vocabulary_into_sets(
    target_language="es-ES",
    cefr_level="A2",
    topic="Daily Routine",
    unit_ref="a2-unit-3"
)

# إضافة المفردات إلى مجموعة الكلمات
vocabulary_set.words.extend(vocab_entries)
```

---

## إدارة التخزين المؤقت

### الموقع الافتراضي
```bash
/tmp/juba_lisan_cache/
├── tatoeba/
│   ├── search_<hash>.json
│   └── audio/
│       └── eng/
│           └── <sentence_id>.mp3
├── cefrlex/
│   └── EFLLex_A1_50.json
├── common_voice/
│   └── es/
│       └── clips/
└── merlin/
    └── de_B1.json
```

### تغيير مسار التخزين
في `backend/app/core/config.py`:
```python
CACHE_DIR = "/path/to/custom/cache"
```

---

## معالجة الأخطاء والبدائل

النظام مصمم للعمل حتى عند عدم توفر المصادر الخارجية:

1. **Tatoeba:** إذا فشل الاتصال بالـ API، يتم إرجاع بيانات عينة
2. **CEFRLex:** إذا لم توجد الملفات على GitHub، يتم استخدام مفردات مدمجة
3. **Common Voice:** التحميل الفشل لا يؤثر على الوظائف الأخرى
4. **MERLIN:** متاح فقط للغات المحددة (DE, IT, CS)

---

## أفضل الممارسات

### 1. التحميل عند الطلب
لا تقم بتحميل جميع البيانات مسبقًا. استخدم النهج الهجين:
- النصوص: تُحمّل وتُخزن محليًا
- الصوت: يُحمّل فقط عند الحاجة

### 2. احترام التراخيص
- Tatoeba: CC BY 2.0 FR
- Common Voice: CC0 (بعض المجموعات)
- CEFRLex: تراخيص مفتوحة مختلفة
- MERLIN: لأغراض بحثية وتعليمية

### 3. تحسين الأداء
```python
# استخدم التخزين المؤقت بفعالية
sentences = service.tatoeba.search_sentences(query, lang, limit=20)
# النتائج تُخزن تلقائيًا

# اجلب فقط ما تحتاجه
words = service.cefrlex.get_words_by_level("en", "A1", limit=30)
# ليس كل الـ 100 كلمة
```

### 4. تعدد اللغات
```python
# دعم لغات متعددة
languages = ["en-GB", "es-ES", "fr-FR", "de-DE", "it-IT"]

for lang in languages:
    vocab = service.get_cefr_vocabulary_list(lang, "A1", count=20)
    # معالجة المفردات لكل لغة
```

---

## مثال كامل: إثراء درس بالمصادر الخارجية

```python
from app.services.external_resources_service import ExternalResourcesService

def enrich_lesson(topic, level, target_lang, native_lang):
    """إثراء درس بمحتوى من مصادر خارجية"""
    
    service = ExternalResourcesService()
    
    # 1. جلب المفردات المناسبة
    vocab = service.get_cefr_vocabulary_list(
        target_language=target_lang,
        cefr_level=level,
        count=15
    )
    
    # 2. إثراء كل كلمة بأمثلة
    enriched_vocab = []
    for word_entry in vocab:
        enriched = service.enrich_vocabulary_with_examples(
            word=word_entry.word,
            target_language=target_lang,
            native_language=native_lang,
            cefr_level=level
        )
        enriched_vocab.append(enriched)
    
    # 3. الحصول على مواد استماع
    listening_materials = service.get_listening_materials(
        target_language=target_lang,
        cefr_level=level,
        count=5
    )
    
    return {
        "vocabulary": enriched_vocab,
        "listening": listening_materials,
        "topic": topic,
        "level": level
    }

# استخدام الدالة
lesson_content = enrich_lesson(
    topic="Travel",
    level="A2",
    target_lang="en-GB",
    native_lang="ar-SA"
)
```

---

## التوسع المستقبلي

### مصادر مقترحة للإضافة:
1. **OPUS Corpus:** نصوص متوازية ضخمة للترجمة
2. **European Language Grid:** مستودع موارد اللغة الأوروبي
3. **CEFR Reception Tasks:** مهام استماع وقراءة رسمية
4. **Anki Decks:** بطاقات تعليمية جاهزة

### تحسينات مقترحة:
- [ ] واجهة API REST للوصول الخارجي
- [ ] نظام تنزيل دفعي للمجموعات الكبيرة
- [ ] تكامل مع أنظمة LMS (Moodle, Canvas)
- [ ] تحليل تلقائي لصعوبة النصوص
- [ ] توليد تمارين تفاعلية من المحتوى

---

## الدعم الفني

للمزيد من المعلومات أو الإبلاغ عن مشاكل:
- راجع ملف `external_resources_service.py`
- تحقق من السجلات (logs) في مجلد `logs/`
- تأكد من اتصال الإنترنت للوصول إلى المصادر الخارجية
