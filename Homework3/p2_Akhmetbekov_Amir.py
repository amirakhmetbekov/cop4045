class ParkingPermit:
    """Represent a general university parking permit."""

    def __init__(
        self,
        owner_name: str,
        months: int,
        fee_schedule: dict[str, float]
    ) -> None:
        """
        Initialize a parking permit.

        Parameters:
            owner_name: Name of the permit owner.
            months: Number of months purchased.
            fee_schedule: Dictionary containing permit fee information.

        Raises:
            ValueError: If months is negative.
        """
        if months < 0:
            raise ValueError("Number of months cannot be negative")

        self.owner_name = owner_name
        self.months = months
        self.fee_schedule = fee_schedule

    def cost(self) -> float:
        """Return the permit cost. Subclasses must override this method."""
        raise NotImplementedError("Subclasses must implement cost()")

    def __str__(self) -> str:
        """Return a user-friendly description of the parking permit."""
        return (
            f"ParkingPermit(owner={self.owner_name}, "
            f"months={self.months})"
        )

    def __repr__(self) -> str:
        """Return a detailed representation of the parking permit."""
        return (
            f"ParkingPermit({self.owner_name!r}, "
            f"{self.months!r}, {self.fee_schedule!r})"
        )


class StudentPermit(ParkingPermit):
    """Represent a student parking permit."""

    def __init__(
        self,
        owner_name: str,
        months: int,
        fee_schedule: dict[str, float],
        vehicles: int
    ) -> None:
        """
        Initialize a student parking permit.

        Parameters:
            owner_name: Name of the student.
            months: Number of months purchased.
            fee_schedule: Dictionary containing permit fees.
            vehicles: Number of vehicles registered.

        Raises:
            ValueError: If vehicles is less than 1.
        """
        super().__init__(owner_name, months, fee_schedule)

        if vehicles < 1:
            raise ValueError("A student permit must have at least one vehicle")

        self.vehicles = vehicles

    def cost(self) -> float:
        """
        Return the total student permit cost.

        The cost is the monthly student fee plus a one-time fee
        for each registered vehicle after the first.
        """
        monthly_cost = (
            self.fee_schedule["student_monthly"] * self.months
        )

        extra_vehicle_cost = (
            self.fee_schedule["extra_vehicle"]
            * max(0, self.vehicles - 1)
        )

        return monthly_cost + extra_vehicle_cost

    def __str__(self) -> str:
        """Return a user-friendly description of the student permit."""
        return (
            f"StudentPermit: {self.owner_name}, "
            f"{self.months} months, "
            f"{self.vehicles} vehicle(s), "
            f"cost=${self.cost():.2f}"
        )

    def __repr__(self) -> str:
        """Return a detailed representation of the student permit."""
        return (
            f"StudentPermit({self.owner_name!r}, "
            f"{self.months!r}, {self.fee_schedule!r}, "
            f"{self.vehicles!r})"
        )


class FacultyPermit(ParkingPermit):
    """Represent a faculty parking permit."""

    def __init__(
        self,
        owner_name: str,
        months: int,
        fee_schedule: dict[str, float],
        garage_access: bool
    ) -> None:
        """
        Initialize a faculty parking permit.

        Parameters:
            owner_name: Name of the faculty member.
            months: Number of months purchased.
            fee_schedule: Dictionary containing permit fees.
            garage_access: True if garage access is included.
        """
        super().__init__(owner_name, months, fee_schedule)
        self.garage_access = garage_access

    def cost(self) -> float:
        """
        Return the total faculty permit cost.

        Garage access adds an additional monthly fee when included.
        """
        monthly_rate = self.fee_schedule["faculty_monthly"]

        if self.garage_access:
            monthly_rate += self.fee_schedule["garage_monthly"]

        return monthly_rate * self.months

    def __str__(self) -> str:
        """Return a user-friendly description of the faculty permit."""
        garage_text = "Yes" if self.garage_access else "No"

        return (
            f"FacultyPermit: {self.owner_name}, "
            f"{self.months} months, "
            f"garage access={garage_text}, "
            f"cost=${self.cost():.2f}"
        )

    def __repr__(self) -> str:
        """Return a detailed representation of the faculty permit."""
        return (
            f"FacultyPermit({self.owner_name!r}, "
            f"{self.months!r}, {self.fee_schedule!r}, "
            f"{self.garage_access!r})"
        )


def summarize_list(permits: list[ParkingPermit]) -> None:
    """
    Print each permit owner's name and total permit cost.

    Parameters:
        permits: A mixed list containing ParkingPermit subclass objects.
    """
    for permit in permits:
        print(f"{permit.owner_name}: ${permit.cost():.2f}")


def main() -> None:
    """Demonstrate the parking permit classes and summarize_list()."""

    student_id = input("Enter your FAU student ID: ")

    print("\nFAU Student ID:", student_id)
    print("Parking Permit Program")
    print("-" * 60)

    fee_schedule = {
        "student_monthly": 25.0,
        "extra_vehicle": 10.0,
        "faculty_monthly": 40.0,
        "garage_monthly": 15.0
    }

    student1 = StudentPermit(
        "Alice Johnson",
        4,
        fee_schedule,
        1
    )

    student2 = StudentPermit(
        "Michael Smith",
        6,
        fee_schedule,
        3
    )

    faculty1 = FacultyPermit(
        "Dr. Robert Brown",
        5,
        fee_schedule,
        True
    )

    faculty2 = FacultyPermit(
        "Dr. Susan Davis",
        3,
        fee_schedule,
        False
    )

    permits = [
        student1,
        faculty1,
        student2,
        faculty2
    ]

    print("\nObjects using __str__:")
    for permit in permits:
        print(permit)

    print("\nObjects using __repr__:")
    for permit in permits:
        print(repr(permit))

    print("\nPermit Summary:")
    summarize_list(permits)

    print("\nExample cost computations:")
    print(
        f"{student1.owner_name}: "
        f"${fee_schedule['student_monthly']:.2f} x "
        f"{student1.months} months = "
        f"${student1.cost():.2f}"
    )

    print(
        f"{student2.owner_name}: "
        f"${fee_schedule['student_monthly']:.2f} x "
        f"{student2.months} months + "
        f"{student2.vehicles - 1} extra vehicle(s) x "
        f"${fee_schedule['extra_vehicle']:.2f} = "
        f"${student2.cost():.2f}"
    )

    print(
        f"{faculty1.owner_name}: "
        f"(${fee_schedule['faculty_monthly']:.2f} + "
        f"${fee_schedule['garage_monthly']:.2f} garage) x "
        f"{faculty1.months} months = "
        f"${faculty1.cost():.2f}"
    )

    print(
        f"{faculty2.owner_name}: "
        f"${fee_schedule['faculty_monthly']:.2f} x "
        f"{faculty2.months} months = "
        f"${faculty2.cost():.2f}"
    )


if __name__ == "__main__":
    main()


