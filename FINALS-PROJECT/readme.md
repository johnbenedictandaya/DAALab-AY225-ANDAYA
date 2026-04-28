Fashion-MNIST · Analytics Dashboard
A high-performance, web-based data science dashboard designed to visualize and analyze the Fashion-MNIST dataset. This project features a "Deep-Space Terminal" aesthetic and is optimized to handle large-scale CSV parsing (70,000 rows) and grayscale image reconstruction directly in the browser.

🚀 Project Overview
The Fashion-MNIST Analytics Dashboard is a collaborative data science tool that transforms raw CSV data into an interactive visual experience. It allows users to explore clothing categories, view statistical distributions, and generate data-driven narratives regarding image density and classification variance.

This project was developed following a collaborative Git workflow, dividing responsibilities between a Dataset Engine (Student 1) and a Visual Analysis Engine (Student 2).

✨ Features
High-Performance Parsing: Utilizes Web Workers via PapaParse to handle 70,000 rows of data off the main thread, ensuring the UI remains responsive during heavy loads.

Grayscale Image Reconstruction: Dynamically renders 28x28 grayscale images from raw pixel arrays (784 columns) using the HTML5 Canvas API.

Interactive Visualizations: Powered by Chart.js, featuring label distribution bar charts and pixel density analysis.

Statistical Engine: Computes Mean, Variance, and Global Averages in a single pass for maximum efficiency.

Data-Driven Narrative: An automated "Insights" generator that produces a 4-sentence analysis using computed values and Linear Regression predictions for item weight.

Deep-Space Terminal UI: A custom-themed interface using a neon-phosphor green palette (#00ffa3) with responsive side-navigation and "pixel-flicker" loading animations.

🛠 Tech Stack
Frontend: HTML5, CSS3 (Custom Variables & Keyframe Animations)

Logic: JavaScript (ES6+ / Async-Await)

Data Handling: PapaParse (CSV Parsing & Web Workers)

Visuals: Chart.js (Data Visualization)

Typography: Orbitron (Display), Syne (Body), and JetBrains Mono (Data)

📂 Folder Structure
Plaintext
├── archive/
│   ├── fashion-mnist_train.csv  # 60,000 rows (Primary dataset)
│   └── fashion-mnist_test.csv   # 10,000 rows (Testing subset)
├── index.html                   # Main dashboard architecture
├── style.css                    # "Deep-Space" theme and responsive layout
├── script.js                    # Consolidated Master Logic (Modules 1 & 2)
└── README.md                    # Project documentation

## ⚙️ Installation & Data Setup

Because the Fashion-MNIST dataset exceeds GitHub's file size limits, you must add the data manually:

1. **Clone the repo:** `git clone https://github.com/ronzandev/DAALab-AY225-MORANTE.git`
2. **Download Data:** Get the CSV files from [Kaggle Fashion-MNIST](https://www.kaggle.com/datasets/zalando-research/fashion-mnist).
3. **Place Files:** Create a folder named `archive` in the root directory and move `fashion-mnist_train.csv` inside.
4. **Run:** Open `index.html` via a Local Server (e.g., Live Server in VS Code).

VS Code: Use the Live Server extension (Right-click index.html > "Open with Live Server").

Python: Run python -m http.server 8000 in your terminal.

🖱 Usage Instructions
Initialize: Click the "Load Dataset" button in the top bar to trigger the Web Worker.

Explore: Use the Dataset Explorer to filter by specific clothing labels (e.g., "Pullover" or "Ankle Boot").

Sort: Sort the table by "Avg Pixel" to see which items are the most visually dense.

Insights: Scroll to the bottom to see the Automated Data Narrative, which highlights key statistics and classification recommendations based on the current data batch.

📊 Core Logic Awareness
The "Handshake" Protocol
The dashboard uses a global state management system. Module 1 (Student 1) handles the raw data processing. Once complete, it triggers a "Handshake" to Module 2 (Student 2) via a callback (window.onDataReady), ensuring charts only render once valid data is available.

Linear Regression & Metadata Mapping
To satisfy data modeling requirements, the engine performs a mock Linear Regression to predict physical shipping weight:
Predicted Weight (g) = (Mean Pixel Intensity * 1.2) + 50

Additionally, items are mapped into two metadata categories:

Heavy/Outerwear: Pullovers, Coats, Sneakers, Ankle Boots.

Lightwear: T-shirts, Trousers, Dresses, Sandals, Shirts.

⚠️ Known Limitations
Browser Memory: Parsing the full 60k-row training set can consume significant browser memory. If the page crashes, try using the 10k-row test set.

CORS Requirements: The project will not function if opened directly as a file (file://...). It requires a http:// or localhost environment.

👥 Contributors
Student 1: MORANTE, RON ZANDRO — Dataset Engine, Stats Logic, & Table Rendering.

Student 2: FUASO, JOHN WILLFORD — Data Visualization, Narrative Engine, & UI Polishing.

Developed for the Data Science Collaborative Git Project.