#include <iostream>
// #include <boost/version.hpp>
// #define __ARM_ARCH 8
#include "sse2neon.h"

typedef __m128i simd128i;
typedef __m128 simd128;

int main()
{
    // std::cout << "Hello, Boost! Version " << BOOST_VERSION / 100000 << "."
    //           << BOOST_VERSION / 100 % 1000 << "." << BOOST_VERSION % 100 << std::endl;
    simd128i A;
    _mm_minpos_epu16(A);

    return 0;
}