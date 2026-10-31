---
title: Line Follower Robot Tutorial: Build One With Arduino (Circuit Diagram + Code)
seo_title: Line Follower Robot Tutorial with Circuit Diagram & Arduino Code
description: Build a line follower robot step by step: parts list, wiring diagram for IR sensors and an L298N driver, tested-logic Arduino code, tuning tips and a PID upgrade.
date: 2026-10-31T09:10:00
updated: 2026-10-31T09:10:00
category: robotics-diy
desk: science
---
<div class="key"><b>In short:</b> a line follower is a small robot that drives along a dark line on a light floor (or the reverse). Two infrared sensors look at the floor, an Arduino decides which way to steer, and a motor driver powers two wheels. It is the classic first robot because it teaches sensors, logic and motor control in one weekend build.
<ul><li>Cost: roughly the price of an Arduino starter kit plus a robot chassis</li><li>Time: 3–5 hours for a first build</li><li>Skills: basic wiring, uploading a sketch; soldering is optional</li></ul></div>

<p>Line followers are a textbook example of a <a href="https://en.wikipedia.org/wiki/Mobile_robot" rel="noopener" target="_blank">mobile robot</a> that navigates by following a marked path, the same idea used by some warehouse and factory robots that follow tape or magnetic strips. This guide builds the simplest reliable version first, then shows how to make it faster and smoother.</p>

<h2>How a line follower works</h2>
<p>An infrared (IR) sensor module has an IR LED and a phototransistor side by side. The LED shines on the floor; a white surface reflects lots of IR back, while a black line absorbs most of it. A comparator chip on the module (usually an LM393) turns that difference into a clean digital signal: one level for "line", the other for "floor". A small trimmer potentiometer sets the threshold.</p>
<p>With two sensors mounted either side of the line, the robot only needs four rules:</p>
<table><thead><tr><th>Left sensor</th><th>Right sensor</th><th>What it means</th><th>Action</th></tr></thead><tbody>
<tr><td>Floor</td><td>Floor</td><td>Line is between the sensors</td><td>Drive forward</td></tr>
<tr><td>Line</td><td>Floor</td><td>Robot drifted right</td><td>Turn left</td></tr>
<tr><td>Floor</td><td>Line</td><td>Robot drifted left</td><td>Turn right</td></tr>
<tr><td>Line</td><td>Line</td><td>Junction, finish mark or lost</td><td>Stop (or follow your junction rule)</td></tr>
</tbody></table>

<h2>Parts list</h2>
<ul>
<li><b>Arduino Uno</b> (or a compatible board such as a Nano)</li>
<li><b>2 × IR obstacle/line sensor modules</b> based on the TCRT5000 sensor, with digital output</li>
<li><b>L298N dual motor driver module</b> (or a more efficient TB6612FNG board)</li>
<li><b>2 × geared DC motors</b> with wheels (the yellow "TT"/BO motors in most kits) and a front caster wheel</li>
<li><b>Chassis</b>: a two-wheel robot car kit, acrylic plate or even stiff cardboard</li>
<li><b>Battery</b>: 2 × 18650 Li-ion cells in a holder (about 7.4 V) or a 6 × AA pack (about 9 V)</li>
<li>Jumper wires, a switch, and black electrical tape for the track</li>
</ul>
[[amazon:2WD smart robot car chassis kit Arduino|2WD robot car chassis kit|Motors, wheels, caster and battery holder in one box, so the build starts on the wiring.]]
[[amazon:TCRT5000 IR line tracking sensor module|TCRT5000 line sensor modules|Buy a 5- or 10-pack; you will want spares and later a third sensor.]]

<h2>Circuit diagram</h2>
<figure>
<svg viewBox="0 0 760 420" role="img" aria-label="Wiring diagram: battery to L298N, L298N 5V to Arduino, two IR sensors to pins 2 and 3, L298N control pins to Arduino pins 5 to 10, motors to L298N outputs" style="width:100%;height:auto;font:13px Inter,sans-serif">
<defs><style>.b{fill:var(--card);stroke:var(--text);stroke-width:2}.t{fill:var(--text)}.s{font-size:11px;fill:var(--muted)}.w{fill:none;stroke-width:2.5}</style></defs>
<rect class="b" x="20" y="30" width="150" height="70" rx="10"/><text class="t" x="95" y="60" text-anchor="middle" font-weight="700">Battery 7–9 V</text><text class="s" x="95" y="80" text-anchor="middle">via ON/OFF switch</text>
<rect class="b" x="300" y="20" width="190" height="150" rx="10"/><text class="t" x="395" y="45" text-anchor="middle" font-weight="700">L298N driver</text>
<text class="s" x="312" y="70">12V in ←  battery +</text><text class="s" x="312" y="88">GND ← battery − &amp; Arduino GND</text><text class="s" x="312" y="106">5V out → Arduino 5V*</text><text class="s" x="312" y="124">ENA ENB IN1–IN4 ← Arduino</text><text class="s" x="312" y="150">OUT1/2 = left · OUT3/4 = right</text>
<rect class="b" x="300" y="250" width="190" height="150" rx="10"/><text class="t" x="395" y="275" text-anchor="middle" font-weight="700">Arduino Uno</text>
<text class="s" x="312" y="300">D2 ← left sensor OUT</text><text class="s" x="312" y="318">D3 ← right sensor OUT</text><text class="s" x="312" y="336">D5 → ENA · D6 → ENB (PWM)</text><text class="s" x="312" y="354">D7 D8 → IN1 IN2</text><text class="s" x="312" y="372">D9 D10 → IN3 IN4</text>
<rect class="b" x="20" y="250" width="150" height="60" rx="10"/><text class="t" x="95" y="276" text-anchor="middle" font-weight="700">Left IR sensor</text><text class="s" x="95" y="295" text-anchor="middle">VCC 5V · GND · OUT</text>
<rect class="b" x="20" y="330" width="150" height="60" rx="10"/><text class="t" x="95" y="356" text-anchor="middle" font-weight="700">Right IR sensor</text><text class="s" x="95" y="375" text-anchor="middle">VCC 5V · GND · OUT</text>
<rect class="b" x="590" y="20" width="150" height="60" rx="10"/><text class="t" x="665" y="55" text-anchor="middle" font-weight="700">Left motor</text>
<rect class="b" x="590" y="110" width="150" height="60" rx="10"/><text class="t" x="665" y="145" text-anchor="middle" font-weight="700">Right motor</text>
<path class="w" stroke="#e5484d" d="M170 55 H300"/><path class="w" stroke="#3b82f6" d="M170 80 H240 V95 H300"/>
<path class="w" stroke="#e5484d" d="M395 170 V250"/><path class="w" stroke="#16a34a" d="M455 170 V250"/>
<path class="w" stroke="#f59e0b" d="M170 280 H300"/><path class="w" stroke="#f59e0b" d="M170 360 H235 V318 H300"/>
<path class="w" stroke="#8b5cf6" d="M490 50 H590"/><path class="w" stroke="#8b5cf6" d="M490 140 H590"/>
<text class="s" x="200" y="48">+ power</text><text class="s" x="408" y="215">5V*</text><text class="s" x="462" y="215">control (6 wires)</text><text class="s" x="190" y="273">signal</text>
</svg>
<figcaption>Wiring overview. *Only use the L298N's 5 V output to power the Arduino when the battery is under 12 V and the board's 5 V jumper is fitted; otherwise feed the Arduino from its own USB power bank. All grounds must be connected together.</figcaption>
</figure>

<h2>Build it step by step</h2>
<ol class="steps">
<li><b>Assemble the chassis.</b> Fit the two motors at the back, the caster at the front, and mount the battery holder low and central so the robot does not tip.</li>
<li><b>Mount the sensors.</b> Fix both IR modules at the front, facing down, about 5–10 mm above the floor. Space them slightly wider than your line: with 19 mm electrical tape, about 25–30 mm apart works well, so both see floor when centred.</li>
<li><b>Wire the motor driver.</b> Battery + goes through the switch to the L298N's 12V terminal, battery − to GND. Left motor to OUT1/OUT2, right motor to OUT3/OUT4. Remove the ENA and ENB jumpers so the Arduino can control speed.</li>
<li><b>Connect the Arduino.</b> Wire the control pins as in the diagram, connect GND to GND, and power the Arduino (see the note under the diagram).</li>
<li><b>Calibrate the sensors.</b> Power up, hold each sensor over the floor and then over the tape, and turn its trimmer until the module's indicator LED changes cleanly between the two. Do this on the actual floor you will use.</li>
<li><b>Lay a track.</b> Start with a big oval of black tape on a light, matte surface. Avoid very tight corners until the robot is tuned.</li>
<li><b>Upload the code</b> below, put the robot on the line and switch on.</li>
</ol>

<h2>Arduino code</h2>
<pre><code>// TechForLive line follower: 2 IR sensors + L298N
const int L_SENSOR = 2, R_SENSOR = 3;
const int ENA = 5, IN1 = 7, IN2 = 8;   // left motor
const int ENB = 6, IN3 = 9, IN4 = 10;  // right motor
const int LINE = HIGH;   // many TCRT5000 modules read HIGH over black; change to LOW if yours is reversed
int baseSpeed = 150;     // 0-255, start slow
int turnSpeed = 120;

void setup() {
  pinMode(L_SENSOR, INPUT); pinMode(R_SENSOR, INPUT);
  int outs[] = {ENA, IN1, IN2, ENB, IN3, IN4};
  for (int p : outs) pinMode(p, OUTPUT);
}

void motors(int left, int right) {          // -255..255 each
  digitalWrite(IN1, left >= 0);  digitalWrite(IN2, left < 0);
  digitalWrite(IN3, right >= 0); digitalWrite(IN4, right < 0);
  analogWrite(ENA, abs(left));   analogWrite(ENB, abs(right));
}

void loop() {
  bool l = digitalRead(L_SENSOR) == LINE;
  bool r = digitalRead(R_SENSOR) == LINE;
  if (!l && !r)      motors(baseSpeed, baseSpeed);     // centred
  else if (l && !r)  motors(-turnSpeed, turnSpeed);    // line under left: pivot left
  else if (!l && r)  motors(turnSpeed, -turnSpeed);    // line under right: pivot right
  else               motors(0, 0);                     // both on line: stop
}</code></pre>
<p>If the robot turns the wrong way, swap that motor's two wires (or swap IN1/IN2 in the code). If it ignores the line entirely, flip the <code>LINE</code> constant: modules differ in which level they output over black.</p>
[[tool:led-resistor-calculator]]

<h2>Tuning: from wobbly to smooth</h2>
<ul>
<li><b>Too fast, overshoots corners:</b> lower <code>baseSpeed</code>. Cheap geared motors often will not start below about 80–100 PWM, so do not go too low.</li>
<li><b>Zig-zags on straights:</b> instead of pivoting (one wheel backwards), slow the inner wheel: try <code>motors(60, baseSpeed)</code> for a gentle turn.</li>
<li><b>Loses the line on sharp bends:</b> remember the last side that saw the line, and keep turning that way when both sensors see floor for more than a moment.</li>
<li><b>Works at night, fails by the window:</b> sunlight contains infrared. Shield the sensors with a small skirt of black card.</li>
<li><b>Slows down as it runs:</b> the L298N loses around 1.5–2 V internally, which matters on small batteries. Fresh cells or a TB6612FNG driver help.</li>
</ul>

<h2>Upgrade: 5 sensors and PID control</h2>
<p>Competition line followers use a row of five to eight sensors (or an analog array such as the QTR series) and a PID controller. Each sensor gives a position, the code calculates how far the line is from centre (the <em>error</em>), and steers proportionally: a small error makes a small correction, a big one a big correction.</p>
<pre><code>error = position - centre;            // e.g. -2..+2 with 5 sensors
integral += error;
derivative = error - lastError;
correction = Kp*error + Ki*integral + Kd*derivative;
motors(baseSpeed + correction, baseSpeed - correction);
lastError = error;</code></pre>
<p>Tune with <code>Ki = 0</code> first: raise <code>Kp</code> until the robot follows but oscillates, then add <code>Kd</code> until the oscillation settles. Only add a little <code>Ki</code> if it drifts to one side on long straights.</p>
[[amazon:5 channel IR line tracking sensor array|5-channel line sensor array|One board, five evenly spaced sensors: the easiest step up to PID.]]

<h2>Can you build one without a microcontroller?</h2>
<p>Yes. The original analog design uses each sensor's comparator output to switch a transistor that powers the opposite motor: when the left sensor sees the line, the right motor stops (or slows) and the robot turns left. It is a great lesson in comparators and transistors, but it cannot remember the last turn direction, handle junctions or run PID, which is why most builders now use an Arduino.</p>

<h2>Quick answers</h2>
<h3>Why does my robot spin in circles?</h3>
<p>One motor is wired backwards, or one sensor is reading "line" all the time. Check each sensor's indicator LED over floor and tape, then test each motor on its own.</p>
<h3>Black line on white, or white on black?</h3>
<p>Either works. For a white line on a dark floor, swap the meaning of <code>LINE</code> in the code.</p>
<h3>What line width should I use?</h3>
<p>Standard 19 mm electrical tape is the usual choice. Many robotics contests use lines between about 15 and 25 mm; check your event's rules.</p>
<h3>Can I use a Raspberry Pi instead?</h3>
<p>You can, but the Pi's GPIO pins are 3.3 V, so the sensor outputs must be 3.3 V-safe, and an Arduino's simple, instant start-up suits this job better. See our <a href="/raspberry-pi-3-specifications-ever-mini-computer-of-world/">Raspberry Pi guide</a> for where a Pi shines.</p>
