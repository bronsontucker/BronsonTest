---
name: stl-part-designer
description: Design, modify, repair, validate, and export parametric printable mechanical parts as real STL and STEP. Use for dimensional CAD, threaded fittings, cable glands, brackets, enclosures, jigs, tolerances, and multi-piece assemblies.
---

# STL Part Designer — v2

Use millimetres and CadQuery/OpenCascade for solid CAD. Deliver editable named-parameter Python source, separate STL and STEP files per printed part, and a machine-readable validation report. Never substitute meshes renamed as STEP or claim physical performance from a geometry check.

## 1. Establish the mechanical interfaces

Extract required dimensions, cable/shaft diameters, mating threads, panel attachment, part count, materials, load direction, manufacturing method, and sealing expectations. Ask only about missing information that changes topology. Otherwise state a useful assumption and proceed. Default rigid parts to PETG, 0.4 mm nozzle, 0.2 mm layers. Flexible seals require a specified elastomer such as TPU 95A, not rigid PETG.

Before modeling, enumerate the components and explain how they assemble. Count all required printed pieces; do not hide an extra locknut or seal. A three-piece cable gland can use a body, cap, and TPU insert when the body screws into a tapped panel. A plain panel hole usually needs another retention mechanism.

## 2. Prepare and probe the CAD backend

Run `python -c "import cadquery,trimesh,numpy; print('CAD ready')"`. Install missing dependencies with `python -m pip install -r <skill-dir>/requirements.txt` when authorized, then repeat the probe. Follow environment network policy. Report actual install failures instead of claiming a tool is unavailable without checking.

## 3. Build reproducible solid geometry

Author `model.py` with `build(**params)`, returning a Shape, single-object Workplane, or dictionary of filename-safe part names to shapes. Each printed part must be exactly one connected valid solid. Use named dimensions, reject unknown/invalid parameters, and record all defaults in source. Export each component in print coordinates with its bottom at Z=0; record assembly transforms separately.

For threads, model actual helical surfaces with pitch, major/root diameters, flank profile, lead-in, handedness, runout, and radial/axial fit allowances. Decorative rings do not make a screw. Do not call custom printed thread profiles ISO-standard threads. Start with 0.15–0.30 mm radial clearance and calibrate using a fit coupon. Rotate and translate together when checking screw travel: angle = 360 × travel / pitch, with the sign appropriate to handedness.

For cable glands, use cable OD plus a modest passage allowance (9.3 mm for a 9.1 mm cable). Provide an independent compressible grip/seal, a support shoulder, compression travel, cap roof clearance, and sufficient thread engagement. Distinguish undeformed CAD interference in a compressible seal from collisions between rigid components. Do not infer gripping force, pull-out resistance, or ingress protection from dimensions alone.

Avoid walls below 0.8 mm with a 0.4 mm nozzle; allow more for loaded parts. Check critical wall thickness analytically or with a suitable tool and identify the method. Provide assembly order and layer-orientation advice. Use entry chamfers around cable passages.

## 4. Export and validate every component

Run:

```sh
python <skill-dir>/scripts/export_validate.py model.py --out-dir output --expected-parts 3
```

Optional `--params '{"cable_od":9.1}'`, `--tolerance 0.03` (mm), and `--angular-tolerance 0.08` (radians). The exporter checks:

- exactly one valid B-rep solid per component, positive finite volume and bounds;
- genuine STEP export followed by re-import, volume and dimension comparison;
- STL finite coordinates, identical-vertex welding, degenerate and duplicate triangles;
- one connected mesh, two incident faces per edge, watertightness, winding and volume;
- STL/CAD dimension and volume agreement, file hashes and dependency versions.

Vertex welding accounts for STL's independent triangle vertices; do not silently repair or discard defects to force a pass. If export fails, inspect and fix the source, then rerun. Only a report with `success: true` establishes these checks passed. A failure report invalidates earlier output in the same directory. Do not deliver stale exports as newly validated files.

For assemblies also check rigid-part collisions in assembly coordinates, intended travel, cable passage, and clearances. Explicitly distinguish software checks from physical testing. This exporter does not certify absence of every mesh self-intersection, minimum wall thickness, structural strength, slicer behavior, print fit, or sealing.

## 5. Review and deliver

Generate and inspect an assembled or exploded preview from the exported geometry. Include actual bounding dimensions, material per part, print orientation, tolerances, panel interface, assembly instructions, and all unresolved fit assumptions. Deliver links for STL, STEP, source, and reports. Use a ZIP for multi-part packages. Never claim a printed prototype is IP-rated or physically tested unless that testing actually happened.

## Bundled resources

- `scripts/export_validate.py`: strict multi-part export, STEP roundtrip, mesh audits, provenance.
- `tests/test_export_validate.py`: positive export and negative defect regression tests.
- `examples/cable_gland_9p1/model.py`: parametric body, compression cap, TPU insert with real custom helical threads.
- `requirements.txt`: backend requirements.

Run the regression suite with `python -m unittest discover -s <skill-dir>/tests -v` after changing the exporter.
