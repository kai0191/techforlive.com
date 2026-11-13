---
title: What is an ESP32, and what can it do for you?
seo_title: What is an ESP32? A beginner's guide to the board
description: The ESP32 is a small, cheap board with Wi-Fi and Bluetooth built in. Here is what it is, what it can do, and your first project.
date: 2026-11-13T15:10:00
updated: 2026-11-13T15:10:00
category: robotics-diy
desk: science
image: https://tse4.mm.bing.net/th?q=what+is+an+esp32+and+what+can+it+do&w=820&h=462&c=7&rs=1&p=0&o=5&pid=1.7
image_alt: ESP32 development board with a USB cable on a desk
source: contentforge
cf_id: 14110
---
<div class="key"><b>In short:</b> The ESP32 is a small microcontroller board with Wi-Fi and Bluetooth built in. It reads sensors, switches lights and motors, and talks to your phone or the internet without extra parts. It runs on 3.3 volts and suits first robots, smart-home gadgets and weather stations.<ul><li>The ESP32 is a small board with Wi-Fi and Bluetooth built in, made by Espressif.</li><li>It runs at up to 240 MHz with 520 KB of working memory, and only sees 2.4 GHz Wi-Fi.</li><li>Its pins use 3.3 volts, so check every part before you wire it, or use a level shifter.</li><li>Start with one sensor and one program; the wireless features can wait for project two.</li></ul></div>
<h2>What is an ESP32, in plain English</h2>
<p>A microcontroller is a tiny computer on one chip. It has no screen, no keyboard and no operating system like Windows. It runs one program, over and over, and its job is to talk to the real world. It reads a sensor, decides what to do, and switches something on or off. The ESP32 is one of these chips, made by a company called Espressif. You buy it on a small board with a USB socket.</p>
<p>What makes the ESP32 special is the wireless radio built into the same chip. Most small boards need an extra part for Wi-Fi. The wireless radio is built into that same chip. That is why it turns up in smart plugs, plant monitors, garage door openers and small robots. You write a program, the board joins your home Wi-Fi, and you can check a sensor or flip a switch from your phone. No extra radio board, no extra wiring.</p>
<p>The board you buy is usually a development board, not the bare chip. The common one is built around the ESP32-WROOM-32 module, a small metal-can module with an antenna on the board. It has a USB socket for power and programming, and two rows of pins for your wires. The pins are the board&#x27;s hands: each one can read a sensor, switch a light, or talk to another chip.</p>
<table><thead><tr><th>At a glance</th><th>Answer</th></tr></thead><tbody><tr><td>Maker</td><td>Espressif Systems</td></tr><tr><td>Processor</td><td>Xtensa LX6, up to 240 MHz</td></tr><tr><td>Memory</td><td>520 KB SRAM, 448 KB ROM</td></tr><tr><td>Wi-Fi</td><td>802.11 b/g/n, 2.4 GHz only</td></tr><tr><td>Bluetooth</td><td>4.2 BR/EDR and Bluetooth LE</td></tr><tr><td>Pins</td><td>Up to 34 GPIO, 3.3 V logic</td></tr></tbody></table>
[[tool:led-resistor-calculator]]
<h2>What is an ESP32 and what can it do</h2>
<p>Under the hood, the ESP32 is a dual-core processor that runs at up to 240 megahertz. Megahertz, or MHz, is a speed measure: how many million simple steps the chip takes each second. Two cores means it can do two things at once, such as running your program on one core while Wi-Fi runs on the other. It has 520 kilobytes of working memory, called SRAM, and 448 kilobytes of built-in program memory, called ROM. Those figures come from the ESP32 Series Datasheet, version 5.3, published by Espressif.</p>
<p>The wireless side is 2.4 gigahertz Wi-Fi, the same band most home routers use for the 2.4 GHz network. It follows the 802.11 b/g/n standards and reaches up to 150 megabits per second. It also has Bluetooth 4.2, both the classic kind that talks to speakers and the low-energy kind that talks to watches and tags. One warning: the ESP32 only sees 2.4 GHz networks, so join that network, not the 5 GHz one.</p>
<p>So what can you build? Start with the jobs that need Wi-Fi. A plant monitor that texts you when the soil is dry. A garage door you can check from the sofa. A weather station that posts readings to a web page. A door sensor that tells you when a parcel arrives. Then add Bluetooth: a remote control for a robot car. The board also suits jobs with no wireless at all, such as a clock, a light controller or a small robot.</p>
<table><caption>The ESP32 at a glance</caption><thead><tr><th>Part</th><th>What the ESP32 has</th><th>What it means for you</th></tr></thead><tbody><tr><td>Processor</td><td>Xtensa LX6, one or two 32-bit cores, up to 240 MHz</td><td>Runs your program and Wi-Fi at the same time</td></tr><tr><td>Working memory</td><td>520 KB SRAM</td><td>Room for big programs and web pages</td></tr><tr><td>Wi-Fi</td><td>802.11 b/g/n, 2.4 GHz, up to 150 Mbps</td><td>Joins home Wi-Fi and phone hotspots</td></tr><tr><td>Bluetooth</td><td>4.2 BR/EDR and Bluetooth LE</td><td>Talks to phones and small Bluetooth devices</td></tr><tr><td>Pins</td><td>Up to 34 GPIO</td><td>Plenty of room for sensors and motors</td></tr><tr><td>Logic level</td><td>3.3 V</td><td>Use 3.3 V parts, or a level shifter</td></tr></tbody></table>
<h2>ESP32 vs Arduino Uno: which board for which job</h2>
<figure class="fig"><img src="https://tse3.mm.bing.net/th?q=what+is+an+esp32+and+what+can+it+do+vs+Arduino+Uno+board+job&amp;w=560&amp;h=380&amp;c=7&amp;rs=1&amp;p=0&amp;o=5&amp;pid=1.7" alt="what is an esp32 and what can it do - ESP32 vs Arduino Uno: which board for which job" loading="lazy" decoding="async"></figure>
<p>The Arduino Uno is the board most beginners meet first. It is simple, tough and well documented, and thousands of guides use it. The ESP32 is newer and faster, with wireless built in. Neither is better in general. The right one depends on the job. If your project needs Wi-Fi or Bluetooth, the ESP32 wins. If it needs 5 volt parts and nothing else, the Uno is often the easier start.</p>
<p>The numbers tell the story. The ESP32 runs at up to 240 MHz with 520 KB of working memory. The Uno runs at 16 MHz with 2 KB of working memory. That gap matters when your program juggles Wi-Fi, sensors and a display at once. The Uno handles one simple job well. The ESP32 handles several at once. For a blinking light or a single button, the difference is invisible. For a weather station that reads sensors, joins Wi-Fi and serves a web page, the ESP32 is the comfortable choice.</p>
<p>Voltage is the real trap. The Uno&#x27;s pins use 5 volts, and most classic Arduino parts expect 5 volts. The ESP32&#x27;s pins use 3.3 volts and are not 5 volt tolerant, so a 5 volt signal can damage a pin. Check every sensor and module before you wire it. Parts made for 3.3 volt logic are safe. Parts made for 5 volts need a level shifter, a small part that translates between the two voltages.</p>
<table><caption>ESP32 vs Arduino Uno</caption><thead><tr><th></th><th>ESP32</th><th>Arduino Uno</th></tr></thead><tbody><tr><td>Speed</td><td>Up to 240 MHz, dual-core</td><td>16 MHz, single-core</td></tr><tr><td>Working memory</td><td>520 KB SRAM</td><td>2 KB SRAM</td></tr><tr><td>Wi-Fi</td><td>Built in</td><td>Needs an extra part</td></tr><tr><td>Bluetooth</td><td>Built in (4.2)</td><td>Needs an extra part</td></tr><tr><td>Pin voltage</td><td>3.3 V</td><td>5 V</td></tr><tr><td>Best for</td><td>Wi-Fi projects and robots</td><td>Simple 5 V circuits</td></tr></tbody></table>
[[amazon:ESP32 development board starter kit|ESP32 development board|For a first project, a board with USB and pins ready to go.]]
<h2>Your first ESP32 project: connect it to Wi-Fi</h2>
<p>You need three things: an ESP32 development board, a USB cable that carries data, and a computer with the Arduino IDE installed. The IDE is the free program you write code in, from Arduino. Some USB cables only charge and carry no data, so if the board never appears on your computer, try another cable first. Plug the board in. A small light on the board should come on.</p>
<p>Next, teach the IDE about the ESP32. Open the Boards Manager from the Tools menu, search for esp32, and install the package by Espressif Systems. Then pick your board from the Tools menu: Tools, then Board, then ESP32 Arduino, then the board you own. Set the port the same way, under Tools, then Port. If no port appears, the cable or the driver is the problem, not the board. Most boards use a standard USB-to-serial chip.</p>
<p>Now load the sketch below. It joins your home Wi-Fi and prints the board&#x27;s address. Type your own Wi-Fi name and password where the capitals say so. Press the upload arrow and wait. The IDE compiles the sketch, sends it to the board, and the board restarts. Open the Serial Monitor from the Tools menu, set the speed to 115200 baud, and watch. You should see dots while it connects, then the words Wi-Fi connected and an address such as 192.168.1.20. That address is your board on your network.</p>
<ol class="steps"><li>Plug the board in with a data USB cable and open the Arduino IDE.</li><li>Install the ESP32 board package from the Boards Manager.</li><li>Pick your board and port from the Tools menu.</li><li>Paste the sketch, fill in your Wi-Fi name and password, and upload it.</li><li>Open the Serial Monitor at 115200 baud and look for the connected message.</li></ol>
<p><b>Connect the ESP32 to Wi-Fi (Arduino sketch)</b></p><pre><code>#include &lt;WiFi.h&gt;

const char* ssid = &quot;YOUR_WIFI_NAME&quot;;
const char* password = &quot;YOUR_WIFI_PASSWORD&quot;;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print(&quot;Connecting&quot;);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(&quot;.&quot;);
  }
  Serial.println();
  Serial.println(&quot;Wi-Fi connected&quot;);
  Serial.println(WiFi.localIP());
}

void loop() {
}</code></pre>
<h2>Power, pins and the 3.3 V trap</h2>
<figure class="fig"><img src="https://tse2.mm.bing.net/th?q=what+is+an+esp32+and+what+can+it+do+Power+pins+3.3+V+trap&amp;w=560&amp;h=380&amp;c=7&amp;rs=1&amp;p=0&amp;o=5&amp;pid=1.7" alt="what is an esp32 and what can it do - Power, pins and the 3.3 V trap" loading="lazy" decoding="async"></figure>
<p>Most development boards take power from the USB socket. A phone charger or a computer USB port is enough for learning. The board turns the 5 volts from USB down to 3.3 volts for the chip. For a finished project, you can power the board from the VIN pin, which accepts a wider range, or from a battery pack. Check your board&#x27;s own guide for the voltage its VIN pin accepts, because boards differ. Never connect power to both USB and VIN at once unless the guide says it is safe.</p>
<p>The pins are where beginners break boards. The ESP32 has up to 34 pins you can program, called GPIO pins. GPIO stands for general-purpose input/output, which means each pin can read a signal or switch one on. Some pins do double duty: a few are input-only, and some are used by the board at start-up. If your program works on one pin and not another, try a different pin before you blame the code. Your board&#x27;s pinout diagram shows which pins are safe to use.</p>
<p>Here is the voltage rule in one place. A 5 volt signal on an ESP32 pin can damage it. That includes the 5 volt output of many older sensors and the 5 volt pin on an Arduino Uno. If a part runs on 5 volts, use a level shifter between it and the ESP32. A level shifter is a small, cheap board that translates signals between 3.3 and 5 volts. Buy the 3.3 volt version of a sensor when one exists.</p>
<h2>Myths you can ignore about the ESP32</h2>
<p>The first myth is that the ESP32 is too hard for a beginner. It is not. The Arduino IDE treats it like any other board once the package is installed. The same Blink sketch that lights an LED on an Uno lights one on an ESP32. The extra power is there when you need it, and it stays out of your way until then. Start with one sensor and one small win. The wireless features can wait for project two.</p>
<p>The second myth is that you need the newest ESP32 for every job. You do not. The original ESP32 suits most first projects. Newer chips in the family, such as the ESP32-S3, suit bigger jobs such as cameras and displays. For a plant monitor or a garage sensor, the original is plenty. Buy the newer chip when a project outgrows the old one, not before.</p>
<p>The third myth is that Wi-Fi projects need a strong signal everywhere. They do not. The ESP32 only needs a 2.4 GHz signal where the board sits. A board in a shed at the edge of the garden may struggle, and a board beside the router will not. If the signal is weak, move the board, move the router, or add a small access point near the job. Test the signal with your phone first: if your phone shows one bar in that spot, the board will struggle too.</p>
<h2>Quick answers</h2>
<h3>Does the ESP32 have Wi-Fi built in?</h3>
<p>Yes. The radio is part of the chip, so you wire sensors, not a radio module. It joins 2.4 GHz networks only, not 5 GHz ones.</p>
<h3>Is the ESP32 better than an Arduino Uno?</h3>
<p>It depends on the job. The ESP32 is faster and has wireless built in. The Uno is simpler and speaks 5 volts. For a Wi-Fi project, pick the ESP32. For a simple 5 volt circuit, pick the Uno.</p>
<h3>Can I program the ESP32 with the Arduino IDE?</h3>
<p>Yes. Install the ESP32 board package from the Boards Manager and pick your board under Tools, then Board. Then write sketches the same way you would for an Uno.</p>
<h3>How do I power an ESP32?</h3>
<p>A USB cable is enough while you learn. For a finished project, use the VIN pin or a battery pack, and check your board&#x27;s guide for the voltage its VIN pin accepts.</p>
<h3>What is the difference between the ESP32 and the ESP32-S3?</h3>
<p>The S3 is a newer chip in the same family, with faster Bluetooth and more memory. The original ESP32 suits most first projects; the S3 suits bigger jobs such as cameras.</p>
