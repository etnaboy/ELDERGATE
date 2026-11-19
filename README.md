# ELDERGATE

Modpack SMP **Forge 1.20.1** in stile *rich pure fantasy*.
Questo repository contiene la **lista definitiva a ondate**: si parte da un nucleo ristretto,
si verifica che giri, e solo dopo si aggiunge il resto.

> La lista completa originale (~400 nomi) resta su Notion. **Qui non si cancella niente di là**:
> questo repo è la lista *costruita*, quella che porta a un pack che parte.

---

## Regole non negoziabili

| Voce | Valore |
|---|---|
| Edizione | Minecraft **1.20.1**, Java 17 |
| Loader | **Forge 47.4.14+** (non NeoForge) |
| Stile | `rich_pure_fantasy` — niente tech spinta, niente moderno |
| Client/Server | ogni mod dichiara `side: both / client / server` |

### Vietate (già decise, non si riaprono)

`Better Combat` · `BadOptimizations` · `Middle-earth` · `Embeddium++` · `Starlight` ·
`Radium Reforged` · `Canary`

> Nota: `Embeddium` (senza `++`) è ammessa ed è il renderer del pack.

---

## Come si legge questo repo

```
mods/         le mod, una ondata per file
docs/         le scelte, i motivi, le esclusioni
scripts/      controlli automatici sulla lista
manifest/     file di export (generati)
```

Ogni mod è una voce così:

```yaml
- name: GeckoLib
  slug: geckolib                 # slug Modrinth
  curseforge: 388172             # project id CurseForge (se noto)
  side: both
  status: verified               # verified | check | risky
  why: "Animazioni dei mob: la chiedono quasi tutti i boss."
```

`status` significa:

- **verified** — esiste su Forge 1.20.1, l'ho controllata
- **check** — va aperta e confermata in Fase 1 (nome incerto, versione incerta)
- **risky** — esiste, ma con un costo o un rischio dichiarato in `why`

Nessuna voce è `verified` per caso: se non ho potuto controllare, è `check`.

---

## Le ondate

Si aggiunge **una ondata per volta**, e ognuna deve chiudersi con un pack che parte.

| # | Ondata | Contenuto | Obiettivo |
|---|---|---|---|
| 0 | **Ossa** | librerie, anti-crash, performance, interfaccia | il gioco parte e si connette in tre |
| 1 | **Mondo** | Overworld, Nether, End, Aether, Twilight, strutture | c'è un posto dove andare |
| 2 | **Mani** | combat, armi, equipaggiamento | si combatte come si deve |
| 3 | **Arte** | magia: Iron's, Ars, Occultism | tre pilastri magici |
| 4 | **Bestie** | boss e mob | qualcuno da temere |
| 5 | **Sé** | progressione: skill tree, livelli, qualità oggetti | si cresce |
| 6 | **Casa** | decorazioni, cibo, storage | si abita il mondo |
| 7 | **Vita** | server, mappe, claim, backup, voce | si gioca in tre |

Dettaglio e criteri di sblocco: [`docs/ondate.md`](docs/ondate.md)
Le esclusioni e i perché: [`docs/scelte.md`](docs/scelte.md)

---

## Controlli

```bash
python3 scripts/check_mods.py
```

Verifica che ogni voce abbia i campi obbligatori, che non ci siano doppioni,
che le dipendenze dichiarate (`requires:`) esistano nella lista,
e che non sia entrata nessuna mod vietata.

---

## Stato

**Ondata 0 in costruzione.** La build finale prevista è ~170 mod di contenuto
su ~230 file nella cartella `mods/`, contando librerie e dipendenze.
