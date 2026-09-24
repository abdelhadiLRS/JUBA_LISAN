"""
Language-aware curriculum dispatcher.

For backward compatibility, CEFR_LEVELS remains a module-level constant.
All curriculum queries accept a ``target_language`` parameter (e.g. "en-GB",
"es-ES", "it-IT", "pt-PT") to resolve the correct language module.
"""

from __future__ import annotations

import sys

from app.data._types import CEFRLevel, CurriculumUnit  # noqa: F401

CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

_LANG_MODULES: dict[str, str] = {
    "en-GB": "app.data.en_GB.curriculum",
    "en-US": "app.data.en_US.curriculum",
    "de": "app.data.de.curriculum",
    "es": "app.data.es.curriculum",
    "fr": "app.data.fr.curriculum",
    "it": "app.data.it.curriculum",
    "ja": "app.data.ja.curriculum",
    "ko": "app.data.ko.curriculum",
    "pt": "app.data.pt.curriculum",
    "zh": "app.data.zh.curriculum",
    "ar": "app.data.ar.curriculum",
    "tr": "app.data.tr.curriculum",
    "ru": "app.data.ru.curriculum",
    "nl": "app.data.nl.curriculum",
    "pl": "app.data.pl.curriculum",
    "el": "app.data.el.curriculum",
    "sv": "app.data.language_foundations.sv",
    "da": "app.data.da.curriculum",
    "no": "app.data.no.curriculum",
    "fi": "app.data.fi.curriculum",
    "cs": "app.data.cs.curriculum",
    "cs": "app.data.language_foundations.cs",
    "ro": "app.data.language_foundations.ro",
    "hu": "app.data.language_foundations.hu",
    "uk": "app.data.language_foundations.uk",
    "he": "app.data.language_foundations.he",
    "vi": "app.data.language_foundations.vi",
    "bg": "app.data.language_foundations.bg",
    "sr": "app.data.language_foundations.sr",
    "hr": "app.data.language_foundations.hr",
    "sk": "app.data.language_foundations.sk",
    "sl": "app.data.language_foundations.sl",
    "lt": "app.data.language_foundations.lt",
    "lv": "app.data.language_foundations.lv",
    "is": "app.data.language_foundations.is",
    "ga": "app.data.language_foundations.ga",
    "cy": "app.data.language_foundations.cy",
    "ka": "app.data.language_foundations.ka",
    "hy": "app.data.language_foundations.hy",
    "az": "app.data.language_foundations.az",
    "kk": "app.data.language_foundations.kk",
    "uz": "app.data.language_foundations.uz",
    "ur": "app.data.language_foundations.ur",
    "ta": "app.data.language_foundations.ta",
    "te": "app.data.language_foundations.te",
    "mr": "app.data.language_foundations.mr",
    "gu": "app.data.language_foundations.gu",
    "sq": "app.data.language_foundations.sq", "eu": "app.data.language_foundations.eu", "gl": "app.data.language_foundations.gl", "mt": "app.data.language_foundations.mt", "af": "app.data.language_foundations.af",
    "eo": "app.data.language_foundations.eo", "lb": "app.data.language_foundations.lb", "gd": "app.data.language_foundations.gd", "yo": "app.data.language_foundations.yo", "ha": "app.data.language_foundations.ha",
    "am": "app.data.language_foundations.am", "so": "app.data.language_foundations.so", "zu": "app.data.language_foundations.zu", "xh": "app.data.language_foundations.xh", "rw": "app.data.language_foundations.rw",
    "ig": "app.data.language_foundations.ig", "mg": "app.data.language_foundations.mg", "ny": "app.data.language_foundations.ny", "sn": "app.data.language_foundations.sn", "st": "app.data.language_foundations.st",
}

_CACHE: dict[str, object] = {}

_I18N = {
    "en-GB": {
        "lesson_title": "{title} - Lesson {n}",
        "test_unit_title": "Level {level} Completion Test",
        "test_title": "Level {level} Completion Test",
        "test_objectives": [
            "Review all grammar topics from this level",
            "Complete the assessment to unlock the next level",
        ],
    },
    "en-US": {
        "lesson_title": "{title} - Lesson {n}",
        "test_unit_title": "Level {level} Completion Test",
        "test_title": "Level {level} Completion Test",
        "test_objectives": [
            "Review all grammar topics from this level",
            "Complete the assessment to unlock the next level",
        ],
    },
    "es-ES": {
        "lesson_title": "{title} - Lección {n}",
        "test_unit_title": "Examen de nivel {level}",
        "test_title": "Examen de nivel {level}",
        "test_objectives": [
            "Repasar todos los temas de gramática de este nivel",
            "Completar la evaluación para desbloquear el siguiente nivel",
        ],
    },
    "it-IT": {
        "lesson_title": "{title} - Lezione {n}",
        "test_unit_title": "Test di livello {level}",
        "test_title": "Test di livello {level}",
        "test_objectives": [
            "Ripassare tutti gli argomenti di grammatica di questo livello",
            "Completare la valutazione per sbloccare il livello successivo",
        ],
    },
    "pt-PT": {
        "lesson_title": "{title} - Lição {n}",
        "test_unit_title": "Exame de nível {level}",
        "test_title": "Exame de nível {level}",
        "test_objectives": [
            "Rever todos os tópicos de gramática deste nível",
            "Concluir a avaliação para desbloquear o próximo nível",
        ],
    },
    "fr-FR": {
        "lesson_title": "{title} - Leçon {n}",
        "test_unit_title": "Test de niveau {level}",
        "test_title": "Test de niveau {level}",
        "test_objectives": [
            "Revoir tous les thèmes de grammaire de ce niveau",
            "Réussir l'évaluation pour débloquer le niveau suivant",
        ],
    },
    "de-DE": {
        "lesson_title": "{title} - Lektion {n}",
        "test_unit_title": "Niveautest {level}",
        "test_title": "Niveautest {level}",
        "test_objectives": [
            "Alle Grammatikthemen dieses Niveaus wiederholen",
            "Die Prüfung bestehen, um das nächste Niveau freizuschalten",
        ],
    },
    "ja-JP": {
        "lesson_title": "{title} - レッスン {n}",
        "test_unit_title": "{level} レベル修了テスト",
        "test_title": "{level} レベル修了テスト",
        "test_objectives": [
            "このレベルの文法項目を復習する",
            "評価を完了して次のレベルを解放する",
        ],
    },
    "ko-KR": {
        "lesson_title": "{title} - 레슨 {n}",
        "test_unit_title": "{level} 레벨 완료 테스트",
        "test_title": "{level} 레벨 완료 테스트",
        "test_objectives": [
            "이 레벨의 모든 문법 항목을 복습하기",
            "평가를 완료하여 다음 레벨 잠금 해제하기",
        ],
    },
    "ar": {
        "lesson_title": "{title} - الدرس {n}",
        "test_unit_title": "اختبار إتمام المستوى {level}",
        "test_title": "اختبار إتمام المستوى {level}",
        "test_objectives": ["مراجعة موضوعات هذا المستوى", "إتمام التقييم للانتقال إلى المستوى التالي"],
    },
    "sv-SE": {
        "lesson_title": "{title} - Lektion {n}",
        "test_unit_title": "Sluttest för nivå {level}",
        "test_title": "Sluttest för nivå {level}",
        "test_objectives": [
            "Repetera alla grammatikområden på denna nivå",
            "Slutför bedömningen för att låsa upp nästa nivå",
        ],
    },
    "el-GR": {
        "lesson_title": "{title} - Μάθημα {n}",
        "test_unit_title": "Τελική αξιολόγηση επιπέδου {level}",
        "test_title": "Τελική αξιολόγηση επιπέδου {level}",
        "test_objectives": [
            "Επανάληψη όλων των γραμματικών θεμάτων του επιπέδου",
            "Ολοκλήρωση της αξιολόγησης για ξεκλείδωμα του επόμενου επιπέδου",
        ],
    },
    "da-DK": {
        "lesson_title": "{title} - Lektion {n}",
        "test_unit_title": "Afsluttende test for niveau {level}",
        "test_title": "Afsluttende test for niveau {level}",
        "test_objectives": [
            "Gennemgå alle grammatikemner fra dette niveau",
            "Gennemfør evalueringen for at låse næste niveau op",
        ],
    },
    "pl-PL": {
        "lesson_title": "{title} - Lekcja {n}",
        "test_unit_title": "Test końcowy poziomu {level}",
        "test_title": "Test końcowy poziomu {level}",
        "test_objectives": [
            "Powtórzyć wszystkie zagadnienia gramatyczne z tego poziomu",
            "Ukończyć ocenę, aby odblokować kolejny poziom",
        ],
    },
    "no-NO": {
        "lesson_title": "{title} - Leksjon {n}",
        "test_unit_title": "Sluttprøve for nivå {level}",
        "test_title": "Sluttprøve for nivå {level}",
        "test_objectives": [
            "Repetere alle grammatikktemaene på dette nivået",
            "Fullføre vurderingen for å låse opp neste nivå",
        ],
    },
    "fi-FI": {
        "lesson_title": "{title} - Oppitunti {n}",
        "test_unit_title": "Tason {level} lopputesti",
        "test_title": "Tason {level} lopputesti",
        "test_objectives": ["Kerrata kaikki tämän tason kielioppiaiheet","Suorittaa arviointi seuraavan tason avaamiseksi"],
    },

    "cs-CZ": {\n        "lesson_title": "{title} - Lekce {n}",\n        "test_unit_title": "Závěrečný test úrovně {level}",\n        "test_title": "Závěrečný test úrovně {level}",\n        "test_objectives": [\n            "Zopakovat všechna gramatická témata této úrovně",\n            "Dokončit hodnocení a odemknout další úroveň",\n        ],\n    },\n    "zh-CN": {
        "lesson_title": "{title} - 第 {n} 课",
        "test_unit_title": "{level} 等级完成测试",
        "test_title": "{level} 等级完成测试",
        "test_objectives": [
            "复习本等级的所有语法项目",
            "完成评估以解锁下一个等级",
        ],
    },
}


def _resolve_module(target_language: str) -> object:
    module_name = _LANG_MODULES.get(target_language) or _LANG_MODULES.get(
        target_language.split("-")[0], "app.data.en_GB.curriculum"
    )

    if module_name not in _CACHE:
        __import__(module_name)
        _CACHE[module_name] = sys.modules[module_name]

    return _CACHE[module_name]


def get_curriculum(target_language: str) -> dict:
    """Return the full CURRICULUM dict for the given target language."""
    mod = _resolve_module(target_language)
    return mod.CURRICULUM


def get_curriculum_units(level: str, target_language: str = "en-GB") -> list:
    """Return curriculum units for a CEFR level in the given target language."""
    curriculum = get_curriculum(target_language)
    return curriculum.get(level, [])


def distribute_units(
    units: list[CurriculumUnit],
    total_weeks: int,
    days_per_week: int,
    target_language: str = "en-GB",
) -> list[dict]:
    """Distribute curriculum units across lesson slots."""
    i18n = _I18N.get(target_language) or _I18N.get(target_language.split("-")[0], _I18N["en-GB"])

    total_slots = total_weeks * days_per_week
    lesson_slots = max(1, total_slots - 1)

    lesson_types_per_unit = [lt for u in units for lt in u.lesson_types]

    if not lesson_types_per_unit:
        return []

    slots: list[dict] = []
    unit_index = 0
    type_index = 0

    for slot in range(lesson_slots):
        unit = units[min(unit_index, len(units) - 1)]
        lt_list = unit.lesson_types
        lt = lt_list[type_index % len(lt_list)] if lt_list else "grammar"

        slots.append(
            {
                "week": slot // days_per_week + 1,
                "day": slot % days_per_week + 1,
                "unit_id": unit.id,
                "unit_title": unit.title,
                "lesson_type": lt,
                "title": i18n["lesson_title"].format(title=unit.title, n=type_index + 1),
                "objectives": (unit.competency_checklist[:2] if unit.competency_checklist else []),
                "estimated_minutes": 25,
                "grammar_points": (unit.grammar_points[:2] if unit.grammar_points else []),
                "vocabulary_set_ids": (
                    unit.vocabulary_set_ids[:1] if unit.vocabulary_set_ids else []
                ),
            }
        )

        type_index += 1
        if type_index % len(lt_list) == 0 and unit_index < len(units) - 1:
            remaining_slots = lesson_slots - slot - 1
            remaining_units = len(units) - unit_index - 1
            if remaining_slots <= remaining_units * len(units[unit_index + 1].lesson_types):
                unit_index += 1

    last_unit = units[-1]
    level = units[0].level
    slots.append(
        {
            "week": total_weeks,
            "day": days_per_week,
            "unit_id": "completion-test",
            "unit_title": i18n["test_unit_title"].format(level=level),
            "lesson_type": "review",
            "title": i18n["test_title"].format(level=level),
            "objectives": i18n["test_objectives"],
            "estimated_minutes": 45,
            "grammar_points": last_unit.grammar_points,
            "vocabulary_set_ids": [],
        }
    )

    return slots
