cmake_minimum_required(VERSION 3.1.0)

project(depth_cleaner)

# librealsense2 
find_package(realsense2 REQUIRED)

# opencv
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

# enable C++11
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

# add source to the target
add_executable(cleaned_depth cleaned_depth.cpp)

# add library to the target
target_link_libraries(cleaned_depth ${realsense2_LIBRARY}
                                    ${OpenCV_LIBS})

                                    