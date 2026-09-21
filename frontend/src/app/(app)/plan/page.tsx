          apiFetch('/api/study-plan/today').catch(() => null),
          apiFetch('/api/study-plan/pending-lessons').catch(() => null),
          apiFetch('/api/study-plan/lessons').catch(() => null),
        ])

      if (!planRes.ok) {
        if (planRes.status === 404) {
          router.push('/assessment')
          return
        }
        throw new Error(`Failed to load plan (${planRes.status})`)
      }

      const planData = (await planRes.json()) as StudyPlan
      setPlan(planData)

      if (journeyRes?.ok) {
        const journey = (await journeyRes.json()) as LearningJourneyResponse
        if (journey.next_lesson_id != null) {
          setActiveLessonId(journey.next_lesson_id)
        }
        const journeyMap: CompetencyMap = {}
        for (const section of journey.sections) {
          for (const unit of section.units) {
            journeyMap[unit.id] = unit.progress
          }
        }
        if (Object.keys(journeyMap).length > 0) {
          setCompetencies(journeyMap)
        }
      }

      // Learning Journey is the authoritative progression snapshot.
      // Use the legacy competency endpoint only if the journey request failed.
      if (compRes?.ok && !journeyRes?.ok) {
        const compData = await compRes.json()
        if (Array.isArray(compData)) {
          const map: CompetencyMap = {}
          for (const item of compData as { unit_id: string; score: number }[]) {
            map[item.unit_id] = item.score
          }
          setCompetencies(map)
        } else {
          setCompetencies(compData as CompetencyMap)
        }
      }
