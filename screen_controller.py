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

    def display(self):
        pygame.init()
        screen = pygame.display.set_mode(self.size)

        game_objects_controller = GameObjectsController(self.window_width, self.window_height, screen)
        game_objects_controller.display_menu()
        game_objects_controller.number_of_cars = constants.CARS_NO
        game_objects_controller.initialize_track_with_random_cars()

        keyboardEvents = KeyboardEventHandler()

        genetic_algorithm = GeneticAlgorithm(125, game_objects_controller.number_of_cars, 40, 0.05)
        population = genetic_algorithm.perform_crossing_and_mutation()
        print("POP1")
        print(population)
        print(len(game_objects_controller.cars[0].neural_network.get_weight_list()))
        game_objects_controller.reinitialize_cars(population)

        clock = pygame.time.Clock()
        fps = 200

        simulation_length = 600

        # I should use timers but I don't know how they work in PyGame
        # Everything is based on this loop anyway so I might as well use it - Wojtek
        while True:
            if game_objects_controller.play_action_frame_count % simulation_length == 0:
                for _ in range(5):
                    game_objects_controller.reinitialize_cars(population)
                    for _ in range(simulation_length):
                        game_objects_controller.update_simulation()
                    distances = game_objects_controller.get_car_distances()
                    print(distances)
                    print(sum(distances) / (len(distances)))  # print average distance
                    distance_and_weights = zip(distances, population)

                    def distance_mapper(x):
                        for distance, weights in distance_and_weights:
                            if weights == x:
                                return distance,

                    learning_data = map(distance_mapper, population)
                    genetic_algorithm.perform_selection(learning_data)
                    population = genetic_algorithm.perform_crossing_and_mutation()



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pass
                keyboardEvents.process(event)
                game_objects_controller.check_pressed_buttons(event)

            game_objects_controller.perform_action(keyboardEvents)

            pygame.display.flip()
            clock.tick(fps)