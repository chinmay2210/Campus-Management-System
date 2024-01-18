# AttendanceManagmentSystem

# 📋 Attendance Management System for College Campus Recruitment

Welcome to the Attendance Management System for college campus recruitment! This project is designed to help college recruiters efficiently take attendance of students during campus recruitment events using QR codes. It leverages Flask for the backend and Python KivyMD for the coordinator interface. Additionally, it automates the process of sending admit cards to students via email. 🎓📝💌

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Recruiting students during campus placements is a crucial process for colleges and companies alike. However, managing and recording attendance manually can be cumbersome and prone to errors. This Attendance Management System simplifies the process by providing a user-friendly interface for coordinators to mark attendance using QR codes. Additionally, it automates the process of sending admit cards to students via email, enhancing the overall efficiency of the recruitment process. 💼👨‍🎓📷🔐📧

## Features

- **User-friendly Interface:** The system offers a simple and intuitive interface built using KivyMD, making it easy for coordinators to use. 🖥️💼

- **Backend with Flask:** The Flask backend handles the logic of attendance management, making it easy to integrate with other systems or extend functionality. 🐍

- **Secure QR Code Scanning:** Coordinators can scan QR codes generated for each student, ensuring accurate and secure attendance tracking. 📷🔐

- **Automated Admit Card Emailing:** The system automates the process of sending admit cards to students via email, reducing manual administrative work. 💌

- **Data Export:** Attendance data can be easily exported for analysis and reporting. 📊📈

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system. 🐍
- The required Python packages mentioned in the `requirements.txt` file. 📦
- Configuration for sending emails (SMTP server settings, email templates, etc.) set up in the project.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/attendance-management-system.git
   ```

2. Navigate to the project directory:
   ```
   cd attendance-management-system
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask backend:
   ```
   python app.py
   ```

2. Open the KivyMD coordinator interface:
   ```
   python AttendanceApp.py
   ```

3. Use the coordinator interface to manage attendance during campus recruitment events by scanning QR codes. 📋📅

4. Admit cards will be automatically generated and emailed to students.

## Contributing

We welcome contributions from the community. If you would like to contribute to this project, please follow these steps:

1. Fork the repository on GitHub. 🍴

2. Clone your forked repository to your local machine. 💻

3. Create a new branch for your feature or bug fix. 🌿

4. Make your changes and commit them with descriptive commit messages. 🛠️

5. Push your changes to your fork on GitHub. 🚀

6. Create a pull request to the `main` branch of the original repository. 🔄

Please ensure that your code follows best practices, is well-documented, and includes relevant tests when applicable. 📝✅



---

Thank you for using the Attendance Management System for college campus recruitment! If you have any questions or encounter any issues, please feel free to open an issue on the GitHub repository. We appreciate your feedback and contributions. 🙌🚀
