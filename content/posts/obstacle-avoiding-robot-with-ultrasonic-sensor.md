---
title: Obstacle Avoiding Robot With Arduino and an Ultrasonic Sensor (HC-SR04): Full Tutorial
description: Turn a two-wheel robot car into an obstacle-avoiding robot with an HC-SR04 ultrasonic sensor and Arduino: wiring, distance code, decision logic and upgrades with a servo scanner.
date: 2026-11-10T10:39:00
category: robotics-diy
desk: science
---
<div class="key"><b>What you will build:</b> a robot that drives forward, measures the distance ahead with sound pulses, and turns away before it hits anything. If you built our <a href="/line-follower-robot-tutorial/">line follower</a>, you can reuse the same chassis, motors and L298N driver and just add one sensor.</div>

<h2>How the HC-SR04 sensor measures distance</h2>
<p>The HC-SR04 has two round "eyes": a transmitter and a receiver. When triggered, it sends a burst of ultrasonic sound (about 40 kHz, above human hearing) and raises its ECHO pin for as long as it takes the echo to return. Sound travels about 343 metres per second in room-temperature air, so:</p>
<p><code>distance (cm) = echo time (µs) × 0.0343 ÷ 2</code></p>
<p>We divide by two because the sound travels there and back. The sensor works best from about 2 cm to a few metres, and struggles with soft, angled or very small objects that do not reflect sound well.</p>

<h2>Parts</h2>
<ul>
<li>The robot car from the line follower build (Arduino Uno, L298N, two geared motors, battery)</li>
<li>1 × HC-SR04 ultrasonic sensor</li>
<li>Optional: 1 × SG90 micro servo to let the sensor look left and right</li>
</ul>
[[amazon:HC-SR04 ultrasonic sensor|HC-SR04 ultrasonic sensors|Usually sold in multi-packs; cheap enough to keep spares.]]

<h2>Wiring</h2>
<table><thead><tr><th>HC-SR04 pin</th><th>Arduino</th></tr></thead><tbody>
<tr><td>VCC</td><td>5V</td></tr>
<tr><td>TRIG</td><td>D12</td></tr>
<tr><td>ECHO</td><td>D11</td></tr>
<tr><td>GND</td><td>GND</td></tr>
</tbody></table>
<p>The motor wiring stays the same as the line follower (ENA D5, IN1 D7, IN2 D8, ENB D6, IN3 D9, IN4 D10). The HC-SR04 is a 5 V device: on a 3.3 V board like a Raspberry Pi, the ECHO pin needs a voltage divider.</p>

<h2>Code</h2>
<pre><code>const int TRIG = 12, ECHO = 11;
const int ENA = 5, IN1 = 7, IN2 = 8, ENB = 6, IN3 = 9, IN4 = 10;
const int SAFE_CM = 25;   // turn when something is closer than this
int speed = 160;

void setup() {
  pinMode(TRIG, OUTPUT); pinMode(ECHO, INPUT);
  int outs[] = {ENA, IN1, IN2, ENB, IN3, IN4};
  for (int p : outs) pinMode(p, OUTPUT);
  randomSeed(analogRead(A0));
}

long distanceCm() {
  digitalWrite(TRIG, LOW); delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long t = pulseIn(ECHO, HIGH, 30000);   // time out after 30 ms (nothing in range)
  return t == 0 ? 999 : t * 0.0343 / 2;
}

void motors(int left, int right) {
  digitalWrite(IN1, left >= 0);  digitalWrite(IN2, left < 0);
  digitalWrite(IN3, right >= 0); digitalWrite(IN4, right < 0);
  analogWrite(ENA, abs(left));   analogWrite(ENB, abs(right));
}

void loop() {
  if (distanceCm() > SAFE_CM) {
    motors(speed, speed);                 // clear ahead
  } else {
    motors(-speed, -speed); delay(300);   // back off
    if (random(2)) motors(-speed, speed); // turn a random way
    else           motors(speed, -speed);
    delay(400);
  }
  delay(40);   // let echoes die down between pings
}</code></pre>

<h2>Upgrade: look before you turn</h2>
<p>Mount the sensor on an SG90 servo (signal to D3, powered from 5 V). When an obstacle appears, stop, turn the servo to look left and right, measure both distances, and turn toward the side with more space. This makes the robot noticeably smarter in cluttered rooms.</p>

<h2>Troubleshooting</h2>
<ul>
<li><b>Always reads 0 or 999:</b> check TRIG and ECHO are not swapped, and that GND is shared.</li>
<li><b>Random false stops:</b> average three readings, or ignore single odd values.</li>
<li><b>Hits chair legs:</b> thin objects reflect little sound; add a second sensor angled sideways, or IR sensors at the corners.</li>
<li><b>Stops working when motors run:</b> motor noise on the power line; add a capacitor across the battery and keep sensor wires away from motor wires.</li>
</ul>
[[tool:led-resistor-calculator]]
<p>Want to go further? Read <a href="/arduino-vs-raspberry-pi/">Arduino vs Raspberry Pi</a> to see when to add a Pi and a camera.</p>

<h2>Quick answers</h2>
<h3>What is the HC-SR04's range?</h3>
<p>About 2 cm to 400 cm according to common datasheets, with the best accuracy within a couple of metres.</p>
<h3>Can I combine line following and obstacle avoidance?</h3>
<p>Yes: follow the line normally and stop (or go around) when the ultrasonic sensor sees something ahead, a popular competition challenge.</p>
