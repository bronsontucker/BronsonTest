#!/usr/bin/env python3
"""Export real STEP/STL files and fail closed on geometry or mesh defects."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import sys
import tempfile
import cadquery as cq
import numpy as np
import trimesh


def validate_shape(name, item):
    if isinstance(item, cq.Workplane):
        values = item.vals()
        if len(values) != 1:
            raise ValueError(f'{name}: Workplane must contain exactly one shape')
        item = values[0]
    if not isinstance(item, cq.Shape):
        raise TypeError(f'{name}: expected a CadQuery Shape or Workplane')
    if item.isNull() or not item.isValid() or len(item.Solids()) != 1:
        raise ValueError(f'{name}: expected exactly one valid connected solid')
    volume = item.Volume()
    box = item.BoundingBox()
    dims = np.array([box.xlen, box.ylen, box.zlen])
    if not math.isfinite(volume) or volume <= 0 or not np.isfinite(dims).all() or (dims <= 0).any() or (dims > 100000).any():
        raise ValueError(f'{name}: invalid volume or dimensions')
    return item, dims, volume


def validate_mesh(path, dims, cad_volume, tolerance):
    # STL stores independent triangle vertices. Weld identical coordinates ONLY;
    # do not silently remove invalid faces or repair geometry to manufacture a pass.
    mesh = trimesh.load_mesh(path, process=False)
    if not isinstance(mesh, trimesh.Trimesh) or not len(mesh.faces):
        raise ValueError('STL must contain triangles')
    if not np.isfinite(mesh.vertices).all() or not np.isfinite(mesh.faces).all():
        raise ValueError('Nonfinite mesh coordinates')
    mesh.merge_vertices(digits_vertex=8)
    if (mesh.area_faces <= 1e-12).any():
        raise ValueError('Degenerate triangles')
    canonical=np.sort(mesh.faces,axis=1)
    if len(np.unique(canonical,axis=0)) != len(mesh.faces):
        raise ValueError('Duplicate triangles')
    counts=np.bincount(mesh.edges_unique_inverse)
    if not np.all(counts == 2):
        raise ValueError('Nonmanifold or boundary edges')
    components=len(mesh.split(only_watertight=False))
    if components != 1 or not mesh.is_watertight or not mesh.is_winding_consistent or not mesh.is_volume:
        raise ValueError('STL connectivity / watertight / winding / volume failure')
    if not math.isfinite(mesh.volume) or mesh.volume <= 0:
        raise ValueError('Invalid mesh volume')
    if not np.allclose(mesh.extents,dims,atol=2*tolerance,rtol=1e-5):
        raise ValueError('STL and CAD bounding boxes disagree')
    relative_error=abs(mesh.volume-cad_volume)/cad_volume
    if relative_error > .01:
        raise ValueError(f'STL volume differs from CAD by {relative_error:.2%}')
    return dict(mesh_volume_mm3=float(mesh.volume),faces=len(mesh.faces),
                components=components,watertight=True,winding_consistent=True,
                edge_manifold=True,finite_coordinates=True,degenerate_faces=0,
                duplicate_faces=0,volume_relative_error=relative_error)


def _export_model(model, out_dir, params=None, tolerance=.03, angular_tolerance=.08, expected_parts=None):
    model=Path(model).resolve(); out_dir=Path(out_dir)
    if not math.isfinite(tolerance) or not 0 < tolerance <= .1:
        raise ValueError('Linear tolerance must be >0 and <=0.1 mm')
    if not math.isfinite(angular_tolerance) or not 0 < angular_tolerance <= .2:
        raise ValueError('Angular tolerance must be >0 and <=0.2 radians')
    params={} if params is None else params
    if not isinstance(params,dict): raise TypeError('Parameters must be a JSON object')
    spec=importlib.util.spec_from_file_location('cad_project',model)
    if spec is None or spec.loader is None: raise ValueError('Cannot load model')
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    built=module.build(**params)
    named=list(built.items()) if isinstance(built,dict) else ([(f'part_{i+1}',v) for i,v in enumerate(built)] if isinstance(built,(list,tuple)) else [(model.stem,built)])
    if not named or (expected_parts is not None and len(named)!=expected_parts):
        raise ValueError(f'Unexpected part count: {len(named)}')
    names=[str(name) for name,_ in named]
    if any(not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*',n) for n in names) or len(set(n.lower() for n in names))!=len(names):
        raise ValueError('Part names must be unique, filename-safe identifiers')
    out_dir.mkdir(parents=True,exist_ok=True)
    # A failed rerun must not leave a stale success report.
    report_path=out_dir/'validation.json'
    report_path.write_text(json.dumps({'success':False,'status':'in_progress'}))
    try:
        with tempfile.TemporaryDirectory(prefix='.export-',dir=out_dir) as temporary:
            staging=Path(temporary); results=[]
            for name,item in named:
                shape,dims,volume=validate_shape(name,item)
                step=staging/f'{name}.step'; stl=staging/f'{name}.stl'
                cq.exporters.export(shape,str(step),exportType='STEP')
                cq.exporters.export(shape,str(stl),exportType='STL',tolerance=tolerance,angularTolerance=angular_tolerance)
                roundtrip,step_dims,step_volume=validate_shape(name,cq.importers.importStep(str(step)))
                if not np.allclose(dims,step_dims,atol=1e-5,rtol=1e-7) or not math.isclose(volume,step_volume,rel_tol=1e-6,abs_tol=1e-6):
                    raise ValueError(f'{name}: STEP roundtrip changed dimensions or volume')
                metrics=validate_mesh(stl,dims,volume,tolerance)
                results.append(dict(part=name,step=step.name,stl=stl.name,bbox_mm=dims.tolist(),
                    brep_volume_mm3=volume,brep_valid=True,step_roundtrip_valid=True,**metrics,
                    sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (step,stl)}))
            report=dict(success=True,units='mm',parameters={**getattr(module,'DEFAULTS',{}),**params},tessellation=dict(linear_mm=tolerance,angular_radians=angular_tolerance),
                        versions=dict(cadquery=cq.__version__,trimesh=trimesh.__version__,numpy=np.__version__),parts=results,
                        limitations=['Mesh self-intersection, minimum wall thickness, printer fit, sealing, and strength require separate assessment.'])
            for file in staging.iterdir(): file.replace(out_dir/file.name)
            report_path.write_text(json.dumps(report,indent=2)+'\n')
            return report
    except Exception as exc:
        report_path.write_text(json.dumps({'success':False,'error':str(exc)},indent=2)+'\n')
        raise


def export_model(model, out_dir, params=None, tolerance=.03, angular_tolerance=.08, expected_parts=None):
    out_dir=Path(out_dir)
    out_dir.mkdir(parents=True,exist_ok=True)
    report=out_dir/'validation.json'
    report.write_text(json.dumps({'success':False,'status':'in_progress'}))
    try:
        return _export_model(model,out_dir,params,tolerance,angular_tolerance,expected_parts)
    except Exception as exc:
        report.write_text(json.dumps({'success':False,'error':str(exc)},indent=2)+'\n')
        raise


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('model',type=Path); p.add_argument('--out-dir',type=Path,default=Path('output'))
    p.add_argument('--params',default='{}'); p.add_argument('--expected-parts',type=int)
    p.add_argument('--tolerance',type=float,default=.03); p.add_argument('--angular-tolerance',type=float,default=.08)
    args=p.parse_args()
    result=export_model(args.model,args.out_dir,json.loads(args.params),args.tolerance,args.angular_tolerance,args.expected_parts)
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    try: main()
    except Exception as exc:
        print(f'FAILED: {type(exc).__name__}: {exc}',file=sys.stderr); sys.exit(1)
