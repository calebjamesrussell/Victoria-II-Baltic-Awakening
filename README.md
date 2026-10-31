# Baltic Awakening

A flavor and content mod for Victoria II focused on Estonia, from the 1836 start through the game's end. Everything is built on Heart of Darkness expansion engine and has been audited for stability against a clean game installation.

Content includes a historically accurate literacy start and dozens of decisions and events spanning the whole era: the national awakening (the Kalevipoeg, the song festivals, the Students' Society, the Land Reform), the Soomusrong armored train and its own unit type, and the young republic (the Kroon and Eesti Pank, the Kaitseliit and the Narva Line, the Treaty of Tartu). Estonia can also form the United Baltic Duchy through vanilla's cultural-union mechanic, and every decision and event applies to it as well.

To install, copy the `Baltic_Awakening` folder and the `Baltic_Awakening.mod` file into your Victoria II installation's `mod` folder, then activate the mod in the launcher. See the [releases](https://github.com/calebjamesrussell/Victoria-II-Baltic-Awakening/releases) page for downloadable versions.

## Playing with an AI advisor

`tools/vic2_advisor.py` turns a save file into a game-state brief you can paste into Mistral Large 4 (Le Chat or the Mistral API) for advice, and lists the mod's decisions available to your nation:

```
python tools/vic2_advisor.py "Documents/Paradox/Victoria II/savegames/autosave.v2" --format prompt --ask "What should I prioritize?"
python tools/vic2_advisor.py savegame.v2 --out brief.md --watch   # refresh as you play
```

It is read-only and never modifies your saves. Run `python tools/vic2_advisor.py --selftest` to verify the parser.

## Credits

- Main menu background: Mistral AI-generated original artwork in the style of a 19th-century Baltic seascape painting, created for this mod. No third-party copyright applies.
- Decision and event art: some are 19th century photos taken from Wikimedia Commons; others are created for this mod and filtered to match the sepia tone of Victoria II's own event art. No third-party copyright applies.
