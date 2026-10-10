"""Check exported STEP assembly interfaces, write an assembled STEP and geometry preview."""
import argparse
import json
from pathlib import Path
import cadquery as cq
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

p=argparse.ArgumentParser(); p.add_argument('directory',type=Path); args=p.parse_args(); root=args.directory
parts={n:cq.importers.importStep(str(root/f'{n}.step')).val() for n in ['body','compression_cap','tpu_insert']}
body=parts['body']; cap=parts['compression_cap']; seal=parts['tpu_insert']
initial_cap=cap.translate((0,0,10)); initial_seal=seal.translate((0,0,13))
checks=[]
for travel in [0,.2,.4,.6,.8]:
    moved=cap.rotate((0,0,0),(0,0,1),-360*travel/2).translate((0,0,10-travel))
    overlap=body.intersect(moved).Volume()
    if overlap > 1e-5: raise ValueError(f'Rigid collision at {travel} mm: {overlap} mm3')
    checks.append({'cap_travel_mm':travel,'cap_rotation_deg':-360*travel/2,'rigid_overlap_mm3':overlap})
for label,a,b in [('body_insert',body,initial_seal),('cap_insert',initial_cap,initial_seal)]:
    overlap=a.intersect(b).Volume()
    if overlap > 1e-5: raise ValueError(f'{label} unintended initial interference: {overlap}')
# Full length nominal cable must pass through each undeformed component.
cable=cq.Solid.makeCylinder(9.1/2,26,cq.Vector(0,0,-1))
for name,shape in [('body',body),('cap',initial_cap),('insert',initial_seal)]:
    if shape.intersect(cable).Volume()>1e-5: raise ValueError(f'Cable clashes with {name}')
assembly=cq.Assembly(name='cable_gland_9p1')
for name,shape in [('body',body),('compression_cap',initial_cap),('tpu_insert',initial_seal)]: assembly.add(shape,name=name)
assembly.save(str(root/'assembly.step'))
report={'success':True,'rigid_travel_checks':checks,'cable_od_mm':9.1,'nominal_passage_mm':9.3,
 'initial_insert_clearance_radial_mm':.1,'body_root_wall_at_pocket_mm':1.5,
 'cap_min_wall_at_thread_crest_mm':1.75,'cap_roof_thickness_mm':3.0,
 'compressed_insert_height_target_mm':7.2,'panel_thread':'Custom nominal 16 mm x 2 mm pitch; not ISO M16',
 'cap_thread':'Custom nominal 20 mm x 2 mm pitch; 0.25 mm radial and 0.12 mm axial flank clearance',
 'limitations':['TPU deformation not simulated. Cable gripping and sealing require physical testing.',
 'Wall figures are analytical nominal section dimensions, not a global thickness scan.',
 'Compression travel sampled at 0.2 mm intervals, not a continuous collision proof.']}
(root/'assembly_validation.json').write_text(json.dumps(report,indent=2)+'\n')
fig=plt.figure(figsize=(12,6),facecolor='#f5f6f8')
colors={'body':'#508ba8','compression_cap':'#e6a54b','tpu_insert':'#525964'}
for index,(title,offsets) in enumerate([('Assembled • 9.1 mm cable',{'body':0,'tpu_insert':13,'compression_cap':10}),('Exploded • body / TPU insert / cap',{'body':0,'tpu_insert':25,'compression_cap':39})]):
    ax=fig.add_subplot(1,2,index+1,projection='3d',computed_zorder=False)
    for name in ['body','tpu_insert','compression_cap']:
        mesh=trimesh.load_mesh(root/f'{name}.stl'); mesh.apply_translation([0,0,offsets[name]])
        poly=Poly3DCollection(mesh.triangles,facecolors=colors[name],edgecolor='none',alpha=1,shade=True,zorder=2)
        poly.set_zsort('average'); ax.add_collection3d(poly)
    if index==0:
        mesh=trimesh.creation.cylinder(radius=4.55,height=38,sections=48);mesh.apply_translation([0,0,12])
        ax.add_collection3d(Poly3DCollection(mesh.triangles,facecolor='#383c43',edgecolor='none',zorder=1))
    ax.set_xlim(-17,17); ax.set_ylim(-17,17); ax.set_zlim(-7,32 if index==0 else 58)
    ax.set_box_aspect((34,34,39 if index==0 else 65)); ax.view_init(elev=23,azim=-55)
    ax.set_title(title,pad=12);ax.set_axis_off()
fig.tight_layout();fig.savefig(root/'preview.png',dpi=160,bbox_inches='tight');plt.close(fig)
print(json.dumps(report,indent=2))
