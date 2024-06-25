from vpython import *
import random

# Buat jendela VPython
scene = canvas(
    title='Game Ball UAS', 
    width=800, height=600, 
    center=vector(0,0,0))

point = 0
start_time = clock()
duration = 60  # Durasi dalam detik
mode = 'bounce'  # Mode default

# Teks untuk menampilkan poin dan waktu
point_display = label(pos=vector(-4, 5, 0), text=f'Point: {point}', color=color.white, height=30, box=False)
time_display = label(pos=vector(4, 5, 0), text=f'Time: {duration}', color=color.white, height=30, box=False)
mode_display = label(pos=vector(0, 6, 0), text=f'Mode: {mode}', color=color.white, height=30, box=False)

# Warna-warna yang telah ditentukan
colors = [vector(0, 0, 1),  # Biru
          vector(1, 1, 0),  # Kuning
          vector(1, 0, 1),  # Ungu
          vector(0, 1, 0),  # Hijau
          vector(1, 0, 0),  # Merah
          vector(1, 0.5, 0)]  # Oranye  

# Fungsi untuk menghasilkan kecepatan acak di sumbu x dan y
def random_velocity():
    return vector(random.uniform(-1, 1), random.uniform(-1, 1), 0)

# Buat bola-bola
balls = []
for i in range(6):
    ball = sphere(pos=vector(random.uniform(-5, 5), random.uniform(-5, 5), 0),
                  radius=0.5,
                  color=colors[i])
    ball.velocity = random_velocity()
    balls.append(ball)

# Menandai bola ungu
purple_ball = balls[2]

# Kecepatan awal untuk bola ungu
purple_ball.velocity = random_velocity()
player_velocity = 0.5

# Fungsi untuk menangani input dari keyboard
def key_input(evt):
    global mode
    s = evt.key
    if s == 'left':
        if purple_ball.pos.x > -5:
            purple_ball.pos.x -= player_velocity
    elif s == 'right':
        if purple_ball.pos.x < 5:
            purple_ball.pos.x += player_velocity
    elif s == 'up':
        if purple_ball.pos.y < 5:
            purple_ball.pos.y += player_velocity
    elif s == 'down':
        if purple_ball.pos.y > -5:
            purple_ball.pos.y -= player_velocity
    elif s == 'm':  # Ganti mode saat tombol 'm' ditekan
        if mode == 'bounce':
            mode = 'stop'
        else:
            mode = 'bounce'
        mode_display.text = f'Mode: {mode}'

# Bind fungsi key_input ke canvas
scene.bind('keydown', key_input)

# Tambahkan batas visual
border_thickness = 0.1
border_color = color.white

# Dinding atas
top_wall = box(pos=vector(0, 5.5, 0), size=vector(10, border_thickness, 0.1), color=border_color)
# Dinding bawah
bottom_wall = box(pos=vector(0, -5.5, 0), size=vector(10, border_thickness, 0.1), color=border_color)
# Dinding kiri
left_wall = box(pos=vector(-5.5, 0, 0), size=vector(border_thickness, 10, 0.1), color=border_color)
# Dinding kanan
right_wall = box(pos=vector(5.5, 0, 0), size=vector(border_thickness, 10, 0.1), color=border_color)

# Loop untuk menggerakkan bola
dt = 0.05
while True:
    rate(100)  # Tentukan kecepatan animasi

    current_time = clock()
    elapsed_time = current_time - start_time
    remaining_time = max(0, duration - elapsed_time)
    time_display.text = f'Time: {int(remaining_time)}'
    
    if remaining_time == 0:
        break
    
    for ball in balls:
        if ball != purple_ball:  # Bola ungu hanya dikendalikan oleh keyboard
            ball.pos += ball.velocity * dt
        
            # Memantul dari dinding
            if ball.pos.x < -5 or ball.pos.x > 5:
                ball.velocity.x *= -1
            if ball.pos.y < -5 or ball.pos.y > 5:
                ball.velocity.y *= -1
        
            # Deteksi tabrakan antara bola-bola
            for other_ball in balls:
                if other_ball != ball:
                    distance = mag(ball.pos - other_ball.pos)
                    if distance <= ball.radius + other_ball.radius:
                        # Memastikan bola tidak tembus
                        overlap = ball.radius + other_ball.radius - distance
                        direction = norm(ball.pos - other_ball.pos)
                        ball.pos += direction * overlap / 2
                        other_ball.pos -= direction * overlap / 2

                        # Hitung kecepatan baru setelah tabrakan elastis
                        v1 = ball.velocity
                        v2 = other_ball.velocity
                        m1 = m2 = 1  # Asumsi massa bola sama

                        if ball == purple_ball or other_ball == purple_ball:
                            if mode == 'bounce':
                                # Bola lain memantul saat ditabrak
                                if ball == purple_ball:
                                    other_ball.velocity = random_velocity()
                                else:
                                    ball.velocity = random_velocity()
                            elif mode == 'stop':
                                # Bola lain berhenti saat ditabrak
                                if ball == purple_ball:
                                    other_ball.velocity = vector(0, 0, 0)
                                else:
                                    ball.velocity = vector(0, 0, 0)

                            # Tambah poin saat bola ungu bertabrakan
                            point += 1
                            point_display.text = f'Point: {point}'
                        else:
                            # Tabrakan elastis
                            ball.velocity = v1 - 2 * m2 / (m1 + m2) * dot(v1 - v2, ball.pos - other_ball.pos) / mag(ball.pos - other_ball.pos)**2 * (ball.pos - other_ball.pos)
                            other_ball.velocity = v2 - 2 * m1 / (m1 + m2) * dot(v2 - v1, other_ball.pos - ball.pos) / mag(other_ball.pos - ball.pos)**2 * (other_ball.pos - ball.pos)

def show_applause(applause_text, applause_color):
    applause_label = label(pos=vector(0, 0, 0), text=applause_text, color=applause_color, height=50, box=False)
    start_time = clock()
    while clock() - start_time < 5:
        rate(1)  # Tunggu selama 1 detik
    applause_label.visible = False  # Sembunyikan label setelah 5 detik

# Menampilkan apresiasi berdasarkan poin
if point >= 80:
    applause_text = "Gold Medal!"
    applause_color = color.yellow
elif point >= 50:
    applause_text = "Silver Medal!"
    applause_color = color.gray(0.7)  # Warna abu-abu
elif point >= 25:
    applause_text = "Bronze Medal!"
    applause_color = color.orange
else:
    applause_text = "Better luck next time!"
    applause_color = color.red

# Tampilkan apresiasi
show_applause(applause_text, applause_color)
