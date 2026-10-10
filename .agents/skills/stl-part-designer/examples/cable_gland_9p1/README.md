# Compact three-piece gland for a 9.1 mm OD cable

All dimensions are millimetres. This is a printable prototype with custom threads, intended for a matching threaded panel/boss. It does not include a locknut for a plain panel hole.

| Printed component | Material | Overall XYZ size | Key interface |
|---|---|---|---|
| Body | PETG | 25.40 × 22.00 × 20.00 | 22 mm hex flats; 6 mm mounting spigot |
| Compression cap | PETG | 27.71 × 24.00 × 14.00 | 24 mm hex flats |
| Insert | TPU 95A | 14.60 × 14.60 × 8.00 | 9.30 mm relaxed bore |

Assembly length at initial insert contact is 24 mm, including the 6 mm panel spigot. Maximum nominal outside diameter across cap corners is 27.71 mm. The cap advances up to 0.8 mm (144 degrees at 2 mm pitch) from initial insert contact; actual tightening must be judged from physical fit.

## Files

`body`, `compression_cap`, and `tpu_insert` each have STL and true solid STEP exports. `assembly.step` places the three undeformed components together. `model.py` contains editable dimensions and real helical thread geometry. `validation.json` reports per-component checks; `assembly_validation.json` reports sampled motion and interface checks. `preview.png` shows the assembly and exploded parts.

## Threads and fit

- Panel mounting thread: custom nominal 16 mm OD, 2 mm pitch, truncated trapezoidal profile. **Not an ISO M16 thread; do not assume an M16 tap or standard nut will fit.** A matching printed female panel interface must use this profile and printer-specific clearance.
- Body-to-cap thread: custom nominal 20 mm OD, 2 mm pitch, right handed, approximately 4.75 turns on the body. Female profile has 0.25 mm radial and 0.12 mm axial flank allowance.
- Cable passage: 9.3 mm in body and insert; 9.5 mm in the cap. Cable jacket diameter and roundness vary; measure your actual cable.
- Pocket diameter: 14.8 mm; insert diameter: 14.6 mm. Shoulder at body Z=13 supports the 8 mm insert, initially protruding 1 mm beyond the body.
- Analytical wall dimensions: 1.5 mm body root wall around seal pocket; 1.75 mm cap wall at female thread crest; 3 mm cap roof. Chamfers, thread runouts and local transitions are not a global thickness scan.

## Printing

Use a calibrated 0.4 mm nozzle and approximately 0.2 mm layers for PETG; five perimeters and 40–60% infill are reasonable starting settings. Use dry filament and inspect the slicer preview around thread flanks and runouts. Print a thread-fit trial before committing to the panel interface.

Body: mounting spigot down, axis vertical. Use removable build-plate supports beneath the flange overhang; keep support out of the cable bore and internal seal pocket. Cap: flip it in the slicer so the flat closed roof is down and the threaded opening is upward. Insert: axis vertical, flat annular face on the bed, TPU 95A, solid walls/100% infill and a TPU-appropriate slow profile. Remove burrs and strings, especially at cable entry and threads.

## Assembly

1. Prepare a matching custom-threaded panel/boss with sufficient thread engagement; a plain hole alone will not retain this three-piece design.
2. Slide the cap over the free cable end, then the TPU insert, then pass the cable through the body. A pre-attached connector larger than the bore will not pass.
3. Screw the body into the matching panel, holding its hex. Seat the TPU insert against the internal shoulder.
4. Screw the cap onto the body until its roof contacts the insert. Tighten gradually while holding the body. The design allows 0.8 mm of intended compression, with 0.2 mm nominal roof-to-body clearance remaining.
5. Check cable grip and jacket condition. Do not force a binding printed thread or keep tightening against the body stop. Reprint with adjusted clearance if needed.

TPU deformation, gripping force and leakage have not been physically tested or simulated. A volume-conservation estimate suggests inward grip after the initial radial clearance is taken up, but actual TPU print porosity and compliance govern performance. Panel-face sealing is not provided as a separate fourth piece. This prototype is not a certified IP-rated gland.

## Reproduce

Install the included `requirements.txt`, then run:

```sh
python export_validate.py model.py --out-dir regenerated --expected-parts 3
python check_assembly.py regenerated
```

The first command needs CadQuery, NumPy and trimesh. The preview script additionally needs Matplotlib. Default parameters are in `model.py` and the validation report. Review the report before using any exports; only `success: true` establishes a successful validation run.
