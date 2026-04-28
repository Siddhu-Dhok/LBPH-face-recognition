# Smart Virtual Classroom - Face Recognition Attendance System

A comprehensive face recognition system designed to automate attendance tracking in virtual classrooms using LBPH (Local Binary Patterns Histograms) algorithm and OpenCV.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset Setup](#dataset-setup)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## Features

✨ **Key Features:**
- Real-time face detection and recognition
- Automated attendance tracking and recording
- LBPH algorithm for efficient face recognition
- Django REST API backend
- Dataset management and model training
- CSV-based attendance records
- Support for multiple student profiles

## Project Structure

```
smart-virtual-classroom-face-recognition/
├── capture_images.py              # Capture student face images
├── preprocess.py                  # Image preprocessing utilities
├── train_lbph.py                  # Train LBPH model
├── recognition_service.py         # Face recognition service
├── mock_attendance_backend.py     # Mock backend for testing
├── attendance.csv                 # Attendance records
│
├── face-dataset/                  # Student face dataset
│   ├── student_001/
│   ├── student_002/
│   ├── student_003/
│   ├── student_004/
│   └── student_005/
│
├── models/                        # Trained models
│   └── lbph_model.yml            # LBPH model file
│
└── face_recognition_backend/      # Django REST API
    ├── manage.py
    ├── db.sqlite3
    ├── face_recognition_backend/  # Project settings
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    └── recognition/               # Recognition app
        ├── models.py
        ├── views.py
        ├── urls.py
        ├── face_loader.py
        └── lbph/
            └── lbph_model.yml
```

## Requirements

- Python 3.8+
- Django 3.2+
- OpenCV (cv2)
- NumPy
- Pillow
- Flask (optional, for alternative backend)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/smart-virtual-classroom.git
cd smart-virtual-classroom-face-recognition
```

### 2. Create Virtual Environment
```bash
python3 -m venv svc-face-env
source svc-face-env/bin/activate  # On Windows: svc-face-env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Django Backend
```bash
cd face_recognition_backend
python manage.py migrate
python manage.py runserver
```

## Usage

### Step 1: Capture Student Faces
Capture images for each student:
```bash
python capture_images.py --student-id student_001 --num-images 20
```

### Step 2: Preprocess Images
Preprocess captured images:
```bash
python preprocess.py --input-dir face-dataset/ --output-dir face-dataset/
```

### Step 3: Train LBPH Model
Train the face recognition model:
```bash
python train_lbph.py --dataset-path face-dataset/ --model-output models/lbph_model.yml
```

### Step 4: Run Recognition Service
Start the recognition service:
```bash
python recognition_service.py
```

### Step 5: Mark Attendance
Run the mock backend or Django API to mark attendance:
```bash
python mock_attendance_backend.py
```

The attendance records will be saved to `attendance.csv`

## Dataset Setup

### Creating the Face Dataset

1. **Directory Structure**
```
face-dataset/
├── student_001/
│   ├── 0.jpg
│   ├── 1.jpg
│   └── ...
├── student_002/
│   ├── 0.jpg
│   ├── 1.jpg
│   └── ...
```

2. **Capture Images** (at least 20-30 per student):
   - Vary lighting conditions
   - Vary angles (front, left, right)
   - Include different expressions
   - Ensure clear face visibility

3. **Image Requirements**:
   - Format: JPG/PNG
   - Minimum resolution: 200x200 pixels
   - Face should be clearly visible and centered

## Architecture

### Core Components

1. **Face Detection**: OpenCV Cascade Classifiers
2. **Face Recognition**: LBPH (Local Binary Patterns Histograms)
3. **Backend**: Django REST Framework
4. **Data Storage**: SQLite database + CSV logs

### Workflow
```
Capture Images → Preprocess → Train Model → Recognition Service → Attendance Recording
```

## API Endpoints (Django Backend)

### Get All Students
```
GET /api/students/
```

### Mark Attendance
```
POST /api/attendance/
{
  "student_id": "student_001",
  "timestamp": "2026-04-28T10:30:00Z"
}
```

### Get Attendance Records
```
GET /api/attendance/?date=2026-04-28
```

## Configuration

Edit `face_recognition_backend/settings.py` for:
- Database configuration
- Model paths
- Recognition confidence threshold
- API settings

## Troubleshooting

### Issue: Model not found
**Solution**: Ensure you've run `train_lbph.py` first to generate the model file

### Issue: Poor recognition accuracy
**Solution**: 
- Add more training images
- Ensure good lighting during capture
- Retrain the model

### Issue: Django migrations failing
**Solution**: 
```bash
python manage.py makemigrations
python manage.py migrate
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- **Siddhesh Dhok** - Initial work - [[GitHub Profile](https://github.com/YOUR_USERNAME)](https://github.com/Siddhu-Dhok)

## Acknowledgments

- OpenCV community for excellent computer vision library
- Django community for robust web framework
- Local Binary Patterns algorithm research

## Support

For issues, questions, or suggestions, please open an issue on the [GitHub Issues](https://github.com/YOUR_USERNAME/smart-virtual-classroom/issues) page.

---

**Last Updated**: April 28, 2026
