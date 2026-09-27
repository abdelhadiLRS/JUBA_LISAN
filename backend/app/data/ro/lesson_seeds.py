"""Curated Romanian A2-C2 lesson seeds."""
from __future__ import annotations
from typing import Any

S: dict[tuple[str,str,str],dict[str,Any]] = {}

def add(level, unit, data):
    for skill, value in data.items():
        S[(level, unit, skill)] = value

add("A2","ro-a2-unit-1",{
"grammar":{"title":"Perfectul compus","objective":"Relatează experiențe trecute.","grammar":["perfectul compus","auxiliarul a avea"],"examples":["Am vizitat Brașovul anul trecut.","Am cumpărat bilete înainte de plecare."]},
"vocabulary":{"title":"Călătorii","objective":"Folosește vocabularul de bază pentru călătorii.","words":[("călătorie","trip","Am făcut o călătorie scurtă."),("gară","station","Gara este aproape."),("bilet","ticket","Am cumpărat un bilet.")]},
"reading":{"title":"Un weekend la Brașov","objective":"Înțelege o narațiune scurtă.","text":"Sâmbătă dimineață, Andrei a plecat cu trenul spre Brașov. A ajuns la prânz și a vizitat centrul vechi. Duminică s-a întors acasă.","questions":["Unde a mers Andrei?","Cum a călătorit?"]},
"listening":{"title":"Planul de weekend","objective":"Identifică informații despre o călătorie.","transcript":"Vineri seara plecăm spre Sibiu. Sâmbătă vizităm centrul și duminică ne întoarcem.","questions":["Când pleacă?","Ce vizitează sâmbătă?"]},
"speaking":{"title":"Povestește o călătorie","objective":"Povestește o experiență recentă.","prompt":"Vorbește 45 de secunde despre o călătorie recentă.","phrases":["Am fost la...","Am ajuns...","Apoi am..."],"examples":["Am fost la Cluj weekendul trecut. Am vizitat centrul orașului."]},
"writing":{"title":"Mesaj despre o excursie","objective":"Scrie despre o experiență trecută.","prompt":"Scrie 80-100 de cuvinte despre o excursie recentă.","guidance":["Folosește cel puțin cinci verbe la perfectul compus.","Menționează unde ai fost și ce ai făcut."],"examples":["Weekendul trecut am fost la..."]},
"review":{"title":"Recapitulare: călătorii","objective":"Consolidează trecutul și vocabularul.","questions":["Transformă «Merg la Sibiu» la trecut.","Completează: Am ___ un bilet ieri.","Povestește o excursie."]}
})

add("B1","ro-b1-unit-1",{
"grammar":{"title":"Condiționalul","objective":"Exprimă situații ipotetice.","grammar":["aș + infinitiv","dacă + condițional"],"examples":["Aș participa dacă aș avea timp.","Dacă aș locui acolo, aș folosi bicicleta."]},
"vocabulary":{"title":"Muncă și dezvoltare","objective":"Discută despre obiective profesionale.","words":[("experiență","experience","Am experiență în acest domeniu."),("abilitate","skill","Vreau să-mi dezvolt o abilitate."),("obiectiv","goal","Obiectivul meu este clar.")]},
"reading":{"title":"Un nou curs profesional","objective":"Înțelege motivele unei decizii.","text":"Mara lucrează în administrație, dar vrea să-și schimbe specializarea. A ales un curs de analiză de date deoarece poate studia seara și poate aplica imediat ceea ce învață.","questions":["De ce urmează cursul?","Când studiază?"]},
"listening":{"title":"O decizie profesională","objective":"Identifică motive și planuri.","transcript":"Am decis să urmez un curs avansat pentru că vreau să comunic mai bine la serviciu. Dacă reușesc să-mi organizez timpul, voi participa la toate sesiunile.","questions":["De ce urmează cursul?","Ce condiție menționează vorbitorul?"]},
"speaking":{"title":"O alegere importantă","objective":"Prezintă o decizie și justifică alegerea.","prompt":"Vorbește un minut despre o alegere profesională și explică motivele.","phrases":["Am ales să...","Motivul principal este...","Dacă aș putea..."],"examples":["Am ales să învăț o limbă străină deoarece îmi poate extinde oportunitățile."]},
"writing":{"title":"Plan de dezvoltare","objective":"Scrie despre un obiectiv și pașii necesari.","prompt":"Scrie 120-150 de cuvinte despre un obiectiv profesional.","guidance":["Explică motivul.","Folosește două structuri condiționale.","Propune pași concreți."],"examples":["În următoarele luni vreau să..."]},
"review":{"title":"Recapitulare: decizii","objective":"Consolidează condiționalul.","questions":["Completează: Dacă aș avea timp, aș ___.","Explică diferența dintre obiectiv și abilitate.","Formulează un plan."]}
})

add("B2","ro-b2-unit-1",{
"grammar":{"title":"Vorbirea indirectă","objective":"Raportează opinii și construiește argumente.","grammar":["a spune că","a întreba dacă","conectori de concesie"],"examples":["Expertul a spus că măsura ar putea reduce costurile.","Deși există avantaje, rezultatele depind de context."]},
"vocabulary":{"title":"Dezbatere și societate","objective":"Argumentează pe teme sociale.","words":[("argument","argument","Argumentul se bazează pe date."),("dovadă","evidence","Avem nevoie de dovezi."),("impact","impact","Impactul trebuie analizat.")]},
"reading":{"title":"Munca hibridă","objective":"Analizează argumente pro și contra.","text":"Munca hibridă poate reduce timpul petrecut pe drum și poate oferi flexibilitate. Totuși, comunicarea informală poate deveni mai dificilă. Eficiența depinde de organizare și de natura activității.","questions":["Care este un avantaj?","Care este o limită?"]},
"listening":{"title":"Două perspective","objective":"Identifică poziții și contraargumente.","transcript":"Munca hibridă funcționează bine pentru echipele autonome. Pe de altă parte, colegii noi au nevoie de mai mult contact direct.","questions":["Pentru cine funcționează bine?","Cine are nevoie de contact direct?"]},
"speaking":{"title":"Dezbatere argumentată","objective":"Susține o poziție și răspunde unei perspective alternative.","prompt":"Vorbește 90 de secunde despre avantajele și limitele muncii hibride.","phrases":["Pe de o parte...","Pe de altă parte...","Un argument important este..."],"examples":["Munca hibridă oferă flexibilitate, însă eficiența depinde de tipul echipei."]},
"writing":{"title":"Text argumentativ","objective":"Scrie un text echilibrat.","prompt":"Scrie 180-220 de cuvinte despre munca hibridă.","guidance":["Prezintă două argumente.","Include un contraargument.","Încheie cu o concluzie."],"examples":["Munca hibridă a schimbat modul în care echipele colaborează."]},
"review":{"title":"Recapitulare: argumentare","objective":"Consolidează raportarea opiniilor și folosirea conectorilor.","questions":["Raportează o opinie.","Adaugă un contraargument.","Scrie o concluzie."]}
})

add("C1","ro-c1-unit-1",{
"grammar":{"title":"Precizie și prudență","objective":"Formulează afirmații academice cu gradul potrivit de certitudine.","grammar":["se pare că","este posibil ca + conjunctiv","a sugera că"],"examples":["Datele sugerează că efectul este limitat.","Este posibil ca rezultatele să difere."]},
"vocabulary":{"title":"Cercetare și analiză","objective":"Folosește terminologie pentru evidență.","words":[("ipoteză","hypothesis","Ipoteza trebuie verificată."),("eșantion","sample","Eșantionul este relativ mic."),("limitare","limitation","Studiul are o limitare importantă.")]},
"reading":{"title":"Interpretarea datelor","objective":"Distinge rezultate, interpretări și limite.","text":"Rezultatele indică o asociere între utilizarea platformei și frecvența studiului. Cu toate acestea, datele nu permit stabilirea unei relații cauzale. Eșantionul a fost format din voluntari.","questions":["Ce indică rezultatele?","De ce nu se poate stabili cauzalitatea?"]},
"listening":{"title":"Prezentarea unei cercetări","objective":"Extrage concluzii și limite.","transcript":"Rezultatele sunt promițătoare, dar trebuie interpretate cu prudență. Eșantionul este mic și nu putem exclude alte explicații.","questions":["Cum trebuie interpretate rezultatele?","Care este limita?"]},
"speaking":{"title":"Analiză critică","objective":"Prezintă o interpretare nuanțată.","prompt":"Vorbește două minute despre o afirmație bazată pe date și explică limitele.","phrases":["Datele sugerează...","Această interpretare trebuie privită cu prudență.","O limitare importantă este..."],"examples":["Datele sugerează o asociere, dar nu demonstrează cauzalitatea."]},
"writing":{"title":"Paragraf academic","objective":"Redactează o analiză prudentă.","prompt":"Scrie 220-280 de cuvinte despre interpretarea unui set de date.","guidance":["Separă rezultatele de interpretare.","Folosește formulări prudente.","Menționează două limitări."],"examples":["Rezultatele indică... Cu toate acestea..."]},
"review":{"title":"Recapitulare: analiză critică","objective":"Consolidează limbajul de evidență.","questions":["Formulează concluzie prudentă.","Menționează o limitare.","Transformă o afirmație absolută într-o formulare mai precisă."]}
})

add("C2","ro-c2-unit-1",{
"grammar":{"title":"Pragmatică și nuanță","objective":"Controlează sensul implicit și registrul.","grammar":["eufemism","ironie contextuală","emfază","atenuare retorică"],"examples":["Nu este tocmai o soluție ideală.","Așa-zisa eficiență depinde de criteriul folosit."]},
"vocabulary":{"title":"Discurs și precizie","objective":"Alege expresii cu diferențe fine de sens.","words":[("subtext","subtext","Subtextul mesajului este important."),("nuanță","nuance","Există o nuanță importantă."),("retoric","rhetorical","Întrebarea are un rol retoric."),("ambiguitate","ambiguity","Ambiguitatea poate fi intenționată.")]},
"reading":{"title":"Sensul implicit","objective":"Interpretează intenția și efectul stilistic.","text":"Autorul nu contestă direct propunerea; în schimb, enumeră consecințele și încheie cu observația că «experiența ne va lămuri». Formula pare neutră, dar în context poate transmite scepticism.","questions":["Cum este exprimată critica?","Ce sugerează ultima formulare?"]},
"listening":{"title":"Ton și intenție","objective":"Identifică sensul pragmatic.","transcript":"Sigur, putem considera că planul este «perfect» — mai ales dacă nu ne interesează costurile. În acest context, formularea sugerează ironie.","questions":["Este vorbitorul aprobator?","Ce indică ironia?"]},
"speaking":{"title":"Controlul nuanței","objective":"Adaptează formularea la intenție și registru.","prompt":"Vorbește 2-3 minute despre aceeași opinie în registru neutru, diplomatic și ironic.","phrases":["O formulare mai precisă ar fi...","Nu rezultă neapărat că...","În acest context..."],"examples":["O formulare diplomatică poate evita critica directă și poate pune accentul pe consecințe."]},
"writing":{"title":"Analiză pragmatică","objective":"حلّل المعنى الضمني والأثر الأسلوبي باللغة الرومانية.","prompt":"Scrie 300-350 de cuvinte despre modul în care contextul schimbă interpretarea unei afirmații.","guidance":["Distinge sensul literal de cel implicit.","Analizează registrul și tonul.","Folosește exemple în limba română."],"examples":["La nivel literal, afirmația pare neutră; pragmatic, contextul îi modifică interpretarea."]},
"review":{"title":"Recapitulare: pragmatica","objective":"Consolidează controlul tonului și al sensului implicit.","questions":["Explică diferența dintre sensul literal și cel implicit.","Reformulează o critică directă diplomatic.","Identifică un exemplu de ironie contextuală."]}
})

def get_lesson_seed(level: str, unit_id: str, lesson_type: str) -> dict[str, Any] | None:
    return S.get((str(level).upper(), str(unit_id), str(lesson_type)))
