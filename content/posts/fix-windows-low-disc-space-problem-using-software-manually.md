---
title: Low Disk Space on Windows 11? 12 Safe Ways to Free Up Your C: Drive
seo_title: Fix Low Disk Space on Windows 11: 12 Safe Ways to Free Up C Drive
description: Free up space on a full C: drive safely with Windows' own tools first: Storage Sense, Cleanup recommendations, old update files, hibernation and finding the biggest folders.
date: 2026-10-31T11:20:00
updated: 2026-10-31T11:20:00
category: pc-storage
desk: pc
---
<div class="key"><b>Fastest wins, in order:</b> empty the Recycle Bin and Downloads, run <b>Settings › System › Storage › Cleanup recommendations</b>, delete "Previous Windows installation(s)" if you are happy with your current version, then uninstall apps and games you no longer use. Most people recover 10–50 GB in 15 minutes without installing anything.</div>

<h2>First, see what is using the space</h2>
<p>Open <b>Settings › System › Storage</b>. Windows shows a breakdown by category (apps, temporary files, documents, other). Click a category to drill in. "Other" is often large folders from games, virtual machines or video projects.</p>

<h2>Built-in fixes (safe for everyone)</h2>
<ol class="steps">
<li><b>Cleanup recommendations.</b> In Storage, open Cleanup recommendations. It lists large or unused files, unused apps and files already backed up to OneDrive.</li>
<li><b>Temporary files.</b> Storage › Temporary files. Tick Windows Update Cleanup, Delivery Optimization files and Temporary files. Leave "Downloads" unticked unless you have checked that folder.</li>
<li><b>Previous Windows installation(s).</b> After a big Windows upgrade, a copy of the old version can take tens of gigabytes. Deleting it removes the ability to roll back, so only do this when the new version works well.</li>
<li><b>Turn on Storage Sense.</b> It empties the Recycle Bin and clears temp files automatically on a schedule.</li>
<li><b>Uninstall what you do not use.</b> Settings › Apps › Installed apps, sorted by size. Games are usually the biggest items.</li>
<li><b>Empty Downloads.</b> Installers you ran once years ago pile up here.</li>
</ol>

<h2>Bigger moves (read before you click)</h2>
<ol class="steps" start="7">
<li><b>OneDrive Files On-Demand.</b> Right-click big OneDrive folders and choose "Free up space": files stay in the cloud and download when opened.</li>
<li><b>Move libraries to another drive.</b> Right-click Documents, Pictures or Videos › Properties › Location, and move them to a second drive.</li>
<li><b>Move games.</b> Steam, Xbox and Epic launchers can move installed games to another drive without re-downloading.</li>
<li><b>Turn off hibernation</b> if you never use it. Run <code>powercfg /h off</code> in an administrator Terminal to delete <code>hiberfil.sys</code>, which can be several gigabytes. This also disables Fast Startup.</li>
<li><b>Reduce restore point space.</b> System Properties › System Protection › Configure lets you cap the space restore points can use. Keep some: they rescue broken updates.</li>
<li><b>Find giant folders.</b> Free tools such as WinDirStat or WizTree draw a map of your drive so you can spot a forgotten 40 GB video folder in seconds.</li>
</ol>

<div class="note warn"><b>Do not</b> delete files from <code>C:\Windows</code>, <code>WinSxS</code> or <code>System32</code> by hand, and be wary of "registry cleaner" or "PC booster" apps. They rarely free meaningful space and can break Windows.</div>

<h2>Why does the drive look smaller than advertised?</h2>
<p>A "512 GB" SSD shows about 476 GB in Windows because drive makers use decimal units and Windows uses binary ones, and Windows itself takes 20–30 GB. Our converter shows the exact number.</p>
[[tool:storage-size-converter]]

<h2>The lasting fix: more space</h2>
<p>If you are constantly cleaning, the drive is simply too small. A bigger internal SSD or an external one for photos, videos and games ends the cycle.</p>
[[amazon:1TB NVMe SSD|1 TB NVMe SSD|The single most effective upgrade for an older or cramped laptop or desktop.]]

<h2>Quick answers</h2>
<h3>How much free space should I keep on C:?</h3>
<p>Aim for at least 10–15% free, or 20 GB minimum. Windows updates need room to download and unpack, and SSDs perform best with some free space.</p>
<h3>Is it safe to delete the Windows.old folder?</h3>
<p>Yes, using Temporary files › Previous Windows installation(s). You just lose the option to go back to the earlier version.</p>
<h3>Why does space fill up again by itself?</h3>
<p>Updates, browser caches, restore points and app caches grow over time. Storage Sense keeps that under control automatically.</p>
