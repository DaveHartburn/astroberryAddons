/* Astroberry Case - Dave Hartburn Jan 2021
 *
 * Contains a Pi 4, a power convertor, a relay board,
 * a stepper motor driver and a IO shield with a display
 *
 * For details see: *** Link to blog post ***
 */
 
 
/* **** FAULTS *****
 * Side port holes need to be a little bigger, inc audio
 * Power socket holders shorter
 * Smaller screws for Pi, 3mm too big
 */
 
// Include libraries for the hardware
use <Pi_Hardware/RPi4board-modded.scad>;
use <Libs/simplethreads.scad>

$fn=256;

// Basic settings
baseTH=2;   // Thickness of the base
th=2;       // Wall thickness
intSize=[100.5, 110,27];    // The interior size
soH=5;      // Height of standoffs
soTH=2;     // Stand off wall thickness
// Define a list of top screw x,y positions. The third component is rotation, not z
topScrews= [ [25,th+3.5,90 ], [intSize.x-25,th+3.5,90 ], 
        [th+3.5,74, 0], [intSize.x-th,85, 180] ];

// What to show (1 show, 0 don't
showPi=1;
showBoards=1;   // The other boards
showSocket=1;   // The 12v socket
showBase=1;     // Bottom half of the case
showLid=0;      // Case lid
showButton=1;   // Button cap
// Rear holder
showHolder=0;   // The main part of disk and battery
showHoldBack=0; // The clamp back part
showHoldScrews=0;   // Screws to hold the clamp

// Positions
// Reference - Pi is 56mm wide, 85mm long, excluding overhanging components
piPos=[46,26,baseTH+soH];
relayPos=[-42,85-50,0];
relayRot=180;
stepDrivPos=[-43,10,0];
stepDrivRot=90;
stepExtendPos=[th,9,19];
stepExtendRot=0;

powConvPos=[-40, -23,0];
powConvRot=90;
socketPos=[76,20,baseTH];
socketRot=270;

if(showBase==1) {
    astroPiBase();
}

if(showLid==1) {
    astroPiLid();
}

if(showButton==1) {
    astroPiButton();
}

// Show the Pi?
if(showPi==1) {
    translate(piPos) {
        board_raspberrypi_4_model_b();
    }
}

if(showBoards==1) {
    translate(piPos) {
        translate(relayPos) {
            two_channel_relay(relayRot);
        }
        translate(stepDrivPos) {
            uln2003_module(stepDrivRot);
        }
        translate(powConvPos) {
            step_down_module(powConvRot);
        }
        translate([-1.45,-2.7,12.25]) ioBoard();
    }
    translate(stepExtendPos) stepExtender(stepExtendRot);

}

if(showSocket==1) {
    translate(socketPos) {
        rotate(socketRot) 55dc_jack_female();
    }
}

if((showHolder+showHoldBack+showHoldScrews)>0) {
    //rotate([-90,0,0]) {
        translate([0,0,25]) {
        holder(showHolder,showHoldBack,showHoldScrews);
        }
    //}
}

// The base
module astroPiBase() {
    difference() {
        roundedCube([intSize.x+th*2, intSize.y+th*2, intSize.z+baseTH], 4);
        translate([th,th,baseTH]) roundedCube(intSize+[0,0,2], 2);
        // Cut out panels for Pi
        // Network
        translate(piPos+[1.8,85,1]) cube([16.7,10,15]);
        // USB 3 
        translate(piPos+[21.5,85,0]) cube([15,10,18]);
        translate(piPos+[39.5,85,0]) cube([15,10,18]);
        // Side cutouts
        // Had these slightly too small, m is a margin to add to each side
        m=0.6;
        // Power
        translate(piPos+[52,6.2-m,1-m]) cube([10,10+m*2,4+m*2]);
        // USB
        translate(piPos+[52,22.4-m,1-m]) cube([10,7.2+m*2,3.8+m*2]);
        translate(piPos+[52,35.9-m,1-m]) cube([10,7.2+m*2,3.8+m*2]);
        // Audio
        translate(piPos+[52,53.5,4.3]) rotate([0,90,0]) cylinder(d=7.5, h=10);
       
        // Relay cables
        translate(piPos+relayPos+[4,44,1.8]) cube([32,10,5]);
        
        // Power socket
        translate(socketPos+[20,-7,6]) rotate([0,90,0]) cylinder(d=11,h=10);
        
        // Stepper motor socket
        translate(stepExtendPos+[-10,5.5,1.4]) cube([20,15.5,6.2]);
        
        // Temp delete
        //translate([0,-1,0]) cube([30,50,50]);
    }
    // Secure power socket
    translate(socketPos+[-5.5,-16,0]) {
        cube([5,3,6]);
        translate([0,14.5,0]) cube([5,3,6]);
    }
    
    // Hold stepper driver (it doesn't have mounting holes)
    translate(piPos+stepDrivPos+[15,-3.5,-soH]) {
        cube([20,3,6+soH]);
        translate([0,3,4.4+soH]) {
            rotate([0,90,0]) cylinder(h=20,d=3);
        }
        translate([0,21+4,0]) {
            cube([20,3,6+soH]);
            translate([0,0,4.4+soH]) {
                rotate([0,90,0]) cylinder(h=20,d=3);
            }
        }
    }
    
    // Mount points for stepper extender
    translate(stepExtendPos+[-0.5,-1,-2]) {
        cube([5,8,2]);
        translate([0,21.5,-3]) cube([5,7,5]);
    }
    
    // Standoffs (Pi and power have 2.5mm holes, relay has 3mm
    // Pi
    translate(piPos-[0,0,soH]) {
        x=56;   // Pi width
        translate([3.5,3.5,0]) m25_standoff();
        translate([x-3.5,3.5,0]) m25_standoff();
        translate([3.5,3.5+58,0]) m25_standoff();
        translate([x-3.5,3.5+58,0]) m25_standoff();
        
        // Relay position (it is relative to the Pi
        translate(relayPos) {
            bsize=[39, 50, 1.6];
            holeOffset=2.5;
            translate([holeOffset, holeOffset, 0]) m3_standoff();
            translate([bsize.x-holeOffset, holeOffset, 0]) m3_standoff();
            translate([holeOffset, bsize.y-holeOffset, 0]) m3_standoff();
            translate([bsize.x-holeOffset, bsize.y-holeOffset, 0]) m3_standoff();
        }
        
        // Power module
        translate(powConvPos) {
            // Swapping around the dimensions from where we define it
            // to deal with the rotation
            bsize=[59.3,20.8,1.6];
            translate([bsize.x-37.5,2.3,0]) m25_standoff();
            translate([bsize.x-2.3,2.3,0]) m25_standoff();
            translate([bsize.x-37.5,bsize.y-2.3,0]) m25_standoff();
            translate([bsize.x-2.3,bsize.y-2.3,0]) m25_standoff();
        }
        
    }
    
    // Lid screws
    for(s=topScrews) {
        // List component s is [x,y,rotation];
        translate([s.x, s.y, intSize.z+baseTH-1]) {
            lidScrewHolder(s.z);
        }
    }
    
    // Strap securing 
    yDist=76;
    translate([-9,yDist,0]) {
        rotate([0,0,270]) strapSecure();
    }
    translate([intSize.x+th*2+9,yDist-35,0]) {
        rotate([0,0,90]) strapSecure();
    }
}


module astroPiLid() {
    // Case lid. Includes a 1mm recess which sits inside the base
    
    recm=0.6;   // Recess margin, so it is not too tight
    screenPos=[piPos.x+6.8, piPos.y+40.5,0];
    color("Red") translate([0,0,intSize.z+baseTH]) {
        difference() {
            union() {
                roundedCube([intSize.x+th*2, intSize.y+th*2, th], 4);
                // Lower recess
                translate([th+recm,th+recm,-0.6]) {
                    roundedCube([intSize.x-recm*2, intSize.y-recm*2, 1]);
                }
            }
            // Cut out screw holes
            for(s=topScrews) {
                translate([s.x, s.y, -2]) {
                    cylinder(d=3.2, h=th+5);
                }
                // Screw head recess
                translate([s.x, s.y, th-1.5]) {
                    cylinder(d=6.5, h=2);
                }
            }
            // Cut out for screen
            translate([screenPos.x, screenPos.y,-10]) {
                cube([28,14,20]);
            }
            // Cut out for button
            translate([screenPos.x+36, screenPos.y+5.8,-10]) {
                cylinder(d=9, h=20);
            }
            
            // Cut out for IR receiver
            translate([piPos.x+19.2, piPos.y+16.9, -3]) {
                roundedCube([9,7,10],3);
            }
            // Cut out for relay terminal screws
            translate([piPos.x+relayPos.x+6.5, piPos.y+relayPos.y+41, -30]) {
                hull() {
                    cylinder(d=4, h=40);
                    translate([27,0,0]) cylinder(d=4, h=40);
                }
            }
            // Place cut out text/image here. Would be too messy with petg
        }
    }
}
            
module astroPiButton() {
    // Draws a button cap
    screenPos=[piPos.x+6.8, piPos.y+40.5,intSize.z+baseTH];
    color("Green") translate([screenPos.x+36, screenPos.y+5.8,screenPos.z-2.8]) {
        cylinder(d=8, h=6);
        cylinder(d=11, h=1.2);
    }
}

module strapSecure() {
    // A loop to hold a velcro strap
    h=6;
    strap=25;   // Strap width
    th=5;
    difference() {
        cube([strap+th*2, th+4, h]);
        translate([th,th,-1]) cube([strap,4,h+2]);
    }
}

module lidScrewHolder(rot) {
    // Mounting screw holder for the lid to attach to
    // Draws about the centre of the current point rotated around the z
    // Holds a brass insert
    insDiam=4.25;
    th=soTH;
    h=soH;
    gradH=4;    // Height to slowly graduate out from
    
    rotate([0,0,rot]) {
        translate([0,0,-h]) difference() {
            cylinder(d=insDiam+th*2, h=h);
            translate([0,0,-1]) cylinder(d=insDiam,h=h+2);
        }
        // Graduation part
        od=insDiam+th*2;    // Outer diameter
        hull() {
            translate([0,0,-h-0.01]) cylinder(d=od,h=0.01);
            translate([-od/2,-od/2,-h-gradH]) cube([0.1,od,0.01]);
            translate([-od/2,-od/2,-h]) cube([0.1,od,0.01]);
        }
    }
}

module roundedCube(size, r=2) {
    // Draw a cube with rounded corners (square top and bottom)
    hull() {
        translate([r,r,0]) cylinder(r=r, h=size.z);
        translate([r,size.y-r,0]) cylinder(r=r, h=size.z);
        translate([size.x-r,r,0]) cylinder(r=r, h=size.z);
        translate([size.x-r,size.y-r,0]) cylinder(r=r, h=size.z);
    }
}

module m3_standoff() {
    // A standoff for a M3 brass insert
    // Diameter 4.25mm, height 4.75mm
    // We use the soH and soTH (height and thickness) variables defined at the top
    insDiam=4.25;
    difference() {
        cylinder(d=insDiam+soTH*2, h=soH);
        translate([0,0,-1]) cylinder(d=insDiam, h=soH+2);
    }
}

module m25_standoff() {
    // A standoff for a M2.5 brass insert
    // The ones I have are actually the same external dimensions as the M3
    // Diameter 4.25mm, height 4.75mm
    // We use the soH and soTH (height and thickness) variables defined at the top
    insDiam=4.25;
    difference() {
        cylinder(d=insDiam+soTH*2, h=soH);
        translate([0,0,-1]) cylinder(d=insDiam, h=soH+2);
    }
}
// ******* Hardware - to move to own file eventually 
module two_channel_relay(rot) {
    // 2 channel relay board, various manufacturers
    // rot is the rotation about z, ensuring the board still appears at current position
    bsize=[39, 50, 1.6];
    holeSize=3.5;
    holeOffset=2.5; // Holes are consistently the same distance in from each side
    
    rotAdjust=rotAdjust(bsize, rot);
    
    translate(rotAdjust) rotate(rot) {
        // Main board
        difference() {
            color("DarkGreen") {
                cube(bsize);    // In reality the board has rounded corners
            }
            translate([holeOffset, holeOffset, -1]) cylinder(d=holeSize, h=bsize.z+2);
            translate([bsize.x-holeOffset, holeOffset, -1]) cylinder(d=holeSize, h=bsize.z+2);
            translate([holeOffset, bsize.y-holeOffset, -1]) cylinder(d=holeSize, h=bsize.z+2);
            translate([bsize.x-holeOffset, bsize.y-holeOffset, -1]) cylinder(d=holeSize, h=bsize.z+2);
        }
        // Terminal blocks
        translate([3.8,3.8,bsize.z]) {
            color("DarkBlue") {
                cube([30.5, 7.8, 10.7]);
            }
        }
        // Relays (as single block)
        translate([3.8, 12.5,bsize.z]) {
            color("MediumBlue") {
                cube([31.5, 18.8, 15]);
            }
        }
        // Header pins
        translate([6.8, bsize.y-4.2, bsize.z]) male_header_pins(4,1);
        translate([22.5, bsize.y-4.2, bsize.z]) male_header_pins(3,1);
    }
}

module uln2003_module(rot) {
    // Draws a ULN2003 stepper motor module
    bsize=[21,41,1.6];
    
    // Rotation fugde
    rotAdjust=rotAdjust(bsize, rot);
    
    translate(rotAdjust) rotate(rot) {
        // Main board
        color("DarkBlue") cube(bsize);
        // Pins
        translate([1.7,0,bsize.z]) male_header_pins(7,1);
        translate([1.7,bsize.y-2.54,bsize.z]) male_header_pins(7,1);
        translate([17,6.7,bsize.z]) rotate([0,0,90]) male_header_pins(4,1);
        // Motor socket
        translate([3.2,30,bsize.z]) color("White") cube([15,5.8,7]);   
    }
}

module stepExtender(rot) {
    // Small board to extend the stepper motor socket and give an external socket
    bsize=[11.8,27.1,1.6];
    
    // Rotation fudge
    rotAdjust=rotAdjust(bsize, rot);
    
    translate(rotAdjust) rotate(rot) {
        difference() {
            color("Brown") cube(bsize);
            // Holes. Note they are slightly offset due to clumsy drilling!
            translate([2.26, 4.9, -1]) cylinder(d=2, h=bsize.z+2);
            translate([2.73, 24.1, -1]) cylinder(d=2, h=bsize.z+2);
        }
        // Socket block
        translate([-3.77, 5.78, bsize.z]) color("White") cube([7, 15, 5.7]);
    }
}
    
module step_down_module(rot) {
    // Draws a step down module
    bsize=[20.8,59.3,1.6];
    
    holesize=2.6;
    
    // Rotation fugde
    rotAdjust=rotAdjust(bsize, rot);
    
    translate(rotAdjust) rotate(rot) {
        // Main board
        difference() {
            color("Red") cube(bsize);
            translate([2.3,2.3,-1]) cylinder(d=holesize, h=bsize.z+2);
            translate([bsize.x-2.3,2.3,-1]) cylinder(d=holesize, h=bsize.z+2);
            translate([2.3,37.5,-1]) cylinder(d=holesize, h=bsize.z+2);
            translate([bsize.x-2.3,37.5,-1]) cylinder(d=holesize, h=bsize.z+2);
        }
        // Terminal block
        translate([4.5,0,bsize.z]) color("DarkBlue") cube([10.6, 7.8, 10.7]);
        // Buck convertor
        translate([0,11,bsize.z]) color("Black") cube([bsize.x, 22, 9]);
        // Capacitor
        translate([bsize.x/2,42.5,bsize.z]) color("Silver") cylinder(d=10, h=10.5);
        // USB connector
        translate([3.8,48,bsize.z]) color("Silver") cube([13.2,13.5,7.3]);
    }
}

module ioBoard() {
    // The custom IO board
    // Crude representation, not showing the wires or connectors in detail
    bsize=[50, 70, 1.6];
    
    // Draw the main board
    color("Green") cube(bsize);
    // The screen
    translate([8.5,35,bsize.z+3]) sdd1306_128x64();
    translate([41, 45.5, bsize.z]) 6mm_push_button();
    // IR sensor
    translate([21, 20, bsize.z]) color("Silver") cube([8, 6.4, 5.6]);
    // Motor and relay header pins
    translate([14.3, -4, bsize.z]) color("Black") cube([10.16,17, 4.54]);
    translate([29.5, -4, bsize.z]) color("Black") cube([15.24,17, 4.54]);
    // Female header on underside
    translate([2.43,9.74,0]) rotate([180,0,90]) female_header_pins(20,2);
}

module 6mm_push_button() {
    // Small tactile switch (no pins)
    color("DimGray") cube([6,6,4.5]);
    translate([3,3,0]) color("Black") cylinder(d=3.5, h=4.5+1.3);
}

module sdd1306_128x64() {
    // Draws an i2c OLED screen
    bsize=[27.3, 27.8, 1.5];
    // Main board
    difference() {
        color("Blue") cube(bsize);
        // Cable cut out
        translate([6.65, -1, -1]) cube([14,3,2+bsize.z]);
        // Holes
        translate([2,2,-1]) cylinder(d=2, h=2+bsize.z);
        translate([bsize.x-2,2,-1]) cylinder(d=2, h=2+bsize.z);
        translate([2,bsize.y-2,-1]) cylinder(d=2, h=2+bsize.z);
        translate([bsize.x-2,bsize.y-2,-1]) cylinder(d=2, h=2+bsize.z);
    }
    // Screen part
    translate([0,4.8,bsize.z]) {
        color("Black") cube([bsize.x, 17,1.2]);
        // And the display surface
        translate([0,3.5,1.2]) color("DarkSlateGrey") cube([bsize.x,13.5,0.1]);
    }
    // Pins
    translate([8.57,bsize.y,0]) {
        rotate([180,0,0]) male_header_pins(4,1);
    }
}

module female_header_pins(pins, rows) {
    // Draws a block of male 2.54 pitch header pins
    sp=2.54;    // Spacing
    pw=0.65;    // Pin width
    pl=3.2;       // Pin lower, the under part
    blh=8.3;      // Height of the plastic block
    
    // Draw the plastic base block
    color("Black") cube([sp*pins,sp*rows,blh]);
    // Draw the pins
    for(i=[0:rows-1]) {
        translate([(sp-pw)/2,(sp-pw)/2+i*sp,-pl]) {
            for(j=[0:pins-1]) {
                translate([j*sp,0,0]) {
                    color("Silver") cube([pw,pw,pl+blh]);
                }
            }
        }
    }       
}

module male_header_pins(pins, rows) {
    // Draws a block of male 2.54 pitch header pins
    sp=2.54;    // Spacing
    pw=0.65;    // Pin width
    ph=6;       // Pin height
    pl=3;       // Pin lower, the under part
    blh=3;      // Height of the plastic block
    
    // Draw the plastic base block
    color("Black") cube([sp*pins,sp*rows,blh]);
    // Draw the pins
    for(i=[0:rows-1]) {
        translate([(sp-pw)/2,(sp-pw)/2+i*sp,-pl]) {
            for(j=[0:pins-1]) {
                translate([j*sp,0,0]) {
                    color("Silver") cube([pw,pw,ph+pl+blh]);
                }
            }
        }
    }       
}

module 55dc_jack_female() {
    // Draws a 2.1/5.5mm DC female socket. Usually used for CCTV or LED lights
    // Consists of a block (w x h x d) 14.3mm x 12mm x 11mm
    // stepping down to a cylinder 10mm wide. Total length of black part 33mm.
    // it then has a terminal block on the end and exposed metal
    color("Black") {
        hull() {
            cube([14.3, 11, 12]);
            translate([14.3/2, 0, 12/2]) {
                rotate([270,0,0]) cylinder(h=22.5, d=10);
            }
        }
        translate([14.3/2, 22, 12/2]) {
            rotate([270,0,0]) cylinder(h=11, d=10);
        }
    }
    translate([14.3/2, 33, 12/2]) {
        rotate([270,0,0]) color("Silver") cylinder(h=1.4, d=7);
    }
    // The terminal block
    translate([2,-5.5,3]) color("LimeGreen") cube([10.3, 6, 10.1]);
}

// ******************************************************* //
// The holder. The case holds the Pi, but the holder can
// go on the back of it to hold the whole pi case, a battery
// disk, and attatch to the tripod

module holder(sfront=1,sback=1,sscrews=1) {
    // Disk dimensions
    dw=43;
    dd=13;
    dh=115;
    // Battery dimensions
    bw=77;
    bd=23;
    bh=155;

    b=3;    // How thick to make the base for cutouts
    w=intSize.x+2*th;
    d=bd+b*3+dd;
    h=60;

    legd=33;    // Leg diameter
    cside=20;   // Space either side of the leg on the clamp
    cw=legd+cside*2; // Width of the clamp

    // Screw parameters
    scp=2;   // Screw pitch
    scd=8;   // Screw diameter
    scs=6;   // Screw step
    scl=legd+b*2+2;   // Screw length
    scr=scl/scp;  // Screw rotations
    sct=0.2; // Tollerance for screw hole
    headSize=6;

    if(sfront==1) {
        difference() {
            cube([w,d,h]);
            
            // Disk drive cutout. Disk is 40mm wide, 11.2mm deep, with
            // 'diamond' corners. A cylinder will do
            #translate([(w-dw+dd)/2,b*2+bd+dd/2,b]) {
                cylinder(h=dh,d=dd);
                translate([0,-dd/2,0]) cube([dw-dd,dd,dh]);
                translate([dw-dd,0,0]) cylinder(h=dh,d=dd);
            }
            
            // Battery. Slightly rounded corners but we should be fine with
            // straight edges
            #translate([(w-bw)/2,b,b]) {
                cube([bw,bd,bh]);
            }
        }
        // Strap securing 
        yDist=76;
        translate([-9,6,51]) {
            rotate([90,90,0]) strapSecure();
        }
        translate([intSize.x+th*2+9,6,16]) {
            rotate([0,-90,90]) strapSecure();
        }
    }
    
    difference() {
        // Both the front and back part of the clamp are in the same
        // difference block so we can cut the same thread all
        // the way through
        union() {
            // Bits we want
            if(sfront==1) {
                // Clamp for around the leg
                translate([(w-cw)/2,d,0]) {
                    difference() {
                        cube([cw,b+legd/2,h]);
                        
                        // Leg cutout
                        translate([cw/2,b+legd/2,-1]) cylinder(h=200,d=legd);
                        
                    }
                }
            }
            
            if(sback==1) {
                // Back part of the clamp
                translate([(w-cw)/2,d+b+legd/2,0]) {
                    color("cyan") {
                        difference() {
                            cube([cw,b+legd/2,h]);
                            
                            // Leg cutout
                            translate([cw/2,0,-1]) cylinder(h=200,d=legd);
                        }
                    }
                } 
            }
        }
        
        // Cut the screw threads
        if(sfront+sback>0) {
            translate([(w-cw)/2+cside/2,d+legd+b*2+4+6,h/2]) {
                rotate([90,0,0]) thread(scp,scd,scs,scr,sct,true);
                translate([cw-cside,0,0]) {
                    rotate([90,0,0]) thread(scp,scd,scs,scr,sct,true);
                }
            }
        }
        
    }
    if(sscrews==1) {
        // The screws
        translate([(w-cw)/2+cside/2,d+legd+b*2+4+6,h/2]) {
            rotate([90,0,0]) hexHeadScrew(scp,scd,scs,scr,headSize);
            translate([cw-cside,0,0]) {
                rotate([90,0,0]) hexHeadScrew(scp,scd,scs,scr,headSize);
            }
        }
    }
}

module hexHeadScrew(p,d,s,r,h) {
    // Draws a hex headed screw with head height h
    cylinder(h=h,d=d*1.5,$fn=6);
    translate([0,0,h]) {
        thread(p,d,s,r);
    }
}











// A way to bodge rotating around the centre, giving the translation to
// shift the object back to origin when rotating about the z axis.
// size is the footprint of the object, a is a rotation of 0,90,180 or 270
function rotAdjust(size, a) = a==0 ? [0,0,0]
                            : a == 180 ? [size.x, size.y,0]
                            : a == 90 ? [size.y,0,0]
                            : a == 270 ? [0, size.x,0]
                            : [0,0,0];