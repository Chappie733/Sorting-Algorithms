import pygame
import sys
import random
from math import floor

def minimum_index(arr):
	min_i = 0
	for i in range(len(arr)):
		if arr[i] < arr[min_i]:
			min_i = i
	return min_i

def is_sorted(arr):
	for i in range(len(arr)-1):
		if arr[i] > arr[i+1]:
			return False
	return True

def bubble(arr, *args):
	idx = int(args[0])
	if arr[idx] > arr[idx+1]:
		temp = arr[idx]
		arr[idx] = arr[idx+1]
		arr[idx+1] = temp
	return arr, (idx+1 if idx != len(arr)-2 else 0)

def selection(arr, *args):
	idx = args[0]
    min_index = idx
    for j in range(idx+1, len(arr)):
        if arr[j] < arr[min_index]:
            min_index = j
    arr[idx], arr[min_index] = arr[min_index], arr[idx]
    return arr, idx+1

# merge sort
def merge(arr, *args):
	sub = []
	if type(arr[0]) == int or type(arr[0]) == float:
		for i in range(floor(len(arr)/2)):
			sub.append([arr[i*2], arr[i*2+1]])
		if len(arr)%2 != 0:
			sub.append([ arr[len(arr)-1] ])
	if len(sub) == 0:
		sub = arr

	removed = 0
	for i in range(floor(len(sub)/2)):
		first, second = sub[i*2-removed], sub[i*2+1-removed]
		index = sub.index(first)
		sub.remove(first)
		sub.remove(second)
		removed += 1
		sub.insert(index, [])
		elements_amt = len(first) + len(second)
		while len(first) != 0 or len(second) != 0:
			minimum = sys.maxsize
			for i in first:
				if i < minimum:
					minimum = i
			for i in second:
				if i < minimum:
					minimum = i
			sub[index].append(minimum)
			if minimum in first:
				first.remove(minimum)
			else:
				second.remove(minimum)
	return sub, 0, len(sub[0]) == len(arr)

algos = {"bubble": bubble,
		 "selection": selection,
		 "merge": merge}

pygame.init()

w,h = 800, 600
win = pygame.display.set_mode((w,h))
canvas = pygame.Surface((w,h))

running = True
clock = pygame.time.Clock()

try:
	algo = sys.argv[1]
	values_amt = int(sys.argv[2])
	tps = int(sys.argv[3])
except IndexError:
	algo = "bubble"
	values_amt = 25
	tps = 30

val_max = 100
val_min = 0

values = [random.randint(0, val_max) for _ in range(values_amt)]
rect_w = w/values_amt
mult = h/val_max

idx = 0
finished = False

while running:
	clock.tick(tps)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	keys = pygame.key.get_pressed()

	canvas.fill((0,0,0))

	if type(values[0]) == int or type(values[0]) == float:
		for i in range(len(values)):
			pygame.draw.rect(canvas, (255,255,255) if idx != i else (255,0,0), (i*rect_w, h-values[i]*mult, rect_w, values[i]*mult))
			pygame.draw.rect(canvas, (100,100,100), (i*rect_w, h-values[i]*mult, 5, values[i]*mult))
	else:
		for i in range(len(values)):
			for p in range(len(values[i])):
				pygame.draw.rect(canvas, (255,255,255) if idx != i else (255,0,0), (p*rect_w, h-values[i][p]*mult, rect_w, values[i][p]*mult))
				pygame.draw.rect(canvas, (100,100,100), (p*rect_w, h-values[i][p]*mult, 5, values[i][p]*mult))


	if not is_sorted(values):
		if algo != "merge":
			values, idx = algos[algo](values,idx)
		elif not finished:
			values, idx, finished = algos[algo](values, idx)

	win.blit(canvas, (0,0))
	pygame.display.flip() # flip the buffer

pygame.quit()
