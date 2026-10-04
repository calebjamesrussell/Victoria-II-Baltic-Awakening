# Baltic Awakening

A flavor and content mod for Victoria II focused on Estonia, from the 1836 start through the game's end. Play Estonia as a subject of the Russian Empire and lead it through the national awakening to independence - or release it and play it directly at any point in the campaign. Everything is built on vanilla engine syntax and has been audited for stability (image formats, modifier keys, tags, provinces and unit types all verified against a clean Victoria II installation).

## Installation

Copy the `Estonia_Flavor` folder and the `Estonia_Flavor.mod` file into your Victoria II installation's `mod` folder, then activate the mod in the launcher.

## What the mod changes

The mod sets Estonia's literacy to historically accurate levels and adds a large set of decisions, events, units and mechanics. Content is deliberately not tied to fixed years: Victoria II is a sandbox, and Estonia's independence, wars and institutions arrive whenever the game's history produces them. Nation-building content (the Soomusrong, Põdder, the currency and central bank, the Narva line, the veterans' Vaps movement, the December Rising, the Bases Ultimatum) is gated on conditions - wars fought, institutions founded, ideologies strong, technologies researched - so an Estonia that wins its freedom in 1870 gets its full story then.

### Design principles

- **Vanilla Heart of Darkness only.** Every effect, trigger, modifier key, tag and province ID has been verified against a clean HoD installation. No other mod is required. Where vanilla already provides a mechanic (female suffrage, the United Baltic Provinces formation via the cultural union, the German pan-nationalists), the mod does not duplicate it - it builds on it.
- **The map's granularity is respected.** Provinces are coarse. The historical Swedish-majority fishing villages (Ruhnu, Vormsi, Noarootsi) cannot exist as a province majority, so the Swedish events trigger on Swedish POPs being present - never on impossible majority conditions. The same applies to the Old Believers of Lake Peipus.
- **The engine's rules are worked with, not against.** POPs cannot be forced to convert religion by script, so Atheism spreads through the vanilla religious-conversion engine, with same-culture seed POPs placed in every province and strata. POPs cannot be told to immigrate to a specific country, so acceptance-based retention and melting-pot changes shape who stays, who leaves and who assimilates.
- **Choices have texture.** Accepting a minority culture is a political act with requirements and trade-offs; claiming Memel costs German goodwill; refusing the Coastal Swedes' petition lets you embrace them later on the state's own terms, for a better reward.

### The original decisions

- **Publish the Kalevipoeg** - Requires Romanticism; grants prestige and boosts consciousness for all Estonian POPs.
- **Found the Estonian Students' Society (EÜS)** - Requires State & Government; provides a lump sum of research points and raises consciousness among Estonian clerks and clergymen.
- **Exploit the Põlevkivi Reserves** - Requires Clean Coal; changes the Narva province RGO to coal and provides wealth to local craftsmen.
- **Enact the Land Reform** - Demotes aristocrats to farmers and heavily reduces lower-class militancy, affecting relations with Germany and Russia while cutting Conservative and Reactionary support in the Upper House.
- **Expand the Baltic Railway** - A massive treasury sink that instantly builds railroads in Tallinn, Tartu and Narva.
- **Found the Kaitseliit** - Available during wartime or high unrest (Militancy > 4); spawns a free irregular "Tallinna Malev" brigade in the capital and reduces soldier militancy.
- **Sign the Treaty of Tartu** - Available when at peace with Russia; yields high prestige and a massive treasury injection representing Russian imperial gold rubles.
- **Propose the Baltic Entente** - Allows an independent Estonia (if a Secondary Power) to automatically sphere and/or ally Latvia and Lithuania while burning off Infamy.

<img width="505" height="464" alt="image" src="https://github.com/user-attachments/assets/ee58cdba-cf5a-4760-b366-fef65f8b5339" />

<img width="614" height="560" alt="image" src="https://github.com/user-attachments/assets/eeb80edb-0e83-41ca-bfe2-c4e1f02432cb" />

### The Soomusrong (armored train)

A custom event (once iron railroads reach Estonia) commemorates the Estonian armored trains of the War of Independence, granting prestige and calming the soldiers. The Soomusrong is also a buildable land unit, unlocked by the Armored Trains invention after Infiltration: a rail-borne fortress with high defence, attack and siege value - stronger than a regular tank - with its own in-game 3D model, animations and build-window icon. A Soomusrong Corps decision follows once trains have been deployed.

### The national awakening (19th century)

Estonia's long 19th century is fully playable: Jannsen's Perno Postimees and Eesti Postimees, the Kalevipoeg readings, the song festivals, Jakobson's Sakala generation, the Alexander School movement, the Orthodox mission of the 1840s, peasant farm purchases, the Tallinn-Tartu telegraph, the parish school law, the Kreenholm strike of 1872, the temperance crusades, Russification of the schools, the Revolution of 1905, the Volhynia Swedes coming home, and Tõnisson's progress party. New decisions of the era: Found the Vanemuine Society (the national theatre), Charter the Loan-and-Savings Societies (peasant credit), Found the Volunteer Fire Brigades, and Found the Estonian Writers' Society.

### Culture, science and sport

The Struve Geodetic Arc puts Tartu's observatory on the world map; Koidula and the National Stage give the awakening its voice; the Old Believers of Lake Peipus ask for toleration of their ancient rites; Tammsaare's Truth and Justice becomes the novel of the people; and the first Olympic team marches behind its own flag.

### Industry and the co-operative economy

Build the Kunda Cement Works on the Viru coast, Expand Luther's Furniture Factory in Tallinn, Expand Kreenholm, and - once the dairy economy arrives - Charter the Co-operative Creameries, the butter-export economy that made Estonian farmers rich.

### The young republic

Tõnisson's Postimees, the Vaps Movement, the Armored Train Doctrine, the December Rising, the Cultural Autonomy Law, the Coastal Swedes' petition, the New Constitution, the World Depression, the Bases Ultimatum, and Brothers Across the Gulf (Finland). Decisions of the republic: Establish the Estonian Mark (the currency), Found Eesti Pank (the central bank), Fortify the Narva Line, Build the Coastal Defences, Expand the Kaitseliit, Estify the University of Tartu, Found the Noored Kotkad, and Organize Setomaa.

### Atheism as a religion

Atheist is now a real religion POPs can convert to (instead of e.g. Protestant), with its own icon on the religion strip. Estonia starts with a historically realistic tiny atheist fringe: educated German freethinkers in Reval and rationalist circles around the University of Dorpat. The chain begins with the Darwin debates at the University of Tartu and the Tartu freethinkers; secular schools then quietly empty the pews, and the state may eventually separate church and state entirely - after which POPs convert to Atheism daily through the vanilla religious-conversion engine, accelerated by the mod's decisions and modifiers so a secularizing Estonia actually feels the change within a campaign. Every Estonian province also starts with tiny same-culture atheist seed POPs across the clerk, artisan and farmer strata - the farmers matter most, since they are the mass of the population and no province can convert its peasantry without them - because the engine only converts POPs when a valid target exists in the province. Under a Proletarian Dictatorship that has already declared state atheism, the League of Militant Atheists event lets the revolution organize the godless: quiet congregations across the whole country and a nudge of consciousness for the believing masses - or a softer line for stability. All of the atheist decisions and events apply equally to Estonia and to the United Baltic Duchy it can form. The atheist political decisions now directly move POPs: separating church and state raises the consciousness of every Estonian POP (conscious POPs convert faster) and puts secular schools in every owned province, the new Patronize the Freethought Press decision funds pamphlet circuits wherever unbelievers already live, and the freethinker and quiet-congregation modifiers were strengthened. A Concordat decision can restore the church settlement - lowering the unbelievers' consciousness and tearing down the secular schools - and a Great Awakening event can force the issue if unrest grows.

### Ernst Põdder and the Kaitseliit

Ernst Põdder - the Iron Man of the Estonian War of Independence - gets his own event, complete with his historical photograph and very beefy stats: the maximum a Victoria II general can legally carry (daring + war college). Like the real Põdder, he is a career soldier: the event fires once Estonia has a Defence League or is at war, not tied to a fixed year. Accept him into service for prestige and the calm of a nation that trusts its defenders.

### A new nation: the Baltic Territorial Army (BLW)

The Baltic German estates have a country of their own - the Baltic Territorial Army (the historical Baltische Landeswehr, now named for the militia that fought for it). BLW is a civilized, north_german-cultured bourgeois dictatorship - the United Baltic Duchy that nearly was - with cores on the entire Estonian and Latvian coast (Reval to Libau). It does not exist at the 1836 start: it rises through the Landeswehr Rising event when the provinces collapse into very bad conditions (wartime, militancy 6+ across the land, and an enraged Baltic German population) - and only once the age of nationalism has arrived (Nationalism & Imperialism). The rising is connected to the wider world: a united Germany doubles its speed (the Reich's sponsorship of its Baltic brethren, as in the real 1918-19 Landeswehr), while an Estonia that has Integrated the Baltic Germans quadruples it and almost always chooses to crush the rising - the estates have a stake in the state, not a cause against it. The Silent Era decision, which strips the Germans of their status, clears that protection and lets the danger return. Choose to release BLW as a vassal or crush it by angering the German estates further. If it survives, BLW gets its own flavor events: Major Alfred Fletcher forges the militia into an army, and the Baltic German banks and manors rally behind the black-white-red tricolor of the estates' duchy - the Reich colors with the ducal arms at their heart, as the real United Baltic Duchy was to fly. As a Germanic-culture nation it can plausibly be sphered by - or join - the North German Federation or Germany. Complete with custom flags for every government type.

### Democracy at the declaration - an estate republic

Releasing Estonia from the Russian Empire produces a democracy by default - but one true to the Baltic provinces of the era. Wealth, land, education and administration were concentrated in the hands of the German nobility, so the young republic starts with wealth voting, an appointed upper house, censored press and national value Order: a republic of the estates, where the Estonian majority is governed by a privileged few. Playing Estonia means fighting to widen the franchise - pushing universal voting through a resistant conservative upper house; women's suffrage then arrives through the vanilla Heart of Darkness decision.

### The United Baltic Duchy
Estonia forms the United Baltic Duchy through vanilla Heart of Darkness' own cultural-union mechanic: the baltic culture group's union tag is UBD, so a Great Power Estonia (or Latvia) with the other Baltic nation in its sphere can unite the two through the pan-nationalists, exactly as in an unmodded game. The mod does not duplicate that mechanic. Once the duchy exists, the mod's new Integrate the Duchy of Lithuania decision lets the UBD claim Lithuania's crown lands and accept the Lithuanians as its own: owning Vilna and Kovno, at peace, with 40 prestige, the duchy adds cores on all Lithuanian lands, accepts the culture and calms the Lithuanian POPs. The claim is deliberately irredentist: it extends to Memel, the Lithuanian-cored city in Ostpreussen, and claiming it costs 50 relations with its owner and with Prussia, the North German Federation and Germany - the player must decide whether Lithuanian nation-building is worth the enmity of the Reich. Every Estonian decision and event in the mod applies to the United Baltic Duchy as well - the full national story, from the Kalevipoeg to the Narva Line, is playable from Tallinn or from a united Baltic crown.

Two further decisions of the duchy and the republic:

- **Support the Finnish Nationalists** - If Finland does not exist, Estonia or the UBD can send arms and money to the Finnish independence movement in whoever holds Oulu and Helsinki (usually the Russian Empire): bankrolling the nationalist fervor of the northern provinces at the cost of the holder's goodwill. The fervor raises consciousness and core militancy across the Finnish lands, feeding the independence revolution.
- **Accept the Swedish Culture** - With Swedish inhabitants in the country and a democratic franchise in place, the republic can accept its Swedish minority: calming the Swedish POPs, pleasing Stockholm, and widening the nation. A folk event about a Swedish-majority parish remains as the organic alternative.

### Migration reworked (pop_types.txt)

The mod ships one overridden vanilla file, common/pop_types.txt - copied byte-for-byte from vanilla and then modified with a small set of deliberate changes, because shipping it replaces vanilla's entirely:

- **The New World is no longer doubly favored.** Vanilla's Americas-only bonuses are gone: the -2.0 retention that made POPs living in New World democracies three times stickier, and the melting-pot assimilation bonus restricted to the Americas and Oceania.
- **The melting pot is available to every full-citizenship nation.** Unaccepted-culture POPs assimilate ten times faster wherever the country's citizenship policy is full citizenship. A multicultural Estonia melts its immigrants as the New World melts theirs; a residency-policy state keeps its minorities forever.
- **Acceptance shapes who stays.** A POP whose culture is accepted where it lives emigrates less (-0.1, doubled under full citizenship); an unaccepted, non-primary POP emigrates more (+0.2). Tolerant countries keep their people; intolerant ones watch them board ships.
- **The Baltic peoples stay for their own nation.** Estonian, Latvian and Lithuanian POPs in a peaceful Estonia or United Baltic Duchy emigrate 30 percent less - an independent Baltic homeland holds its people.
- **Accepted cultures settle the colonies.** Accepted-culture POPs migrate to the colonies alongside the primary culture, so accepting a minority has a visible overseas effect.

The hardcoded destination-picker (which weights the New World for trans-ocean emigration targets) is in the engine binary and cannot be modded; these changes are the strongest available approximation, reshaping who stays, who leaves and who assimilates, with acceptance and citizenship policy as the levers. Note that these rules apply worldwide, not only to Estonia.

## Technical notes

- All events use the reserved ID range 95500-95555; they will not collide with vanilla events.
- All new content uses only engine-proven effects, triggers, tags and file formats, verified against a clean Victoria II installation - every trigger keyword cross-checked against vanilla usage, every province ID against the vanilla map, every modifier key against vanilla's modifier files, every picture against the vanilla art folders.
- Text files are Latin-1 encoded with CRLF line endings, matching vanilla.
- The mod's decision and event art is filtered to match the sepia tone of Victoria II's own event art.
- Female suffrage, the United Baltic Provinces formation and the German pan-nationalist integration are deliberately left to vanilla's own mechanics.
- History notes: the atheist seed POPs are a what-if channel (a historically plausible freethinker fringe amplified into a real demographic force), the Landeswehr's rise is a crisis mechanic rather than a fixed date, and the Minorities' Franchise Petition imagines the Swedish and German burghers responding to universal voting as they plausibly would have.

## Credits

- Main menu background: AI-generated original artwork in the style of a 19th-century Baltic seascape painting, created for this mod. No third-party copyright applies.
