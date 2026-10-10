---
name: stl-part-designer
description: Create, edit, repair, validate, and export mechanical 3D-printable CAD models from dimensional instructions, photographs, sketches, or existing CAD. Use for STL, STEP, printable fittings, threads, enclosures, jigs, brackets, cable glands, tolerance-critical and parametric parts.
---

# STL Part Designer for Codex

Build **real geometry**, not empty file stubs or invented download links. Use millimetres and CadQuery/OpenCascade for newly authored solid CAD; preserve a named-parameter Python source. Favor functional PETG/FDM geometry with 0.4 mm nozzle when the user has not specified manufacturing details.

## Workflow
1. Extract dimensional constraints, datum surfaces, functional interfaces, fit class and intended manufacturing method. Ask only when a missing detail would change the part topology; otherwise state assumptions.
2. Probe Python and CAD tools using `python -c "import cadquery,trimesh; print('CAD ready')"`. If missing, install from `requirements.txt` in this skill folder if internet and permissions allow. Never claim dependencies installed before checking.
3. Author `model.py` defining `def build(**params):` that returns a CadQuery Workplane or Shape. Use named dimensions and avoid magical numerical constants. Design actual solid(s), realistic threads and clearance (printed threads can require a fit coupon).
4. Execute `python .agents/skills/stl-part-designer/scripts/export_validate.py model.py --out-dir output`. For the output of multi-piece assemblies create one file per printed solid. Do not merely rename a mesh as STEP.
5. Inspect validator output: CadQuery solid validity, non-zero volume, expected bounding box; STL watertight, winding-consistent, manifold, finite coordinates, non-degenerate triangle faces. Rework geometry rather than bypassing failures.
6. Deliver links or repository paths for STL, STEP and source. State all fit-sensitive assumptions, actual outer dimensions and validation status. A basic mechanical cable clamp does not constitute a certified IP-rated cable gland.

## CadQuery example source contract
```python
import cadquery as cq
def build(**params):
    outer_d = float(params.get("outer_d", 20.0))
    bore_d = float(params.get("bore_d", 9.3))
    height = float(params.get("height", 12.0))
    return cq.Workplane("XY").circle(outer_d/2).circle(bore_d/2).extrude(height)
```

## Print considerations
- Start with 0.15-0.30 mm radial clearance for independent PETG mating cylindrical parts, then calibrate printer-specific offsets.
- Avoid sub-0.8 mm walls for a 0.4 mm nozzle; use more thickness in highly loaded regions.
- Orient for layer strength; round transitions; provide assembly order for multi-part components.
- For flexible grippers, account for PETG's limited cyclic strain and use a replaceable elastomeric seal when waterproofing matters.
- For 9.1 mm OD cable, use a nominal 9.3 mm passage and a separately designed compressive grip/seal.
- Never describe an output as validated unless the script actually ran and reported success.

## Included automation
- `scripts/export_validate.py`: export CadQuery STEP and STL, audit exported mesh and geometry.
- `requirements.txt`: backend Python dependencies.
