# 🏰 Dungeon Battle Simulator - DevOps CI/CD Pipeline

Welcome to the **Dungeon Battle Simulator**!
This project is a DevOps demonstration of a CI/CD pipeline using **Jenkins**, **Python**, and **Groovy**. It simulates a battle between a custom Hero and a dungeon Enemy, generating detailed logs and a styled HTML report for every build.

## 🚀 Key Features

* **Cross-Platform Support:** The pipeline dynamically runs on either **Windows** or **Linux** agents based on user selection.
* **Parameterized Builds:** Users can customize the simulation input directly from Jenkins:
    * **Player Name:** Custom hero name.
    * **Hero Class:** Warrior, Mage, or Rogue.
    * **Level:** 1-100 validation.
    * **Hardcore Mode:** Boolean flag for increased difficulty.
* **Automated Environment:** Automatically installs Python dependencies (`requirements.txt`) inside the pipeline.
* **Atomic Artifacts Management:** Prevents "Zombie Files" by cleaning the workspace before execution and publishing artifacts immediately after generation.
* **Rich Reporting:** Generates a CSS-styled HTML report (`battle_report.html`) and a text log (`game_log.txt`).

---

## 🛠️ Pipeline Workflow

The `Jenkinsfile` defines the following stages:

1.  **Clean Workspace:** Removes all old files (`cleanWs()`) to ensure a fresh build environment.
2.  **Checkout Code:** Pulls the latest script version from GitHub.
3.  **Validate Parameters:** Ensures the input level is valid (1-100).
4.  **Install Requirements:** Runs `pip install` (adapts command for Windows vs. Linux).
5.  **Run Script & Generate HTML:**
    * Executes `dungeon_sim.py` with the provided arguments.
    * Passes flags like `--hardcore_mode` if selected.
    * **IMMEDIATELY** archives and publishes the HTML report to avoid race conditions.

---

## 📋 Prerequisites

To run this pipeline, you need:
* **Jenkins** (Controller) with access to GitHub.
* **Agents:** At least one Windows node and/or one Linux node connected to Jenkins.
* **Python 3.x:** Installed and added to PATH on all agents.
* **Plugins:**
    * Pipeline
    * HTML Publisher Plugin
    * Workspace Cleanup Plugin (Optional but recommended)

---

## 🎮 How to Run

1.  Open the Jenkins Job.
2.  Click on **Build with Parameters**.
3.  **Select Node:** Choose `windows` or `linux`.
4.  **Enter Details:** Name your hero, choose a class and level.
5.  **Hardcore Mode:** Check the box if you dare! 😈
6.  Click **Build**.
7.  Once finished, click **Battle Report** on the sidebar (or download the artifact) to see the results.

---

## 💻 Tech Stack

* **Logic:** Python 3 (`argparse`, `random`, `datetime`).
* **Orchestration:** Jenkins (Declarative Pipeline).
* **Version Control:** Git & GitHub.
* **Networking:** Ngrok (for public access tunneling).

---

### 📜 License
This project was created for educational purposes as part of a DevOps Final Project.
