from app.data._types import PhrasebookCategory
def _c(i,l,s,p): return PhrasebookCategory(id=i,level=l,situation=s,icon=p,phrases=[])
PHRASEBOOK_CATEGORIES=[_c("greetings_a1","A1","Greetings","👋"),_c("daily_a2","A2","Daily life","🏠"),_c("work_b1","B1","Work","💼"),_c("formal_b2","B2","Formal","📝"),_c("academic_c1","C1","Academic","🎓"),_c("advanced_c2","C2","Advanced","🧠")]