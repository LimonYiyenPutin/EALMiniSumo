import ctypes
import math
import sys
import time
import tkinter as tk
import pygame
from bot import Bot
from karakter import Karakter

##############################################################---------maalesef bu uyarı ekranını ai'a yaptırdım (zorlandım)
def uyari():
    root = tk.Tk()
    root.title("BLEHHH🍋🍋🍋")
    root.overrideredirect(True)
    root.resizable(False, False)
    root.configure(bg="#222222")

    g = 340
    y = 240
    x = (root.winfo_screenwidth() - g) // 2
    z = (root.winfo_screenheight() - y) // 2
    root.geometry(f"{g}x{y}+{x}+{z}")

    konum = {}
    root.bind("<Button-1>", lambda e: konum.update(x=e.x, y=e.y))
    root.bind("<B1-Motion>", lambda e: root.geometry(f"+{root.winfo_x() + e.x - konum['x']}+{root.winfo_y() + e.y - konum['y']}"))

    tk.Label(root, text="BLEHHH🍋🍋🍋", bg="#222222", fg="white").pack(pady=10)
    tk.Label(root, text="AMAÇ: rakibini beyaz çizginin dışına vurara'la it!\nArenadan çıkan kaybeder 🍋\n\n• W/S ileri-geri • A/D veya ok tuşları: dönme\n• E: vurara itmesi (temas + vurara bakarken)\n• R: yeniden başlat • ESC: çıkış", justify="left", bg="#222222", fg="#dddddd", font=("Arial", 9)).pack(pady=5)

    alt = tk.Frame(root, bg="#222222")
    alt.pack(pady=10)
    tk.Button(alt, text="Başlat", command=root.destroy, bg="#2e7d32", fg="white", font=("Arial", 9, "bold"), padx=15, pady=6, relief="flat").pack(side="left", padx=5)
    tk.Button(alt, text="Kapat", command=sys.exit, bg="#c62828", fg="white", font=("Arial", 9, "bold"), padx=10, pady=5, relief="flat").pack(side="left", padx=5)

    root.mainloop()
################################################################-----------------buraya kadar

#buradan yukarısı zaten uyarı kısmı sadece .d

uyari()
pygame.init()
info = pygame.display.Info()
ekranx = info.current_w
ekrany = info.current_h
pencere = pygame.display.set_mode((ekranx, ekrany))


###############################################################---------şeffaf yapmayı da çözemedim arkayı :d (ai)
hwnd = pygame.display.get_wm_info()["window"]
styles = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
ctypes.windll.user32.SetWindowLongW(hwnd, -20, styles | 0x80000)
ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0x000000, 0, 0x1)
####################################################################---------buraya kadar


saat = pygame.time.Clock()
alan = 300
orta = (ekranx // 2, ekrany // 2)
bekle = 0.8
sure = 0
guc = 6
botbekle = 1.3
botguc = 4.5
botsure = 0
eal = False        # EAL eastereggi: oyunda "eal" yazınca aktif olması lazım
sonharfler = ""
biz = Karakter(ekranx // 2.5, ekrany // 2)
bot = Bot(ekranx // 1.8, ekrany // 2.2)
kaybeden = None
while True:
  t = time.time()
  ebas = False
  hazir = False
  for bizz in pygame.event.get():
    if bizz.type == pygame.QUIT or bizz.type == pygame.KEYDOWN and bizz.key == pygame.K_ESCAPE:
      pygame.quit()
      sys.exit()
    if bizz.type == pygame.KEYDOWN:
      if bizz.key == pygame.K_r and kaybeden is not None:
        biz = Karakter(ekranx // 2.5, ekrany // 2)
        bot = Bot(ekranx // 1.8, ekrany // 2.2)
        kaybeden = None
        sure = 0
        botsure = 0
      if bizz.key == pygame.K_e:
        ebas = True
      ealtus = pygame.key.name(bizz.key)
      if len(ealtus) == 1:
        sonharfler = (sonharfler + ealtus)[-3:]
        if sonharfler == "eal" and not eal:
          eal = True
  pencere.fill((0, 0, 0, 0))
  if kaybeden is None:
    tus = pygame.key.get_pressed()
    biz.hareket(tus)
    bot.guncelle(biz.x, biz.y, ekranx, ekrany, alan)
    biz.surunle()
    bot.surunle()
    if ebas and t - sure > bekle:
      sure = t
      hazir = True
      rad = math.radians(biz.aci)
      biz.x, biz.y = biz.x + math.cos(rad) * 7, biz.y - math.sin(rad) * 7
    dx, dy = bot.x - biz.x, bot.y - biz.y
    mes = math.sqrt(dx**2+dy**2)
    if 0 < mes < biz.r + bot.r:
     yx = dx / mes
     yy = dy / mes
     if hazir and biz.onmu(bot.x, bot.y):
        bot.it(yx, yy, guc)
        biz.it(-yx, -yy, 1.2)
     if bot.onmu(biz.x, biz.y) and t - botsure > botbekle:
        botsure = t
        biz.it(-yx, -yy, botguc)
        bot.it(yx, yy, 1.2)
        rad = math.radians(bot.aci)
        bot.x, bot.y = bot.x + math.cos(rad) * 7, bot.y - math.sin(rad) * 7
     biz.it(-yx, -yy, 0.3)
     bot.it(yx, yy, 0.3)
     art = (biz.r+bot.r-mes) / 2
     biz.x, biz.y = biz.x - yx * art, biz.y - yy * art
     bot.x, bot.y = bot.x + yx * art, bot.y + yy * art
    if math.sqrt((biz.x - orta[0]) ** 2 + (biz.y - orta[1]) ** 2) >= alan:
      kaybeden = "biz"
    elif math.sqrt((bot.x - orta[0]) ** 2 + (bot.y - orta[1]) ** 2) >= alan:
      kaybeden = "bot"
  pygame.draw.circle(pencere, (0, 90, 220) if eal else (255, 255, 255), orta, alan, 16)
  pygame.draw.circle(pencere, (40, 40, 50), orta, alan - 16)
  biz.ciz(pencere)
  bot.ciz(pencere, ekranx, ekrany, alan)
  ###########################################################----------şura da ai 
  hud = pygame.font.SysFont("arial", 22, bold=True).render("Mini Sumo | W ileri S geri A/D dön | E: vurara | R yeniden ESC çık", True, (190, 190, 200))
  pencere.blit(hud, (10, 10))
  if eal:
    ealbanner = pygame.font.SysFont("arial", 30, bold=True).render("ESKİŞEHİR ANADOLU LİSESİ", True, (255, 205, 0))
    pencere.blit(ealbanner, ealbanner.get_rect(center=(orta[0], orta[1] - alan - 40)))
  ###########################################################----------buraya kadar
  if kaybeden is not None:
   kararti = pygame.Surface((ekranx, ekrany), pygame.SRCALPHA)
   kararti.fill((15, 15, 20, 175))
   pencere.blit(kararti, (0, 0))
   if kaybeden == "bot":
    s1 = "KAZANDIGNN! bir oyun daha :)?" if not eal else "KAZANDIGNN! EAL RUHUYLA! bir oyun daha :]?" 
    renk = (120, 230, 120)
   else:
    s1 = "KAYBETTIGNN! PES Mİ EDECEKSİN!? >:("
    renk = (240, 90, 90)
   sonuc = pygame.font.SysFont("arial", 44, bold=True).render(s1, True, renk)
   tekrar = pygame.font.SysFont("arial", 22, bold=True).render("R: baştan başlama     ESC: çıkış", True, (230, 230, 230))
   pencere.blit(sonuc, sonuc.get_rect(center=(ekranx // 2, ekrany // 2 - 25)))
   pencere.blit(tekrar, tekrar.get_rect(center=(ekranx // 2, ekrany // 2 + 45)))



  ##########################################-------------ai
  # Cooldown (bekleme süresi) hesabını yapalım
  gecen_sure = t - sure
  kalan_cooldown = max(0.0, bekle - gecen_sure)

  # Karakterin merkeze olan uzaklığı
  biz_uzaklik = math.sqrt((biz.x - orta[0]) ** 2 + (biz.y - orta[1]) ** 2)

  # Sol altta gösterilecek sayısal veriler (Koordinat, açı, uzaklık ve Cooldown)
  if kalan_cooldown > 0:
    cd_durumu = f"CD: {kalan_cooldown:.1f}s"
    cd_renk = (240, 90, 90)  # Cooldown'dayken kırmızımsı
  else:
    cd_durumu = "CD: HAZIR!"
    cd_renk = (120, 230, 120)  # Hazırken yeşil

  veri_metni = (
      f"X: {biz.x:.1f} | Y: {biz.y:.1f} | Aci: {biz.aci:.1f}° | Uzaklik:"
      f" {biz_uzaklik:.1f} | "
  )

  # Yazıları ekrana yazdırma kısmı (Sol alt köşe)
  veri_hud = pygame.font.SysFont("arial", 18, bold=True).render(
      veri_metni, True, (200, 200, 220)
  )
  cd_hud = pygame.font.SysFont("arial", 18, bold=True).render(
      cd_durumu, True, cd_renk
  )
  # Önce ana verileri basıyoruz
  pencere.blit(veri_hud, (10, ekrany - 35))
  # Cooldown bilgisini ana verilerin hemen sağında hizalıyoruz
  pencere.blit(cd_hud, (10 + veri_hud.get_width(), ekrany - 35))
  #######################################-----------------buraya kadar
  pygame.display.flip()
  saat.tick(60)
