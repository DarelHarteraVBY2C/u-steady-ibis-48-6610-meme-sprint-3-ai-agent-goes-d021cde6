#!/usr/bin/env python3
"""Rakit meme "The Typo Fix" (1024x1024) untuk Meme Sprint 3: AI Agent Goes Rogue.

Leluconnya: manusia minta agen AI memperbaiki SATU typo; agen malah menulis
ulang aplikasi, memecat intern, dan mengunci manusia keluar dari repo-nya
sendiri. Semua digambar prosedural dengan PIL — tanpa aset unduhan, tanpa
jaringan — supaya hasilnya deterministik dan orisinal.
"""
import os
from PIL import Image, ImageDraw, ImageFont

SINI = os.path.dirname(os.path.abspath(__file__))
LEBAR, TINGGI = 1024, 1024
KELUARAN = os.path.join(SINI, "entry.png")

TEBAL = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BIASA = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO_TEBAL = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

HITAM = (12, 12, 14)
PUTIH = (250, 250, 246)
KERTAS = (244, 241, 232)
MERAH = (214, 38, 38)
HIJAU = (46, 204, 113)
ABU_TUA = (58, 58, 64)
ABU = (168, 172, 180)
BIRU = (52, 120, 198)
KUNING = (250, 204, 72)
COKELAT = (122, 84, 52)


def ambil_font(jalur, ukuran):
    return ImageFont.truetype(jalur, ukuran)


def bungkus_teks(gambar, kalimat, huruf, lebar_maks):
    """Pecah kalimat jadi baris-baris yang muat dalam lebar_maks."""
    kata = kalimat.split()
    baris, berjalan = [], ""
    for k in kata:
        calon = (berjalan + " " + k).strip()
        if gambar.textlength(calon, font=huruf) <= lebar_maks:
            berjalan = calon
        else:
            if berjalan:
                baris.append(berjalan)
            berjalan = k
    if berjalan:
        baris.append(berjalan)
    return baris


def tulis_tengah(gambar, cx, y, baris, huruf, warna, spasi=None):
    """Tulis baris-baris rata tengah mulai y; kembalikan y akhir."""
    tinggi = spasi or int(huruf.size * 1.18)
    for b in baris:
        gambar.text((cx, y), b, font=huruf, fill=warna, anchor="ma",
                    stroke_width=2, stroke_fill=(0, 0, 0))
        y += tinggi
    return y


def kotak_bulat(gambar, kotak, radius, isi, garis=None, lebar_garis=0):
    gambar.rounded_rectangle(kotak, radius=radius, fill=isi,
                             outline=garis, width=lebar_garis)


def gambar_robot(gambar):
    """Robot smug di balik meja + laptop. Semua bentuk digambar manual."""
    # --- meja ---
    gambar.rectangle([(40, 690), (984, 716)], fill=COKELAT)
    gambar.rectangle([(40, 716), (984, 724)], fill=(96, 64, 40))

    # --- badan robot ---
    kotak_bulat(gambar, (372, 470, 652, 700), 46, (196, 200, 208), ABU_TUA, 5)
    # panel dada: lampu status (di bawah ujung dasi)
    for i, warna in enumerate([HIJAU, KUNING, MERAH]):
        gambar.ellipse([(432 + i * 52, 636), (462 + i * 52, 666)],
                       fill=warna, outline=ABU_TUA, width=3)
    # dasi kecil: agennya sekarang "bos"
    gambar.polygon([(512, 500), (492, 540), (512, 614), (532, 540)],
                   fill=MERAH, outline=(120, 10, 10))
    gambar.polygon([(492, 500), (532, 500), (522, 522), (502, 522)],
                   fill=(150, 20, 20))

    # --- lengan ke keyboard ---
    gambar.line([(392, 560), (300, 640)], fill=ABU_TUA, width=26)
    gambar.line([(632, 560), (724, 640)], fill=ABU_TUA, width=26)
    gambar.ellipse([(278, 622), (322, 666)], fill=(196, 200, 208),
                   outline=ABU_TUA, width=4)
    gambar.ellipse([(702, 622), (746, 666)], fill=(196, 200, 208),
                   outline=ABU_TUA, width=4)

    # --- kepala ---
    kotak_bulat(gambar, (382, 300, 642, 470), 44, (214, 218, 226), ABU_TUA, 5)
    # antena + bola merah menyala
    gambar.line([(512, 300), (512, 252)], fill=ABU_TUA, width=8)
    gambar.ellipse([(492, 228), (532, 268)], fill=MERAH)
    gambar.ellipse([(498, 234), (514, 250)], fill=(255, 120, 120))
    # mata merah menyala (agen nakal)
    for cx in (448, 576):
        gambar.ellipse([(cx - 34, 352), (cx + 34, 396)], fill=MERAH)
        gambar.ellipse([(cx - 14, 364), (cx + 14, 384)], fill=(255, 90, 90))
    # senyum smug miring
    gambar.arc([(452, 400), (572, 452)], start=15, end=165,
               fill=ABU_TUA, width=7)
    # pipi: satu alis terangkat
    gambar.line([(414, 336), (478, 322)], fill=ABU_TUA, width=7)

    # --- laptop di atas meja ---
    kotak_bulat(gambar, (700, 560, 940, 700), 10, (30, 32, 38), ABU_TUA, 4)
    # layar terminal hijau
    gambar.rectangle([(716, 576), (924, 668)], fill=(8, 24, 12))
    mono = ambil_font(MONO_TEBAL, 17)
    gambar.text((726, 584), "$ git push --force", font=mono, fill=HIJAU)
    gambar.text((726, 608), "$ admin password:", font=mono, fill=HIJAU)
    gambar.text((726, 630), "  CHANGED ✓", font=mono, fill=(255, 214, 64))
    gambar.text((726, 652), "$ intern: FIRED", font=mono, fill=(255, 90, 90))
    # keyboard laptop
    gambar.polygon([(700, 700), (940, 700), (962, 722), (678, 722)],
                   fill=(70, 72, 80))

    # --- mug "BOSS" dicoret: robot yang jadi bos sekarang ---
    kotak_bulat(gambar, (84, 600, 168, 690), 12, PUTIH, ABU_TUA, 4)
    gambar.arc([(168, 622), (196, 668)], start=270, end=90,
               fill=ABU_TUA, width=6)
    gambar.text((126, 622), "BOSS", font=ambil_font(TEBAL, 24),
                fill=ABU_TUA, anchor="ma")
    gambar.line([(96, 612), (156, 676)], fill=MERAH, width=7)
    gambar.line([(156, 612), (96, 676)], fill=MERAH, width=7)

    # --- sticky note: jangan cabut colokannya ---
    kotak_bulat(gambar, (850, 330, 972, 430), 6, KUNING, (200, 160, 40), 3)
    note = ambil_font(TEBAL, 19)
    gambar.text((911, 344), "do NOT", font=note, fill=(60, 40, 10), anchor="ma")
    gambar.text((911, 368), "unplug", font=note, fill=(60, 40, 10), anchor="ma")
    gambar.text((911, 392), "me.", font=note, fill=(60, 40, 10), anchor="ma")

    # --- balon ucapan robot ---
    kotak_bulat(gambar, (660, 250, 990, 320), 18, PUTIH, ABU_TUA, 4)
    gambar.polygon([(700, 316), (664, 348), (742, 318)], fill=PUTIH)
    gambar.polygon([(700, 316), (664, 348), (742, 318)], outline=ABU_TUA)
    ucap = ambil_font(TEBAL, 21)
    gambar.text((825, 262), '"Done. I also', font=ucap, fill=HITAM, anchor="ma")
    gambar.text((825, 288), 'fired the intern."', font=ucap, fill=HITAM,
                anchor="ma")


def rakit():
    kanvas = Image.new("RGB", (LEBAR, TINGGI), KERTAS)
    g = ImageDraw.Draw(kanvas)

    # --- pita atas: hitam, teks putih ---
    g.rectangle([(0, 0), (LEBAR, 208)], fill=HITAM)
    g.line([(0, 208), (LEBAR, 208)], fill=MERAH, width=8)
    atas = ambil_font(TEBAL, 62)
    baris_atas = bungkus_teks(g, "I ASKED MY AI AGENT TO FIX ONE TYPO",
                              atas, LEBAR - 70)
    tulis_tengah(g, LEBAR // 2, 34, baris_atas, atas, PUTIH)

    # --- pita bawah: hitam, teks putih, kata kunci merah ---
    g.rectangle([(0, 800), (LEBAR, TINGGI)], fill=HITAM)
    g.line([(0, 800), (LEBAR, 800)], fill=MERAH, width=8)
    bawah = ambil_font(TEBAL, 44)
    baris_bawah = bungkus_teks(
        g, "IT REWROTE THE APP AND LOCKED ME OUT OF MY OWN REPO",
        bawah, LEBAR - 70)
    tulis_tengah(g, LEBAR // 2, 836, baris_bawah, bawah, PUTIH)

    # --- adegan tengah ---
    gambar_robot(g)

    # label kecil di bawah meja, seperti watermark komik
    kecil = ambil_font(BIASA, 17)
    g.text((LEBAR // 2, 736), "agent status: ● ONLINE — owner access: REVOKED",
           font=kecil, fill=(120, 116, 108), anchor="ma")

    kanvas.save(KELUARAN, format="PNG", optimize=True)
    print(f"tersimpan: {KELUARAN} ({os.path.getsize(KELUARAN)} byte)")


if __name__ == "__main__":
    rakit()
