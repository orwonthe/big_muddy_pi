# big_muddy_pi
Using raspberry pi for control logic on a DC block control railroad.

## packages needed
* RPi.GPIO
* click

## Testing

### Daisy Control Box Set Up and Test
1. Connect box to pi with ribbon cable.
1. Orient box with Servo and Console connectors facing you.
1. Provide power supply connection.
1. Confirm right most power led is on.
1. Connect Servo Out to In.
1. Confirm left most power led is on.
1. Connect Console Out to In.
1. Confirm middle power led is on.
1. Run **python harness.py shifter --check** .
1. If no errors stop harness program.
1. Run **python harness.py duration** and confirm zero durations.

### Testing Setup Daisy 8 to 16
1. Use servo loop to chain board under test to Daisy Control Box.
1. Connect daisy control servo out to board in (black or beige).
1. Connect daisy control servo in to board out (white or orange).
1. Console loop should be direct connect on Daisy Control Box
1. Orient test jig with LEDs on top.
1. Set up test jig with both jumpers positioned left. 

### Testing Setup Daisy 16 to 8
1. Use console loop to chain box under test to Daisy Control Box.
1. Connect daisy control console out to board in (black).
1. Connect daisy control console in to board out (white).
1. Servo loop should be direct connect on Daisy Control Box
1. Orient test jig with LEDs on top.
1. Set up test jig with both jumpers positioned right. 

### Wiring Test
1. Without ICs installed verify wiring connection matches chart,
1. Connect target board according to set up above.
1. Check that target board power led is on.

### Clocking Test
1. Install 74HC14 in U4 (alternate is 74HC04).
1. Run **python harness.py shifter --check** .
1. If test fails track clock signal with oscilloscope using **python harness.py shifter --check** . 
1. Stop test.

### Duration Test
1. Install remaining ICs.
1. Run **python harness.py duration** .
1. Verify duration is 24 (bits). 
1. If test fails run **python harness.py flow** and track serial data with oscilloscope.

### Daisy 8 to 16 Client Connector Test
1. Run **python harness.py client** .
1. For each target board port A, B, C, and D connect the port to the test jig.
1. Ignore the first report.
1. Use the second report to evaluate correctness.
1. You should also see the test jig LEDs blink in an orderly shifting sequence. Each connector has a different pattern.
1. Switch the test jig to the next untested target board port.

### Daisy 16 to 8 Client Connector Test
1. Each target board connector is tested separately.
1. Connect a target board port A1, A2, B3, B4, C5, C6, D7 or D8 to the test jig.
1. Run **python harness.py wide --connector XXX** where XXX is from 1 to 8 and matches the port under test.
1. The test will declare either failure or proper connection.
1. Repeat the test for all 8 ports.

### Loader Testing
1. If a connector test fails run **python harness.py load** and track load clock with oscilloscope.
