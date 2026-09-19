            answer = " → ".join(map(str, base))
            alternatives = [answer, " → ".join(map(str, reversed(base))), " → ".join(map(str, base[1:] + base[:1]))]
            if " → ".join(map(str, scrambled)) not in alternatives:
                alternatives.append(" → ".join(map(str, scrambled)))
            choices = list(dict.fromkeys(alternatives))[:4]
            rng.shuffle(choices)
            prompt = (
                f"Order from smallest to largest: {' · '.join(map(str, scrambled))}"
                if language == "en"
                else (f"Ordonne du plus petit au plus grand : {' · '.join(map(str, scrambled))}"
                      if language == "fr"
                      else f"رتّب الأرقام من الأصغر إلى الأكبر: {' · '.join(map(str, scrambled))}"))
            skill, topic = "ordering", "ordering"
        questions.append({
            "id": question_id,
            "prompt": prompt,
            "choices": choices,