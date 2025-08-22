# 🔍 System Monitoring App — Built with Flask


A lightweight system monitoring dashboard built using **Flask** that provides real-time stats for:

* 🧠 **CPU usage**
* 🧵 **RAM usage**
* 📯 **Disk I/O**
* 🌐 **Network activity**

This app features both **gauge meters** and **graph views** to visualize system performance dynamically.

---

## 🚀 Live Demo
**Give Some Time For Rendering**
* 👉 Try the app here:
🔗 [https://monitoring-app-t664.onrender.com](https://monitoring-app-t664.onrender.com)

---

## 💻 How to Use

### 🔧 Run from Source

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Karthick-MurugesanG/Monitoring_app.git
   cd Monitoring_app
   ```

2. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask application:**

   ```bash
   python app.py
   ```

4. Open your browser and visit:
   👉 `http://127.0.0.1:5000/`

---

### �� Windows Users

* Download the \*\*standalone \*\*\`\` file from the `distt/` folder.
* No Python installation is required — just run the executable.

---

## 📆 Key Features

* 🔁 Real-time resource monitoring via `/api/stats`
* 🔄 Toggle between **accelerator view (gauge)** and **graph view**
* 🖥️ Minimal, responsive UI
* ⚙️ Python-powered backend using `psutil`
* 🧳 Single-file `.exe` for distribution

---

## 🛠️ Tech Stack

**Backend:**

* Python
* Flask
* psutil

**Frontend:**

* HTML
* CSS
* JavaScript (Chart.js)

**Packaging:**

* PyInstaller (for `.exe` generation)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
