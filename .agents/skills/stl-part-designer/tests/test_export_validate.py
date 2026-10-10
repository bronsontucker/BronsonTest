"""Regression tests exercise exported files and intentionally invalid inputs."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import cadquery as cq
import numpy as np
import trimesh
spec=importlib.util.spec_from_file_location('validator',Path(__file__).parents[1]/'scripts/export_validate.py')
v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)

class ExportTests(unittest.TestCase):
    def test_real_roundtrip_and_multi_part(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); model=root/'model.py'
            model.write_text("import cadquery as cq\ndef build(**p):\n return {'ring':cq.Workplane('XY').circle(5).circle(2).extrude(3),'cube':cq.Workplane('XY').box(2,3,4)}\n")
            r=v.export_model(model,root/'out',expected_parts=2)
            self.assertTrue(r['success']); self.assertEqual(len(r['parts']),2)
            self.assertTrue(all(p['step_roundtrip_valid'] and p['edge_manifold'] for p in r['parts']))
    def test_multiple_solids_rejected(self):
        with self.assertRaises(ValueError):
            v.validate_shape('bad',cq.Compound.makeCompound([cq.Workplane('XY').box(1,1,1).val(),cq.Workplane('XY').box(1,1,1).translate((3,0,0)).val()]))
    def test_open_mesh_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            mesh=trimesh.creation.box(); mesh.update_faces(np.arange(len(mesh.faces)-1)); path=Path(d)/'bad.stl'; mesh.export(path)
            with self.assertRaises(ValueError): v.validate_mesh(path,np.ones(3),1,.03)
    def test_duplicate_triangle_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            mesh=trimesh.creation.box(); mesh.faces=np.vstack([mesh.faces,mesh.faces[0]]); path=Path(d)/'bad.stl'; mesh.export(path)
            with self.assertRaises(ValueError): v.validate_mesh(path,np.ones(3),1,.03)
    def test_failure_replaces_stale_success(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); model=root/'model.py'; out=root/'out'; out.mkdir(); (out/'validation.json').write_text('{"success":true}')
            model.write_text("import cadquery as cq\ndef build(**p):\n return cq.Workplane('XY').circle(2).wire()\n")
            with self.assertRaises(ValueError): v.export_model(model,out)
            self.assertFalse(json.loads((out/'validation.json').read_text())['success'])
    def test_build_failure_invalidates_stale_success(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); model=root/'model.py'; out=root/'out'; out.mkdir()
            (out/'validation.json').write_text('{"success":true}')
            model.write_text("def build(**p):\n raise RuntimeError('build failed')\n")
            with self.assertRaises(RuntimeError): v.export_model(model,out)
            self.assertFalse(json.loads((out/'validation.json').read_text())['success'])
    def test_unsafe_names_and_empty_assembly_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); model=root/'model.py'
            for result in ["{}", "{'../bad':cq.Workplane('XY').box(1,1,1)}", "{'A':cq.Workplane('XY').box(1,1,1),'a':cq.Workplane('XY').box(1,1,1)}"]:
                model.write_text('import cadquery as cq\ndef build(**p):\n return '+result+'\n')
                with self.assertRaises(ValueError): v.export_model(model,root/'out')

if __name__=='__main__': unittest.main()
