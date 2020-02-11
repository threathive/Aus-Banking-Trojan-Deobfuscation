# Aus-Banking-Trojan-Deobfuscation
Program to de-obfuscate web injects being dropped by Gozi and Danabot that is creating fraud impacting Australians and Australian Banks.

The aim of this program is to assist Australian Banks by allowing them to uplift their malware detection capabilities by having easy and automatable access to the de-obfuscated web injects infecting their customers.

Targets: 
  Gozi,
  Danabot

Tested and Working on: 
  Linux Ubuntu,
  Mac OS
  
This program can deobfuscate the malware web injects that Gozi and Danabot would retrieve and inject into your browser session.

Targeted Banks:
  ANZ
  Bank of Melbourne
  Bank of South Australia
  Commonwealth Bank
  NAB
  St George's Bank
  Westpac

No URLs that are hosting web injects are included in the source code. If you have a use for this program you should probably already know the URLs hosting the injects and you can add them in as explained in the Setup_and_Usage doc.

This program works by:
  1. Sending a request to the URL that is hosting the web injects 
  2. Processing the response of the request
  3. Deobfuscating the inject
  4. Storing the obfuscated and deobfuscated injects

As the malware changes parts of this code will have to be changed.
