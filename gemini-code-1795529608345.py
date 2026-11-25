import struct
import math

def make_box(cx, cy, cz, sx, sy, sz):
    """Generates 12 outward-facing triangles for an axis-aligned box."""
    hx, hy, hz = sx / 2.0, sy / 2.0, sz / 2.0
    v = [
        (cx - hx, cy - hy, cz - hz), # 0
        (cx + hx, cy - hy, cz - hz), # 1
        (cx + hx, cy + hy, cz - hz), # 2
        (cx - hx, cy + hy, cz - hz), # 3
        (cx - hx, cy - hy, cz + hz), # 4
        (cx + hx, cy - hy, cz + hz), # 5
        (cx + hx, cy + hy, cz + hz), # 6
        (cx - hx, cy + hy, cz + hz), # 7
    ]
    faces = [
        (0, 3, 2), (0, 2, 1), # -Z
        (4, 5, 6), (4, 6, 7), # +Z
        (0, 1, 5), (0, 5, 4), # -Y
        (2, 3, 7), (2, 7, 6), # +Y
        (0, 4, 7), (0, 7, 3), # -X
        (1, 2, 6), (1, 6, 5), # +X
    ]
    return [(v[a], v[b], v[c]) for a, b, c in faces]

def make_cylinder_y(cx, cy, cz, radius, height, segments=28):
    """Generates triangles for a vertical cylinder aligned along the Y axis."""
    hy = height / 2.0
    y_bot, y_top = cy - hy, cy + hy
    tris = []
    for i in range(segments):
        a0 = 2.0 * math.pi * i / segments
        a1 = 2.0 * math.pi * (i + 1) / segments
        x0, z0 = cx + radius * math.cos(a0), cz + radius * math.sin(a0)
        x1, z1 = cx + radius * math.cos(a1), cz + radius * math.sin(a1)
        # Top cap
        tris.append(((cx, y_top, cz), (x1, y_top, z1), (x0, y_top, z0)))
        # Bottom cap
        tris.append(((cx, y_bot, cz), (x0, y_bot, z0), (x1, y_bot, z1)))
        # Side quad
        tris.append(((x0, y_bot, z0), (x0, y_top, z0), (x1, y_top, z1)))
        tris.append(((x0, y_bot, z0), (x1, y_top, z1), (x1, y_bot, z1)))
    return tris

def compute_normal(p1, p2, p3):
    ux, uy, uz = p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]
    vx, vy, vz = p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]
    nx = uy * vz - uz * vy
    ny = uz * vx - ux * vz
    nz = ux * vy - uy * vx
    length = math.sqrt(nx*nx + ny*ny + nz*nz) or 1.0
    return (nx / length, ny / length, nz / length)

def generate_aquaclean_stl(filename="aquaclean_fpv.stl"):
    triangles = []

    # Scale: 1 unit = 1 mm (1:10 scale prototype, ~165mm wide x 70mm long)
    panel_span = 140.0
    robot_length = 64.0

    # 1. Main Top Bridge Chassis
    triangles += make_box(0, 22.0, 0, robot_length, 8.0, panel_span + 22.0)

    # 2. Top IP67 Electronics & Micro-Mist Tank Enclosure
    triangles += make_box(0, 31.0, 0, 34.0, 10.0, 52.0)

    # 3. Dual C-Clamp Side Arms & Bottom Locking Lips
    for side in (-1, 1):
        z_arm = side * (panel_span / 2.0 + 7.5)
        # Vertical side bracket
        triangles += make_box(0, 11.0, z_arm, robot_length, 26.0, 7.0)
        # Bottom C-clamp hook lip (grips underside of solar frame)
        z_lip = side * (panel_span / 2.0 + 2.0)
        triangles += make_box(0, 0.0, z_lip, robot_length, 5.0, 16.0)

        # Nested Track Wheel Housings (front & rear)
        for wx in (-22.0, 22.0):
            triangles += make_box(wx, 14.0, side * (panel_span / 2.0 - 2.0), 10.0, 8.0, 8.0)

    # 4. Staggered 5-Brush Matrix on Underside
    brush_coords = [
        (-14.0, -46.0),
        ( 14.0, -23.0),
        (-14.0,   0.0),
        ( 14.0,  23.0),
        (-14.0,  46.0),
    ]
    for bx, bz in brush_coords:
        # Motor shaft
        triangles += make_cylinder_y(bx, 15.0, bz, radius=3.5, height=8.0)
        # Rotary brush pad
        triangles += make_cylinder_y(bx, 10.0, bz, radius=15.0, height=4.0)

    # Write Binary STL
    with open(filename, "wb") as f:
        header = b"AquaClean FPV 3D Printable Model - Hackwarts 2026".ljust(80, b"\0")
        f.write(header)
        f.write(struct.pack("<I", len(triangles)))
        for p1, p2, p3 in triangles:
            n = compute_normal(p1, p2, p3)
            f.write(struct.pack("<3f", *n))
            f.write(struct.pack("<3f", *p1))
            f.write(struct.pack("<3f", *p2))
            f.write(struct.pack("<3f", *p3))
            f.write(struct.pack("<H", 0))

    print(f"Successfully generated {filename} with {len(triangles)} triangles.")

if __name__ == "__main__":
    generate_aquaclean_stl()