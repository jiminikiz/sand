# Falling Sands

A falling-sand toy in one HTML file, `index.html`, with no dependencies. It
installs as an app and plays offline (see "App" below).

## Materials

| Material  | Paint      | Behaviour                                                                    |
| --------- | ---------- | ---------------------------------------------------------------------------- |
| sand      | yes        | Powder. Sinks slowly through liquids.                                        |
| salt      | yes        | Powder. Dissolves in water as brine; melts ice and snow into brine, a few cells a grain. |
| seed      | yes        | Falls like sand. On sand or ash with water touching it, sprouts a stem; on ash a taller one. |
| gunpowder | yes        | Powder. Lit, it blows a hole of radius 5; the rest of a pile goes off as a ripple. |
| water     | yes        | Liquid. Puts out fire (smoke, some steam), quenches lava (obsidian, steam).  |
| oil       | yes        | Liquid, floats on water. Burns slowly; burning oil stays put and flames.     |
| acid      | yes        | Liquid. Eats what it touches, 10 bites each, except glass, clone and drain. Water dilutes it. |
| lava      | yes        | Viscous. Ignites fuel, melts sand to glass, crusts to stone doing it; froths to pumice on ice. |
| fire      | yes        | Stays on fuel and throws flames and embers; loose fire drifts up & dies. Fixed: what falls on it waits. |
| lightning | yes        | One bolt per press, from the top of the sky to the first thing under the pointer. |
| stone     | yes        | Static.                                                                      |
| wood      | yes        | Static. Catches slowly, burns long throwing embers, leaves ash.              |
| metal     | yes        | Static. Rusts in water, faster in brine. Carries lightning.                  |
| ice       | yes        | Freezes water with a limited cold budget; melts near anything hot.          |
| smoke     | no         | fire dying out or doused. Soots stone and glass darker.                      |
| steam     | no         | water meeting fire, lava or an ember. Rises, half condenses into rain.       |
| rain      | no         | steam condensing. Falls through air and gas, turns to water on landing.      |
| ash       | once found | wood or plants burnt down. Light powder: rests on sand, sinks in water.      |
| plant     | once found | seed + water on sand. Drinks touching water into more plant; spare water sprouts upward. |
| glass     | once found | lava or lightning + sand. Static; acid can't eat it.                         |
| brine     | no         | salt + water. Sinks under water, never freezes; boiled, leaves its salt.     |
| obsidian  | once found | lava + water. Static; acid barely eats it.                                   |
| ember     | no         | thrown by fire on fuel, or a blast; arcs 30–60 cells and lights fuel it lands on |
| snow      | once found | steam + ice. Falls, floats on water, melts near heat.                        |
| fume      | no         | a quarter of what acid eats goes up as this green gas                        |
| flower    | no         | top of a seed's stem: a yellow heart, one petal colour per bloom             |
| pumice    | once found | lava + ice. A powder that floats on water.                                   |
| rust      | no         | metal left in water. Powder; acid eats it readily.                           |
| hydrogen  | no         | half of the metal acid eats. Rises; lit, pops with a blast of radius 2.      |
| acid rain | no         | fume condensing. Falls like rain, lands as acid with 3 bites.               |
| cloud     | once found | steam reaching the top of the sky. Drifts, rains from its base, now and then strikes. |
| bee       | once found | a flower heart with three more within 10 cells. Gathers pollen, drips honey. |
| honey     | once found | bees carrying pollen. Thick; sinks under water and brine.                    |
| clone     | the prize  | takes the first thing that touches it, passes it to the clone beside it, pours it out. |
| drain     | the prize  | swallows anything loose that touches it.                                     |

The nineteen discoveries (`SECRETS`) are saved per browser in `localStorage`
under `sand.found`. Each has a `how` in `MAT`, shown once found. A discovery
that is also in `TOOLS` joins the materials sheet once found; until then its
tile stays out of the sheet, search included. Clone and drain join once all
nineteen are: the reward for the "every last one" achievement (below). The
rest are never paintable.

Flowers drop one seed from each petal with room under it, and a heart amid a
patch lets out one bee; each flower cell keeps what it has given in `life`.

## How the code works

- State is typed arrays over the grid: `type`, `life`, `col` (shade), `aux`,
  `clock`. `shapeGrid()` reallocates them when the stage changes size (see
  below).
- `MAT` is the one place a material is described: density, fixed or airy, its
  `act` (update per tick), starting life, how it burns, blasts, holds, etches,
  what a gas condenses into, and the recipe. The lookup tables `step()` reads
  (`dens`, `movable`, `airy`, `burn`, `etch`, `hot`, `acts`) are built from
  it. A material without an `act` is skipped.
- `life` means something different per material: how long fire, smoke,
  steam, fume, hydrogen and lightning last; plant sap; ice's cold; acid's
  bites; an ember's flight; a cloud's water; a bee's pollen; what a clone
  pours; what a flower has given. `aux` is an ember's or a bee's heading, or
  for fire whether it leaves ash.
- Discovering takes a reaction. Reactions make cells with `set()`, which
  credits a secret and counts the cell in `made`; `place()` puts a cell down
  without either. Scenes and painting place, and so does plant spreading from
  plant, so plant is discovered only by a seed sprouting, and `made` counts
  only what reactions made.
- `ignite()` lights fuel. Fuel with a `blast` is lit at once and queued; the
  blasts go off after the scan, so none moves a cell out from under the one
  acting. Gunpowder caught in a blast is only lit, and goes off a tick later
  through the fire beside it, which makes a pile ripple rather than vanish:
  4230 cells went off in 26 ticks.
- A blast flings loose cells along their line to the first open cell past
  the rim, keeps fixed ones by their `hold`, lights fuel, and leaves the hole
  mostly in short flame with embers off the rim.
- Lightning walks down from the top (or a cloud's base) through airy cells,
  within 5 columns of where it was aimed, and the whole bolt shares one
  lifetime so it goes out at once. Into sand it fuses a crooked glass tube
  (a fulgurite); into metal it runs through every joined cell, up to 4000,
  lighting fuel and boiling water along it.
- Acid's `etch` is the chance per bite of eating each material. Glass is
  missing from it on purpose: it's what you keep acid in.
- Plant sap from drinking water is 0–6. A seed sprouts with `STEM` + 6–18
  (12–30 on ash); that stem climbs, and when its sap is down to exactly `STEM`
  it blooms instead of growing. The two ranges never overlap, so one byte
  holds both.
- `step()` scans bottom-up, alternating left/right each tick. `clock[i] ===
  tick` marks a cell already moved this tick, so nothing moves twice.
- `sinks(t, j)` is the one density rule: a mover displaces anything movable
  with lower `dens`. Densities are fractional where they need to slot in:
  pumice 2.5 floats on water, brine 3.5 sinks under it, honey 3.8 under that,
  ash 4.5 rests on sand with seeds resting on it.
- The materials sheet is built from `TOOLS`: material, group, tip, and the
  share of the brush it fills (30% for loose things and fire, all for fixed
  ones, 3% for bees). Every swatch is a 6 × 6 pixel picture drawn from the
  material's own shades or palette by `swatch()`.
- Fixed 60 Hz timestep; at most three steps per frame.
- `rnd()` is a xorshift seeded from `Math.random()` on load, so every load
  starts on a different scene.

## Scenes

- `scene()` (on load, `r`, and new scene in the menu) rolls a new one: rolling sand over a thin
  bedrock, then ground pieces left to right in a shuffled order while they
  fit, then up to one ledge, stone or now and then wood, in each half of the
  sky.
- The pieces: a basin (water under oil, water under ice, or an oil tank), a
  lake dug into the ground, a stone mound with lava sealed inside, and a
  planter of dry sand with seeds on it.
  Basins and planters stand on the highest ground under them, half the time
  up on legs. Nothing on the ground rises past `SKY`, where the ledges float.
- Hints: up to two discoveries stand in a scene (none 20%, one 60%, two 20%),
  each in place of a piece of its kind. Plant is reeds in a basin of water,
  glass a jar of acid, honey a pot of it, obsidian a cap on the lava mound,
  snow lying on an iced basin, pumice a raft on the lake, ash a layer under
  the planter's seeds. Ones not found yet are three times as likely. Hovering
  one names it, and searching that name gives its recipe, so nothing has to
  call it a hint. Flower is left out: one bloom gives away the whole seed
  chain. So are bees and clouds, which would set things off.
- A scene only places cells, so a hint isn't a discovery. Nothing reacts at
  the start either, since a reaction would be: lava has 3 cells of stone on
  every side, seeds sit dry, acid comes only in a glass jar, and there are no
  flowers, metal or clouds.
- Ground waves and lake banks stay under 45°, so no sand slides at the start.
  The pumice raft's top row is a cell shorter at each end for the same reason.
- Checked in Brave: 60 scenes each at 300×180, 214×160, 158×341 and 341×158
  cells, 300 ticks apiece, with hints: no secret made, nothing changed but
  water turning to ice or plant. 2000 scenes at 300×180 gave none 21%, one
  59%, two 21%. A placed plant watered for 1200 ticks grew and stayed
  undiscovered; seeds on wet sand still discovered it.

## Layout

- Full window, laid out at 640 × 480 or more. A smaller window (a phone, a
  zoomed-in browser) gets the app laid out at 640 × 480 and scaled down to
  fit by `fitApp()`, which sets `--fit`, rather than scrolled. The canvas
  fills all of it, with no margin or border.
- The canvas runs under notches and camera cutouts (`viewport-fit=cover`).
  The rail, sheets and overlays sit in `.safe`, inset by
  `env(safe-area-inset-*)` divided by `--fit`.
- One UI for desktop and touch, built for a tablet first: a rail down the
  left (64 px before `--ui`) and sheets that open beside it. From the top:
  menu, the material slots, "all", then erase, brush size and pause. The
  sandbox gets the rest of the width, and scenes are laid out right of the
  rail.
- The slots hold the materials picked last, and each keeps its place: a
  material picked from the sheet, if it isn't on the rail already, takes the
  slot used longest ago. As many show as fit, up to nine (keys 1–9). Below
  640 px of rail the slot names go, so a phone in landscape gets four slots
  instead of two. Kept in `sand.slots`.
- Sheets open one at a time beside the rail. A tap on the sandbox, Escape or
  × closes one, and that tap pours nothing.
  - Materials ("all", or `/` with the search focused): a search box, the
    paintable materials as tiles in groups (powders, liquids, fire and sky,
    solids, living, prizes) with their tips, then the discoveries and the
    achievements, each with a count. A material that unlocks, or an
    achievement earned, puts a dot on "all" until the sheet opens, and its
    tile or row flashes.
  - Menu: new scene, clear, install (while offered), ui size, help, footer.
  - Size: four brush widths on screen, 6, 14, 28 and 56 px; the wheel and
    `[ ]` step between them. The rail's size button shows a dot to match.
- Erase is a mode on the rail (`e`); picking a material ends it. Right-drag
  still erases with a mouse. The brush ring turns red while erasing.
- New scene and clear keep the world they replace. The toast they pop has an
  undo button for 8 s, and ctrl or ⌘ z works after that, as long as the grid
  is the same size.
- Keys: 1–9 slots, `/` find a material, `e` erase, space pause, `r` new
  scene, `c` clear, ctrl or ⌘ z undo, `[ ]` brush, `- =` ui size, Escape
  closes a sheet. Materials no longer have letters of their own: there were
  too many to remember, and search finds any of them by name.
- UI size (`-` / `=`, or − + in the menu) scales the rail, sheets, strip and
  toast through the `--ui` CSS variable, using `transform: scale`. Until the
  player picks, it follows the layout: 100% up to 900 px tall, up to 125%
  above that. Clicking the percentage goes back to automatic. Kept in
  `sand.ui`.
- Search filters the materials sheet by name and description. Enter picks
  the first tile left, Escape clears, then closes. A discovery not yet made
  only shows when searched by its exact name, and then shows its recipe.
- What's under the brush (for a clone, what it pours) shows in a strip at
  the bottom right while a pointer is over the sandbox, with pause; the strip
  hides when there's nothing to say. Discoveries pop a toast at the top.

## Screens and touch

- The grid fills the stage with cells of 3 layout px or more, as many as fit
  up to `MAX_CELLS` (54,000). Measured: 640×480 gives 213×160 at 3 px per
  cell, 900×700 gives 263×205 at 3.4 px, 1280×960 gives 268×201 at 4.8 px.
- When the stage changes size, `shapeGrid()` runs once the resize settles
  (150 ms) and builds a new grid. Content keeps its place from the bottom
  left; whatever no longer fits is lost. Above about 800×600 the cell count
  is at the cap, so resizing mostly rescales cells: 1280×960 down to 900×700
  and back kept 99% of a scene. Until then the canvas stretches, and cells
  can end up a hair off square.
- `scene()` is drawn on a 300×180 plan, scaled evenly to fit right of the
  rail and standing on the bottom edge, with walls kept 3 cells thick. The
  ground runs the full width. In portrait that leaves open sky above.
- `pointers` holds one stroke per finger, so several fingers pour at once.
  The starting brush is the size sheet's 14 px, whatever the cell size.
- Every button is at least 44 px tall; rail buttons are 58 (44 on a short
  rail). Touch screens (`hover: none` and `pointer: coarse`) only lose the
  key labels and get their own help lines.
- A Pixel 8 running the installed app gave the page only about 528 × 247 CSS
  px in landscape, likely from zoom or a large display size. The first
  layout overflowed it: the panel filled the view and the canvas sat off
  screen. A viewport-tag fix was tried next, but it relied on `screen`,
  which zoom skews, and desktop browsers can't test it; scaling the app in
  script replaced it.
- Checked in Brave at 640×480, in iframes resized between 900×700 and
  1280×960, and at 528×247 and 247×528. At 528×247 the app lays out at
  1026×480, scaled by 0.51, and a drag pours under the pointer. Not yet seen
  on the phone itself.
- The rail, checked in Brave in iframes: 1180×820 (an iPad in landscape)
  shows 8 slots, 820×1180 shows 9 at 125%, 1024×768 shows 7, and 844×390 (a
  phone in landscape, scaled to fit) 4 on a short rail. A tap on the sandbox
  with a sheet open closed it and changed no cell; the next tap poured. Not
  yet tried with real touch on a tablet.

## App

- `manifest.webmanifest`: name, fullscreen display (no status or navigation
  bar on phones; desktop falls back to a window), dark theme, icons. All
  paths are relative, so it works served from any subfolder.
- `sw.js` is network first: online, every file comes fresh and refreshes the
  cached copy; offline, the copy. There's no stale version to wait out after a
  change. Bump `CACHE` only when the `SHELL` list changes.
- Service workers need https, or `localhost` / `127.0.0.1`. Opened straight
  from disk (`file://`) the game runs fine, just without offline or install.
- An "install" button joins the menu only while the browser offers
  installation (`beforeinstallprompt`: Chromium browsers). Safari installs
  from Share → Add to Home Screen, using `apple-touch-icon.png`.
- Icons are pixel art drawn by `scripts/make-icons.py` (standard library
  only): a sand pile under a falling stream, with a flower. The maskable one
  shrinks the art into the safe circle and runs the sand out to the edges.
  Change `ART` and rerun it.
- Checked in Brave on `127.0.0.1`: the worker registers and controls the page,
  all seven files are cached, the install offer arrives, and with the server
  stopped a reload still loads and runs.

## Tuning that mattered

- `burn[OIL]` was 0.5 at first and the whole oil layer went up in 1.5 s and
  floated away. At 0.06, with fuelled fire staying put, a burn front creeps
  across for about 5 s.
- `EMBER_RATE` 0.004 gave one or two embers in the air; 0.03 gives about 15 on
  a big fire.
- Painting happens in pointer events as well as the frame loop. Without that,
  a fast drag paints nothing.
- A seed on wet sand sprouts at 2% a tick; a bed of them shows its first
  flower about 4 s in.
- Acid at 10 bites: 25 × 24 cells of it ate through a 3-cell stone bowl and
  a whole sand floor in 30 s. The same acid in a glass jar stayed put.
- Fire was movable at first, so the ash a burning wood block made sank
  through its flames and lifted them off the wood: a 41 × 30 block stalled
  after about 160 cells, every time. Fire is fixed now, so ash (or sand)
  piles on a flame until it burns out, and the same block burns through in
  under 20 s. Wood catches at 0.02 a tick, so a single spark on it still
  fails about a third of the time.
- Clouds first rained only from their bottom row, so a big painted one rained
  for minutes. Water now settles to the base, which darkens, and rains at
  1.2% a tick per base cell: a 31 × 11 cloud rains out in about 65 s.
- A cloud cell strikes with a chance of 0.000002 × its water a tick: a giant
  cloud every second or so, a brush-sized one every few seconds.
- Bees with 20 pollen to a drop and a 2% drip made 21 honey cells in 200 s
  from five bees. At 12 and 5%, with twice the glancing for flowers, a bed of
  43 seeds gave its first bee at about 21 s and 19 bees and 113 honey cells
  by 130 s.
- Metal in water shows its first rust in about 4 s; a 11 × 21 plate had lost
  a quarter of itself in 100 s.
- A full 54,000-cell scene steps in 0.22 ms and renders in 0.14 ms.

## Achievements

Seventeen, listed in the materials sheet under the discoveries and saved per
browser in `sand.achieved`. Earning one pops a toast, or joins the toast of
the discovery that earned it.

| Achievement      | Goal                                                       |
| ---------------- | ---------------------------------------------------------- |
| halfway          | make 10 of the 19 discoveries                              |
| every last one   | make all 19; clone and drain join the materials            |
| chain reaction   | 25 blasts within a second                                  |
| firestorm        | 1,500 cells burning at once                                |
| demolition       | blast away 1,000 cells of stone                            |
| storm            | a cloud strikes on its own                                 |
| lightning rod    | a bolt runs through 200 cells of metal and lights something |
| glassblower      | make 1,000 cells of glass                                  |
| salt flats       | boil brine down to 200 grains of salt                      |
| shipwreck        | rust 100 cells of metal                                    |
| green thumb      | 30 flowers in bloom at once                                |
| beekeeper        | 12 bees at once                                            |
| sweet tooth      | bees make 300 cells of honey                               |
| full palette     | 20 different materials on screen at once                   |
| perpetual motion | a drain swallows 1,000 cells while a clone pours           |
| second thoughts  | secret: undo a clear or a new scene                        |
| rainbow          | secret: the ↑ ↑ ↓ ↓ code                                   |

- The rule is the one discoveries follow: an achievement needs the player.
  Nothing a scene does on its own may earn one, so counts of what's made come
  from reactions only (`made`), and "at once" thresholds sit well above what
  a scene places. Freezing water was left out for that reason, since the ice
  basins in scenes do it unasked; so was anything timed.
- The ones with a `test` are checked twice a second of play (every 30 ticks,
  from the frame loop) against `census()`, which counts what's on screen, and
  against `made` and `feats`, which the simulation keeps: the most blasts in
  any second, stone blasted, clouds striking, the longest run of metal a bolt
  lit something through, and cells drained. Those counts start at zero each
  load. Undo and the code are earned where they happen. On load, any already
  due (halfway, every last one) are earned quietly.
- Checked in Brave, each from a fresh start: a gunpowder pile on a stone floor
  made 374 blasts in a second (chain reaction) and blasted 374 stone, so
  demolition went from 300 to 1,000; seams of gunpowder in stone blasted
  6,147. An oil pool lit along its top burned 1,683 cells at once. A painted
  cloud struck on its own 17 times in 30 s. A bolt down 240 cells of metal set
  off gunpowder at the foot. Brine over lava gave 300 salt, metal in brine 514
  rust in 30 s. Twenty materials side by side made full palette, and a clone
  of water over a drain swallowed 9,427 cells in 40 s. A bed of 68 seeds gave
  green thumb within 25 s, beekeeper within 50 s and sweet tooth by 150 s.
- Glass: lava poured on flat sand glazes one row of it, and the glass shields
  the rest, so a pour 300 cells wide makes exactly 300, however much lava
  follows. Sand poured into a pool of lava sinks through it and keeps melting:
  1,131 glass in 20 s. That's the trick glassblower asks for.
- 60 scenes at each of four sizes, run 300 ticks and checked as play would:
  no achievement, no discovery, and at most 9 materials on screen at once.

## Easter eggs

- ↑ ↑ ↓ ↓ ← → ← → b a toggles rainbow sand: freshly poured sand takes a hue
  that drifts with time and across the grid. Not saved, though the first time
  earns the secret "rainbow" achievement.
- Searching a locked discovery's exact name gives its recipe (above).

## Not done yet

- Wind, or any field that pushes gases sideways. Clouds drift with one
  shared `drift` that turns now and then, and nothing else feels it.
- Lightning doesn't seek metal; a rod only works under the strike.
- Save and load a scene (the typed arrays serialise easily).
