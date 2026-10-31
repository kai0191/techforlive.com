---
title: What Is a Passkey? How Passkeys Replace Passwords (and How to Set One Up)
description: Passkeys explained simply: how they work, why they stop phishing, how they sync between devices, and step-by-step setup for Google, Apple, Microsoft and other accounts.
date: 2026-11-02T11:05:00
category: privacy-security
desk: security
---
<div class="key"><b>In short:</b> a passkey lets you sign in with your fingerprint, face or device PIN instead of a password. Nothing secret is ever typed or sent to the website, so passkeys <b>cannot be phished or leaked in a data breach</b>. Google, Apple, Microsoft, Amazon, PayPal and many others support them today.</div>

<h2>How a passkey works</h2>
<p>When you create a passkey, your device makes a matching pair of cryptographic keys:</p>
<ul>
<li>A <b>public key</b> that the website stores. It is useless to a thief on its own.</li>
<li>A <b>private key</b> that never leaves your device or password manager.</li>
</ul>
<p>When you sign in, the website sends a random challenge. Your device asks for your fingerprint, face or PIN, signs the challenge with the private key, and sends back the signature. The site checks it with the public key. No password crosses the internet.</p>
<p>Passkeys are tied to the real website's domain, so a fake look-alike site simply cannot trigger them. That is what makes them phishing-resistant. They are built on open standards (FIDO2/WebAuthn) developed by the FIDO Alliance with Apple, Google and Microsoft.</p>

<h2>Where passkeys are stored</h2>
<table><thead><tr><th>Ecosystem</th><th>Where they live</th><th>Syncs to</th></tr></thead><tbody>
<tr><td>Apple</td><td>iCloud Keychain / Passwords app</td><td>Your iPhone, iPad and Mac</td></tr>
<tr><td>Google</td><td>Google Password Manager</td><td>Android and Chrome where you are signed in</td></tr>
<tr><td>Microsoft</td><td>Windows Hello / Microsoft account</td><td>Windows devices (sync support is expanding)</td></tr>
<tr><td>Password managers</td><td>1Password, Bitwarden, Dashlane and others</td><td>Every device the manager runs on</td></tr>
<tr><td>Hardware keys</td><td>A physical security key (USB/NFC)</td><td>Wherever you plug or tap it</td></tr>
</tbody></table>
<p>To sign in on someone else's computer, choose "use a phone or tablet", scan the QR code with your phone and approve with your fingerprint.</p>

<h2>Set up your first passkeys</h2>
<ol class="steps">
<li><b>Google:</b> go to your Google Account › Security › Passkeys and security keys › Create a passkey.</li>
<li><b>Apple Account:</b> devices signed in to iCloud with two-factor authentication can use passkeys on supported sites; Apple prompts you when a site offers one.</li>
<li><b>Microsoft account:</b> account.microsoft.com › Security › Advanced security options › Add a new way to sign in.</li>
<li><b>Other sites:</b> look in Security or Login settings for "Passkey", or accept the prompt that appears after you sign in.</li>
</ol>
<p>Start with your email account: whoever controls your email can reset almost everything else.</p>

<h2>Keep a backup way in</h2>
<ul>
<li>Have passkeys on at least two devices (they sync within an ecosystem).</li>
<li>Keep recovery codes or a recovery email/phone up to date.</li>
<li>Do not delete your password straight away on every site until you are comfortable.</li>
</ul>
[[amazon:FIDO2 security key USB C NFC|FIDO2 hardware security key|A physical passkey for your most important accounts, independent of any phone.]]

<h2>Passkeys vs passwords vs 2FA codes</h2>
<table><thead><tr><th></th><th>Password</th><th>Password + SMS code</th><th>Passkey</th></tr></thead><tbody>
<tr><td>Can be phished</td><td>Yes</td><td>Yes (code can be relayed)</td><td>No</td></tr>
<tr><td>Leaks in breaches</td><td>Yes</td><td>Password yes</td><td>No (only public key stored)</td></tr>
<tr><td>Effort</td><td>Typing</td><td>Typing + waiting</td><td>One touch</td></tr>
</tbody></table>
<p>Still using passwords somewhere? Check how strong they are privately:</p>
[[tool:password-strength-checker]]

<h2>Quick answers</h2>
<h3>What happens if I lose my phone?</h3>
<p>If your passkeys sync (iCloud, Google, a password manager), they are restored when you sign in on a new device. Keep a second device or recovery method set up.</p>
<h3>Can a website see my fingerprint?</h3>
<p>No. Your fingerprint or face only unlocks the key on your device; it is never sent to the website.</p>
