import sys
import pygame

from genetic_algorithm import GeneticAlgorithm
from handlers.keyboardEventHandler import KeyboardEventHandler
from game_objects_controller import GameObjectsController
import constants


class ScreenController:
    def __init__(self):
        super().__init__()
        self.size = self.window_width, self.window_height = constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT

    def reinitialize_genetic_algorithm(self, params):
        self.genetic_algorithm = GeneticAlgorithm(
            38, self.game_objects_controller.number_of_cars, params.cars_amount, 0.05)
        population = self.genetic_algorithm.perform_crossing_and_mutation()
        self.game_objects_controller.reinitialize_cars(population)

    def display(self):
        pygame.init()
        screen = pygame.display.set_mode(self.size)

        self.game_objects_controller = GameObjectsController(
            self.window_width, self.window_height, screen, self)
        self.game_objects_controller.display_menu()
        self.game_objects_controller.number_of_cars = constants.CARS_NO
        self.game_objects_controller.initialize_track_with_random_cars()

        keyboardEvents = KeyboardEventHandler()

        self.genetic_algorithm = GeneticAlgorithm(
            38, self.game_objects_controller.number_of_cars, 40, 0.05)
        population = self.genetic_algorithm.perform_crossing_and_mutation()
        print(
            len(self.game_objects_controller.cars[0].neural_network.get_weight_list()))
        self.game_objects_controller.reinitialize_cars(population)

        clock = pygame.time.Clock()
        fps = constants.FPS

        simulation_length = 400
        iteration_number = 0

        # I should use timers but I don't know how they work in PyGame
        # Everything is based on this loop anyway so I might as well use it - Wojtek
        while True:
            if self.game_objects_controller.play_action_frame_count % simulation_length == 0:
                distances = self.game_objects_controller.get_car_distances()
                population = self.perform_learning_iteration(
                    distances, population, self.genetic_algorithm, iteration_number)
                # print average distance
                print(sum(distances) / (len(distances)))

                for _ in range(0):  # number of hidden algorithm iterations
                    self.game_objects_controller.reinitialize_cars(population)
                    self.game_objects_controller.multithreaded_update_simulation(
                        simulation_length)
                    # for _ in range(simulation_length):
                    #    game_objects_controller.update_simulation()
                    distances = self.game_objects_controller.get_car_distances()
                    print(distances)
                    # print average distance
                    print(sum(distances) / (len(distances)))
                    population = self.perform_learning_iteration(
                        distances, population, self.genetic_algorithm, iteration_number)
            elif self.game_objects_controller.play_action_frame_count % simulation_length == 1:
                self.game_objects_controller.reinitialize_cars(population)

            keyboardEvents.reset()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pass
                keyboardEvents.process(event)
                self.game_objects_controller.check_pressed_buttons(event)

            self.game_objects_controller.perform_action(keyboardEvents)

            pygame.display.flip()
            clock.tick(fps)

    def perform_learning_iteration(self, distances, population, genetic_algorithm, iteration_number):

        distance_and_weights = zip(distances, population)

        def distance_mapper(x):
            for distance, weights in distance_and_weights:
                if weights == x:
                    return distance,

        learning_data = map(distance_mapper, population)
        genetic_algorithm.perform_selection(learning_data)
        population = genetic_algorithm.perform_crossing_and_mutation()

        with open("populations/population"+str(iteration_number), "a") as f:
            f.write(str(population))

        return population
