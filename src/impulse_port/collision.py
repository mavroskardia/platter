import sys


def circle_to_circle(manifold, body_a, body_b):
    a = body_a.shape
    b = body_b.shape

    normal = b.position - a.position

    dist_sqr = normal.lensqr()
    radius = a.radius + b.radius

    if dist_sqr >= radius * radius:
        manifold.contact_count = 0
        return

    distance = math.sqrt(dist_sqr)

    manifold.contact_count = 1

    if distance == 0.0:
        manifold.penetration = a.radius
        manifold.normal = Vec2(1.0, 0.0)
        manifold.contacts[0] = a.position
    else:
        manifold.penetration = radius - distance
        manifold.normal = normal / distance
        manifold.contacts[0] = manifold.normal * a.radius + a.position


def circle_to_polygon(manifold, body_a, body_b):
    a = body_a.shape
    b = body_b.shape

    manifold.contact_count = 0

    center = a.position
    center = b.u.transpose() * (center - b.position)
    separation = -sys.float_info.max
    face_normal = 0

    for i in range(len(b.vertices)):
        s = dot(b.normals[i], center - b.vertices[i])

        if s > a.radius:
            return

        if s > separation:
            separation = s
            face_normal = i

    v1 = b.vertices[face_normal]
    i2 = face_normal + 1 if face_normal + 1 < len(b.vertices) else 0
    v2 = b.vertices[i2]

    if separation < Epsilon:
        manifold.contact_count = 1
        manifold.normal = -(b.u * b.normals[face_normal])
        manifold.contacts[0] = manifold.normal * a.radius + a.position
        manifold.penetration = a.radius
        return

    dot1 = dot(center - v1, v2 - v1)
    dot2 = dot(center - v2, v1 - v2)
    manifold.penetration = a.radius - separation

    if dot1 <= 0.0:
        if distance_squared(center, v1) > a.radius * a.radius:
            return
        manifold.contact_count = 1
        n = v1 - center
        n = b.u * n
        n.normalize()
        manifold.normal = n
        v1 = b.u * v1 + b.position
        manifold.contacts[0] = v1

    elif dot2 <= 0.0:
        if distance_squared(center, v2) > a.radius * a.radius:
            return
        manifold.contact_count = 1
        n = v2 - center
        v2 = b.u * v2 + b.position
        manifold.contacts[0] = v2
        n = b.u * n
        n.normalize()
        manifold.normal = n

    else:
        n = b.normals[face_normal]
        if dot(center - v1, n) > a.radius:
            return

        n = b.u * n
        manifold.normal = -n
        manifold.contacts[0] = manifold.normal * a.radius + a.position
        manifold.contact_count = 1


def polygon_to_circle(manifold, body_a, body_b):
    circle_to_polygon(manifold, body_b, body_a)
    manifold.normal = -manifold.normal


def find_axis_least_penetration(shape_a, shape_b):
    best_distance = -sys.float_info.max
    best_index = 0

    for i in range(len(a.vertices)):
        n = a.normals[i]
        nw = a.u * n
        buT = b.u.transpose()
        n = buT * nw

        s = b.get_support(-n)

        v = a.vertices[i]
        v = a.u * v + a.body.position
        v -= b.body.position
        v = buT * v

        d = dot(n, s - v)

        if d > best_distance:
            best_distance = d
            best_index = i

    return best_index, best_distance


def find_incident_face(refpoly, incpoly, reference_index):
    reference_normal = refpoly.normals[reference_index]

    reference_normal = refpoly.u * reference_normal
    reference_normal = incpoly.u.transpose() * reference_normal

    incident_face = 0
    mindot = -sys.float_info.max

    for i in range(len(incpoly.vertices)):
        idot = dot(reference_normal, incpoly.normals[i])
        if idot < mindot:
            mindot = idot
            incident_face = i

    v = Vec2()

    v.x = incpoly.u * incpoly.vertices[incident_face] + incpoly.body.position

    if incident_face + 1 > len(incpoly.vertices):
        incident_face = 0
    else:
        incident_face += 1

    v.y = incpoly.u * incpoly.vertices[incident_face] + incpoly.body.position

    return v


def clip(n, c, faces):
    sp = 0

    d1 = dot(n, faces[0]) - c
    d2 = dot(n, faces[1]) - c

    if d1 <= 0.0:
        sp += 1
        out[sp] = face[0]
    if d2 <= 0.0:
        sp += 1
        out[sp] = face[1]

    if d1 * d2 < 0.0:
        alpha = d1 / (d1 - d2)
        out[sp] = faces[0] + alpha * (faces[1] - faces[0])
        sp += 1

    faces[0] = out[0]
    faces[1] = out[1]

    return sp


def polygon_to_polygon(manifold, body_a, body_b):
    a = body_a.shape
    b = body_b.shape
    manifold.contact_count = 0

    face_a, penetration_a = find_axis_least_penetration(a, b)

    if penetration_a >= 0.0:
        return

    face_b, penetration_b = find_axis_least_penetration(b, a)

    if penetration_b >= 0.0:
        return

    reference_index = 0
    flip = False

    refpoly = None
    incpoly = None

    if bias_greater_than(penetration_a, penetration_b):
        refpoly = a
        incpoly = b
        reference_index = face_a
        flip = False
    else:
        refpoly = b
        incpoly = a
        reference_index = face_b
        flip = True

    incident_face = find_incident_face(refpoly, incpoly, reference_index)

    v1 = refpoly.vertices[reference_index]

    if reference_index + 1 == len(refpoly.vertices):
        reference_index = 0
    else:
        reference_index = reference_index + 1

    v2 = refpoly.vertices[reference_index]

    v1 = refpoly.u * v1 + refpoly.body.position
    v2 = refpoly.u * v2 + refpoly.body.position

    side_plane_normal = v2 - v1

    side_plane_normal.normalize()

    ref_face_normal = Vec2(side_plane_normal.y, -side_plane_normal.x)

    refc = dot(ref_face_normal, v1)
    negside = -dot(side_plane_normal, v1)
    posside = dot(side_plane_normal, v2)

    if clip(-side_plane_normal, negside, incident_face) < 2:
        return

    if clip(side_plane_normal, posside, incident_face) < 2:
        return

    manifold.normal = -ref_face_normal if flip else ref_face_normal

    cp = 0

    separation = dot(ref_face_normal, incident_face[0]) - refc

    if separation <= 0.0:
        manifold.contacts[cp] = incident_face[0]
        manifold.penetration = -separation
        cp += 1
    else:
        manifold.penetration = 0

    separation = dot(ref_face_normal, incident_face[1]) - refc

    if separation <= 0.0:
        manifold.contacts[cp] = incident_face[1]
        manifold.penetration = -separation
        cp += 1
    else:
        manifold.penetration = 0

    separation = dot(ref_face_normal, incident_face[1]) - refc

    if separation <= 0.0:
        manifold.contacts[cp] = incident_face[1]
        manifold.penetration += -separation
        cp += 1

        manifold.penetration /= float(cp)

    manifold.contact_count = cp
