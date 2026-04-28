# capture_images.py
import cv2
import os

def capture(student_id, save_dir='face-dataset', samples=20):
    path = os.path.join(save_dir, student_id)
    os.makedirs(path, exist_ok=True)

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    count = 0
    print("Press 'c' to capture, 'q' to quit")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
        cv2.imshow('capture', frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('c'):
            if len(faces) == 0:
                print("No face detected, try again.")
                continue
            # crop the largest face
            x,y,w,h = max(faces, key=lambda f: f[2]*f[3])
            face_img = gray[y:y+h, x:x+w]
            fname = os.path.join(path, f'{count+1}.jpg')
            cv2.imwrite(fname, cv2.resize(face_img, (200, 200)))
            count += 1
            print(f"Saved {fname} ({count}/{samples})")
            if count >= samples:
                break
        elif k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', required=True, help='student id (e.g. student_001)')
    parser.add_argument('--samples', type=int, default=15)
    args = parser.parse_args()
    capture(args.id, samples=args.samples)
