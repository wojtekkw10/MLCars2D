import random

from deap import creator, base, tools, algorithms


class GeneticAlgorithm:
    # Cross and mutate should be always called before select
    def __init__(self, number_of_weights, population_size, tournament_size, mutation_prb):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_bool", random.uniform, 0, 1)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual,
                              self.toolbox.attr_bool, n=number_of_weights)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.population = self.toolbox.population(n=population_size)

        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutGaussian, mu=2, sigma=0.2, indpb=mutation_prb)
        self.toolbox.register("select", tools.selTournament, tournsize=tournament_size)

        self.offspring = None

    def perform_crossing_and_mutation(self):
        self.offspring = algorithms.varAnd(self.population, self.toolbox, cxpb=0.5, mutpb=0.1)
        return self.offspring

    def perform_selection(self, fits):
        for fit, ind in zip(fits, self.offspring):
            ind.fitness.values = fit
        self.population = self.toolbox.select(self.offspring, k=len(self.population))

    def select_best(self, k):
        _top = tools.selBest(self.population, k=k)
        return _top


if __name__ == '__main__':
    # ------------------------------------------------
    # ----------------USAGE EXAMPLE ------------------
    # ------------------------------------------------
    def eval_one_max(individual):
        return (sum(individual),)


    number_of_generations = 10000
    ga = GeneticAlgorithm(number_of_weights=2, population_size=3, tournament_size=2, mutation_prb=0.05)

    for _ in range(number_of_generations):
        offspring = ga.perform_crossing_and_mutation()
        fitness_scores = map(eval_one_max, offspring)
        print(list(fitness_scores))
        ga.perform_selection(fitness_scores)
        top = ga.select_best(3)





