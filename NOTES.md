# Falling Sands

A falling-sand toy in one HTML file, `index.html`, with no dependencies. It
installs as an app and plays offline (see "App" below).

## Materials

| Material | Key | Behaviour                                                                 |
| -------- | --- | ------------------------------------------------------------------------- |
| sand     | 1   | Powder. Sinks slowly through liquids.                                     |
| water    | 2   | Liquid. Puts out fire (smoke, some steam), quenches lava (obsidian, steam). |
| oil      | 3   | Liquid, floats on water. Burns slowly; burning oil stays put and flames.  |
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
| flower   | no  | top of a seed's stem: a yellow heart, one petal colour per bloom          |

The seven unpaintable ones are the discoveries (`SECRETS`), saved per browser
in `localStorage` under `sand.found`. Each has a `how` in `MAT`, shown once
found.

## How the code works

- State is typed arrays over the grid: `type`, `life`, `col` (shade), `vel`
  (ember heading), `clock`. The grid's size is fixed at load (see below).
- `life` means something different per material: fire/smoke/steam lifetime,
  plant sap, ice cold budget, ember flight time.
- Plant sap from drinking water is 0–6. A seed sprouts with `STEM` + 6–18;
  that stem climbs, and when its sap is down to exactly `STEM` it blooms
  instead of growing. The two ranges never overlap, so one byte holds both.
- `step()` scans bottom-up, alternating left/right each tick. `clock[i] ===
  tick` marks a cell already moved this tick, so nothing moves twice.
- `sinks(t, j)` is the one density rule: a mover displaces anything movable
  with lower `dens`.
- Fixed 60 Hz timestep; at most three steps per frame.

## Layout

- Full window (`100vw` × `100vh`), never smaller than 640 × 480; below that
  the page scrolls.
- A panel on the left holds everything: search, materials, brush, world
  controls, discoveries, help. It scrolls on its own. `n` or the « button
  folds it to a 60 px rail of swatches; the choice is kept in `sand.nav`.
- Search (`/`) filters every panel item by name and description. Enter picks
  the first button left, Escape clears. A discovery not yet made only shows
  when searched by its exact name, and then shows its recipe.
- What's under the brush, and pause, show in a strip over the stage.
  Discoveries also pop a toast there, so they're seen with the panel folded.

## Screens and touch

- The grid takes the shape of the stage it loads in: aspect clamped to
  0.45–3.2, and about one cell per 9 px² up to 54,000 cells (minimum 20,000).
  Measured: 640×480 gives 129×155 at 2.9 px per cell, 1024×768 gives
  235×230 at 3.2 px, 1366×768 gives 283×191 at 3.9 px, a desktop 1874×1122
  gives 282×191 at 5.7 px.
- The grid doesn't change after load; on resize, or folding the panel, `fit()`
  rescales the canvas with square cells. Reload to get a grid shaped for the
  new stage.
- The panel's buttons are in the HTML, not built by the script, and its saved
  folded state is applied before the stage is measured. Either way, the grid
  is measured against the stage the player actually sees.
- `scene()` is drawn on a 300×180 plan and stretched, with walls kept 3
  cells thick.
- `pointers` holds one stroke per finger, so several fingers pour at once.
  The starting brush is about 15 px across on screen, whatever the cell
  size.
- Touch screens (`hover: none` and `pointer: coarse`) get 40 px buttons, no
  key labels and their own help line.
- With the 640 × 480 floor, a phone in portrait scrolls sideways. Not tried
  on a real phone or tablet. The layout was checked in Brave, and in iframes
  at 560×420, 640×480, 1024×768 and 1366×768.

## App

- `manifest.webmanifest`: name, standalone display, dark theme, icons. All
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

## Easter eggs

- ↑ ↑ ↓ ↓ ← → ← → b a toggles rainbow sand: freshly poured sand takes a hue
  that drifts with time and across the grid. Not saved.
- Searching a locked discovery's exact name gives its recipe (above).

## Not done yet

- Wind, or any field that pushes gases sideways.
- Save and load a scene (the typed arrays serialise easily).
- Acid, which would need a rule for what it can't dissolve. Glass is the
  obvious answer, and it's a discovery, so you'd have to make the jar first.
