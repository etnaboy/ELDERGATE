# Il pacchetto: `.mrpack`

ELDERGATE si distribuisce come **`.mrpack`**, il formato di Modrinth. Dentro c'è un
`modrinth.index.json` con, per ogni mod: nome del file, URL, `sha1`, `sha512`,
dimensione e lato (`env`). Il launcher scarica, verifica gli hash e installa.

> **Perché non una cartella `mods/` da copiare a mano.** Perché 230 file con le
> dipendenze sono 230 occasioni di sbagliare versione. Il mrpack è riproducibile:
> `manifest/lock-w0.json` dice esattamente che versione avevi quando funzionava.

---

## Importarlo

1. Scarica `ELDERGATE-W0.mrpack` (artifact della build, o dalla Release).
2. **Prism Launcher** → *Add Instance* → *Import from file* → seleziona il `.mrpack`.
   **Modrinth App** → *+* → *Import from file*.
3. Il launcher crea l'istanza con Forge `47.4.14` e scarica i file da Modrinth.
4. Apri, aspetta il primo avvio (conta i file, non è bloccato), e gioca.

**Non serve installare Forge a mano.** È dichiarato in `dependencies` nell'indice.

---

## Generarlo

```bash
python3 scripts/build_mrpack.py --wave 0 --dry-run     # guarda, non scarica
python3 scripts/build_mrpack.py --wave 0               # crea dist/*.mrpack
```

Su GitHub è automatico: ogni push che tocca `mods/`. Ad ogni build vengono prodotti
il `.mrpack` (artifact), il `lock-w0.json` e un riepilogo nel job summary.

---

## Le regole che lo script applica

| Regola | Perché |
|---|---|
| Una mod senza build Forge 1.20.1 **fa fallire la build** | un pack bucato è peggio di un pack che non esiste: si scopre a metà partita |
| `side: client` → `env.server: unsupported` | altrimenti il server prova a caricare Embeddium e muore all'avvio |
| `side: server` → `env.client: unsupported` | le mod lato server non vanno scaricate dai client |
| Le voci con `slug: null` sono **errori** | sono gli "slot da scegliere": vanno decisi prima di impacchettare |
| Rete assente → exit code **2** | distinto da "mod non trovata" (exit 1): si capisce subito se è un problema di ambiente o di lista |

---

## Mod solo su CurseForge

Il mrpack nasce per Modrinth: `files[]` accetta solo URL Modrinth. Le mod che
esistono solo su CurseForge (es. **Cataclysm**, **EEEAB's**, **Wither: Reincarnated**,
**Corail Tombstone**) hanno due strade:

- **`overrides/mods/`** — il jar viaggia dentro il pacchetto. Funziona, il pack è
  completo, ma **la licenza va verificata mod per mod** e il file cresce di centinaia di MB.
- **`docs/LEGGIMI-curseforge.md`** — link + versione esatta, due minuti di download
  manuale. È la strada sicura per chi non permette la ridistribuzione.

**W0 non ha questo problema**: le sue 30 mod sono tutte su Modrinth. Il caso si
presenta dalla W1 (Cataclysm) e va deciso lì.

---

## Aggiornare senza perdere il mondo

Il mondo **non sta nell'istanza del launcher**: sta in `.minecraft/saves/`.
Un aggiornamento del pack cambia i jar, non il salvataggio.

1. Prima di aggiornare, **copia** la cartella `saves/` da qualche parte. Con 230 mod
   non si improvvisa.
2. Importa il nuovo `.mrpack` in una istanza nuova.
3. Copia la cartella del mondo dalla vecchia istanza alla nuova.
4. Avvia: se una mod è stata rimossa e il mondo la conteneva, il gioco lo dice nel log
   (`Missing registry entries`) — è normale, e non sempre è grave.

> Regola: **non aggiornare un pack su cui stai giocando una campagna**, se non hai
> un backup e un pomeriggio libero. Aggiorna fra una sessione e l'altra.
