// Metric Screw Thread Library
// by Maximilian Karl <karlma@in.tum.de> (2014)
// modified the api to create internal threads, smooth the start and
// stop threads, and use imperial units: 
//
//
//
// use module thread_imperial(pitch, majorD, stepAngle, numRotations, tol, internal) 
//         or thread(pitch, majorD, stepAngle, numRotations, tol, internal)
// with the parameters:
// pitch        - screw thread pitch
// majorD       - screw thread major diameter
// step         - step size in degrees (36 gives ten steps per rotation)
// numRotations - the number of full rotations of the thread
// tol          - (optional parameter for internal threads) the amount to increase the 
//                 thread size in mm.Default is 0
// internal     - (optional parameter for internal threads) - this can be set true or  
//                false.  Default is true
//
// Performance improvements by Volker Schuller

root3 = sqrt(3);

//-----------------------------------------------------------------------------------------------
//EXAMPLES:
//example: this creates a 3/8-inch 16TPI bolt using metric units
thread(1.5875, 9.5250, 12, 12);

//the same thread using imperial units
//thread_imperial(1/16,3/8,12,12);

//an internal thread that will accomodate the two examples above
translate([15, 0, 0]) {
    difference() {
        cylinder(r = 8, h = 8);
        translate([0, 0, -1.5875 / 2])
        thread(1.5875, 9.5250, 12, 8, 0.2, true);
    }
}
//------------------------------------------------------------------------------------------------

//Creates a thread cross section starting with an equilateral triangle
//and removing the point.  Internal threads (for creating nuts) will 
//have a non-zero tolerance value which enlarges the triangle to
//accomodate a bolt of the same size
function screwthread_triangle(P, tol) =
let (a = P + 2 * tol,
    h = root3 * a / 2,
    y = P / 16 + tol / root3,
    x1 = root3 * P / 16 - P * h / a + tol * 2,
    x2 = root3 / 16 * P - h + tol * 2)
        [[tol, -y], [tol, y], [x1, P / 2], [x2, P / 2], [x2, -P / 2 + 0.00001], [x1, -P / 2 + 0.00001]];

//Creates a polyhedron by placing the triangle points along the thread and connecting them with faces
module threadPolyhedron(P, D_maj, step, rotations, tol) {
    t = screwthread_triangle(P, tol);
    n = floor(360 / step) * rotations;
    points = [for (i = [0: step: 360 * rotations], p = t)
        let (d = p[0] + D_maj / 2)
        [d * cos(i), d * sin(i), p[1] + i / 360 * P]
    ];
    faces = concat([[0, 5, 4], [1, 3, 2], [0, 3, 1], [0, 4, 3],
        [6 * n, 6 * n + 4, 6 * n + 5],[6 * n + 1, 6 * n + 2, 6 * n + 3],
        [6 * n, 6 * n + 1, 6 * n + 3],[6 * n, 6 * n + 3, 6 * n + 4]],
        [for (i = [0: n - 1], j = [0: 5])[i * 6 + j, i * 6 + 1 + j, i * 6 + 6 + j]],
        [for (i = [0: n - 1], j = [0: 4])[i * 6 + 1 + j, i * 6 + 7 + j, i * 6 + 6 + j]],
        [for (i = [0: n - 1])[i * 6 + 6, i * 6 + 5, i * 6]]);
    polyhedron(points = points, faces = faces);
}

//creates a thread using inches as units (tol is still in mm)
module thread_imperial(pitch, majorD, stepAngle, numRotations, tol = 0, internal = false) {
    p = pitch * 25.4;
    d = majorD * 25.4;
    thread(p, d, stepAngle, numRotations, tol);
}

//creates a thread using mm as units
module thread(P, D, step, rotations, tol = 0, internal = false) {
    // added parameter "rotations"
    // as proposed by user bluecamel
    D_min = D - 5 * root3 / 8 * P;
    if (internal == false) {
        difference() {
            threadPolyhedron(P, D, step, rotations, 0);

            //The first and last portion of external threads (for making bolts)
            //are tapered at a 20 degree angle for an easier fit
            translate([D / 2 - P / 2, 0, -P / 2])
            rotate(-20, [0, 0, 1]) translate([0, -P * 5, 0])
            cube([P, P * 10, P]);

            translate([D / 2 - P / 2, 0, (rotations - 0.5) * P])
            rotate(20, [0, 0, 1]) translate([0, -P * 5, 0])
            cube([P, P * 10, P]);
        }
    } else {
        threadPolyhedron(P, D + tol, step, rotations, tol);
    }
    //make the cylinder a little larger if this is to be an internal thread
    translate([0, 0, (rotations * 0.5) * P])
    if (internal == false) {
        cylinder(r = D_min / 2, h = (rotations + 1) * P, $fn = 360 / step, center = true);
    } else {
        cylinder(r = D_min / 2 + tol, h = (rotations + 1) * P, $fn = 360 / step, center = true);
    }
}