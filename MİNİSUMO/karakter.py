import math
import pygame


class Karakter:
	def __init__(aa, x0, y0):
		aa.x, aa.y = x0, y0
		aa.aci, aa.r = 0, 27
		aa.hiz = 2.2
		aa.vx, aa.vy = 0.0, 0.0
	def hareket(aa, tus):
		if tus[pygame.K_LEFT] or tus[pygame.K_a]:
			aa.aci += 3
		if tus[pygame.K_RIGHT] or tus[pygame.K_d]:
			aa.aci -= 3
		sincos = math.radians(aa.aci)
		if tus[pygame.K_UP] or tus[pygame.K_w]:
			aa.x, aa.y = aa.x + math.cos(sincos) * aa.hiz, aa.y - math.sin(sincos) * aa.hiz
		if tus[pygame.K_DOWN] or tus[pygame.K_s]:
			aa.x, aa.y = aa.x - math.cos(sincos) * aa.hiz * 0.7, aa.y + math.sin(sincos) * aa.hiz * 0.7
	def onmu(aa, x1, y1):
		yon = math.degrees(math.atan2(-(y1 - aa.y), x1 - aa.x))
		fark = (yon - aa.aci + 180) % 360 - 180
		return abs(fark) <= 55
	def it(aa, dx, dy, guc):
		aa.vx += dx * guc
		aa.vy += dy * guc
		sav = math.sqrt(aa.vx ** 2 + aa.vy ** 2)
		if sav > 8:
			aa.vx, aa.vy = aa.vx * 8 / sav, aa.vy * 8 / sav
	def surunle(aa):
		aa.x, aa.y = aa.x + aa.vx, aa.y + aa.vy
		aa.vx, aa.vy = aa.vx * 0.92, aa.vy * 0.92
	def ciz(aa, pencere):
		rialbiz = pygame.Surface((50, 50), pygame.SRCALPHA)
		pygame.draw.rect(rialbiz, (240, 240, 240), (0, 0, 50, 50))
		pygame.draw.rect(rialbiz, (220, 20, 60), (35, 15, 15, 20))
		rialbizz = pygame.transform.rotate(rialbiz, aa.aci)
		pencere.blit(rialbizz, rialbizz.get_rect(center=(aa.x, aa.y)).topleft)