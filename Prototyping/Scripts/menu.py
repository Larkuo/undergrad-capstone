from camera import run
from robot import Robot
from object import Object
from time import sleep
import cv2
import RPi.GPIO as GPIO


model_path = '/model_final_001.tflite'
camera_id = 0
frame_width = 300 # pixels
frame_height = 250 # pixels
num_threads = 4

motor1 = 26
motor2 = 12
motor3 = 13

l1 = 20 # cm
l2 = 15 # cm
l3 = 5 # cm
Robot1 = Robot(motor1, motor2, motor3, l1, l2, l3)

model_path = '/model_final.tflite'

menu_msg_intro = 'PLATE ASSEMBLY MENU\n\nEnter a number for your choice among the following options\n'

menu_optns = ['1. Chicken Only\n',
             '2. Potato Fries Only\n',
             '3. Chicken + Ketchup\n',
             '4. Potato Fries + Ketchup\n',
             '5. Potato Fries + Chicken\n', 
             '6. Potato Fries + Chicken + Ketchup\n',
             '7. Exit menu\n']

def get_menu_option():
    try:
        menu_msg = menu_msg_intro

        for optn in menu_optns:
            menu_msg+= optn

        print(menu_msg)
        menu_option = input()

        return int(menu_option)
    except Exception as e:
        print(f'Input Error: {e}')

def get_chicken():
    name = 'chicken'
    detections = run(model_path, camera_id, frame_width, frame_height, num_threads)
    for d in detections:
        category = d.categories[0]

        xmin = d.bounding_box.left
        ymin = d.bounding_box.top
        xmax = d.bounding_box.right
        ymax = d.bounding_box.bottom

        if category.label == name:
            break
    obj = Object(name, [xmin,ymin,xmax,ymax], round(category.score, 2))
    x,y,z = obj.get_object_position(12)
    Robot1.moveToPosition(x, y, z)
    sleep(1)
    Robot1.returnToOrigin()

def get_potato_fries():
    name = 'potatoe_fries'
    detections = run(model_path, camera_id, frame_width, frame_height, num_threads)
    for d in detections:
        category = d.categories[0]

        xmin = d.bounding_box.left
        ymin = d.bounding_box.top
        xmax = d.bounding_box.right
        ymax = d.bounding_box.bottom

        if category.label == name:
            break
    obj = Object(name, [xmin,ymin,xmax,ymax], round(category.score, 2))
    x,y,z = obj.get_object_position(12)
    Robot1.moveToPosition(x, y, z)
    sleep(1)
    Robot1.returnToOrigin()

def get_ketchup_bottle():
    name = 'ketchup_bottle'
    detections = run(model_path, camera_id, frame_width, frame_height, num_threads)
    for d in detections:
        category = d.categories[0]

        xmin = d.bounding_box.left
        ymin = d.bounding_box.top
        xmax = d.bounding_box.right
        ymax = d.bounding_box.bottom

        if category.label == name:
            break
    obj = Object(name, [xmin,ymin,xmax,ymax], round(category.score, 2))
    x,y,z = obj.get_object_position(12)
    Robot1.moveToPosition(x, y, z)
    sleep(1)
    Robot1.returnToOrigin()



def assemble_plate():
    option = get_menu_option()
    try:
        while option != 7:
            print(f'Starting plate assembly for option {menu_optns[option-1]}')
            if option == 1:
                get_chicken()
            elif option == 2:
                get_potato_fries()
            elif option == 3:
                get_chicken()
                get_ketchup_bottle()
            elif option == 4:
                get_potato_fries()
                get_ketchup_bottle()
            elif option == 5:
                get_chicken()
                get_potato_fries()
            elif option == 6:
                get_chicken()
                get_potato_fries()
                get_ketchup_bottle()
            else:
                print('Invalid option selected, try again\n')
            print('-------------------------------------------\n')
            option = get_menu_option()

        print('Exiting Plate Assembly Script')
    except Exception as e:
        print(f'Menu Error: {e}')

if __name__ == "main":
    GPIO.setmode(GPIO.BCM)

    assemble_plate()

    cv2.destroyAllWindows()
    GPIO.cleanup()