#pragma once
#include <string>
#include <iostream>
inline std::string think(const std::string& q) {
std::cout << "CrownStar would answer: " << q << std::endl;
return "CrownStar: " + q;
}
