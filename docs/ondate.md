# Le ondate

Ogni ondata è un blocco di `mods/W*.yml`. Si apre la successiva **solo quando**
l'attuale passa i quattro controlli qui sotto.

## I quattro controlli (valgono per ogni ondata)

1. **Si avvia** — il client arriva al menu principale senza crash.
2. **Si connette** — il server accetta due client contemporaneamente.
3. **Si gioca** — 20 minuti reali: un dungeon, un combattimento, un salvataggio.
4. **Il log è pulito** — nessun `Missing or unsupported mandatory dependency`,
   nessun mixin fallito, nessun crash di worldgen.

Se un controllo fallisce, si torna indietro di una ondata non si "aggiusta dopo".

---

## W0 — Ossa

> Senza queste non c'è gioco. Nessuna di queste è divertente, tutte sono obbligatorie.

- **Librerie**: quelle che servono alle ondate successive (si aggiungono man mano)
- **Anti-crash**: `SerializationIsBad`, `Neruina`, `Crash Assistant`
- **Performance**: `Embeddium`, `Oculus`, `Ferrite Core`, `Modern Fix`, `Entity Culling`,
  `Krypton Reno` (*uno solo* dei Krypton), `Distant Horizons`
- **Correzioni**: `AttributeFix`, `Max Health Fix`, `EMF`, `ETF`
- **Interfaccia**: `Controlling`, `Keybind Purger`, `Default Options`, `Jade`, `JEI`

**Uscita**: gioco avviato, interfaccia leggibile, nessun crash all'avvio.

---

## W1 — Mondo

Tutto ciò che ti dà un posto dove andare.

- **Overworld**: `William Wythers' Overhauled Overworld`, `Terralith`, `Tectonic`
- **Nether**: *una sola* overhaul — `Incendium` (boss) *o* `Jaden's Nether` (bellezza)
- **End**: *una sola* — `Eldritch End` *o* `End's Phantasm` *o* `BetterEnd`
- **Aether**: `The Aether` + `Aether Villages` + `Deep Aether` + `Aether Redux`
  - richiede `AeroBlender`, `Nitrogen`, `Cumulus`
  - *Redux* chiede in più `Advanced Tooltips`, `Aether Gravitation`, `TerraBlender Fix`
- **Twilight Forest**
- **Bumblezone**
- **Deeper and Darker**
- **Undergarden**
- **Alex's Caves** (+ `Citadel`)
- **Strutture**: `YUNG's` (tutte) + `When Dungeons Arise` + suite `Integrated` + `Lootr`
- **Biomi**: `TerraBlender`

**Uscita**: un mondo nuovo si genera, il portale dell'Aether si accende, i dungeon
compaiono. Nessun buco di chunk.

---

## W2 — Mani

- **Epic Fight** + le sue patch (raccordi, non mod: stanno insieme)
- **Simply Swords** + `Simply More` + `Simply Bows` — la base
- **Marium's Soulslike Weaponry** — il sapore souls
- **Parry / off-hand / dodge**: una per funzione, non tre
- **Curios** + `Artifacts`

**Uscita**: si mena una spada, si para, si schiva. I danni si vedono.

---

## W3 — Arte

Tre pilastri, non sei.

1. **Iron's Spells 'n Spellbooks** + gli addon scelti (non tutti e 17)
2. **Ars Nouveau** + gli addon scelti
3. **Occultism** (summoning) — richiede `Modonomicon`

`Goety` resta fuori da questa ondata: fa già ciò che fa Iron's, ma più oscuro e con un
secondo albero di ricerca. Da valutare per una W3.5 se i tre pilastri reggono bene.

**Uscita**: si lancia un incantesimo di Iron's, si crea un glifo di Ars, si evoca un demone.

---

## W4 — Bestie

10-12 mod di boss, non 20. Accoppiate alle dimensioni.

- `Cataclysm` + 1 addon
- `Mowzie's Mobs`
- `Bosses of Mass Destruction`
- `EEEAB's`
- `Born in Chaos`
- `Meet Your Fight`
- `Wither: Reincarnated`
- i boss "di frontiera" che chiudono una progressione

**Uscita**: il primo boss è battibile al livello giusto e non oneshot al primo minuto.

---

## W5 — Sé

- `Skill Tree (RPG Series)` + gli 8 addon di classe
- `Just Leveling`
- `Passive Skill Tree` + `Mob Kill Points` *(fragile: provare in questa fase)*
- `Tierify Reforged`
- `Yet Another Gravestone` + `Hardcore Revival`
- `BN Blood Particles`

**Uscita**: si guadagna un punto, si spende, si muore, si torna alla tomba.

---

## W6 — Casa

- `Farmer's Delight` + addon
- `Supplementaries` (+ `Moonlight Lib`)
- `Tom's Simple Storage`
- `Create` (+ `Flywheel`) — se resta: è tech *soft*, ammessa dallo stile
- decorazioni: `Macaw's`, `Another Furniture`, `Handcrafted`

**Uscita**: si costruisce una casa che non fa schifo e si cucina qualcosa.

---

## W7 — Vita

- `Simple Voice Chat`
- mappa: `JourneyMap` *o* `Xaero's`
- claim: `FTB Chunks` (se si usa FTB) *o* alternativa leggera
- backup periodici
- `FTB Quests` come sistema di obiettivi **unico**
- `Patchouli` + una guida scritta da noi

**Uscita**: tre persone giocano una serata intera, si parlano, nulla si perde.
