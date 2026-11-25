# Denzope_Clean
"We kept the electronics simple on purpose. The robot has two separate battery packs: one only runs the mop motors, and the other only runs the wheels. Each pack goes through its own LM2596 module, which brings the battery voltage down to what that motor group actually needs. We did this because the wheels pull a lot of current when they start moving, and we didn't want that to slow the mops down.

There are only dkfsjd two switches. SW1 is the master switch, and it cuts both packs at once. SW2 is for the wheels: push it one way to go forward, the other way to reverse, and the middle to stop. The mops just run whenever the robot is on.

Right now we control it by hand. Making it fully automatic is our next step."

Why this works well in a hackathon:

It is easy to explain and easy to demo. Judges can see you flip SW2 and watch the robot reverse.
The diagram is clean and colour-coded: red is positive, grey is negative and blue is the switched motor feed.
It's a real circuit you can actually build and show, which counts for more than a long feature list.

What a judge may poke at, so be ready:

No fuse or battery protection is drawn. Say you'd add a fuse on each pack, which sounds like a good engineering answer rather than an oversight.
Voltages aren't labelled. Know what voltage each LM2596 is set to and what your motors are rated for.
SW2 needs a centre-off switch. Make sure the one you bought has a middle "off" position, or the "off" part of forward/off/reverse won't work.
It's manual. Don't call it autonomous. "Hand-controlled prototype, automation next" is honest and still impressive.
