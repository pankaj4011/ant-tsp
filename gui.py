import pygame
import sys
from pygame.locals import *
import time
import random
import subprocess
import math

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)


pygame.init()
display = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Ant Colony Optimisation Visualisation')

vertices = []
vertex_map = {}
edges = []
source = None
dest = None


def draw_graph():
	display.fill(black)
	for vertex in vertices:
		pygame.draw.circle(display, white, vertex, 10)
	for edge in edges:
		ux, uy = vertices[edge[0]]
		vx, vy = vertices[edge[1]]
		pygame.draw.line(display, white, (ux, uy), (vx, vy), 1)
		dist = int(((ux - vx) ** 2 + (uy - vy) ** 2) ** 0.5)
		mf = pygame.font.SysFont("monospace", 15)
		label = mf.render(str(dist), 2, blue)
		display.blit(label, ((ux + vx) / 2, (uy + vy) / 2 - 5))


def print_iteration(ant, iteration):
	mf1 = pygame.font.SysFont("monospace", 25)
	label1 = mf1.render('Iteration %d' % iteration, 2, blue)
	mf2 = pygame.font.SysFont("monospace", 25)
	label2 = mf2.render('Ant %d' % ant, 2, blue)
	display.blit(label1, (100, 100))
	display.blit(label2, (600, 100))


def run_ants():
	print "call to run ants"
	if source is None or dest is None:
		return
	f = open("input", "w")
	n = len(vertices)
	m = len(edges)
	f.write(str(n) + " " + str(m) + "\n")
	for edge in edges:
		ux, uy = vertices[edge[0]]
		vx, vy = vertices[edge[1]]
		dist = int(((ux - vx) ** 2 + (uy - vy) ** 2)**0.5)
		f.write(str(edge[0] + 1) + " " + str(edge[1] + 1) + " " + str(dist) + "\n")
	f.write(str(vertex_map[source] + 1) + " " + str(vertex_map[dest] + 1) + "\n")
	f.close()
	f = open("input", "r")
	of = open("output", "w")
	subprocess.call(["./a.out"], stdin = f, stdout = of)
	of.close()
	of = open("output", "r")
	line_number = 0
	ant = 0
	iteration = 0
	for line in of:
		if line.startswith('//'):
			continue
		draw_graph()
		if line_number == 0:
			ants, iterations = map(int, line.split())
			line_number += 1
			continue
		print_iteration(ant + 1, iteration + 1)
		ant = (ant + 1) % ants
		if ant == 0:
			iteration += 1
		path = map(int, line.split())
		print(path)
		for i in range(len(path) - 1):
			ux, uy = vertices[path[i] - 1]
			vx, vy = vertices[path[i + 1] - 1]
			pygame.draw.line(display, (255, 0, 0), (ux, uy), (vx, vy), 5)
			pygame.display.update()
		line_number += 1
	of.close()

def add_edge(u, v):
	pygame.draw.line(display, white, u, v, 1)
	edges.append((vertex_map[u], vertex_map[v]))

def already(x, y):
	for v in vertices:
		vx, vy = v
		if (x - vx) ** 2 + (y - vy) ** 2 <= 100:
			return vx, vy
	return None, None

selected_node = None
select_source = False
select_dest = False
while True:
	for event in pygame.event.get():
		pygame.draw.rect(display, (255, 255, 255), (100, 700, 120, 50))
		mf = pygame.font.SysFont("monospace", 20)
		label = mf.render("Run Ants!", 2, black)
		display.blit(label, (105, 715))
		pygame.draw.rect(display, white, (580, 700, 120, 50))
		label = mf.render("Reset!", 2, black)
		display.blit(label, (605, 715))
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEBUTTONDOWN:
			mouse_pos = pygame.mouse.get_pos()
			print mouse_pos[0], mouse_pos[1]
			x, y = mouse_pos
			if 100 <= x <= 220 and 700 <= y <= 750:
				run_ants()
			elif 580 <= x <= 700 and 700 <= y <= 750:
				display.fill(black)
				vertices = []
				selected_node = None
			else:
				if select_source:
					x, y = already(x, y)
					if x and y:
						source = (x, y)
						pygame.draw.circle(display, yellow, (x, y), 10)
						select_source = False
					continue
				if select_dest:
					x, y = already(x, y)
					if x and y:
						pygame.draw.circle(display, red, (x, y), 10)
						dest = (x, y)
						select_dest = False
					continue
				x, y = already(x, y)
				if x and y: # click on already existing node
					if (x, y) == selected_node:
						pygame.draw.circle(display, white, selected_node, 10)
						selected_node = None
						continue
					if selected_node:
						pygame.draw.circle(display, white, selected_node, 10)
						add_edge(selected_node, (x, y))
					selected_node = (x, y)
					pygame.draw.circle(display, green, selected_node, 10)
				else:
					pygame.draw.circle(display, (255, 255, 255), mouse_pos, 10)
					vertices.append(mouse_pos)
					vertex_map[mouse_pos] = len(vertices) - 1
					if selected_node:
						pygame.draw.circle(display, white, selected_node, 10)
						add_edge(selected_node, mouse_pos)
					selected_node = mouse_pos
					pygame.draw.circle(display, green, selected_node, 10)
		elif event.type == pygame.KEYDOWN:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_s]:
				select_source = not select_source
			elif keys[pygame.K_d]:
				select_dest = not select_dest
		pygame.display.update()
