cmake_minimum_required(VERSION 3.12)
project(my_app)

# Run the 'conan install' command
execute_process(
    COMMAND conan install ${CMAKE_SOURCE_DIR}
    --build missing
    # --profile:build=${CMAKE_SOURCE_DIR}/conan_profiles/build.profile
    # --profile:host=${CMAKE_SOURCE_DIR}/conan_profiles/host.profile
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)

# Add your project's executable
add_executable(my_app main.cpp)
set_target_properties(my_app PROPERTIES CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=armv8-a+fp+simd+crypto+crc")
add_subdirectory(dependencies/sse2neon)
target_link_libraries(my_app PRIVATE sse2neon)

