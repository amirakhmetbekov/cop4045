from __future__ import annotations

import random
import matplotlib.pyplot as plt


class Island:
    """Represent an n by n island containing animals."""

    def __init__(
        self,
        n: int,
        prey_count: int = 0,
        predator_count: int = 0,
        count_humans: int = 0
    ) -> None:
        """Create an empty island and randomly place all initial animals."""
        self.grid_size = n
        self.grid = []

        for _ in range(n):
            self.grid.append([0] * n)

        self.init_animals(
            prey_count,
            predator_count,
            count_humans
        )

    def init_animals(
        self,
        prey_count: int,
        predator_count: int,
        count_humans: int
    ) -> None:
        """Place initial Prey, Predator, and Human objects randomly."""

        count = 0
        while count < prey_count:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)

            if not self.animal(x, y):
                new_prey = Prey(
                    island=self,
                    x=x,
                    y=y
                )
                self.register(new_prey)
                count += 1

        count = 0
        while count < predator_count:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)

            if not self.animal(x, y):
                new_predator = Predator(
                    island=self,
                    x=x,
                    y=y
                )
                self.register(new_predator)
                count += 1

        count = 0
        while count < count_humans:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)

            if not self.animal(x, y):
                new_human = Human(
                    island=self,
                    x=x,
                    y=y
                )
                self.register(new_human)
                count += 1

    def clear_all_moved_flags(self) -> None:
        """Clear the moved flag for every animal before a new tick."""
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y]:
                    self.grid[x][y].clear_moved_flag()

    def size(self) -> int:
        """Return one dimension of the square island."""
        return self.grid_size

    def register(self, animal: Animal) -> None:
        """Place an animal on the island at its coordinates."""
        self.grid[animal.x][animal.y] = animal

    def remove(self, animal: Animal) -> None:
        """Remove an animal from the island."""
        x = animal.x
        y = animal.y

        if self.grid[x][y] is animal:
            self.grid[x][y] = 0

    def animal(self, x: int, y: int) -> Animal | int:
        """Return the animal at a position or -1 outside the island."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]

        return -1

    def __str__(self) -> str:
        """Return a printable representation of the island grid."""
        result = ""

        for y in range(self.grid_size - 1, -1, -1):
            for x in range(self.grid_size):
                if not self.grid[x][y]:
                    result += "{:<3s}".format(".")
                else:
                    result += "{:<3s}".format(
                        str(self.grid[x][y])
                    )

            result += "\n"

        return result

    def count_prey(self) -> int:
        """Return the number of Prey objects currently on the island."""
        count = 0

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                animal = self.animal(x, y)

                if isinstance(animal, Prey):
                    count += 1

        return count

    def count_predators(self) -> int:
        """Return the number of Predator objects currently on the island."""
        count = 0

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                animal = self.animal(x, y)

                if isinstance(animal, Predator):
                    count += 1

        return count

    def count_humans(self) -> int:
        """Return the number of Human objects currently on the island."""
        count = 0

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                animal = self.animal(x, y)

                if isinstance(animal, Human):
                    count += 1

        return count


class Animal:
    """Base class for animals that can move and breed."""

    def __init__(
        self,
        island: Island,
        x: int = 0,
        y: int = 0,
        s: str = "A"
    ) -> None:
        """Initialize an animal and its island position."""
        self.island = island
        self.name = s
        self.x = x
        self.y = y
        self.moved = False

    def position(self) -> tuple[int, int]:
        """Return the animal's current coordinates."""
        return self.x, self.y

    def __str__(self) -> str:
        """Return the character used to display the animal."""
        return self.name

    def check_grid(
        self,
        type_looking_for: type = int
    ) -> tuple[int, int] | int:
        """Find the first neighboring cell containing the requested type."""

        offset = [
            (-1, 1),
            (0, 1),
            (1, 1),
            (-1, 0),
            (1, 0),
            (-1, -1),
            (0, -1),
            (1, -1)
        ]

        for dx, dy in offset:
            x = self.x + dx
            y = self.y + dy

            if not 0 <= x < self.island.size():
                continue

            if not 0 <= y < self.island.size():
                continue

            if type(self.island.animal(x, y)) is type_looking_for:
                return x, y

        return 0

    def move(self) -> None:
        """Move to an empty neighboring cell if possible."""
        if not self.moved:
            location = self.check_grid(int)

            if location:
                self.island.remove(self)

                self.x = location[0]
                self.y = location[1]

                self.island.register(self)
                self.moved = True

    def breed(self) -> None:
        """Create another animal of the same type when ready to breed."""
        if self.breed_clock <= 0:
            location = self.check_grid(int)

            if location:
                self.breed_clock = self.breed_time

                animal_class = self.__class__

                new_animal = animal_class(
                    self.island,
                    x=location[0],
                    y=location[1]
                )

                self.island.register(new_animal)

    def clear_moved_flag(self) -> None:
        """Allow this animal to move during the next simulation tick."""
        self.moved = False


class Prey(Animal):
    """Represent prey that moves and breeds."""

    breed_time = 3

    def __init__(
        self,
        island: Island,
        x: int = 0,
        y: int = 0,
        s: str = "O"
    ) -> None:
        """Initialize a Prey object and its breeding clock."""
        super().__init__(island, x, y, s)

        self.breed_clock = self.breed_time

    def clock_tick(self) -> None:
        """Decrease the Prey breeding clock."""
        self.breed_clock -= 1


class Predator(Animal):
    """Represent a predator that eats Prey and can starve."""

    breed_time = 6
    starve_time = 3

    def __init__(
        self,
        island: Island,
        x: int = 0,
        y: int = 0,
        s: str = "X"
    ) -> None:
        """Initialize a Predator and its local clocks."""
        super().__init__(island, x, y, s)

        self.starve_clock = self.starve_time
        self.breed_clock = self.breed_time

    def clock_tick(self) -> None:
        """Update Predator breeding and starvation clocks."""
        self.breed_clock -= 1
        self.starve_clock -= 1

        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None:
        """Eat one neighboring Prey and move into its position."""
        if not self.moved:
            location = self.check_grid(Prey)

            if location:
                prey = self.island.animal(
                    location[0],
                    location[1]
                )

                self.island.remove(prey)
                self.island.remove(self)

                self.x = location[0]
                self.y = location[1]

                self.island.register(self)

                self.starve_clock = self.starve_time
                self.moved = True


class Human(Animal):
    """Represent a Human that hunts Predators but never kills Prey."""

    breed_time = 10
    starve_time = 12
    hunt_time = 2

    def __init__(
        self,
        island: Island,
        x: int = 0,
        y: int = 0,
        s: str = "H"
    ) -> None:
        """Initialize a Human and its breed, starve, and hunt clocks."""
        super().__init__(island, x, y, s)

        self.breed_clock = self.breed_time
        self.starve_clock = self.starve_time
        self.hunt_clock = self.hunt_time

    def hunt(self) -> None:
        """
        Periodically hunt a neighboring Predator.

        Humans do not kill Prey. A successful hunt resets the starvation
        clock and moves the Human into the Predator's cell.
        """
        if self.moved:
            return

        self.hunt_clock -= 1

        if self.hunt_clock > 0:
            return

        self.hunt_clock = self.hunt_time

        location = self.check_grid(Predator)

        if location:
            predator = self.island.animal(
                location[0],
                location[1]
            )

            self.island.remove(predator)
            self.island.remove(self)

            self.x = location[0]
            self.y = location[1]

            self.island.register(self)

            self.starve_clock = self.starve_time
            self.moved = True

    def clock_tick(self) -> None:
        """Update Human breeding and starvation clocks."""
        self.breed_clock -= 1
        self.starve_clock -= 1

        if self.starve_clock <= 0:
            self.island.remove(self)


def populations_converged(
    prey_list: list[int],
    predator_list: list[int],
    human_list: list[int],
    stable_ticks: int = 20
) -> bool:
    """Return True if all three populations stayed constant recently."""

    if len(prey_list) < stable_ticks:
        return False

    prey_constant = (
        len(set(prey_list[-stable_ticks:])) == 1
    )

    predator_constant = (
        len(set(predator_list[-stable_ticks:])) == 1
    )

    human_constant = (
        len(set(human_list[-stable_ticks:])) == 1
    )

    return (
        prey_constant
        and predator_constant
        and human_constant
    )


def main(
    predator_breed_time: int = 6,
    predator_starve_time: int = 3,
    initial_predators: int = 12,
    prey_breed_time: int = 3,
    initial_prey: int = 60,
    human_breed_time: int = 10,
    human_starve_time: int = 12,
    human_hunt_time: int = 2,
    initial_humans: int = 4,
    size: int = 12,
    ticks: int = 1000
) -> None:
    """Run the Prey-Predator-Human simulation and plot populations."""

    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time

    Prey.breed_time = prey_breed_time

    Human.breed_time = human_breed_time
    Human.starve_time = human_starve_time
    Human.hunt_time = human_hunt_time

    # Assignment requires a maximum of 1000 time units.
    if ticks > 1000:
        ticks = 1000

    prey_list = []
    predator_list = []
    human_list = []

    isle = Island(
        size,
        initial_prey,
        initial_predators,
        initial_humans
    )

    print("Initial island grid:")
    print(isle)

    initial_prey_count = isle.count_prey()
    initial_predator_count = isle.count_predators()
    initial_human_count = isle.count_humans()

    print(
        "Initial populations:",
        "Prey =", initial_prey_count,
        "Predators =", initial_predator_count,
        "Humans =", initial_human_count
    )

    prey_list.append(initial_prey_count)
    predator_list.append(initial_predator_count)
    human_list.append(initial_human_count)

    last_tick = 0

    for tick in range(1, ticks + 1):
        isle.clear_all_moved_flags()

        for x in range(size):
            for y in range(size):
                animal = isle.animal(x, y)

                if not isinstance(animal, Animal):
                    continue

                if isinstance(animal, Predator):
                    animal.eat()

                elif isinstance(animal, Human):
                    animal.hunt()

                animal.move()
                animal.breed()
                animal.clock_tick()

        prey_count = isle.count_prey()
        predator_count = isle.count_predators()
        human_count = isle.count_humans()

        prey_list.append(prey_count)
        predator_list.append(predator_count)
        human_list.append(human_count)

        last_tick = tick

        if tick % 10 == 0:
            print(
                "Tick",
                tick,
                "- Prey:",
                prey_count,
                "Predators:",
                predator_count,
                "Humans:",
                human_count
            )

        if populations_converged(
            prey_list,
            predator_list,
            human_list
        ):
            print(
                "\nAll three populations converged "
                f"by tick {tick}."
            )
            break

    print("\nFinal island grid:")
    print(isle)

    print(
        "Final populations:",
        "Prey =", prey_list[-1],
        "Predators =", predator_list[-1],
        "Humans =", human_list[-1]
    )

    print("Simulation length:", last_tick, "ticks")

    time_values = range(len(prey_list))

    plt.plot(
        time_values,
        prey_list,
        label="Prey"
    )

    plt.plot(
        time_values,
        predator_list,
        label="Predators"
    )

    plt.plot(
        time_values,
        human_list,
        label="Humans"
    )

    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.title(
        "Prey, Predator, and Human Populations"
    )

    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
