#include <iostream>
#include <boost/version.hpp>

int main() {
    std::cout << "Hello, Boost! Version " << BOOST_VERSION / 100000 << "."
              << BOOST_VERSION / 100 % 1000 << "." << BOOST_VERSION % 100 << std::endl;

    return 0;
}

