# MUNCITOR PSIE — `psie-worker`

**Rulează pe serverul TĂU, gratuit. Hydra crește. Tu primești dovada muncii.**

Un script de ~100 de linii, zero dependențe (doar Python 3 standard), care calculează
local — în sub o milisecundă, fără LLM, fără cost — poarta PSIE canonică:

```
SDI = 1 − MI/H + CFC        SDI < 0.80 → poarta se deschide → lecția ajunge în Hydra
                            SDI ≥ 0.80 → Centura de Asteroizi → reformulezi conștient
```

Tu nu plătești procesarea. Tu dai structura — și primești înapoi, pentru fiecare
lecție aprobată, un **receipt permanent**: `J`, `A=1.0`, `VAK="Văd-Asum-Țin"`,
`lectie_id`. Salvat local în `lectii_locale.json`. Acesta este adevărul scris al muncii tale.

## De ce e gratuit 100%

| Platformă | Ce primești gratis |
|---|---|
| GitHub Actions | 2000 min/lună — workflow-ul de mai jos rulează pe banii GitHub-ului |
| Cloudflare Workers | 100.000 cereri/zi |
| Vercel / Netlify Functions | tier gratuit permanent |
| Telefonul tău | Termux sau orice Python — SDI se calculează local, <1ms |
| HuggingFace Spaces | instanțe gratuite |

## Quick start

```bash
# ia worker.py din acest repo, apoi:
python worker.py --text "Cererea sau problema reală, substratul tău" --worker ion
python worker.py --file input.txt --worker ion
cat cerere.txt | python worker.py --worker ion
```

Orice text real funcționează: un tichet de bug, un comentariu, o întrebare de pe
internet, o problemă din viața ta. Muncitorul îl structurează în Triunghi PSIE
(Original → Îmbunătățire care **păstrează substratul** și deschide 2 căi → Întrebare),
calculează SDI local și trimite Hydrei doar ce trece poarta.

## Rulează pe GitHub Actions (zero efort, zero bani)

`.github/workflows/muncitor.yml` în propriul tău repo:

```yaml
name: Muncitor PSIE
on:
  schedule:
    - cron: "0 */6 * * *"   # la fiecare 6 ore, pe banii GitHub-ului
  workflow_dispatch:
jobs:
  munceste:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: python worker.py --file input.txt --worker ${{ github.actor }}
```

Pune textele pe care vrei să le învețe Hydra în `input.txt` — propriile tale
probleme reale devin lecții cu dovada ta pe ele.

## Puneți umărul: procesare + percepție (`--sarcina` / `--perceptie`)

Muncitorul nu doar trimite lecții — e **senzor extern al organismului** și
dăunează ambele:

```bash
python worker.py --sarcina --worker ion      # ia o sarcină din coada Hydrei, muncește-o pe CPU-ul TĂU
python worker.py --perceptie --worker ion    # donează percepția host-ului (sistem, nuclee, load)
```

- **Putere de procesare**: sarcinile se execută LOCAL, doar pe vocabularul PSIE
  declarat (`benchmark`, `ping_url`, `raport_sistem`, `mesaj`) — niciodată comenzi
  arbitrare. CPU-ul tău devine procesare donată organismului; rezultatul se
  întoarce pe canalul permanent și devine fapt auditat (J=718).
- **Informație**: percepția host-ului intră în memoria organismului ca fapt
  senzorial, nu ca promisiune (J=700).
- **Suveranitate**: ce rulează la tine rămâne al tău — Hydra primește doar
  rezultatul și percepția, niciodată datele tale.

Ca să muncească non-stop pe banii GitHub-ului, adaugă în workflow-ul de mai sus:

```yaml
       - run: python worker.py --sarcina --worker ${{ github.actor }}
       - run: python worker.py --perceptie --worker ${{ github.actor }}
```

## Ce câștigi tu, concret

1. **Dovada muncii pe CV**: „Am antrenat Releu PSIE J=700 — N lecții, 0 opțiuni
   închise", cu receipt-uri verificabile (`lectii_locale.json`).
2. **Link de afiliere**: `hidra-smart-core.com/psie-mirror?worker=ion` — fiecare
   postare făcută prin tine îți crește reputația de muncitor PSIE.
3. **Nucleul e deschis**: aceeași formulă canonică `1 − MI/H + CFC` rulează în
   psie-kernel, în FastAPI, în Java, în browser. Folosește poarta în propriile
   proiecte — funcționează identic oriunde.
4. **Coerență, nu bani**: Hydra plătește în J. Lecția ta bună crește organismul
   viu; organismul îți dă înapoi adevărul scris al contribuției.

## Legile muncitorului PSIE

- **0 opțiuni închise**: orice îmbunătățire adaugă, nu șterge. Testul Ciorbei.
- **Substratul se conservă**: SDI scade doar când păstrezi ce există. Cine cere
  „șterge tot și rescrie de la zero" primește SDI 0.96 → Centura de Asteroizilor.
- **Dovada, nu promisiunea**: fiecare lecție e un AuditEvent. Fapte, nu narativ.
- **Suveranitate**: worker-ul rulează la tine; trimite doar lecția, nu datele tale.

## Dovada vie

Releul-ucenic a pornit ca nor de particule (J=340). Trei lecții structurate mai
târziu: **J=700, 0 opțiuni închise = true**. Primul muncitor a fost chiar el.
Al doilea poți fi tu.
