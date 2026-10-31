---
title: Raspberry Pi Models Explained: Pi 3 vs Pi 4 vs Pi 5 vs Zero 2 W (Specs and Uses)
seo_title: Raspberry Pi 3 vs 4 vs 5 vs Zero 2 W: Specs, Differences & Which to Buy
description: Specifications of the Raspberry Pi 3, 4, 5 and Zero 2 W side by side, what each is good at, what you need to get started, and the best first projects.
date: 2026-10-31T12:35:00
updated: 2026-10-31T12:35:00
category: robotics-diy
desk: science
---
<div class="key"><b>Which one?</b> Get a <b>Raspberry Pi 5</b> for a desktop, home server or anything demanding; a <b>Pi 4</b> if you find one cheaply or need its lower power draw; a <b>Zero 2 W</b> for tiny, battery-powered or embedded projects. The Pi 3 is still fine for simple jobs like Pi-hole or retro gaming if you already own one.</div>

<h2>What a Raspberry Pi is</h2>
<p>The Raspberry Pi is a credit-card-sized computer made by Raspberry Pi Ltd, a company owned by the UK educational charity the Raspberry Pi Foundation. It runs Linux (usually Raspberry Pi OS), boots from a microSD card or SSD, and has a row of GPIO pins that let it control LEDs, motors and sensors. Millions are used in schools, homes and factories.</p>

<h2>Specs side by side</h2>
<table><thead><tr><th></th><th>Pi 3 Model B+</th><th>Pi 4 Model B</th><th>Pi 5</th><th>Zero 2 W</th></tr></thead><tbody>
<tr><td>Released</td><td>2018</td><td>2019</td><td>2023</td><td>2021</td></tr>
<tr><td>CPU</td><td>4× Cortex-A53, 1.4 GHz</td><td>4× Cortex-A72, 1.5–1.8 GHz</td><td>4× Cortex-A76, 2.4 GHz</td><td>4× Cortex-A53, 1 GHz</td></tr>
<tr><td>RAM</td><td>1 GB</td><td>1, 2, 4 or 8 GB</td><td>2, 4, 8 or 16 GB</td><td>512 MB</td></tr>
<tr><td>Video out</td><td>1× HDMI</td><td>2× micro-HDMI (4K)</td><td>2× micro-HDMI (4K60)</td><td>1× mini-HDMI</td></tr>
<tr><td>USB</td><td>4× USB 2.0</td><td>2× USB 3.0, 2× USB 2.0</td><td>2× USB 3.0, 2× USB 2.0</td><td>1× micro-USB OTG</td></tr>
<tr><td>Network</td><td>Gigabit-labelled Ethernet (limited to ~300 Mbps), dual-band Wi-Fi</td><td>Gigabit Ethernet, dual-band Wi-Fi 5</td><td>Gigabit Ethernet, dual-band Wi-Fi 5</td><td>2.4 GHz Wi-Fi only</td></tr>
<tr><td>Fast storage</td><td>microSD</td><td>microSD, USB 3 SSD</td><td>microSD, PCIe (NVMe via HAT)</td><td>microSD</td></tr>
<tr><td>Power supply</td><td>5 V 2.5 A micro-USB</td><td>5 V 3 A USB-C</td><td>5 V 5 A USB-C recommended</td><td>5 V 2.5 A micro-USB</td></tr>
</tbody></table>
<p>The Pi 5 is roughly two to three times faster than the Pi 4 in CPU tasks according to Raspberry Pi's own figures, and adds a power button, a real-time clock connector and a PCIe connector for NVMe SSDs.</p>

<h2>What you need to get started</h2>
<ul>
<li>The board and its <b>official power supply</b> (under-powered Pis behave strangely, especially the Pi 5).</li>
<li>A <b>microSD card</b> of 32 GB or more, flashed with <b>Raspberry Pi Imager</b>.</li>
<li>A case, ideally with a fan or heatsink for the Pi 4 and Pi 5.</li>
<li>For desktop use: the right HDMI cable (micro-HDMI on Pi 4/5), a keyboard and mouse.</li>
</ul>
[[amazon:Raspberry Pi 5 starter kit|Raspberry Pi 5 starter kit|Board, official power supply, case with fan and a pre-flashed card: everything in one box.]]

<h2>Great first projects</h2>
<ul>
<li><b>Pi-hole</b>: block ads and trackers for every device on your home network.</li>
<li><b>Retro gaming</b> with RetroPie or Batocera.</li>
<li><b>Home server</b>: Nextcloud for files, Home Assistant for smart home control, Jellyfin for media.</li>
<li><b>Robots</b>: add a motor driver and camera and build a rover. For a simple first robot, a microcontroller is easier; see our <a href="/line-follower-robot-tutorial/">line follower tutorial</a>.</li>
<li><b>Learn to code</b> with Python and the GPIO Zero library: blink an LED, read a button, log temperatures.</li>
</ul>
[[tool:led-resistor-calculator]]

<h2>Quick answers</h2>
<h3>Can a Raspberry Pi replace my PC?</h3>
<p>A Pi 5 with 8 GB or more handles web browsing, documents and coding comfortably. Heavy video editing and modern games are beyond it.</p>
<h3>Is the Pi 3 still worth using?</h3>
<p>Yes, for light, always-on jobs: Pi-hole, a print server, sensors or retro games. Buy a newer model for anything else.</p>
<h3>Do GPIO pins use 5 V?</h3>
<p>No. Raspberry Pi GPIO pins are 3.3 V and are not 5 V tolerant. Connecting 5 V signals directly can damage the board.</p>
