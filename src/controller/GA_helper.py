import numpy as np
import heapq

class genetic_helper():
    def __init__(self, gene,size_population, mutation_rates):
        self.size_population = size_population
        self.population = np.random.randn(size_population,gene) # fisrt generaton
        self.gene_score = []
        self.mutation_rates = mutation_rates
        self.max_value = 10
        self.min_value = -10

        self.number_of_children = size_population//2


    def assign_fitness(self, score):
        self.gene_score = score
        self.gene_score = self.gene_score[np.argsort(self.gene_score[:, 0])]





    def next_generatoin(self):
        # make children
        for i in range(self.number_of_children):
            self.population[int(self.gene_score[i][1])] = self.mate(self.population[int(self.gene_score[-1][1])],self.population[int(self.gene_score[-2][1])])
        # mutate parents
        for i in range(self.size_population-self.number_of_children):
            self.population[int(self.gene_score[-i][1])] = self.mutate(self.population[int(self.gene_score[i][1])])

    def mutate(self,gene):
        for i in range(len(gene)):
            chance = np.random.rand()
            if chance < self.mutation_rates:
                gene[i] = (np.random.rand())*(self.max_value - self.min_value) + self.min_value
            else:
                gene[i] = gene[i]
        return gene


    def mate(self,parent1,parent2):
        child = np.zeros(parent1.shape)
        for i in range(len(parent1)):
            chance = np.random.rand()
            if chance <= (1.0 - self.mutation_rates)/2:
                child[i] = parent1[i]
            elif chance <= (1.0 - self.mutation_rates):
                child[i] = parent2[i]
            else:
                child[i] = (np.random.rand())*(self.max_value - self.min_value) + self.min_value
        return child



if __name__ == "__main__":

    target = np.array([1,2,3,4])
    gh = genetic_helper(4,10, 0.2)
    gh.min_value = 0
    gh.number_of_children = 8
    score = np.zeros([gh.size_population,2])
    for j in range(100000):
        for i in range(gh.size_population):
            score[i,0] = np.sum(-np.abs(target - gh.population[i]))
            score[i,1] = i
        
        gh.assign_fitness(score)

        # print(gh.gene_score)
        # print("======================")
        gh.next_generatoin()

    for i in range(gh.size_population):
            score[i,0] = np.sum(-np.abs(target - gh.population[i]))
            score[i,1] = i

    gh.assign_fitness(score)
    print(gh.gene_score)
    print("======================")
    print(gh.population[int(gh.gene_score[-1,1])])
    