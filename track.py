import pyglet
from pyglet import clock, shapes
from pyglet.window import key

from src.Track import Track
from src.Vector import Vector
from src.qlearning import QLearning

track_img = 'tracks/track05.png'

track = Track(track_img, startPos=Vector(26, 3), finishA=Vector(25, 1), finishB=Vector(25, 5),
                  checkPointC=Vector(20, 44), checkPointD=Vector(20, 48),
                  checkPointA=Vector(89, 8), checkPointB=Vector(99, 8))

ql = QLearning(track, alpha=0.1, gamma=0.95)

# Window
tile_size = 10
window = pyglet.window.Window(width=track.width*tile_size, height=(track.height*tile_size) + 200)

track_img = pyglet.image.load(track_img)
sprite = pyglet.sprite.Sprite(img=track_img,
                              x=0, y=0)
sprite.scale = 10

f1_img = pyglet.image.load('ui/f1.png')
sprite_f1 = pyglet.sprite.Sprite(img=f1_img, x=0, y=0)
sprite_f1.scale = 0.01



label1 = pyglet.text.Label('Epoch:',
                          font_name='Times New Roman',
                          font_size=36,
                          x=20, y=window.height-50,
                          anchor_x='left', anchor_y='center')
epoch_label = pyglet.text.Label('0',
                          font_name='Times New Roman',
                          font_size=36,
                          x=170, y=window.height-50,
                          anchor_x='left', anchor_y='center')

label2 = pyglet.text.Label('Mean score:',
                          font_name='Times New Roman',
                          font_size=36,
                          x=20, y=window.height-150,
                          anchor_x='left', anchor_y='center')

score_label = pyglet.text.Label('0',
                          font_name='Times New Roman',
                          font_size=36,
                          x=270, y=window.height-150,
                          anchor_x='left', anchor_y='center')

lines = []

def simulate(evt):
    lines.clear()

    ql.run_episode()

    epoch_label.text = str(ql.epoch)
    score_label.text = str(ql.MeanScore)

    pos = track.car.Pos
    sprite_f1.x = pos.x * tile_size
    sprite_f1.y = (track.height - pos.y) * tile_size

    path = track.car.Path
    for i in range(len(track.car.Path) - 1):
        p1 = path[i]
        p2 = path[i+1]
        lines.append(shapes.Line(p1.x*tile_size, (track.height - p1.y)*tile_size, p2.x*tile_size, (track.height - p2.y)*tile_size, 1, color=(255, 55, 255)))


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        #lines.append(shapes.Line(0, 0, 500, 500, 1, color=(255, 55, 255)))
        clock.schedule_interval(simulate, 0.08)


@window.event
def on_draw():
    window.clear()
    label1.draw()
    epoch_label.draw()
    label2.draw()
    score_label.draw()
    sprite.draw()
    sprite_f1.draw()
    for l in lines:
        l.draw()




pyglet.app.run()
