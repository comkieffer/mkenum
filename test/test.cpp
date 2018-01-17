
#include <iostream>
#include "generated/ships.hpp"

int main() {

    std::cout << "List of ships: \n";
    for (const auto ship : Universe::SolarSystem::Earth::Sea::Ship_::Values) {
        const auto ship_colour = Universe::SolarSystem::Earth::Sea::get_ship_colour(ship);
        std::cout << "\t- " << to_string(ship) << " (" << to_string(ship_colour) << ")\n";
    }

    return 0;
}
