import pygame
import serial
import time
from collections import deque

SERIAL_PORT = 'COM6'
BAUD_RATE = 115200
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RADIUS = 15

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Visualizer Simulasi Arduino")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE_INFO = (100, 150, 255)

try:
    data_font = pygame.font.SysFont(None, 24)
except Exception as e:
    print(f"Peringatan: Tidak bisa memuat font. {e}")
    data_font = pygame.font.Font(None, 24)

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.05)
    print(f"Terhubung di {SERIAL_PORT}...")
    time.sleep(2) 
except serial.SerialException as e:
    print(f"Tidak bisa membuka port {SERIAL_PORT}.")
    print(e)
    exit()

# 
current_pos_x = SCREEN_WIDTH / 2
current_pos_y = SCREEN_HEIGHT / 2
current_vel_x = 0.0
current_vel_y = 0.0
current_dt = 0.0


trajectory_trace = deque(maxlen=200) 

running = True
while running:
    
    char_to_send = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: char_to_send = b'w'
            if event.key == pygame.K_s: char_to_send = b's'
            if event.key == pygame.K_a: char_to_send = b'a'
            if event.key == pygame.K_d: char_to_send = b'd'
            trajectory_trace.clear() 
            
    if char_to_send:
        ser.write(char_to_send)

    # Baca output dari Arduino
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            parts = line.split(',')
        
            if len(parts) == 5:
                current_pos_x = float(parts[0])
                current_pos_y = float(parts[1])
                current_vel_x = float(parts[2])
                current_vel_y = float(parts[3])
                current_dt = float(parts[4])
                
                trajectory_trace.append((int(current_pos_x), int(current_pos_y)))
                
    except Exception as e:
        pass 

    screen.fill(BLACK) 
    
    if len(trajectory_trace) > 1: 
        pygame.draw.aalines(screen, GREEN, False, list(trajectory_trace))

    pygame.draw.circle(screen, RED, (int(current_pos_x), int(current_pos_y)), RADIUS)

    pos_text = f"Posisi X, Y:  {current_pos_x:.1f}, {current_pos_y:.1f}"
    vel_text = f"Kecep. vX, vY: {current_vel_x:.1f}, {current_vel_y:.1f}"
    dt_text  = f"DeltaTime (dt): {current_dt:.6f} s"
    drag_info = "(Gesekan/Drag terlihat dari vX/vY yang melambat)"
    
    text_surface_pos = data_font.render(pos_text, True, WHITE)
    text_surface_vel = data_font.render(vel_text, True, BLUE_INFO)
    text_surface_dt  = data_font.render(dt_text, True, BLUE_INFO)
    text_surface_drag = data_font.render(drag_info, True, WHITE)
    
    screen.blit(text_surface_pos, (10, 10))
    screen.blit(text_surface_vel, (10, 30))
    screen.blit(text_surface_dt,  (10, 50))
    
    screen.blit(text_surface_drag, (10, SCREEN_HEIGHT - 30))

    pygame.display.flip() 
    
    clock.tick(60)

ser.close()
pygame.quit()
print("Koneksi ditutup.")