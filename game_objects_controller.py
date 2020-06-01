import threading

import pygame

import map_editor
from angle import Angle
from gameObjects.menu import Menu
from gameObjects.car import Car
from gameObjects.track import Track
from handlers.camera import Camera
from map_editor import MapEditor
from params import Params
from stat_display import StatBox
import pygame
from scenes.options_scene import OptionsScene


class GameObjectsController:
    def __init__(self, window_width, window_height, screen, screen_controller):
        super().__init__()
        self.screen = screen
        self.size = self.window_width, self.window_height = window_width, window_height
        self.cars = []
        self.menu = Menu(self.screen, self.window_width, self.window_height)
        self.options_scene = OptionsScene(
            self.window_width, self.window_height)
        self.stat_box = StatBox(screen, 890, 10, 300, 150, 0.05)
        self.track = Track(self.screen)
        self.is_some_action_going_on = False
        self.play_action_frame_count = 1
        self.number_of_cars = 0
        self.screen_controller = screen_controller

        def simple_camera(camera, target_rect):
            l, t, _, _ = target_rect  # l = left,  t = top
            _, _, w, h = camera  # w = width, h = height
            return pygame.Rect(-l + window_width / 2, -t + window_height / 2, w, h)

        def complex_camera(camera, target_rect):
            # we want to center target_rect
            x = -target_rect.center[0] + window_width / 2
            y = -target_rect.center[1] + window_height / 2
            # move the camera. Let's use some vectors so we can easily substract/multiply
            # add some smoothness coolness
            camera.topleft += (pygame.Vector2((x, y)) -
                               pygame.Vector2(camera.topleft)) * 0.06
            # set max/min x/y so we don't see stuff outside the world
            camera.x = max(-(camera.width - window_width), min(0, camera.x))
            camera.y = max(-(camera.height - window_height), min(0, camera.y))

            return camera

        self.camera = Camera(
            complex_camera, self.window_width + 100, self.window_height + 100)  # insert track size here

    # for adjusting menu in the future
    def display_menu(self):
        self.menu.draw()

    def display_stat_box(self):
        self.stat_box.display()

    def update_stat_box(self):
        best_distance = 0
        for car in self.cars:
            if car.distance_traveled > best_distance:
                best_distance = car.distance_traveled
        self.stat_box.new_score(best_distance)

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
                if button_label == "options":
                    self.options_button_action(keyboardEvents)

    def play_button_action(self, keyboardEvents):
        self.play_action_frame_count += 1
        self.update_simulation()
        self.display_track()
        self.display_stat_box()

        if keyboardEvents.is_pressed(pygame.K_b):
            self.go_back_to_menu()

    def update_simulation(self):
        for car in self.cars:
            car.handle_neural_network()
            car.update(self.camera)
            car.detect_collision(self.track.grid, self.track.sectors)

    def map_editor_button_action(self, keyboard_events):
        map_editor = MapEditor(self.screen)
        map_editor.draw_editor()
        map_editor.draw_map(keyboard_events)

        if map_editor.handle_keyboard(keyboard_events):
            self.go_back_to_menu()

    def options_button_action(self, keyboard_events):
        self.options_scene.update(keyboard_events)
        self.options_scene.draw(self.screen)

        if keyboard_events.is_pressed(pygame.K_b):
            amount = self.options_scene.get_cars_amount()
            if amount != "":
                amount = int(amount)

                self.stat_box.clear_score()
                self.number_of_cars = amount
                self.screen_controller.reinitialize_genetic_algorithm(
                    Params(amount//4))

            self.go_back_to_menu()

        if keyboard_events.is_pressed(pygame.K_v):
            self.track.initialize_points(False)

    def go_back_to_menu(self):
        self.is_some_action_going_on = False
        for button_label in self.menu.buttons:
            button = self.menu.buttons.get(button_label)
            button.is_button_pressed = False

        self.display_menu()
