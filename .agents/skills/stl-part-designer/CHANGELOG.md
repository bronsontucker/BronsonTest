# Version 2.0.0

- Fix STL topology checks by welding identical vertices without silently repairing defects.
- Replace scalar `math.isfinite` calls on arrays with NumPy finite checks.
- Validate connected solids, triangle degeneracy, duplicate faces, edge manifoldness, winding, dimensions and volume.
- Re-import every exported STEP and compare B-rep dimensions and volume.
- Add safe unique filenames, configurable tessellation, expected part count, file hashes, dependency versions, effective parameters and failure reports that invalidate stale successes.
- Stage all component exports until every component passes.
- Add regression tests for valid multi-part exports and rejected defective inputs.
- Add a real threaded three-piece 9.1 mm cable gland example, assembly clearance checks and geometry preview.
- Expand the skill with material selection, panel-interface decisions, thread fit allowances, assembly travel, manufacturing guidance and explicit validation limits.
