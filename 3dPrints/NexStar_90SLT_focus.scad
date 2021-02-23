/* Celestron NexStar 90SLT AutoFocus - Dave Hartburn, Jan 2021
 * 
 * Uses a 28BYJ-48 stepper motor for focus control of a NexStar
 * 90SLT, fitting over the stock focus knob, but also being easily
 * removable for manual control.
 *
 * One problem with this 90mm scope, compared to other focus solutions
 * is the narrow gap between the knob and the eyepiece shaft, with only
 * about 7mm of space to play with. With the knob diam about 18.5mm, that
 * gives a maximum size of 32.5mm
 *
 */

// Import gear generator. Originally intended for lego gears, but I liked
// the size and teeth. Besides, could be interesting making it lego compatible
use <gear-v3-solid.scad>
use <StepMotor-28BYJ.scad>

$fn=256;

// Define a few variables
focusOffset=40;         // Distance of middle of focus knob from scope middle
stepperDist=69.5;         // How far should the centre of the stepper be?
stepperAng=0;          // What angle clockwise from 3 o'clock should it be?
                        // A motor straight out may get in the way of the wedge
                        // and mount

// Control shown parts for printing
showFocusRing=0;     // The main ring cog which fits over the focusser knob
showMounting=1;
showMountCover=0;
showMotorCog=0;

// Do not print!
showScope=0;        // Show the telescope - useful for planning
showMotor=0;

/* ************* NEED SCREW HOLES!!!! ***************** */

if(showFocusRing==1) {
    translate([focusOffset, 0, 15]) {
        focusRing();
    }
}
if(showMounting==1) {
    mounting();
}
if(showMountCover==1) {
    color([0.5,0.5,1]) mountCover();
}

if(showMotorCog==1) {
    rotate([0,0,-stepperAng]) {
        translate([stepperDist-8,0,1.6]) {
            motorCog();
        }
    }
}

if(showScope==1) {
    // Show the scope with the eyepiece end at z=0
    translate([0,0,-230]) {
        nexstar90slt();
    }
}

if(showMotor==1) {
    // Show the stepper motor
    rotate([0,0,-stepperAng]) {
        translate([stepperDist,0,-9.5]) {
                rotate([180,0,180]) StepMotor28BYJ();
        }
    }
}

/* ******* Modules ******* */
module mounting() {
    /* There is a small gap formed under the dovetail mount.
     * Removing this allows a mounting arm to be slipped underneath.
     *
     * Wedge dimensions:
     *   Length = 80mm
     *   Inner width = 28mm
     *   Screw size = 4.5mm
     *   Screw hole from edge = 12.7mm
     *   Wedge from scope end = 23mm
     *   First screw hole from scope end = 35.5mm
     *   Gap depth = 3.3mm
     *   Scope tube diameter = 104mm
     */

    barLength = 103;    // 80+23
    
    // Draw main bar
    translate([0,0,-barLength]) {
        difference() {
            // Cut a 28mm wide section along the X axis
            union() {
                intersection() {
                    cylinder(h=barLength, d=110);
                    translate([0,-14,0]) {
                        cube([70,28,barLength]);
                    }
                }
                translate([0,0,barLength-21]) {
                    stepperHousing(21);
                }
            }
            translate([0,0,-1]) cylinder(h=barLength+2, d=104);
            // Cut out screw holes
            translate([0,0,12.7]) {
                rotate([0,90,0]) {
                    cylinder(h=140, d=6);
                }
            }
            translate([0,0,80-12.7]) {
                rotate([0,90,0]) {
                    cylinder(h=140, d=6);
                }
            }
        }
    }
    // Add some level of restraint so we don't have such a severe
    // angle going to the motor housing, which might get knocked and stress it
    translate([107/2,-14,-23]) {
        hull() {
            cube([1,28,2.5]);
            translate([7,0,2]) {
                cube([0.1,28,0.5]);
            }
        }
    }
}

module stepperHousing(h) {
    // A surround for the stepper motor, height h
    // Draws from the centre as the tube cutout will cut the
    // extra section off anyway
    innerD = 28.5;
    th = 2;
    outerD = innerD + th*2;
    contW = 20.5;     // Width for controller plus a margin
    
    translate([0,-outerD/2,0]) {
        difference() {
            union() {
                // The main round part
                hull() {
                    cube([0.1,outerD,h]);
                    translate([stepperDist,outerD/2,0]) {
                        cylinder(d=outerD, h=h);
                    }
                }
                // Controller holder
                translate([stepperDist,outerD/2-contW/2-th,0]) {
                    cube([outerD/2+3.5,contW+2*th,h]);
                }
                // Screw lugs
                translate([stepperDist,+th-3.5,0]) {
                    cylinder(h=h, d=8);
                }
                translate([stepperDist,outerD-th+3.5,0]) {
                    cylinder(h=h, d=8);
                }
            }
            translate([stepperDist,outerD/2,h-19]) {
                cylinder(d=innerD, h=h);
                // Cut out for the controller
                translate([0,-contW/2,0]) {
                    cube([innerD/2+3.5,contW,h]);
                }
                // Recess for screw lugs
                translate([-4,-outerD,18]) {
                    cube([8,outerD*2,2]);
                }
                // Cut out for the wires
                translate([0,-3,19-3.5]) {
                    cube([outerD,6,6]);
                }
                // Cut out the screw shafts
                translate([0,-innerD/2-3.5,-th-1]) {
                    cylinder(h=h*2, d=4.6);
                }
                translate([0,innerD/2+3.5,-th-1]) {
                    cylinder(h=h*2, d=4.6);
                }
            }
        }
    }
}

module mountCover() {
    // Makes a cap on top of the motor.
    
    // For consistancy (and probably laziness), use the stepper
    // housing and take a slice. Need to take away the curve
    // same as we do in mounting()
    // The top of the mounting is z=0, which means we don't need to move this
    difference() {
        intersection() {
            stepperHousing(21);
            translate([0,-30,0]) {
                cube([200,60,2]);
            }
        }
        translate([0,0,-1]) cylinder(h=23, d=104);
        // Cut out for motor spindle
        translate([stepperDist-8,0,-1]) {
            cylinder(h=4,d=11);
        }
    }
}

module focusRing() {
    // The cog which fits over the focus control
    
    difference() {
        // 29 teeth gives an outer diameter of 31mm
        // Put a small disc on the top to stop it slipping down past the
        // motor cog
        union() {
            myGearSolid(29, gearHeight=6);
            translate([0,0,6]) {
                cylinder(h=1, d=32);
            }
        }
        //cylinder(h=1.6, d=31);    // Small ring to see if it fits

        translate([0,0,-18]) focusKnob();
    }
}

module motorCog() {
    // The cog that fits on top of the motor
    shaftWidth=9;       // Shoud make it 5mm thick around a 5mm motor shaft
    cogHeight=6;
    cogElev=12.5;          // How high the base of the cog is
    cogTeeth=17;
    
    difference() {
        union() {
            cylinder(d=shaftWidth,h=cogHeight+cogElev);
            translate([0,0,cogElev]) {
                color([0.8,0.8,0.5]) myGearSolid(cogTeeth, gearHeight=6);
            }
        }
        translate([0,0,-0.5]) StepMotor28BYJ_Shaft(0.2);
    }
}

module focusKnob() {
    // Draws a replica of the focus knob, with a slightly larger
    // margain, in order to be able to cut it away
    
    // Define basic characteristics
    length=34.5;
    mainDiam=19.3;      // Calipers read 18.5
    ribDiam=2;          // Reading 1.8
    ribHeight=1;
    ribCount=10;        // Even spacing
    ribLength=20;
    
    // Main cylinder
    cylinder(h=length, d=mainDiam);
    
    // Draw the ribs
    // Calculate the angle between ribs
    ribAng=360/ribCount;
    translate([0,0,length-ribLength]) {
        for(a = [0:ribCount]) {
            rotate([0,0,a*ribAng]) {
                translate([0,mainDiam/2+(ribDiam/2-ribHeight),0]) {
                    // Use the hull function to make a 'gravestone' cross section
                    hull() {
                        cylinder(h=ribLength, d=ribDiam);
                        translate([-ribDiam/2,-ribDiam/2,0]) {
                            cube([ribDiam,0.01,ribLength]);
                        }
                    }
                }
            }
        }       
    }
}

module nexstar90slt() {
    // A crude representation of a celestron nexstar 90slt
    // Enough for planning autofocus layout. Orientated 
    // aperture down

    // For reference, the inner diameter once the end is 
    // screwed off is 45.5mm
    
    // Main tube
    color([0.45,0.45,0.45]) cylinder(d=104.4, h=230);
    color([0.2,0.2,0.2]) translate([0,0,230]) {
        cylinder(d=54,h=12);
        cylinder(d=44, h=42);
        // Focus knob
        translate([focusOffset,0,0]) {
            focusKnob();
        }
        // Wedge, probably not the correct angle, but rough enough
        translate([0,0,-80-23.5]) {
            hull() {
                cylinder(h=80, d=2);
                translate([(104.4/2)+11.75, -21.5, 0]) {
                    cube([0.5, 43, 80]);
                }
            }
        }
    }
}

module roundedArc(diam, height, cent, ang) {
    // Produces an arc with rounded ends, as if a cylinder had been
    // Dragged by a compass. Arc describes the centres of the two cylinders
    // diam = diameter of the cylinder, height = height of arc
    // cent = distance of arc from circle centre
    // ang = angle it has been dragged through
    $fn=256;
    
    translate([cent+diam/2,0,0]) cylinder(h=height, d=diam);
    rotate([0,0,ang]) translate([cent+diam/2,0,0]) cylinder(h=height, d=diam);
    rotate_extrude(angle=ang)
        translate([cent, 0, 0])
            square([diam,height]);    
}
