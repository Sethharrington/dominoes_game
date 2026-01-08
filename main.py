import pygame

pygame.init()

color = (255, 255, 255)
rect_color = (255,200,100)

canvas = pygame.display.set_mode((500,500))

pygame.display.set_caption("Hello World!")

# image = pygame.image.load("Screenshot.png")
exit = False

while not exit:
    canvas.fill(color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

    pygame.draw.rect(canvas, rect_color, pygame.Rect(30,30,60,60))

    pygame.display.update()
        