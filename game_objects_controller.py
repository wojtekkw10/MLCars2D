import threading

import constants
from gameObjects.menu import Menu
from gameObjects.car import Car
from gameObjects.track import Track
from handlers.camera import Camera
from scenes.map_editor_scene import MapEditor
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
        self.map_editor_scene = MapEditor(self.screen)
        self.stat_box = StatBox(screen, 890, 10, 300, 150, 0.05)
        self.track = Track(self.screen)
        self.actual_menu = constants.MAIN_MENU
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
            # add some smoothness coolnes
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
        self.menu.draw_main_menu()

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
        if self.actual_menu == constants.MAIN_MENU:
            for button_label in self.menu.buttons:
                button = self.menu.buttons.get(button_label)
                button.check_is_button_pressed(event, self.screen)
        elif self.actual_menu == constants.OPTIONS_MENU:
            for button_label in self.options_scene.buttons:
                button = self.options_scene.buttons.get(button_label)
                button.check_is_button_pressed(event, self.screen)
        elif self.actual_menu == constants.EDITOR_MENU:
            for button_label in self.map_editor_scene.buttons:
                button = self.map_editor_scene.buttons.get(button_label)
                button.check_is_button_pressed(event, self.screen)
        elif self.actual_menu == constants.PLAY_MENU:
            button = self.track.back_button
            button.check_is_button_pressed(event, self.screen)

    def perform_action(self, keyboardEvents):
        for button_label in self.menu.buttons:
            button = self.menu.buttons.get(button_label)
            if button.is_button_pressed:
                if button_label == "play":
                    self.actual_menu = constants.PLAY_MENU
                    self.play_button_action()
                if button_label == "map editor":
                    self.actual_menu = constants.EDITOR_MENU
                    self.map_editor_button_action(keyboardEvents)
                if button_label == "options":
                    self.actual_menu = constants.OPTIONS_MENU
                    self.options_button_action(keyboardEvents)

        for button_label in self.options_scene.buttons:
            button = self.options_scene.buttons.get(button_label)
            if button.is_button_pressed:
                if button_label == "back":
                    self.options_back_button_action()
                if button_label == "custom_map":
                    self.options_custom_map_button_action()

        for button_label in self.map_editor_scene.buttons:
            button = self.map_editor_scene.buttons.get(button_label)
            if button.is_button_pressed:
                if button_label == "erase":
                    self.editor_erase_button_action(keyboardEvents)
                if button_label == "back":
                    self.editor_back_button_action(keyboardEvents)

        if self.track.back_button.is_button_pressed:
            self.go_back_to_menu()

    def update_simulation(self):
        # self.camera.update(self.cars[0])
        for car in self.cars:
            # car.handle_keyboard(keyboardEvents)
            car.handle_neural_network()
            car.update(self.camera)

            car_position_x, car_position_y = int(
                car.position_x), int(car.position_y)
            car.detect_collision(self.track.grid, self.track.sectors)

    def car_updating_thread(self, car, number_of_updates):
        for _ in range(number_of_updates):
            car.handle_neural_network()
            car.update(self.camera)
            car.detect_collision(self.track.grid, self.track.sectors)

    def multithreaded_update_simulation(self, number_of_updates):
        threads = []
        for car in self.cars:
            t = threading.Thread(
                target=self.car_updating_thread, args=(car, number_of_updates))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join()

    # -----------------------------buttons actions------------------------------------------
    def map_editor_button_action(self, keyboard_events):
        self.map_editor_scene.draw_editor()
        keyboard_events.drawing_line = True
        self.map_editor_scene.draw_map(keyboard_events)
        self.map_editor_scene.handle_keyboard(keyboard_events)

    def editor_back_button_action(self, keyboardEvents):
        keyboardEvents.line1, keyboardEvents.line2 = [], []
        self.map_editor_scene.clean = True
        keyboardEvents.drawing_line = False
        self.go_back_to_menu()

    def editor_erase_button_action(self, keyboardEvents):
        self.map_editor_scene.screen.fill((56, 59, 56))
        self.map_editor_scene.clean = True
        self.map_editor_scene.draw_editor()
        keyboardEvents.line1, keyboardEvents.line2 = [], []
        self.map_editor_scene.buttons.get("erase").is_button_pressed = False

    def options_button_action(self, keyboard_events):
        self.options_scene.update(keyboard_events)
        self.options_scene.draw(self.screen)

    def options_custom_map_button_action(self):
        button = self.options_scene.buttons.get("custom_map")
        if button.label == "Load Track":
            button.label = "Default"
            self.track.initialize_points(False)
        else:
            button.label = "Load Track"
            self.track.initialize_points()
        button.is_button_pressed = False

    def options_back_button_action(self):
        amount = self.options_scene.get_cars_amount()
        if amount != "":
            amount = int(amount)
            # self.stat_box.clear_score()
            self.number_of_cars = amount
            self.screen_controller.reinitialize_genetic_algorithm(
                Params(amount // 4))
        self.go_back_to_menu()

    def play_button_action(self):
        self.play_action_frame_count += 1
        self.update_simulation()
        self.display_track()
        self.display_stat_box()

    def go_back_to_menu(self):
        self.actual_menu = constants.MAIN_MENU
        for button_label in self.menu.buttons:
            button = self.menu.buttons.get(button_label)
            button.is_button_pressed = False
        for button_label in self.options_scene.buttons:
            button = self.options_scene.buttons.get(button_label)
            button.is_button_pressed = False
        for button_label in self.map_editor_scene.buttons:
            button = self.map_editor_scene.buttons.get(button_label)
            button.is_button_pressed = False
        self.track.back_button.is_button_pressed = False
        self.display_menu()
