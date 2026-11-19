# Le scelte, e perché

Questo documento esiste perché tra sei mesi qualcuno (probabilmente tu) si chiederà
"ma perché non c'è X?". La risposta deve stare scritta, non nella memoria.

---

## 1. Perché a ondate

Un pack con 230 mod non si costruisce mettendo 230 file in una cartella.
Si costruisce così: 40 file, si avvia, si connette, si gioca venti minuti. Poi 40 in più.
Poi altri 40. Se qualcosa si rompe, sai che è colpa degli ultimi 40.

L'altro modo — tutto insieme, poi "vediamo cosa non va" — produce un log di 4000 righe
in cui il crash vero è a riga 3200 e il messaggio che conta è in mezzo a 900 warning
di mixin che non c'entrano niente.

---

## 2. Le tre decisioni del gruppo

Prese in fase di revisione, restano ferme salvo ripensamento esplicito di tutti.

### Dimensioni: 8, scelte per tema — i boss restano

| Dimensione | Ruolo |
|---|---|
| Overworld potenziato | la casa, il 70% del gioco |
| Nether (una sola overhaul) | primo salto |
| End (una sola overhaul) | salto finale |
| Aether (base + Villages + Deep Aether + Redux) | la dimensione "bella" |
| Twilight Forest | il classico, progressione a boss |
| Bumblezone | la dimensione strana e verticale |
| Deeper and Darker (Otherside) | la discesa, il contrasto cupo |
| Undergarden | l'ultima, la prima da tagliare se qualcosa non gira |
| *Alex's Caves* | non è una dimensione: caverne enormi in Overworld |

**Regola del boss in esilio**: una mod può restare installata senza che la sua dimensione
si apra. Il boss si richiama in Overworld con un rituale. Vale per *Eternal Starlight*.

**Non vale** per *Terramity* e *Advent of Ascension*: lì il boss è inseparabile dal mondo.
Fuori entrambe, per intero.

### Progressione: tre sistemi, su tre piani diversi

| Mod | Piano | Ruolo |
|---|---|---|
| **Skill Tree (RPG Series)** | classe | albero principale, fatto con il tool dell'autore |
| **Just Leveling** | crescita | 8 attitudini, passive, blocchi sugli item |
| **Passive Skill Tree** (+ Mob Kill Points) | talenti | secondo albero, punti dai kill |
| **Tierify Reforged** | *non è un livello* | qualità degli oggetti: non litiga con nessuno |

Cadono: *Mine and Slash*, *Remnants RPG Stats*, *History Stages*, *Auto Leveling*, *Runeborn*.

> **Aperto**: l'addon *Mob Kill Points* dichiara multiplayer non funzionante di default
> e non è testato dall'autore. Da provare in Fase 2. Piano B: punti via comando.

### Morte e sangue

- **Yet Another Gravestone** — unica tomba
- **Hardcore Revival** — rianimare un amico a terra
- **KeepInventory: spento.** Con la tomba accesa non ha senso: la tomba resterebbe vuota.

Cadono: *You're in Grave Dangers*, *Bonfires*, *Soul Bound Enchantment*,
*Configurable KeepInventory*.

**Sangue: `BN Blood Particles`.** Oltre 500k download, 13 tipi di particelle, fisica delle
gocce, supporto shader, aggiornata a luglio 2025. Restano solo gli effetti: nessuna
magia del sangue. Cadono *I Have Blood n' Bones* (ossi rotti + tomba = punizione doppia),
*Bleeding System* (troppo nuovo), *Blood Magic* e *Tome of Blood* (quarto pilastro magico).

---

## 3. Le esclusioni tecniche

### Fuori perché non possono stare

| Mod | Motivo |
|---|---|
| **Sinytra Connector** | ponte Fabric→Forge congelato su 1.20.1; ogni mod Fabric è "best effort" e client/server devono avere gli stessi file. Su un SMP non si regge. |
| **Voxy** | nessuna build ufficiale Forge 1.20.1: solo un fork ("Voxy Server Side Horizon") e backport non ufficiali. Al suo posto: **Distant Horizons**. |
| **[Retired] DnT End Castle Standalone** | ritirata dall'autore, non riceve fix. |
| **TFC Grooming Station** | richiede TerraFirmaCraft, che nel pack non c'è. |
| **DLSS STYLE** | non è una mod, è un preset di upscaling: va in `shaderpacks`. |
| **Iris & Oculus Flywheel Compat** | serve Oculus + Flywheel + Create. Sta solo se stanno tutti e tre. |

### Fuori perché si sovrappongono

**Spawn dei mob** — cinque mod che governano la stessa cosa si scrivono sopra a vicenda.
Restano `Mob Control` + `You Shall Not Spawn!`. Fuori: *Mob Population Control*,
*DespawnTweaker*, *Harder Spawners*.

**Difficoltà** — cinque mod che alzano lo stesso numero e non saprai mai quale ha reso
il gioco impossibile. Resta **L2 Hostility** da sola come motore. Fuori: *Difficulty
Enhancement*, *Dungeon Difficulty*, *Majrusz's Progressive Difficulty*, *Progressive
Difficulty: Chaos*.

**Quest** — tre sistemi. Resta **FTB Quests** (ha l'editor e i team di gioco).
Fuori: *Superior Quests*, *Bountiful*.

**Krypton** — `Krypton Reno` va, ma è **incompatibile** con *Krypton Reforged*, *Ceres*,
*Pluto*, *KryptonFoxified*. Se ne tiene **uno**.

**Barre dei boss** — *Enhanced Boss Bars*, *Visual Health* e la barra custom di *EEEAB's*
sono tre riscritture della stessa cosa. Una sola.

---

## 4. Le cose che non sono mod (ma servono)

| Cosa | Perché |
|---|---|
| **Damage indicators** | con Epic Fight i numeri non compaiono da soli: serve la mod che li mostra, altrimenti si combatte alla cieca. |
| **Mappa** (JourneyMap *o* Xaero's) | 8 dimensioni e dungeon enormi: senza mappa ci si perde. Una delle due, non entrambe. |
| **Claim** | in tre, senza claim, la casa dell'altro sparisce per sbaglio. |
| **Backup periodici** | con questa densità di mod, il mondo corrotto è questione di quando. |
| **Controlling + Keybind Purger + Default Options** | ~230 mod = centinaia di tasti. È il problema numero uno di ogni pack grosso. |
| **Simple Voice Chat** | in tre cambia tutto. |

---

## 5. Regola del "una sola"

Se una mod ti fa dire *"ma dai, una sola"*, chiediti se entra nei **170** (contenuto)
o nei **230** (peso). La risposta ti dice subito se stai aggiungendo qualcosa
o solo allungando la fila all'avvio.

Il pack non è piccolo: 3 pilastri magici, 8 dimensioni, 3 sistemi di progressione.
