# Versioni di riferimento

Questa non è la lista delle mod (quella è in `mods/*.yml`): è il **contesto tecnico**
in cui quelle mod devono stare. Serve per non scoprire a Fase 3 che una mod chiede
una versione di Forge che non abbiamo.

| Componente | Versione | Note |
|---|---|---|
| Minecraft | **1.20.1** | fissata. Non si aggiorna: cambierebbe tutto il pack. |
| Forge | **47.4.14+** | minimo. Le mod dichiarano `47.2.0+`, `47.3.x`: 47.4.14 copre tutte. |
| Java | **17** | obbligatorio per 1.20.1. Java 21 non serve e alcune mod non partono. |
| RAM client | 8 GB dedicati | Embeddium + Ferrite Core abbassano il fabbisogno reale. |
| RAM server | 8-10 GB | per 3 giocatori con ~230 mod. |

## Da decidere in Fase 1

Queste sono le scelte che **non** ho potuto chiudere senza aprire i progetti
(da qui non ho accesso a CurseForge/Modrinth: la rete della sandbox arriva solo a GitHub):

- **Overhaul del Nether**: `Incendium` (boss) oppure `Jaden's Nether` (bellezza).
  Nel repo è dentro `Incendium`, ma è la scelta più facile da ribaltare.
- **Overhaul dell'End**: `Eldritch End` (nel repo) oppure `End's Phantasm` o `BetterEnd`.
- **Mappa**: `JourneyMap` (nel repo) oppure `Xaero's`.
- **Addon Iron's**: massimo 3, da scegliere fra i ~17 della lista originale.
- **Addon Ars**: massimo 2, da scegliere fra gli ~11.
- **Addon Farmer's Delight**: massimo 2.

## Le 33 voci marcate `check`

Non sono "forse": sono **da aprire e confermare**. Ognuna ha un motivo scritto nel
campo `why`. Le più a rischio:

| Mod | Rischio |
|---|---|
| `Graveyard` | la versione Forge 1.20.1 va verificata: è nata Fabric |
| `Passive Skill Tree — Mob Kill Points` | l'autore dichiara multiplayer non funzionante di default |
| `Mowzie's Mobs` | va confermata la build 1.20.1 |
| `Terralith` + `Wythers` insieme | possono saturare i biomi: provarli da soli prima |
| `Nitrogen` / `Cumulus` | dipendenze della famiglia Aether, versioni da confermare |
