from calendar import c
import math
from operator import mod
from vpython import *

scene.height = 800
scene.width = 1500
scene.range = 10
scene.title = "Basketball"
scene.center = vec(25, 10, 20)
scene.background = color.white
scene.axis = vec(-1,0,-.5)

def display_instructions():
    s = """In GlowScript programs:
To rotate "camera", drag with right button or Ctrl-drag.
To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
  On a two-button mouse, middle is left + right.
To pan left/right and up/down, Shift-drag.
Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.caption = s

# Display text below the 3D graphics:
display_instructions()

dt = 0.0002
t = 0

pole_height = 10
pole_width = 1
basket_pole = box(pos=vec(0,5,0),
            size=vec(pole_width,pole_height,pole_width),
            color=vec(0.4,0.4,0.5) )
backboard_height = 3.5
backboard_width = 6
backboard_depth = .3

fish = 'https://res.cloudinary.com/dk-find-out/image/upload/q_80,w_1920,f_auto/DCTM_Penguin_UK_DK_AL644648_p7nd0z.jpg'
backboard = box(pos=vec(0,11,.37),
            size=vec(backboard_width,backboard_height,backboard_depth),
            color=vec(.5,.5,.5), texture='https://m.media-amazon.com/images/I/41I2hna17oL._AC_.jpg' )

rim = ring(pos=vec(0,10,1.28), radius=.75, thickness=0.1, color=vec(255/255,119/255,0/255), axis=vec(0,2,0))

court_width = 50
court_length = 94
court = box(pos=vec(0,0,43), axis=vec(0,0,1),
            size=vec(court_length,.001,court_width), color=color.white, texture='https://murals-weblinc.netdna-ssl.com/product_images/wooden-basketball-court-10549029/5ec82f56bd89dd0018f77537/product_large_image.jpg?c=1590177621' )

ball_radius = .4
basketball = sphere(pos=vec(0,5.4,18.5), radius = ball_radius, color=color.orange)

mj_head_radius = 1.2
mj_head = sphere(pos=vec(0,6,18), radius = mj_head_radius, axis=vec(-1,0,0), texture="https://i.ebayimg.com/images/g/8zIAAOSwvwdgt9Zq/s-l400.jpg")

mj_body_height = 4
mj_body_length = 1
mj_body_width = 1.5
mj_body = box(pos=vec(0,3,18), size=vec(mj_body_width, mj_body_height, mj_body_length), color=color.red)

wall_opacity = .5

back_wall_height = 100
back_wall_length = 1
back_wall_width = court_width
back_wall_z = -5
back_wall = box(opacity=wall_opacity, pos=vec(0,50,back_wall_z), size=vec(back_wall_width, back_wall_height, back_wall_length), color=color.black)

front_wall_z = 30
front_wall = box(opacity=wall_opacity, pos=vec(0,50,front_wall_z), size=vec(back_wall_width, back_wall_height, back_wall_length), color=color.black)

g = .1

# Here are the inital x velocity and y velocity!
vel_mult = .0635
friction = .9
angle_deg = 145
init_vel = 62
angle_rad = angle_deg * 0.0174533
dx = init_vel * cos(angle_rad) * vel_mult
dy = init_vel * sin(angle_rad) * vel_mult
time_multiplier = .1
sleep(.5)
move = True
spin = False
congrats_frame = 0
while True:
    rate(300)
    # increment time
    t = t+dt

    # BOUNCE PHYSICS SECTION
    # if we are at the ground (y=0), bounce!
    if (basketball.pos.y == 0):
        # bounce by flipping the change in y, but taking away some of it to simulate loss of energy through friction
        dy = -dy * friction
        dx = dx * friction
        print("Bounced on the ground!")

    # bouncing off the back wall
    elif (basketball.pos.z == back_wall_z):
        # take some energy away from x to simulate friction
        dx = -dx * friction
        dy = dy * friction
        print("Bounced off the back wall!")

    # bouncing off the front wall
    elif (basketball.pos.z == front_wall_z):
        # take some energy away from x to simulate friction
        dx = -dx * friction
        dy = dy * friction
        print("Bounced off the front wall!")
    
    # bouncing off the backboard
    elif (basketball.pos.z == 0 and basketball.pos.y > 8 and basketball.pos.y < 12):
        dx = -dx * friction
        dy = dy * friction
        print("Bounced off the backboard!")

    # bouncing off basket post
    elif (basketball.pos.z == .5 and basketball.pos.y > 0 and basketball.pos.y < 9.25):
        # take some energy away from x to simulate friction
        dx = -dx * friction
        dy = dy * friction
        print("Bounced off the front of the backboard post!")
 
    # bouncing off the front of the rim
    elif (basketball.pos.z == 1.5 and basketball.pos.y > 9 and basketball.pos.y < 10.5):
        dx = -dx * friction
        dy = dy * friction
        print("Bounced off the front of the rim!")

    # bouncing off the top of the rim
    elif (basketball.pos.z <= 2.3 and basketball.pos.z > 1 and basketball.pos.y == 10):
        dx = dx * friction
        dy = -dy * friction
        print("Bounced off the top of the rim!")
    

    # POSITION UPDATING SECTION
    # # update ball pos
    # ball is moving on the y axis (height) and z axis (basically serves as the x). The ball never goes side to side,
    # so the third axis isn't used
    # if the position update would bring it below the ground, put it at the ground
    if (basketball.pos.y + dy <= 0):
        basketball.pos = vec(basketball.pos.x, 0, basketball.pos.z - dx*(time_multiplier))
    # if the basket goes in...
    elif (basketball.pos.y > 10 and basketball.pos.y + dy <= 10 and basketball.pos.z - dx < 1 and basketball.pos.z - dx >=-1):
        print("It went in!")
        basketball.pos = vec(basketball.pos.x, 10, 1)
        dx = 0
        dy = 0
        spin = True
        if (congrats_frame == 0):
            congrats = text(text='Buckets!', pos=vec(-4,5,15), height=5, depth=5, color=color.red, axis=vec(1,0,-1),
            start_face_color=color.black, end_face_color=color.white)
        else:
            congrats_frame = congrats_frame +.1
            congrats.axis = vec(congrats_frame, 0, congrats_frame)
    # if the change would go past the back wall, put it at the back wall
    elif (basketball.pos.z - dx <= back_wall_z):
        basketball.pos = vec(basketball.pos.x, basketball.pos.y + dy*(time_multiplier), back_wall_z)
    # if the change would go past the front wall, put it at the front wall
    elif (basketball.pos.z - dx >= front_wall_z):
        basketball.pos = vec(basketball.pos.x, basketball.pos.y + dy*(time_multiplier), front_wall_z)
    # if the change would go past the basket post, go to the basket post
    elif (basketball.pos.z - dx <= .5 and basketball.pos.y + dy > 0 and basketball.pos.y + dy < 9.25):
        basketball.pos = vec(basketball.pos.x, basketball.pos.y + dy*(time_multiplier), .5)
    # if the change will put us on the backboard, go to the backboard
    elif (basketball.pos.z - dx <= 0 and basketball.pos.y + dy > 8 and basketball.pos.y + dy < 12):
        basketball.pos = vec(basketball.pos.x, basketball.pos.y + dy*(time_multiplier), 0)
    # if the change will put us on the front of the rim, go there
    elif (basketball.pos.z > 1.5 and basketball.pos.z - dx <= 0.75 and basketball.pos.y + dy > 9 and basketball.pos.y + dy < 10.5):
        basketball.pos = vec(basketball.pos.x, basketball.pos.y + dy*(time_multiplier), 1.5)
    # if the change will put us off the top of the rim, go there
    elif (basketball.pos.y > 10 and basketball.pos.z - dx <= 2.3 and basketball.pos.z - dx > 1 and basketball.pos.y + dy <= 10):
        basketball.pos = vec(basketball.pos.x, 10, basketball.pos.z - dx*(time_multiplier))   
    # otherwise, do a regular update
    else:
        basketball.pos = vec(basketball.pos.x, basketball.pos.y + dy*(time_multiplier), basketball.pos.z - dx*(time_multiplier))

    # increment gravity
    if move:
        dy = dy - (g * time_multiplier)

    # stopped bouncing, so end
    if (abs(dy) < .08 and basketball.pos.y < 1 and abs(dx) < .08):
        print("dy: " + str(dy))
        print("dx: " + str(dx))
        dy = 0
        dx = 0
        move = False
        print("Stopped moving!")

    if (spin):
        congrats_frame = congrats_frame +.000001

    
    

