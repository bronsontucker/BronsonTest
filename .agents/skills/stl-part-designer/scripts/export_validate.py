#!/usr/bin/env python3
"""Export and validate a CadQuery build() model. Usage: python export_validate.py model.py --out-dir output"""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument("model", type=Path)
    p.add_argument("--out-dir", type=Path, default=Path("output"))
    p.add_argument("--params", default="{}", help="JSON object of arguments for build()")
    args = p.parse_args()
    import cadquery as cq
    import trimesh
    params = json.loads(args.params)
    if not isinstance(params, dict):
        raise TypeError("--params must be a JSON object")
    spec = importlib.util.spec_from_file_location("cad_project", args.model.resolve())
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load CAD source")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    built = module.build(**params)
    if isinstance(built, (list, tuple)):
        named = [(f"part_{i+1}", s) for i, s in enumerate(built)]
    elif isinstance(built, dict):
        named = list(built.items())
    else:
        named = [(args.model.stem, built)]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for name, item in named:
        shape = item.val() if isinstance(item, cq.Workplane) else item
        if not isinstance(shape, cq.Shape):
            raise TypeError(f"{name}: build() must return CadQuery Shape or Workplane")
        if shape.isNull() or not shape.isValid() or shape.Volume() <= 0:
            raise ValueError(f"{name}: invalid B-rep or zero volume")
        solids = shape.Solids()
        if len(solids) != 1:
            raise ValueError(f"{name}: expected exactly one connected solid, got {len(solids)}")
        bounds = shape.BoundingBox()
        dims = [bounds.xlen, bounds.ylen, bounds.zlen]
        if any(not math.isfinite(v) or v <= 0 or v > 100000 for v in dims):
            raise ValueError(f"{name}: implausible bounding box {dims}")
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in str(name))
        step = args.out_dir / (safe_name + ".step")
        stl = args.out_dir / (safe_name + ".stl")
        cq.exporters.export(shape, str(step), exportType="STEP")
        cq.exporters.export(shape, str(stl), exportType="STL", tolerance=0.05, angularTolerance=0.1)
        mesh = trimesh.load_mesh(str(stl), process=False)
        if not isinstance(mesh, trimesh.Trimesh):
            raise ValueError(f"{name}: STL did not load as a single triangle mesh")
        if not mesh.is_watertight or not mesh.is_winding_consistent or not mesh.is_volume:
            raise ValueError(f"{name}: STL failed watertight / winding / volume checks")
        if not mesh.is_edge_manifold:
            raise ValueError(f"{name}: nonmanifold mesh edges")
        if not math.isfinite(mesh.volume) or mesh.volume <= 0:
            raise ValueError(f"{name}: invalid mesh volume")
        if not math.isfinite(mesh.vertices).all() or not math.isfinite(mesh.faces).all():
            raise ValueError(f"{name}: nonfinite vertices or faces")
        results.append({"part": str(name), "step": str(step), "stl": str(stl),
                        "bbox_mm": dims, "brep_volume_mm3": shape.Volume(),
                        "mesh_volume_mm3": mesh.volume, "faces": len(mesh.faces),
                        "watertight": bool(mesh.is_watertight)})
    report = args.out_dir / "validation.json"
    report.write_text(json.dumps(results, indent=2))
    print(json.dumps({"success": True, "report": str(report), "parts": results}, indent=2))

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)
