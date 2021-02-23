// Stepper motor https://www.thingiverse.com/thing:204734
// By RGriffoGoes December 15, 2013

module StepMotor28BYJ()
{
    // The original looked a big clunky at roundness=32
    roundness=256;
    
	difference(){
	
		union(){
				color("gray") cylinder(h = 19, r = 14, center = true, $fn = roundness );
				color("gray") translate([8,0,-1.5])	cylinder(h = 19, r = 4.5, center = true, $fn = roundness);
				color("gold") translate([8,0,-10])	cylinder(h = 19, r = 2.5, center = true, $fn = roundness);


				color("Silver") translate([0,0,-9]) cube([7,35,0.99], center = true);				
				color("Silver") translate([0,17.6,-9])	cylinder(h = 1, r = 3.5, center = true, $fn = roundness);

				color("Silver") translate([0,-17.6,-9])	cylinder(h = 1, r = 3.5, center = true, $fn = roundness);


				color("blue") translate([-3,0,-1]) cube([28,14.6,16.9], center = true);
				color("blue") translate([-2,0,0])  cube([24.5,16,15], center = true);
			}

				// handle
				color("red") translate([11,0,-16.55]) cube([4,5,6.1], center = true);
				color("red") translate([5,0,-16.55]) cube([4,5,6.1], center = true);

				// screw holes
				color("red") translate([0,17.5,-9])	cylinder(h = 2, r = 2, center = true, $fn = roundness);
				color("red") translate([0,-17.5,-9])	cylinder(h = 2, r = 2, center = true, $fn = 32);
		}
	}


StepMotor28BYJ();
translate([0,0,40]) {
    StepMotor28BYJ_Shaft();
}

module StepMotor28BYJ_Shaft(marg=0) {
    // Draws only the motor shaft/handle.
    // Marge makes it slightly larger, if being used for a cutout
    $fn=256;
    difference() {
        color("gold") cylinder(h=8+marg, d=5+marg);

        color("red") translate([1.5+marg,-10,8+marg-6]) cube([6,20,10]);
        color("red") translate([-1.5-marg-6,-10,8+marg-6]) cube([6,20,10]);
    }
    
    
}
