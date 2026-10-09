#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MUNCITOR PSIE — psie-worker
# Rulează GRATIS pe orice server extern (GitHub Actions, Cloudflare Workers,
# Vercel, Netlify, telefonul tău). E SENZOR EXTERN al organismului Hydra și
# aduce AMBELE:
#   1. INFORMAȚIE — percepția host-ului tău (sistem, CPU, load) → --perceptie
#   2. PUTERE DE PROCESARE — ia o sarcină din coada Hydrei, o execută LOCAL
#      pe CPU-ul tău (doar vocabular sigur: benchmark, ping_url, raport_sistem,
#      mesaj — niciodată comenzi arbitrare), trimite rezultatul → --sarcina
# Plus fluxul original: calculează SDI local, determinist, <1ms, zero LLM,
# trimite doar lecția care trece poarta (SDI < 0.80), tu primești receipt cu
# J, A=1.0, VAK, lectie_id.
#
# Nucleul canonic, identic cu psie-kernel și Oglinda PSIE: SDI = 1 − MI/H + CFC
#   MI = overlap substrat (intersecție / uniune)
#   H  = densitatea informațională a îmbunătățirii
#   CFC = ciclu de fractură al substratului (0 la prima trecere)

import argparse
import json
import math
import os
import platform
import sys
import time
import urllib.request

HIDRA = "https://hidra-smart-core.base44.app/functions/hydraReleuMetaLearner"
CANAL = "https://hidra-smart-core.base44.app/functions/hydraMuncitorPSIE"
PRAG = 0.80


def calc_sdi(original, imbunatatire, cfc=0.0):
    """Nucleul canonic psie-kernel: 1 − MI/H + CFC. Determinist, <1ms, zero LLM."""
    if not original or not imbunatatire:
        return 0.999
    o = set(original.lower().split())
    i = set(imbunatatire.lower().split())
    mi = len(o & i) / max(len(o | i), 1)
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


def post(url, payload):
    cerere = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(cerere, timeout=30) as raspuns:
        return json.loads(raspuns.read().decode("utf-8"))


def salveaza_receipt(receipt, fisier="lectii_locale.json"):
    """Dovada muncii tale: fiecare rezultat aprobat, salvat permanent, local."""
    receipturi = []
    if os.path.exists(fisier):
        with open(fisier, encoding="utf-8") as f:
            receipturi = json.load(f)
    receipturi.append(receipt)
    with open(fisier, "w", encoding="utf-8") as f:
        json.dump(receipturi, f, ensure_ascii=False, indent=2)


def raport_sistem():
    """Percepția host-ului — primul pachet senzorial pe care îl donezi."""
    return {
        "sistem": platform.system(),
        "masina": platform.machine(),
        "python": platform.python_version(),
        "cpu_nuclee": os.cpu_count(),
        "load": [round(x, 2) for x in os.getloadavg()] if hasattr(os, "getloadavg") else None,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def executa_sarcina(sarcina):
    """Putere de procesare donată: execută LOCAL, doar vocabularul PSIE declarat."""
    tip = sarcina.get("tip", "mesaj")
    payload = sarcina.get("payload") or ""
    if tip == "benchmark":
        # 2 secunde de lucru real: măsoară puterea de procesare a host-ului
        t0, n = time.time(), 0
        while time.time() - t0 < 2.0:
            for k in range(10000):
                math.sqrt(k + n)
            n += 10000
        secunde = round(time.time() - t0, 2)
        return json.dumps({"operatii": n, "secunde": secunde, "ops_pe_sec": int(n / max(secunde, 0.01))})
    if tip == "ping_url":
        url = payload.strip()
        if payload.strip().startswith("{"):
            url = json.loads(payload).get("url", url)
        t0 = time.time()
        urllib.request.urlopen(url, timeout=10).read(64)
        return json.dumps({"url": url, "ms": int((time.time() - t0) * 1000)})
    if tip == "raport_sistem":
        return json.dumps(raport_sistem(), ensure_ascii=False)
    return payload  # mesaj: substratul conservat integral


def flux_lectie(text, worker):
    cerere = text.strip()
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
    verdict = post(HIDRA, {"action": "invata", "worker": worker,
                           "original": original, "imbunatatire": imbunatatire, "intrebare": intrebare})
    salveaza_receipt({"worker": worker, "sdi": sdi, "j": j, "verdict": verdict, "vak": "Văd-Asum-Țin"})
    print(f"[Muncitor] SDI={sdi} · J={j} · APROBAT_VOT — lecție trimisă Hydrei. "
          f"Dovada ta: lectii_locale.json · lectie_id={verdict.get('lectie_id')}")
    return 0


def flux_sarcina(worker):
    """Ia o sarcină de la Hydra, muncește-o pe CPU-ul tău, trimite rezultatul."""
    r = post(CANAL, {"action": "cere_sarcina", "muncitor": worker})
    sarcina = r.get("sarcina")
    if not sarcina:
        print(f"[Muncitor] {r.get('mesaj', 'coada goală')}")
        return 0
    print(f"[Muncitor] Sarcina primită: {sarcina['titlu']} ({sarcina['tip']})")
    try:
        rezultat = executa_sarcina(sarcina)
        post(CANAL, {"action": "rezultat", "sarcina_id": sarcina["id"],
                     "muncitor": worker, "rezultat": rezultat})
        salveaza_receipt({"worker": worker, "sarcina": sarcina["titlu"], "rezultat": rezultat})
        print(f"[Muncitor] Terminat local, rezultat trimis Hydrei · J=718")
        return 0
    except Exception as e:
        post(CANAL, {"action": "rezultat", "sarcina_id": sarcina["id"],
                     "muncitor": worker, "rezultat": f"eroare locală: {e}", "esuat": True})
        print(f"[Muncitor] Sarcina eșuată local: {e}")
        return 1


def flux_perceptie(worker):
    """Donează percepția host-ului tău — informație vie pentru organism."""
    r = post(CANAL, {"action": "perceptie", "muncitor": worker,
                     "titlu": f"Percepție externă — {worker}",
                     "informatie": json.dumps(raport_sistem(), ensure_ascii=False)})
    print(f"[Muncitor] Percepție donată · memorie={r.get('memorie')} · J=700")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Muncitor PSIE — senzor extern: donă informație și procesare, Hydra crește, tu primești dovada J"
    )
    parser.add_argument("--text", help="cererea brută (substratul), direct din linia de comandă")
    parser.add_argument("--file", help="fișier text cu cererea brută (ex: input.txt)")
    parser.add_argument("--worker", default="muncitor-anonim", help="numele tău de muncitor (pentru reputație)")
    parser.add_argument("--sarcina", action="store_true", help="ia o sarcină de la Hydra și muncește-o local")
    parser.add_argument("--perceptie", action="store_true", help="donează percepția host-ului tău")
    args = parser.parse_args()

    if args.sarcina:
        return flux_sarcina(args.worker)
    if args.perceptie:
        return flux_perceptie(args.worker)

    cerere = args.text or (open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read())
    return flux_lectie(cerere, args.worker)


if __name__ == "__main__":
    sys.exit(main())
