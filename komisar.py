import sys
from datetime import datetime
import random as random
import numpy as np
import matplotlib.pyplot as plt


class Answer:
    def __init__(self, commissar):
        self.reputation = 1
        self.reputation_avg = 1
        self.reputation_com = None
        self.counted = 0
        self.ratings = []
        self.history_rating = []

    def recount_reputation(self):
        before = self.reputation
        summary = 0
        summary_m = 0
        for rating in self.ratings:
            if rating.rating:
                summary += rating.user.reputation
            else:
                summary_m += rating.user.reputation
        self.reputation = round((summary / (summary + summary_m)),2)

        if self.reputation_com is not None:
            self.reputation = round((self.reputation + self.reputation_com) / 2,2)
            # if self.counted == 0:
            #     self.history_rating.append(1)
            #     self.history_rating.append(0)
            #     self.counted = 1
        if before != self.reputation:
            for rating in self.ratings:
                rating.user.recount_reputation()
        self.history_rating.append(self.reputation)

    def add_rating(self, rating):
        self.ratings.append(rating)
        self.recount_reputation()


class User:
    def __init__(self):
        self.reputation = 1
        self.reputation_avg = 1
        self.reputation_com = 1
        self.ratings = []
        self.history_rating = []

    def add_rating(self, rating):
        self.ratings.append(rating)
        self.recount_reputation()

    def recount_reputation(self):
        if len(self.ratings) > 0:
            before = self.reputation
            summary = 0
            summary_m = 0
            for rating in self.ratings:
                if rating.rating == 1:
                    summary += rating.answer.reputation
                    summary_m += 1 - rating.answer.reputation
                else:
                    summary += 1 - rating.answer.reputation
                    summary_m += rating.answer.reputation
            self.reputation = round((summary / (summary + summary_m)),2)
            self.history_rating.append(self.reputation)
            if before != self.reputation:
                for rating in self.ratings:
                    rating.answer.recount_reputation()


class Rating:
    def __init__(self, user, answer, rating):
        self.user = user
        self.answer = answer
        self.rating = rating

        self.answer.add_rating(self)
        self.user.add_rating(self)

    def __str__(self):
        return 'Rating ' + self.rating


def recount_reputation(answers, users):
    for a in answers:
        a.recount_reputation()


def drawGraphs(name, answers, users):
    for a in answers:
        y = np.array(a.history_rating)
        plt.plot(y, label="U%d" % (answers.index(a) + 1))

    # plt.title(f'Výpočet rep. skóre udalosti s {num_of_answrs} udalosťami a {num_of_users} používateľmi, komisár po {comisar_after + 1}. používateľovi ')
    plt.title(f'Výpočet rep. skóre udalosti s {num_of_answrs} udalosťou a {num_of_users} používateľmi')
    plt.ylabel("Reputačné skóre")
    plt.xlabel("Počet prepočítaní")
    plt.legend()
    fig = plt.gcf()
    plt.grid()
    plt.show()
    plt.draw()
    fig.savefig(f'figs/1AA{num_of_answrs}U{num_of_users}KA{comisar_after + 1}' + '.svg')

    for u in users:
        y = np.array(u.history_rating)
        plt.plot(y, label="P%d" % (users.index(u) + 1))

    # plt.title(f'Výpočet rep. skóre používateľa s {num_of_answrs} udalosťami a {num_of_users} používateľmi, komisár po {comisar_after + 1}. používateľovi ')
    plt.title(f'Výpočet rep. skóre používateľa s {num_of_answrs} udalosťou a {num_of_users} používateľmi')
    plt.ylabel("Reputačné skóre")
    plt.xlabel("Počet prepočítaní")
    plt.legend()
    fig = plt.gcf()
    plt.grid()
    plt.show()
    plt.draw()
    fig.savefig(f'figs/1UA{num_of_answrs}U{num_of_users}KA{comisar_after + 1}' + '.svg')


def drawUserGraph(name, user, index):
    y = np.array(user.history_rating)
    plt.plot(y, label="Object %d" % index)
    ax = plt.gca()
    ax.set_ylim([0.05, 1.05])
    plt.title(name)
    plt.legend()
    fig = plt.gcf()
    plt.show()
    plt.draw()
    fig.savefig(f'figs/Object_#{index}_' + datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '.jpg', dpi=200)


def main():
    for increment in range(num_of_users):
        u = User()
        users.append(u)
        if increment == comisar_after:
            for x in range(num_of_answrs):
                # staticke hodnoteie komisara
                if x % 3 == 0:
                    answers[x].reputation_com = 1
                elif x % 3 == 1:
                    answers[x].reputation_com = 0
                else:
                    answers[x].reputation_com = 1
        for ans in range(num_of_answrs):
            ratings.append(Rating(u, answers[ans], answr[increment * num_of_answrs + ans]))

    print("DEBUG")

    drawGraphs(f"KA{comisar_after}A{num_of_answrs}U{num_of_users}", answers, users)

    # for u in users:
    #     drawUserGraph(u, users.index(u))
    #
    # for a in answers:
    #     drawUserGraph(f"Answer {answers.index(a)}", a, answers.index(a))

    suma = 0
    sumu = 0
    f = open(f'res/Results_K{comisar_after}_A{num_of_answrs}_U{num_of_users}__{datetime.now().strftime("%I_%M_%S_%p")}.txt', "w+")

    for u in users:
        sumu += len(u.history_rating)
        f.write(f'USER#{users.index(u)} - {len(u.history_rating)} - REPUTATION {u.reputation}\n----\n')
        print(f'USER#{users.index(u)} - {len(u.history_rating)}')

    print('--------------')

    for a in answers:
        suma += len(a.history_rating)
        print(f'Answers#{answers.index(a)} - {len(a.history_rating)} - REPUTATION {a.reputation}')
        f.write(f'Answers#{answers.index(a)} - {len(a.history_rating)} - REPUTATION {a.reputation}\n----\n')

    print('--------------')
    f.write(f"U TOTAL: {sumu}\nA TOTAL: {suma}\nTOTAL: {sumu + suma}\n----\n")
    print(f"U TOTAL: {sumu}\nA TOTAL: {suma}\nTOTAL: {sumu + suma}")

    f.close()


def generate_inputs():
    f = open("answr.txt", "w+")
    answr = []
    for i in range(num_of_answrs):
        for x in range(num_of_users):
            answr.append(random.randint(0, 1))
    answr_str = ",".join(str(i) for i in answr)
    f.write(answr_str)
    f.close()


def read_file():
    with open('answr.txt', 'r') as file:
        data = file.read()
    return [int(i) for i in data.split(",")]


if __name__ == "__main__":
    # sys.setrecursionlimit(10000)
    plt.rcParams["figure.figsize"] = [10, 5]
    plt.rcParams["figure.autolayout"] = True

    # Definuj pocet pouzivatelov
    num_of_users = 10
    # Definuj pocet udalosti
    num_of_answrs = 1

    # Definuj po ktorom pouzivatelovi ma hodnotit komisar
    comisar_after = 10

    # generate_inputs()

    users = []
    ratings = []
    answers = []

    # hodnotenie udalosti v subore .txt, kazdy riadok sa rovna hodnotenie jedneho pouzivatela
    answr = read_file()

    for i in range(num_of_answrs):
        answers.append(Answer(1))

    main()
