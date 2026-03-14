# Anime Scrapers for Kodi / XBMC

[![Join Discord](https://img.shields.io/badge/Discord-Join%20Server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/2tRn7GWTRm)
[![Stars](https://img.shields.io/github/stars/suuhm/anime-scrapers-kodi?color=gold&style=for-the-badge&logo=github)](https://github.com/suuhm/anime-scrapers-kodi)
[![Forks](https://img.shields.io/github/forks/suuhm/anime-scrapers-kodi?color=silver&style=for-the-badge&logo=github)](https://github.com/suuhm/anime-scrapers-kodi/network)
[![Issues](https://img.shields.io/github/issues/suuhm/anime-scrapers-kodi?color=red&style=for-the-badge&logo=github)](https://github.com/suuhm/anime-scrapers-kodi/issues)
[![PRs](https://img.shields.io/github/issues-pr/suuhm/anime-scrapers-kodi?color=orange&style=for-the-badge&logo=github)](https://github.com/suuhm/anime-scrapers-kodi/pulls)

A collection of **anime scraping addons and tools** for different generations of Kodi and XBMC.

>

<img width="421" height="446" alt="anime-scraper" src="https://github.com/user-attachments/assets/17b0a0f7-0b51-444d-925a-8502d4f3fef8" />

>

This repository serves as a **central collection of anime scrapers** that work with:

* legacy **XBMC (Xbox Original)**
* **Kodi Python 2 based versions**
* **Kodi Python 3 based versions**

The goal of this project is to preserve compatibility with older systems while also providing modern implementations for current Kodi versions.

---

# Supported Platforms

## Python 2 Kodi Versions

Scrapers designed for older Kodi releases that still rely on **Python 2.7**, including:

* Kodi 16 (Jarvis)
* Kodi 17
* Kodi 18 (partial compatibility)

These addons use legacy APIs such as:

* `urllib2`
* `xbmcplugin`
* `xbmcgui`
* classic resolver implementations

---

## Python 3 Kodi Versions

Newer scrapers compatible with modern Kodi versions:

* Kodi 19 (Matrix)
* Kodi 20 (Nexus)
* Kodi 21+

These implementations use:

* `urllib.request`
* updated Kodi API
* modern resolver structures

---

## XBMC for Original Xbox (Xbox OG)

This repository also includes **special versions adapted for the original Xbox running XBMC**.

Due to the extreme limitations of this platform, these versions include adjustments such as:

* compatibility with **Python 2.4 / 2.5**
* removal of unsupported Kodi API calls
* reduced memory usage
* simplified artwork handling (thumbnail only)
* workarounds for legacy TLS and networking

These builds allow **modern anime websites to be accessed on a classic Xbox console running XBMC**.

---

# Included Scrapers

## Aniworld Scraper

A scraper implementation that extracts:

* anime lists
* seasons
* episode lists
* streaming hoster mirrors

Features include:

* mirror selection dialog
* hoster detection
* support for legacy Kodi/XBMC UI APIs

The scraper parses publicly accessible HTML pages and extracts metadata such as:

* titles
* episode numbers
* descriptions
* available streaming mirrors

---

## Fansubs Scraper

This repository also contains a scraper for **Fansubs**.

The scraper focuses on:

* listing available releases
* parsing episode titles
* accessing release pages
* retrieving metadata from website

The goal of this scraper is to make **fansub releases easier to browse within Kodi/XBMC**.

---

# Project Goals

This repository aims to:

* preserve compatibility with **legacy Kodi/XBMC environments**
* provide **lightweight scraping implementations**
* document techniques for **cross-version Kodi addon development**
* support **retro platforms such as the original Xbox**

---

# Installation

Installation depends on the platform.

Typical methods include:

### Kodi / XBMC Plugin Installation

1. Download the addon folder
2. Copy it to:

```
Kodi:  userdata/addons/
XBMC:  plugins/video/
```

3. Restart Kodi/XBMC

---

# Legal Notice

This repository **does not host, store, or distribute any video content**.

All scrapers in this project:

* only access **publicly available webpages**
* extract **metadata and links already present on those websites**
* do **not provide or host any media files**

The developers of this project:

* have **no affiliation with any streaming websites**
* **do not control external content**
* **do not endorse copyright infringement**

All trademarks and copyrights belong to their respective owners.

Users are solely responsible for how they use this software.

---

# Educational Purpose

This project exists for:

* **educational purposes**
* demonstrating **web scraping techniques**
* documenting **Kodi/XBMC addon development**
* preserving compatibility with **legacy systems**

---

# Contributions

Contributions are welcome.

Possible improvements include:

* additional anime sources
* improved parsers
* better compatibility with legacy Kodi APIs
* resolver improvements

---

# Disclaimer

Use this software at your own risk.

The maintainers assume **no responsibility for how this software is used**.

