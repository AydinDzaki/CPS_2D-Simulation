# Distributed 2D Physics Simulation (Euler Integration)

Proyek ini adalah simulasi fisika hibrida yang memisahkan beban komputasi dan visualisasi ke dua *platform* berbeda. Mikrokontroler (Arduino) bertugas menangani perhitungan fisika vektor menggunakan **Metode Euler**, sementara PC (Python) bertugas menangani GUI.

## 📋 Deskripsi Sistem
Sistem bekerja dengan arsitektur *Hardware-in-the-Loop* sederhana:
1.  **Backend (Arduino):** Menjalankan *loop* fisika (gravitasi, gesekan, tumbukan) dan integrasi Euler ($posisi += kecepatan \cdot \Delta t$).
2.  **Frontend (Python):** Menerima input user, mengirim perintah gaya (*force*) ke Arduino, dan memvisualisasikan data posisi yang diterima via Serial.

## 📂 Struktur File
* `Logika.ino` : Firmware untuk Arduino.
* `Input Output.py` : Skrip Python untuk visualisasi dan kontrol.

## 🛠️ Prasyarat (Requirements)
**Hardware:**
* 1x Arduino Uno (atau board kompatibel lainnya).
* Kabel USB (untuk komunikasi Serial).

**Software:**
* Arduino IDE.
* Python 3.x.
* Library Python:
  ```bash
  pip install pygame pyserial