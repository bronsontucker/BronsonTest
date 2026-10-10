"""Three-piece printable gland. All dimensions in mm; custom 2 mm pitch threads."""
import math
import cadquery as cq

DEFAULTS = dict(cable_od=9.1, passage_clearance=0.2, thread_clearance=0.25,
               flank_clearance=0.12, pitch=2.0, seal_od=14.6, pocket_od=14.8,
               body_af=22.0, cap_af=24.0, compression=0.0)

def helix_ridge(root, crest, pitch, length, z, flank=0.0):
    # A truncated trapezoid, embedded 0.15 mm in its supporting cylinder.
    base_half = 0.70 + flank
    tip_half = 0.18 + flank
    path = cq.Wire.makeHelix(pitch, length, root)
    ridge = (cq.Workplane('XZ').polyline([(root-.15,-base_half),
        (crest,-tip_half),(crest,tip_half),(root-.15,base_half)]).close()
        .sweep(cq.Workplane(obj=path), isFrenet=True))
    return ridge.translate((0,0,z))

def cylinder(radius, height, z=0):
    return cq.Workplane('XY').workplane(offset=z).circle(radius).extrude(height)

def hexagon(af, height, z=0):
    return cq.Workplane('XY').workplane(offset=z).polygon(6,af/math.cos(math.pi/6)).extrude(height)

def build(**params):
    unknown=set(params)-set(DEFAULTS)
    if unknown: raise ValueError(f'Unknown parameters: {sorted(unknown)}')
    p={**DEFAULTS, **params}
    if not all(math.isfinite(float(v)) for v in p.values()): raise ValueError('Nonfinite parameter')
    if not 8.5 <= p['cable_od'] <= 9.5: raise ValueError('This housing supports cable OD 8.5–9.5 mm')
    if not 0 <= p['compression'] <= 0.8: raise ValueError('Compression travel must be 0–0.8 mm')
    if not 0.15 <= p['thread_clearance'] <= 0.35: raise ValueError('Use radial thread clearance 0.15–0.35')
    if not (0 < p['passage_clearance'] <= .5 and 0 <= p['flank_clearance'] <= .2): raise ValueError('Invalid clearance')
    if not 1.8 <= p['pitch'] <= 2.2: raise ValueError('Pitch out of tested range')
    if not 14.4 <= p['seal_od'] < p['pocket_od'] <= 15.0: raise ValueError('Invalid seal/pocket diameter')
    if p['body_af'] < 22 or p['cap_af'] < 24: raise ValueError('Hex flats too small')
    bore=(p['cable_od']+p['passage_clearance'])/2
    pitch=p['pitch']
    # Panel spigot: custom nominal 16 x 2 thread, 6 mm long.
    mount=cylinder(7.0,6).union(helix_ridge(7.0,8.0,pitch,4.5,.75))
    flange=hexagon(p['body_af'],3,6)
    barrel=cylinder(8.9,11,9).union(helix_ridge(8.9,10,pitch,9.5,9.75))
    body=mount.union(flange).union(barrel).cut(cylinder(bore,22,-1))
    body=body.cut(cylinder(p['pocket_od']/2,8,13))
    # Small bore chamfer reduces cable jacket scraping.
    body=body.cut(cq.Solid.makeCone(bore+.3,bore,.3,cq.Vector(0,0,0)))
    # Cap in assembly coordinates; matching helical cutter includes radial and axial fit allowance.
    cap=hexagon(p['cap_af'],14,10)
    cap=cap.cut(cylinder(8.9+p['thread_clearance'],11.01,9.99))
    cutter=helix_ridge(8.9+p['thread_clearance'],10+p['thread_clearance'],pitch,14,9.75-pitch,p['flank_clearance'])
    cutter=cutter.intersect(cylinder(11,11.01,9.99))
    cap=cap.cut(cutter).cut(cylinder(bore+.1,16,9))
    # Bore lead-in at cap mouth eases initial engagement.
    mouth=cq.Solid.makeCone(10.5,9.15,1.35,cq.Vector(0,0,10))
    cap=cap.cut(mouth).edges('>Z').chamfer(.35)
    # Each export rests on Z=0 for printing. Placement is in assembly_positions().
    seal=cylinder(p['seal_od']/2,8).cut(cylinder(bore,10,-1))
    seal=seal.edges().chamfer(.15)
    return {'body':body, 'compression_cap':cap.translate((0,0,-10)), 'tpu_insert':seal}

def assembly_positions(**params):
    p={**DEFAULTS,**params}
    travel=p['compression']
    return {'body':(0,0,0),'compression_cap':(0,0,10-travel),'tpu_insert':(0,0,13)}
