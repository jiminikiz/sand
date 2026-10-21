# Falling Sands

A falling-sand toy in one HTML file, `index.html`, with no dependencies. It
installs as an app and plays offline (see "App" below).

## Materials

| Material | Key | Behaviour                                                                 |
| -------- | --- | ------------------------------------------------------------------------- |
| sand     | 1   | Powder. Sinks slowly through liquids.                                     |
| water    | 2   | Liquid. Puts out fire (smoke, some steam), quenches lava (obsidian, steam). |
| oil      | 3   | Liquid, floats on water. Burns slowly; burning oil stays put and flames.  |
| acid     | a   | Liquid. Eats what it touches, 10 bites each, except glass. Water dilutes it. |
| fire     | 4   | Stays on fuel and throws flames and embers; loose fire drifts up & dies.  |
| plant    | 5   | Drinks touching water into more plant; spare water sprouts upward.        |
| seed     | 6   | Falls like sand. On sand with water touching it, sprouts a stem.          |
| stone    | 7   | Static.                                                                   |
| lava     | 8   | Viscous. Ignites fuel, melts sand to glass, crusts to stone doing it.     |
| ice      | 9   | Freezes water with a limited cold budget; melts near anything hot.        |
| smoke    | no  | left by fire as it dies or meets water. The easy first discovery.         |
| steam    | no  | water meeting fire, lava or an ember. Rises, condenses back to rain.      |
| glass    | no  | lava + sand                                                               |
| obsidian | no  | lava + water                                                              |
| ember    | no  | thrown by fire on fuel; arcs 30–60 cells and lights fuel it lands on      |
| snow     | no  | steam + ice. Falls, floats on water, melts near heat.                     |
| fume     | no  | a quarter of what acid eats goes up as this green gas                     |
| flower   | no  | top of a seed's stem: a yellow heart, one petal colour per bloom          |

The eight unpaintable ones are the discoveries (`SECRETS`), saved per browser
in `localStorage` under `sand.found`. Each has a `how` in `MAT`, shown once
found.

## How the code works

- State is typed arrays over the grid: `type`, `life`, `col` (shade), `vel`
  (ember heading), `clock`. `shapeGrid()` reallocates them when the stage
  changes size (see below).
- `life` means something different per material: fire/smoke/steam/fume
  lifetime, plant sap, ice cold budget, ember flight time, acid bites left.
- Acid's `etch` table is the chance per bite of eating each material. Glass
  is missing from it on purpose: it's what you keep acid in.
- Plant sap from drinking water is 0–6. A seed sprouts with `STEM` + 6–18;
  that stem climbs, and when its sap is down to exactly `STEM` it blooms
  instead of growing. The two ranges never overlap, so one byte holds both.
- `step()` scans bottom-up, alternating left/right each tick. `clock[i] ===
  tick` marks a cell already moved this tick, so nothing moves twice.
- `sinks(t, j)` is the one density rule: a mover displaces anything movable
  with lower `dens`.
- Fixed 60 Hz timestep; at most three steps per frame.

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
- What's under the brush, and pause, show in a strip at the bottom right.
  Discoveries also pop a toast there, so they're seen with the panel folded.

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

## Easter eggs

- ↑ ↑ ↓ ↓ ← → ← → b a toggles rainbow sand: freshly poured sand takes a hue
  that drifts with time and across the grid. Not saved.
- Searching a locked discovery's exact name gives its recipe (above).

## Not done yet

- Wind, or any field that pushes gases sideways.
- Save and load a scene (the typed arrays serialise easily).
