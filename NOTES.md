# Falling Sands

A falling-sand toy in one HTML file, `index.html`, with no dependencies. It
installs as an app and plays offline (see "App" below).

## Materials

| Material  | Key           | Behaviour                                                                    |
| --------- | ------------- | ---------------------------------------------------------------------------- |
| sand      | 1             | Powder. Sinks slowly through liquids.                                        |
| salt      | t             | Powder. Dissolves in water as brine; melts ice and snow into brine, a few cells a grain. |
| seed      | 6             | Falls like sand. On sand or ash with water touching it, sprouts a stem; on ash a taller one. |
| gunpowder | x             | Powder. Lit, it blows a hole of radius 5; the rest of a pile goes off as a ripple. |
| water     | 2             | Liquid. Puts out fire (smoke, some steam), quenches lava (obsidian, steam).  |
| oil       | 3             | Liquid, floats on water. Burns slowly; burning oil stays put and flames.     |
| acid      | a             | Liquid. Eats what it touches, 10 bites each, except glass, clone and drain. Water dilutes it. |
| lava      | 8             | Viscous. Ignites fuel, melts sand to glass, crusts to stone doing it; froths to pumice on ice. |
| fire      | 4             | Stays on fuel and throws flames and embers; loose fire drifts up & dies. Fixed: what falls on it waits. |
| lightning | l             | One bolt per press, from the top of the sky to the first thing under the pointer. |
| stone     | 7             | Static.                                                                      |
| wood      | w             | Static. Catches slowly, burns long throwing embers, leaves ash.              |
| metal     | m             | Static. Rusts in water, faster in brine. Carries lightning.                  |
| ice       | 9             | Freezes water with a limited cold budget; melts near anything hot.          |
| smoke     | no            | fire dying out or doused. Soots stone and glass darker.                      |
| steam     | no            | water meeting fire, lava or an ember. Rises, half condenses into rain.       |
| rain      | no            | steam condensing. Falls through air and gas, turns to water on landing.      |
| ash       | h, once found | wood or plants burnt down. Light powder: rests on sand, sinks in water.      |
| plant     | 5, once found | seed + water on sand. Drinks touching water into more plant; spare water sprouts upward. |
| glass     | g, once found | lava or lightning + sand. Static; acid can't eat it.                         |
| brine     | no            | salt + water. Sinks under water, never freezes; boiled, leaves its salt.     |
| obsidian  | o, once found | lava + water. Static; acid barely eats it.                                   |
| ember     | no            | thrown by fire on fuel, or a blast; arcs 30–60 cells and lights fuel it lands on |
| snow      | s, once found | steam + ice. Falls, floats on water, melts near heat.                        |
| fume      | no            | a quarter of what acid eats goes up as this green gas                        |
| flower    | no            | top of a seed's stem: a yellow heart, one petal colour per bloom             |
| pumice    | p, once found | lava + ice. A powder that floats on water.                                   |
| rust      | no            | metal left in water. Powder; acid eats it readily.                           |
| hydrogen  | no            | half of the metal acid eats. Rises; lit, pops with a blast of radius 2.      |
| acid rain | no            | fume condensing. Falls like rain, lands as acid with 3 bites.               |
| cloud     | k, once found | steam reaching the top of the sky. Drifts, rains from its base, now and then strikes. |
| bee       | e, once found | a flower heart with three more within 10 cells. Gathers pollen, drips honey. |
| honey     | y, once found | bees carrying pollen. Thick; sinks under water and brine.                    |
| clone     | v, the prize  | takes the first thing that touches it, passes it to the clone beside it, pours it out. |
| drain     | d, the prize  | swallows anything loose that touches it.                                     |

The nineteen discoveries (`SECRETS`) are saved per browser in `localStorage`
under `sand.found`. Each has a `how` in `MAT`, shown once found. A discovery
that is also in `TOOLS` joins the materials once found; until then its button
stays out of the panel, search included, and its key does nothing. Clone and
drain join once all nineteen are. The rest are never paintable.

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
  credits a secret; `place()` puts a cell down without crediting. Scenes
  place, and so does plant spreading from plant, so plant is discovered only
  by a seed sprouting.
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
- The material buttons are built from `TOOLS`: material, key, tip, and the
  share of the brush it fills (30% for loose things and fire, all for fixed
  ones, 3% for bees).
- Fixed 60 Hz timestep; at most three steps per frame.
- `rnd()` is a xorshift seeded from `Math.random()` on load, so every load
  starts on a different scene.

## Scenes

- `scene()` (on load, and `r`) rolls a new one: rolling sand over a thin
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
  The panel and overlays sit in `.safe`, inset by `env(safe-area-inset-*)`
  divided by `--fit`.
- A panel floats over the left of the sandbox and holds everything: search,
  materials, brush, ui size, world controls, discoveries, help. It scrolls on
  its own. `n` or the « button folds it to a 60 px rail of swatches. Until
  the player picks, it starts folded when open it would cover more than a
  quarter of the width; the pick is kept in `sand.nav`.
- Sand poured under the panel is still there, just covered.
- UI size (`-` / `=`, or the − + buttons) scales the panel, the strip and
  the toast through the `--ui` CSS variable, using `transform: scale`. Until
  the player picks, it follows the layout: 100% up to 900 px tall, up to 125%
  above that. Clicking the percentage goes back to automatic. Kept in
  `sand.ui`.
- Search (`/`) filters every panel item by name and description. Enter picks
  the first button left, Escape clears. A discovery not yet made only shows
  when searched by its exact name, and then shows its recipe.
- What's under the brush (for a clone, what it pours), and pause, show in a
  strip at the bottom right. Discoveries also pop a toast there, so they're
  seen with the panel folded.

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
  panel and standing on the bottom edge, with walls kept 3 cells thick. The
  ground runs the full width. In portrait that leaves open sky above.
- `pointers` holds one stroke per finger, so several fingers pour at once.
  The starting brush is about 15 px across on screen, whatever the cell
  size.
- Touch screens (`hover: none` and `pointer: coarse`) get 40 px buttons, no
  key labels and their own help line.
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

## App

- `manifest.webmanifest`: name, fullscreen display (no status or navigation
  bar on phones; desktop falls back to a window), dark theme, icons. All
  paths are relative, so it works served from any subfolder.
- `sw.js` is network first: online, every file comes fresh and refreshes the
  cached copy; offline, the copy. There's no stale version to wait out after a
  change. Bump `CACHE` only when the `SHELL` list changes.
- Service workers need https, or `localhost` / `127.0.0.1`. Opened straight
  from disk (`file://`) the game runs fine, just without offline or install.
- An "install" button joins the world controls only while the browser offers
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

## Easter eggs

- ↑ ↑ ↓ ↓ ← → ← → b a toggles rainbow sand: freshly poured sand takes a hue
  that drifts with time and across the grid. Not saved.
- Searching a locked discovery's exact name gives its recipe (above).

## Not done yet

- Wind, or any field that pushes gases sideways. Clouds drift with one
  shared `drift` that turns now and then, and nothing else feels it.
- Lightning doesn't seek metal; a rod only works under the strike.
- Save and load a scene (the typed arrays serialise easily).
