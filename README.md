# 🧠 IntelliMed – AI-Powered Medical Diagnosis Platform

**IntelliMed** is a comprehensive and intelligent diagnostic system that uses advanced deep learning models to assist in early detection of multiple medical conditions. Designed as a web-based platform using **Streamlit**, it enables users to upload medical images and receive instant predictions. It features a secure login system with separate views for users and admins.
# Screenshots
![Screenshot 2025-06-11 203937](https://github.com/user-attachments/assets/eb9256a4-5fe5-4ac0-92b7-d5fa33e0c9d1)
![Screenshot 2025-06-11 204150](https://github.com/user-attachments/assets/3f106b4c-408a-4053-ad49-f3f5001448eb)
![Screenshot 2025-06-11 203745](https://github.com/user-attachments/assets/c375cd38-09e3-4aaa-a56a-367024c0d059)

![Screenshot 2025-06-12 103700](https://github.com/user-attachments/assets/d9c03b60-5012-4842-ab68-6570e97a1b4e)

## 🚀 Features

- ✅ **AI-Based Diagnoses**:
  - Brain Tumor Detection (MRI)
  - Skin Cancer Classification
  - Lung Cancer Prediction (X-Ray)
  - Alzheimer's Detection (MRI)
  - ECG Analysis (Arrhythmia)

- 📈 **Admin Dashboard**:
  - Track registered users and scan activity
  - Visualize scan types, frequency, and trends using Plotly
  - Monitor user engagement and model performance

- 🔐 **Authentication System**:
  - Secure login/registration for users and admins
  - Role-based access control

- 📁 **Real-Time Uploads**:
  - Upload images and receive instant predictions with model confidence scores

- 🌐 **Hosted on AWS EC2 with DuckDNS**:
  - Public access via a custom subdomain (`intellimed.duckdns.org`)

---

## 🧪 AI Models

Each model is trained separately using domain-specific datasets:

| Condition     | Model | Input Type     | Accuracy | Format         |
|---------------|--------|----------------|----------|----------------|
| Brain Tumor   | CNN    | MRI Scans      | ~92%     | `brain_model3.h5` |
| Lung Cancer   | CNN    | Chest X-rays   | ~89%     | `lung_model.h5`   |
| Skin Cancer   | CNN    | Dermoscopy     | ~90%     | `skin_model.h5`   |
| Alzheimer’s   | CNN    | MRI Scans      | ~88%     | `alzheimer_model.h5` |
| ECG Arrhythmia| LSTM   | ECG Sequences  | ~87%     | `ecg_model.h5`      |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit + Plotly
- **Backend**: Python, TensorFlow, OpenCV
- **Database**: MySQL (user data & logs)
- **Hosting**: Ubuntu EC2 (AWS Free Tier)
- **Security**: Role-based auth, hashed passwords (future upgrade)
- **Model Format**: `.h5` (Keras)

---

## 🧬 Workflow Overview

1. 🔐 **Login/Register** (User/Admin)  
2. 🖼️ **Upload Scan/Image**  
3. 🧠 **AI Model Inference**  
4. 📊 **Log Results**  
5. 📋 **Admin Dashboard Monitoring**

---

## 📊 Admin Dashboard Views

- 👥 Registered Users (Table)
- 🧪 All Scan Logs (Table)
- 📊 Scan Count per User (Bar Chart)
- 🔬 Distribution of Scan Types (Pie Chart)
- 📅 Scans Over Time (Line Chart)

---

## ⚙️ Run Locally

```bash
# Clone repo and navigate
git clone https://github.com/yourusername/intellimed.git
cd intellimed

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run main.py
