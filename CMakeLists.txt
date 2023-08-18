cmake_minimum_required(VERSION 3.12)
project(my_app)

# Run the 'conan install' command
execute_process(
    COMMAND conan install ${CMAKE_SOURCE_DIR}
    --build missing
    --profile:build=${CMAKE_SOURCE_DIR}/conan_profiles/build.profile
    --profile:host=${CMAKE_SOURCE_DIR}/conan_profiles/host.profile
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)

# Include Conan-generated CMake configuration
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Add your project's executable
add_executable(my_app main.cpp)

# Find the Boost library
find_package(Boost REQUIRED)
target_include_directories(my_app PRIVATE ${Boost_INCLUDE_DIRS})
target_link_libraries(my_app PRIVATE Boost::boost)

# Find the ffmpeg library
find_package(ffmpeg REQUIRED)
target_include_directories(my_app PRIVATE ${ffmpeg_INCLUDE_DIRS})
target_link_libraries(my_app PRIVATE ffmpeg::ffmpeg)

# Find the qt library
find_package(qt REQUIRED)
target_include_directories(my_app PRIVATE ${qt_INCLUDE_DIRS})
target_link_libraries(my_app PRIVATE qt::qt)

# Find the openal library
find_package(openal REQUIRED)
target_include_directories(my_app PRIVATE ${openal_INCLUDE_DIRS})
target_link_libraries(my_app PRIVATE openal::openal)

# Find the sse2neon library
if("${arch}" STREQUAL "arm" OR "${arch}" STREQUAL "arm64")
    add_subdirectory(dependencies/sse2neon)
    target_link_libraries(my_app PUBLIC sse2neon::sse2neon)
endif()
