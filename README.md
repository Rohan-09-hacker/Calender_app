# Time Manager PRO 📅

An enterprise-grade, high-contrast workspace productivity dashboard engineered with an asynchronous execution architecture and a localized persistent relational database storage layer. Developed as part of the Pinnacle Labs Python Development Internship Program (2026).

---

## 🏗️ Asynchronous System Architecture

To prevent data-heavy input/output cycles from locking or micro-stuttering the primary graphical interface, the application separates layout rendering from storage logic.

<br>

<table align="center" style="border: none; border-collapse: collapse; background: transparent;">
  <tr>
    <td align="center" style="border: none; padding: 0 20px;">
      <div style="background-color: #171a21; color: #00b4d8; border: 2px solid #2d3748; border-radius: 8px; padding: 15px 25px; font-weight: bold; font-family: 'Segoe UI', sans-serif; font-size: 14px;">
        🖥️ Premium CustomTkinter UI <br> <span style="font-size: 11px; color: #e2e8f0; font-weight: normal;">Main Graphical Thread (Responsive)</span>
      </div>
    </td>
    <td align="center" style="border: none; font-size: 24px; color: #00b4d8; padding: 0 10px;">🔄</td>
    <td align="center" style="border: none; padding: 0 20px;">
      <div style="background-color: #1f242e; color: #2ecc71; border: 1px solid #4a5568; border-radius: 8px; padding: 15px 25px; font-weight: bold; font-family: 'Segoe UI', sans-serif; font-size: 14px;">
        ⚙️ Background Thread Worker <br> <span style="font-size: 11px; color: #4a5568; font-family: monospace;">threading.Thread (Non-Blocking)</span>
      </div>
    </td>
  </tr>
  <tr>
    <td colspan="3" align="center" style="border: none; font-size: 20px; color: #2d3748; padding: 10px 0;">⬇️ Upstream Read / Downstream Write</td>
  </tr>
  <tr>
    <td colspan="3" align="center" style="border: none;">
      <div style="background-color: #0f1115; color: #e2e8f0; border: 1px solid #2d3748; border-radius: 6px; padding: 10px 40px; font-family: monospace; font-size: 12px; display: inline-block;">
        🗄️ SQLite Relational Storage Engine [reminders.db]
      </div>
    </td>
  </tr>
</table>

<br>

### 1. Asynchronous Data Ingestion Engine
* Standard UI queries block loops while waiting for disk access. This system bypasses that by offloading SQL actions to distinct background thread pools.
* Clicking calendar grids triggers non-blocking threads to read records smoothly without interface stutter.

### 2. Relational Schema Data Layer (`calendar_engine.py`)
* Automatically manages connection allocations to create a permanent `reminders.db` index file locally.
* Restricts task timestamps strictly to evaluated validation check filters (`HH:MM`).

---

## 🚀 Key Features

* **Cyber-Nordic Slate Aesthetic:** Completely revamped color layout utilizing a deep charcoal base (`#0f1115`) with sharp electric cyan headers and emerald controls.
* **Persistent Local Storage:** Integrated SQLite table mappings to permanently save tasks across system reboots.
* **Dynamic Content Cards:** Schedule logs are cleanly rendered inside individual container blocks rather than raw text spaces, featuring custom time badges and alignment hooks.
* **Interactive Micro-Animations:** Buttons, entry widgets, and custom delete parameters feature hardware-accelerated, fluid hover-fade opacity transitions.
* **Smart Placeholders:** Automatically renders context-aware clean strings (*"Workspace Cleared! No tasks for this day."*) when highlighted calendar spaces contain no logged records.

---

## 🛠️ Technical Stack & Dependencies

* **Language:** Python 3.11+
* **UI Custom Wrapper:** `customtkinter` (Anti-aliased desktop framework layouts)
* **Calendar Engine Matrix:** `tkcalendar` (Dynamic date grid component)
* **Database Pipeline:** Relational SQLite3 Engine
* **Concurrent Workers:** Asynchronous background `threading` daemons

---

## 📦 Local Installation & Setup Guide

Ensure your development environment has your system dependencies updated before launching the script execution paths:

### Step 1: Install Premium Component Packs
Open your terminal window console inside your `task3_calendar_app` directory and install the third-party framework wrappers:
```bash
pip install customtkinter tkcalendar
