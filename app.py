import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# ============ SETUP KAMERA ============
cap = cv2.VideoCapture(0)  # ganti ke 1 kalau kamera tidak muncul

# ============ SETUP GUI ============
root = tk.Tk()
root.title("Color Detective - Move the Slider!")
root.geometry("950x620")
root.configure(bg="#f0f0f0")

# --- Panel kiri: video ---
video_frame = tk.Frame(root, bg="#f0f0f0")
video_frame.pack(side=tk.LEFT, padx=15, pady=15)

video_label = tk.Label(video_frame, bg="black")
video_label.pack()

# --- Panel kanan: slider ---
ctrl_frame = tk.Frame(root, bg="#f0f0f0")
ctrl_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=15, pady=15)

tk.Label(ctrl_frame, text="Adjust until\nyour object is detected!",
         font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=(0, 15))

def buat_slider(parent, label, dari, sampai, awal):
    tk.Label(parent, text=label, font=("Arial", 11, "bold"),
             bg="#f0f0f0", anchor="w").pack(fill=tk.X, pady=(8, 0))
    s = tk.Scale(parent, from_=dari, to=sampai, orient=tk.HORIZONTAL,
                 length=260, bg="#f0f0f0", highlightthickness=0)
    s.set(awal)
    s.pack(fill=tk.X)
    return s

h_min = buat_slider(ctrl_frame, "H Min (Hue)", 0, 180, 100)
h_max = buat_slider(ctrl_frame, "H Max (Hue)", 0, 180, 130)
s_min = buat_slider(ctrl_frame, "S Min (Saturation)", 0, 255, 50)
v_min = buat_slider(ctrl_frame, "V Min (Value)", 0, 255, 50)

# Tombol reset
def reset_slider():
    h_min.set(100); h_max.set(130); s_min.set(50); v_min.set(50)

tk.Button(ctrl_frame, text="Reset", command=reset_slider,
          font=("Arial", 11), bg="#e0e0e0").pack(pady=20)

# ============ LOOP VIDEO ============
def update_frame():
    ret, frame = cap.read()
    if ret:
        # Konversi ke HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Ambil nilai slider
        lower = np.array([h_min.get(), s_min.get(), v_min.get()])
        upper = np.array([h_max.get(), 255, 255])

        # Buat mask & hasil
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # Gabungkan original + hasil (kiri-kanan)
        combined = np.hstack((frame, result))
        combined = cv2.resize(combined, (640, 240))

        # Konversi ke format tkinter
        img = Image.fromarray(cv2.cvtColor(combined, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)

        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    # Ulangi setiap 30ms
    root.after(30, update_frame)

# ============ TUTUP APLIKASI ============
def on_close():
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

# ============ JALANKAN ============
update_frame()
root.mainloop()
