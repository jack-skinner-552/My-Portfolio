# Jack Skinner — Software & Technical Projects

Welcome to my portfolio. This repository contains personal projects I've built to develop and demonstrate skills in **software development, REST API integration, automation, troubleshooting, browser extensions, and application design**.

My projects primarily use **Java, Python, and JavaScript**, with additional experience working with REST APIs, JSON, Maven, Docker, browser APIs, and command-line tooling.

## Featured Projects

### [FIFA World Cup 2026 Tracker](./world-cup-2026-tracker)

A Java application that retrieves and processes FIFA World Cup 2026 data to generate daily match reports, standings, advancement scenarios, and localized kickoff times.

**Highlights**
- REST API integration using Java `HttpClient`
- JSON parsing and domain modeling with Jackson
- Maven dependency management
- Time-zone conversion with the Java Time API
- Retry handling for HTTP, SSL, and network failures
- Graceful handling of partial API failures
- Match, standings, and tournament-advancement logic
- Console and file-based report generation

**Technologies:** Java 17, REST APIs, Jackson, Maven, Java Time API

---

###  [SportsAPI](./sports-api)

A Python command-line application that aggregates schedules and scores across multiple sports using API-Sports services.

Supported sports include soccer, baseball, American football, basketball, and hockey.

**Highlights**
- Integration with multiple REST API endpoints
- HTTP request and error handling
- League filtering, grouping, and sorting
- Seasonal sport detection
- Command-line argument handling
- Free-tier API date validation
- Time-zone-aware date processing
- Logging and file output for troubleshooting and reporting

**Technologies:** Python, REST APIs, Requests, JSON, CLI tooling

---

### [Extension Scheduler](./extension-scheduler) — Work in Progress

A Chrome and Edge extension in development that is designed to automatically enable or disable selected browser extensions according to configurable schedules.

**Current/Planned Features**
- Configurable daily schedules and active days
- Automatic extension state management
- Persistent user settings
- Browser service-worker architecture
- Options and popup interfaces
- Support for Chrome/Edge Extension APIs

**Technologies:** JavaScript, HTML, CSS, Chrome Extension APIs, Manifest V3

---

### [YouTube Category Blocker](./youtube-category-blocker) — Work in Progress

A browser extension in development that uses YouTube metadata to identify videos by category and tags and apply configurable viewing restrictions.

**Current/Planned Features**
- YouTube Data API integration
- Category and tag-based filtering
- Background and content-script communication
- Persistent extension settings
- Configurable blocking behavior
- Dynamic browser-extension UI behavior

**Technologies:** JavaScript, HTML, CSS, REST APIs, YouTube Data API, Chrome Extension APIs

---

### [Python Raycasting Game](./python-raycasting-game)

A first-person game built with Python and Pygame using raycasting techniques similar to early 3D games.

The project is organized into separate components for rendering, player movement, NPC behavior, maps, weapons, sprites, sound, and pathfinding.

**Highlights**
- Raycasting-based rendering
- Object-oriented application structure
- NPC and object management
- Pathfinding logic
- Player movement and interaction
- Sprite and weapon systems
- Modular game components

**Technologies:** Python, Pygame, OOP, graph traversal/pathfinding

---

## Skills Demonstrated

Across these projects, I have worked with:

- **Languages:** Python, Java, JavaScript, PowerShell
- **APIs:** REST, HTTP, JSON, third-party API integration
- **Development:** Object-oriented programming, modular application design, error handling, debugging
- **Automation:** Browser automation, scheduling, scripting, and command-line tools
- **Web/Browser:** HTML, CSS, Chrome/Edge Extension APIs
- **Tools & Platforms:** Git, GitHub, Maven, Docker
- **Reliability:** Retry logic, API error handling, validation, logging, and graceful failure behavior

## Coding Archive

The [`coding-archive`](./coding-archive) directory contains smaller projects and earlier programming exercises.

These projects document my progression while learning different languages, libraries, APIs, automation tools, and development concepts. My more recent and substantial projects are highlighted above.

## Current Focus

I'm continuing to expand this portfolio with projects focused on:

- API and integration development
- Automated software testing
- Python and Java development
- Technical troubleshooting and observability
- Automation and workflow tooling
- Reliable application design

## Repository Structure

```text
My-Portfolio/
├── world-cup-2026-tracker/
├── sports-api/
├── extension-scheduler/
├── youtube-category-blocker/
├── python-raycasting-game/
└── coding-archive/
```

Each featured project contains its own README with additional information about its functionality, architecture, setup, and usage.