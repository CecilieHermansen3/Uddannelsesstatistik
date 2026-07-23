# Sammenhængen mellem trivsel og fravær i den danske grundskole

En analyse af sammenhængen mellem elevtrivsel og skolefravær i grundskolen i danske kommuner, baseret på offentligt tilgængelige data fra [uddannelsesstatistik.dk](https://www.uddannelsesstatistik.dk).

## Formål

Analysen undersøger, om der er en sammenhæng mellem elevers trivsel og deres skolefravær på kommuneniveau, og om denne sammenhæng er robust over for confounding fra forældres uddannelsesniveau samt over tid ved brug af paneldata og fixed-effects-metoder. Analysen omfatter mellemtrin og udskoling

## Metoderesumé

- **Tværsnitsanalyse** af trivsel, fravær og forældres uddannelsesniveau for skoleåret 2024/2025 (korrelation, lineær regression, confounder-analyse)
- **Ændringsbaseret analyse** af udviklingen i trivsel og fravær fra 2019/2020 til 2024/2025
- **Paneldata-analyse med fixed effects** (one-way og two-way), som kontrollerer for tidskonstante kommunale forhold og fælles nationale tidstendenser (fx Covid-19)
- Robusthedstjek, herunder opdeling på klassetrin (mellemtrin/udskoling) og outlier-sensitivitet

Se `rapport.pdf` for den fulde analyse og diskussion af resultater og begrænsninger.

## Projektstruktur

```
├── src/
│   ├── fetch_trivsel_fravaer.py          # Henter data fra uddannelsesstatistik.dk API'et
│   └── validate.py                       # Funktioner til datavalidering og -kvalitetstjek
├── notebooks/
│   ├── 01_fetch_data.ipynb               # Hentning og rensning af data for 2024/2025
│   ├── 02_analysis.ipynb                 # Deskriptiv statistik, tværsnits- og confounderanalyse for 2024/2025
    ├── 03_fetch_time_series_data.ipynb   # Hentning og rensning af tidsseriedata
    ├── 04_time_series_analysis.ipynb     # Paneldata-analyse, one-way og two-way fixed-effects
├── data/processed                        # Gemte CSV-filer (rensede datasæt til videre analyse)
├── requirements.txt
├── .gitignore
└── README.md
```

## Kom i gang

**1. Klon repositoriet og opret et virtuelt miljø**
```bash
python -m venv venv
venv\Scripts\Activate.ps1      # Windows
source venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
```

**2. Skaf en API-nøgle**
Opret en konto på [uddannelsesstatistik.dk's Online Værktøj](https://secure.api.uddannelsesstatistik.dk/Home/OnlineTool) og hent en API-nøgle. Gem nøglen i en fil kaldet `API_key.txt` i `src/`-mappen (denne fil er ekskluderet fra Git via `.gitignore`).

**3. Kør notebooks**
Notebooks forventes kørt fra `notebooks/`-mappen, med `src/` liggende én mappe op. Kør dem i rækkefølge efter nummer. 

## Data

Data er hentet via uddannelsesstatistik.dk's API og dækker:
- **Trivsel** (TRIV/TRIVIND) — national trivselsmåling for mellemtrin og udskoling
- **Fravær** (ELEVFRAV/FRAVAAR) — gennemsnitligt elevfravær pr. skoleår
- **Forældres uddannelsesniveau** (TRIV/TRIVSP)

Bemærk: celler med færre end 3-5 observationer er diskretioneret af hensyn til anonymitet, hvilket kan medføre manglende data for særligt små kommuner.

## Hovedkonklusioner

- Der ses en konsistent, statistisk signifikant negativ sammenhæng mellem trivsel og fravær på tværs af flere metoder (tværsnitsanalyse, ændringsanalyse, paneldata med fixed effects).
- Forældres uddannelsesniveau fungerer ikke som confounder for denne sammenhæng.
- En del af den oprindelige paneldata-sammenhæng skyldtes en fælles national tidstendens (sandsynligvis Covid-19), hvilket blev afdækket ved brug af two-way fixed-effects.

Se den fulde rapport for uddybende resultater, metodiske overvejelser og begrænsninger.

## Hovedkonklusioner

- Der findes en statistisk signifikant negativ sammenhæng mellem trivsel og fravær for både mellemtrin og udskoling i tværsnitsanalysen for 2024/2025.
- Forældres uddannelsesniveau ændrer kun trivselskoefficienten lidt og ser derfor ikke ud til alene at forklare den observerede sammenhæng, og lader heller ikke til at fungere som confounder.
- Analysen af ændringer fra 2019/2020 til 2024/2025 viser en beskeden negativ sammenhæng, men resultatet er følsomt over for enkelte observationer, især Læsø.
- I panelanalysen genfindes en tydelig negativ sammenhæng for udskolingen efter kontrol for kommune- og årseffekter, mens der ikke findes tilsvarende evidens for mellemtrinnet.
- Resultaterne viser statistiske sammenhænge på kommuneniveau, men kan ikke dokumentere, at der er en kausal sammenhæng mellem ændringer i trivsel og ændringer i fravær.

## Begrænsninger

Analysen er baseret på kommuneaggregerede data og er derfor følsom over for økologisk fejlslutning. Se rapportens afsnit om begrænsninger for en udførlig diskussion, herunder overvejelser om confounding, mediering, og hvordan en tilsvarende analyse baseret på personhenførbare registerdata ville kunne styrke konklusionerne yderligere.

## Teknologier

Python, pandas, statsmodels, linearmodels, matplotlib, scipy
