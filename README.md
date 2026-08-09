# AI Proctored Examination System

A microservices-based online examination platform with AI-driven proctoring. Built in response to the shift to remote examinations, it lets institutions run and grade tests at scale while flagging suspicious behavior (face mismatches, missing faces, off-screen gaze, unusual motion) through a webcam feed during the test.

[![License](https://img.shields.io/github/license/SuyashMore/AI-Proctored-Examination-System.svg?style=flat-square)](LICENSE)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

## About

Students register, log in, and take a test; results are computed and available immediately without manual grading. Administrators can create, edit, and delete tests and their questions. While a test is in progress, an anomaly-detection service analyzes the student's webcam feed for signs of malpractice.

## Architecture

The system is split into five independent services, documented in more detail in [`Documents/Architecture.pdf`](Documents/Architecture.pdf):

| Service | Location | Stack | Responsibility |
|---|---|---|---|
| **Backend / Web Server** | `src/BackendServer/` | Node.js, Express, EJS | Serves the student/teacher-facing web app (`routers/mainRouter.js`, `routers/student.js`, `routers/teacher.js`) and views |
| **Auth Server** | `src/AuthServer/` | Python, Flask, Flask-RESTful | Registration, login, and student record management, backed by Oracle Cloud's Borneo NoSQL DB (`dbManager.py`, `auth_functions.py`) |
| **Test Server** | `src/TestServer/` | Python, Flask | Serves test/question data and handles test-taking logic (`test_functions.py`, `dbManager.py`) |
| **Result Server** | `src/ResultServer/` | Python, Flask | Computes and serves exam results (`dbManager.py`) |
| **Anomaly (Proctoring) Server** | `src/AnomalyServer/` | Python, OpenCV, dlib, face_recognition | Real-time webcam analysis: face recognition against the registered student photo, facial landmark tracking, upper-body detection, and motion tracking (`FaceRecognition.py`, `LandmarkDetection.py`, `UpperBodyDetection.py`, `MotionTracking.py`) |

Standalone prototypes for the individual proctoring techniques (face detection, landmark detection, motion detection, upper-body detection) live under [`Documents/Intelligence Service/`](Documents/Intelligence%20Service) for reference.

## Requirements

- Python 3.6.9
- Node.js
- OpenCV, dlib, face_recognition (see `src/AnomalyServer/requirements.txt`)
- Oracle Cloud Infrastructure (OCI) account + API key, and the `oci` / `borneo` Python packages (used by Auth/Test/Result servers for Borneo NoSQL access — see the `.oci/` config folders in each service)

## Installation

```sh
git clone https://github.com/SuyashMore/AI-Proctored-Examination-System.git
cd AI-Proctored-Examination-System

# Backend web server
cd src/BackendServer
npm install
cd ../..

# Python services
pip install oci borneo
pip install -r src/AnomalyServer/requirements.txt
```

Each of the Auth/Test/Result servers expects an OCI API key under its own `.oci/` folder (see `src/AuthServer/.oci/` for the expected layout) to connect to the Borneo database.

## Running the Application

Each service runs independently — start them in separate terminals:

```sh
# Anomaly / proctoring service
sudo python3 src/AnomalyServer/Server.py

# Test service
sudo python3 src/TestServer/server.py

# Result service
sudo python3 src/ResultServer/server.py

# Authorization service
sudo python3 src/AuthServer/server.py

# Main backend/web server
cd src/BackendServer
npm run dev
```

## Documentation

- [Software Requirements Specification](<Documents/AI Exam System SRS.pdf>)
- [Architecture](Documents/Architecture.pdf)
- [Project overview slides](<Documents/AI Exam System.pptx>)

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.
