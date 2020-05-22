import threading

import pygame

from angle import Angle
from gameObjects.menu import Menu
from gameObjects.car import Car
from gameObjects.track import Track
from handlers.camera import Camera
from map_editor import MapEditor
import pygame
import sys


class GameObjectsController:
    def __init__(self, window_width, window_height, screen):
        super().__init__()
        self.screen = screen
        self.size = self.window_width, self.window_height = window_width, window_height
        self.cars = []
        self.menu = Menu(self.screen, self.window_width, self.window_height)
        self.track = Track(self.screen)
        self.is_some_action_going_on = False
        self.play_action_frame_count = 1
        self.number_of_cars = 0

        def simple_camera(camera, target_rect):
            l, t, _, _ = target_rect  # l = left,  t = top
            _, _, w, h = camera      # w = width, h = height
            return pygame.Rect(-l+window_width/2, -t+window_height/2, w, h)

        def complex_camera(camera, target_rect):
            # we want to center target_rect
            x = -target_rect.center[0] + window_width/2
            y = -target_rect.center[1] + window_height/2
            # move the camera. Let's use some vectors so we can easily substract/multiply
            # add some smoothness coolnes
            camera.topleft += (pygame.Vector2((x, y)) -
                               pygame.Vector2(camera.topleft)) * 0.06
            # set max/min x/y so we don't see stuff outside the world
            camera.x = max(-(camera.width-window_width), min(0, camera.x))
            camera.y = max(-(camera.height-window_height), min(0, camera.y))

            return camera

        self.camera = Camera(
            complex_camera, self.window_width+100, self.window_height+100)  # insert track size here

    # for adjusting menu in the future
    def display_menu(self):
        self.menu.draw()

    def initialize_track_with_random_cars(self):
        self.cars = []
        for _ in range(self.number_of_cars):
            self.cars.append(Car(50, 60, self.screen))

    def reinitialize_cars(self, offspring):
        self.cars = []
        for _ in range(self.number_of_cars):
            self.cars.append(Car(50, 60, self.screen))
        for car, weights in zip(self.cars, offspring):
            car.neural_network.set_weight_list(weights)

    def get_car_distances(self):
        distances = []
        for car in self.cars:
            distances.append(car.distance_traveled)
        return distances

    def display_track(self):
        background_color = (186, 193, 204)
        self.screen.fill(background_color)
        self.track.draw_track(self.camera)
        for car in self.cars:
            car.draw(self.screen, self.camera)

    def check_pressed_buttons(self, event):
        if not self.is_some_action_going_on:
            for button_label in self.menu.buttons:
                button = self.menu.buttons.get(button_label)
                button.check_is_button_pressed(event, self.screen)

    def perform_action(self, keyboardEvents):
        for button_label in self.menu.buttons:
            button = self.menu.buttons.get(button_label)
            if button.is_button_pressed:
                self.is_some_action_going_on = True
                if button_label == "play":
                    self.play_button_action(keyboardEvents)
                if button_label == "map editor":
                    self.map_editor_button_action(keyboardEvents)

    def play_button_action(self, keyboardEvents):
        self.play_action_frame_count += 1
        self.update_simulation()
        self.display_track()

    def update_simulation(self):
        for car in self.cars:
            # car.handle_keyboard(keyboardEvents)
            car.handle_neural_network()

            car.update()
            car_position_x, car_position_y = int(
                car.position_x), int(car.position_y)


            car.detect_collision(self.track.grid, self.track.sectors)
            # self.camera.update(car)

    def car_updating_thread(self, car, number_of_updates):
        for _ in range(number_of_updates):
            car.handle_neural_network()
            car.update()
            car.detect_collision(self.track.grid, self.track.sectors)


    def multithreaded_update_simulation(self, number_of_updates):
        threads = []
        for car in self.cars:
            t = threading.Thread(target=self.car_updating_thread, args=(car, number_of_updates))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join()


    def map_editor_button_action(self, keyboard_events):
        map_editor = MapEditor(self.screen)
        map_editor.draw_editor()
        map_editor.draw_map(keyboard_events)
        map_editor.handle_keyboard(keyboard_events)
       
