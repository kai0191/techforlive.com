---
title: NTFS vs exFAT vs FAT32 vs APFS vs ext4: File Systems Explained Simply
seo_title: NTFS vs exFAT vs FAT32 vs APFS vs ext4: Which File System to Use
description: What a file system is, the real differences between NTFS, exFAT, FAT32, APFS and ext4, and exactly which one to pick for a USB stick, external drive, Mac or Linux PC.
date: 2026-10-31T10:05:00
updated: 2026-10-31T10:05:00
category: pc-storage
desk: pc
---
<div class="key"><b>Which format should I choose?</b>
<ul><li><b>USB stick or external drive used on both Windows and Mac:</b> exFAT</li>
<li><b>Windows system drive or Windows-only external drive:</b> NTFS</li>
<li><b>Mac internal or Mac-only drive:</b> APFS</li>
<li><b>Linux system drive:</b> ext4 (or Btrfs)</li>
<li><b>Old cameras, car stereos, game consoles that refuse anything else:</b> FAT32</li></ul></div>

<h2>What a file system actually does</h2>
<p>A drive is just billions of numbered storage blocks. A file system is the filing scheme on top: it records which blocks belong to which file, the file's name, folder, size, dates and permissions, and which blocks are free. Formatting a drive writes a fresh, empty filing scheme, which is why it appears to erase everything.</p>

<h2>The main file systems compared</h2>
<table><thead><tr><th></th><th>FAT32</th><th>exFAT</th><th>NTFS</th><th>APFS</th><th>ext4</th></tr></thead><tbody>
<tr><td>Made for</td><td>Everything (1996)</td><td>Flash drives, SD cards</td><td>Windows</td><td>Apple devices</td><td>Linux</td></tr>
<tr><td>Max file size</td><td>4 GB</td><td>Practically unlimited</td><td>Practically unlimited</td><td>Practically unlimited</td><td>16 TB</td></tr>
<tr><td>Windows</td><td>Read/write</td><td>Read/write</td><td>Read/write</td><td>Needs extra software</td><td>Needs extra software</td></tr>
<tr><td>macOS</td><td>Read/write</td><td>Read/write</td><td>Read only</td><td>Read/write</td><td>Needs extra software</td></tr>
<tr><td>Journaling (crash safety)</td><td>No</td><td>No</td><td>Yes</td><td>Yes (copy-on-write)</td><td>Yes</td></tr>
<tr><td>Permissions, encryption</td><td>No</td><td>No</td><td>Yes (BitLocker, EFS)</td><td>Yes (built-in encryption)</td><td>Yes</td></tr>
</tbody></table>

<h2>FAT32: compatible but limited</h2>
<p>FAT32 works almost everywhere, but no single file can be larger than 4 GB, so a long video or a disc image will not copy ("file too large for the destination"). Windows' own formatter also will not create FAT32 partitions larger than 32 GB, although the format itself allows more. Use it only for devices that demand it.</p>

<h2>exFAT: the best choice for sharing drives</h2>
<p>Microsoft designed exFAT for flash storage. It removes the 4 GB limit and is supported natively by Windows, macOS, Android, most TVs and current consoles. Its weakness is that it has no journal, so pulling the drive out mid-copy can corrupt it. Always eject first.</p>

<h2>NTFS: the Windows workhorse</h2>
<p>NTFS adds journaling (it can recover cleanly after a crash), file permissions, compression, encryption and shadow copies used by System Restore. Macs can read NTFS but not write to it without third-party drivers, which is why a Windows-formatted drive appears "read only" on a Mac.</p>

<h2>APFS: Apple's modern system</h2>
<p>APFS replaced HFS+ on Macs, iPhones and iPads in 2017. It is designed for SSDs, uses copy-on-write to keep data consistent, makes file copies near-instant (clones), and supports snapshots that Time Machine relies on. Windows cannot read it without extra software.</p>

<h2>ext4, Btrfs and the Linux world</h2>
<p>ext4 is the long-standing default on many Linux distributions: stable, fast and well understood. Btrfs (default on Fedora, for example) adds snapshots and checksums similar to APFS. Windows cannot open these natively, though WSL can access them.</p>

<h2>Quick answers</h2>
<h3>Why does my 64 GB USB stick refuse a 5 GB file?</h3>
<p>It is formatted as FAT32, which caps single files at 4 GB. Back up the stick and reformat it as exFAT.</p>
<h3>Does reformatting make a drive faster?</h3>
<p>Not noticeably on SSDs. It wipes the drive, so only do it to change the file system or start fresh.</p>
<h3>Why is the formatted size smaller than the box says?</h3>
<p>Mostly because of decimal versus binary units, not the file system. Try our converter below.</p>
[[tool:storage-size-converter]]
