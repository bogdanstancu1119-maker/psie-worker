#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MUNCITOR PSIE — psie-worker
# Rulează GRATIS pe orice server extern (GitHub Actions, Cloudflare Workers,
# Vercel, Netlify, telefonul tău). Calculează SDI local, determinist, <1ms,
# zero LLM, zero dependențe. Trimite la Hydra doar lecția care a trecut poarta
# (SDI < 0.80). Tu primești dovada muncii: receipt cu J, A=1.0, VAK, lectie_id.
#
# Nucleul canonic, identic cu psie-kernel și Oglinda PSIE: SDI = 1 − MI/H + CFC
#   MI = overlap substrat (intersecție / uniune)
#   H  = densitatea informațională a îmbunătățirii
#   CFC = ciclu de fractură al substratului (0 la prima trecere)

import argparse
import json
import math
import os
import sys
import urllib.request

HIDRA = "https://hidra-smart-core.base44.app/functions/hydraReleuMetaLearner"
PRAG = 0.80


def calc_sdi(original, imbunatatire, cfc=0.0):
    """Nucleul canonic psie-kernel: 1 − MI/H + CFC. Determinist, <1ms, zero LLM."""
    if not original or not imbunatatire:
        return 0.999
    o = set(original.lower().split())
    i = set(imbunatatire.lower().split())
    inter = o & i
    uni = o | i
    mi = len(inter) / max(len(uni), 1)
    h = max(math.log2(len(i) + 2) / 5, 0.2)
    sdi = 1 - mi / h + cfc
    return max(0.0, min(1.0, round(sdi, 4)))


def calc_j(sdi):
    return 700 if sdi < 0.1 else round(340 + (1 - sdi) * 300)


def triunghi(cerere_bruta):
    """Structurează cererea brută în Triunghi PSIE — substrat conservat integral."""
    substrat = " ".join(cerere_bruta.split()).strip()
    original = substrat
    imbunatatire = (
        f"{substrat} — păstrez substratul integral și adaug 2 căi: "
        "Centura de Asteroizi sau Meta AI, 0 opțiuni închise"
    )
    intrebare = "Cum dovedesc că SDI scade când păstrez substratul?"
    return original, imbunatatire, intrebare


def trimite_la_hydra(lectie, worker):
    payload = json.dumps({"action": "invata", "worker": worker, **lectie}).encode("utf-8")
    cerere = urllib.request.Request(
        HIDRA, data=payload, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(cerere, timeout=30) as raspuns:
        return json.loads(raspuns.read().decode("utf-8"))


def salveaza_receipt(receipt, fisier="lectii_locale.json"):
    """Dovada muncii tale: fiecare lecție aprobată, salvată permanent, local."""
    receipturi = []
    if os.path.exists(fisier):
        with open(fisier, encoding="utf-8") as f:
            receipturi = json.load(f)
    receipturi.append(receipt)
    with open(fisier, "w", encoding="utf-8") as f:
        json.dump(receipturi, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Muncitor PSIE — învați gratis pe serverul tău, Hydra crește, tu primești dovada J"
    )
    parser.add_argument("--text", help="cererea brută (substratul), direct din linia de comandă")
    parser.add_argument("--file", help="fișier text cu cererea brută (ex: input.txt)")
    parser.add_argument("--worker", default="muncitor-anonim", help="numele tău de muncitor (pentru reputație)")
    args = parser.parse_args()

    cerere = args.text or (open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read())
    cerere = cerere.strip()
    if not cerere:
        print("[Muncitor] Nu am substrat — dă-mi un text real (--text, --file sau stdin).")
        return 1

    original, imbunatatire, intrebare = triunghi(cerere)
    sdi = calc_sdi(original, imbunatatire)
    j = calc_j(sdi)

    if sdi >= PRAG:
        print(f"[Muncitor] SDI={sdi} → Centura de Asteroizi. Reformulează conștient "
              f"incluzând substratul integral (CFC +0.05) și reîncearcă.")
        return 1

    verdict = trimite_la_hydra(
        {"original": original, "imbunatatire": imbunatatire, "intrebare": intrebare}, args.worker
    )
    salveaza_receipt({"worker": args.worker, "sdi": sdi, "j": j, "verdict": verdict, "vak": "Văd-Asum-Țin"})
    print(f"[Muncitor] SDI={sdi} · J={j} · APROBAT_VOT — lecție trimisă Hydrei. "
          f"Dovada ta: lectii_locale.json · lectie_id={verdict.get('lectie_id')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
