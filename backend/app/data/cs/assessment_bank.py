"""Czech A1-C2 assessment bank for JUBA LISAN."""
from app.data._types import AssessmentQuestion

ASSESSMENT_BANK = [
AssessmentQuestion(id="cs-a1-001",skill="grammar",difficulty="A1",question="Vyber správnou větu.",options=["Jsem student.","Student jsem být.","Jsem studentu.","Jsem studenti."],correct="Jsem student."),
AssessmentQuestion(id="cs-a1-002",skill="vocabulary",difficulty="A1",question="Co znamená „Dobrý den“?",options=["Hello / good day","Good night","Thank you","Goodbye"],correct="Hello / good day"),
AssessmentQuestion(id="cs-a1-003",skill="reading",difficulty="A1",question="Přečti: „Anna bydlí v Praze.“ Kde Anna bydlí?",options=["V Praze","V Brně","Doma","Ve škole"],correct="V Praze"),
AssessmentQuestion(id="cs-a1-004",skill="grammar",difficulty="A1",question="Jak vytvoříš zápor „rozumím“?",options=["Nerozumím.","Ne rozumím.","Nerozumit.","Nerozumě."],correct="Nerozumím."),
AssessmentQuestion(id="cs-a2-001",skill="grammar",difficulty="A2",question="Vyber správný minulý čas.",options=["Včera jsem pracoval.","Včera pracuji.","Včera budu pracovat.","Včera pracovat."],correct="Včera jsem pracoval."),
AssessmentQuestion(id="cs-a2-002",skill="vocabulary",difficulty="A2",question="Co je „vlak“?",options=["train","bus","car","station"],correct="train"),
AssessmentQuestion(id="cs-a2-003",skill="reading",difficulty="A2",question="„Zítra pojedu do Brna.“ Kdy osoba pojede?",options=["Tomorrow","Yesterday","Today","Next month"],correct="Tomorrow"),
AssessmentQuestion(id="cs-a2-004",skill="grammar",difficulty="A2",question="Vyber správný komparativ.",options=["větší","největší","velký","velice"],correct="větší"),
AssessmentQuestion(id="cs-b1-001",skill="grammar",difficulty="B1",question="Vyber správnou podmínkovou větu.",options=["Kdybych měl čas, přišel bych.","Kdyby mám čas, přijdu bych.","Kdybych mít čas, přišel.","Kdyby mám čas, přišel."],correct="Kdybych měl čas, přišel bych."),
AssessmentQuestion(id="cs-b1-002",skill="vocabulary",difficulty="B1",question="Co nejlépe znamená „důkaz“?",options=["evidence","question","habit","journey"],correct="evidence"),
AssessmentQuestion(id="cs-b1-003",skill="reading",difficulty="B1",question="„Studie naznačuje změnu, protože výsledky jsou odlišné.“ Co výsledky vysvětlují?",options=["Naznačují změnu","Popírají studii","Popisují cestu","Mění jazyk"],correct="Naznačují změnu"),
AssessmentQuestion(id="cs-b1-004",skill="grammar",difficulty="B1",question="Která vazba je správná?",options=["čekat na autobus","čekat autobusovi","čekat s autobus","čekat do autobus"],correct="čekat na autobus"),
AssessmentQuestion(id="cs-b2-001",skill="grammar",difficulty="B2",question="Která věta vyjadřuje přípustku?",options=["Ačkoli pršelo, šli jsme ven.","Protože pršelo, zůstali jsme.","Když pršelo, spali jsme.","Pršelo a prší."],correct="Ačkoli pršelo, šli jsme ven."),
AssessmentQuestion(id="cs-b2-002",skill="vocabulary",difficulty="B2",question="Co znamená „námitka“?",options=["objection","agreement","schedule","address"],correct="objection"),
AssessmentQuestion(id="cs-b2-003",skill="reading",difficulty="B2",question="„Výsledky jsou přesvědčivé, nicméně vzorek je malý.“ Co je omezením?",options=["Malý vzorek","Přesvědčivé výsledky","Dlouhý text","Nový projekt"],correct="Malý vzorek"),
AssessmentQuestion(id="cs-b2-004",skill="grammar",difficulty="B2",question="Co je typické pro formální styl?",options=["přesná a neutrální formulace","slang v každé větě","náhodný slovosled","zkratky bez kontextu"],correct="přesná a neutrální formulace"),
AssessmentQuestion(id="cs-c1-001",skill="grammar",difficulty="C1",question="Která formulace je vhodná pro akademické tvrzení?",options=["Výsledky naznačují možný rozdíl.","Výsledky vždy dokazují všechno.","Výsledky jsou určitě pravdivé.","Výsledky nic neznamenají."],correct="Výsledky naznačují možný rozdíl."),
AssessmentQuestion(id="cs-c1-002",skill="vocabulary",difficulty="C1",question="Co znamená „hypotéza“?",options=["hypothesis","conclusion","invoice","appointment"],correct="hypothesis"),
AssessmentQuestion(id="cs-c1-003",skill="reading",difficulty="C1",question="„Studie uvádí, že trend pokračuje.“ Kdo trend uvádí?",options=["Studie","Student","Čtenář","Město"],correct="Studie"),
AssessmentQuestion(id="cs-c1-004",skill="grammar",difficulty="C1",question="Která žádost je profesionálně zdvořilá?",options=["Mohl byste prosím doplnit údaje?","Doplň údaje!","Ty údaje doplň.","Doplň to hned."],correct="Mohl byste prosím doplnit údaje?"),
AssessmentQuestion(id="cs-c2-001",skill="grammar",difficulty="C2",question="Která formulace je nejpřesnější?",options=["Tvrzení je zavádějící, nikoli nutně nepravdivé.","Tvrzení je špatné.","Tvrzení je vždy pravda.","Tvrzení je nic."],correct="Tvrzení je zavádějící, nikoli nutně nepravdivé."),
AssessmentQuestion(id="cs-c2-002",skill="vocabulary",difficulty="C2",question="Co znamená „jednoznačný“?",options=["unambiguous","uncertain","informal","repeated"],correct="unambiguous"),
AssessmentQuestion(id="cs-c2-003",skill="reading",difficulty="C2",question="„Oba zdroje se shodují v trendu, liší se však v interpretaci.“ V čem se liší?",options=["V interpretaci","V trendu","V jazyce","V datech"],correct="V interpretaci"),
AssessmentQuestion(id="cs-c2-004",skill="grammar",difficulty="C2",question="Co je cílem syntézy více zdrojů?",options=["Spojit perspektivy a kvalifikovat závěr.","Opakovat jeden zdroj.","Odstranit všechny rozdíly.","Vyhnout se důkazům."],correct="Spojit perspektivy a kvalifikovat závěr."),
]