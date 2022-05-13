cmake_minimum_required(VERSION 2.8)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_BUILD_TYPE "Release")
project(CppAcceleration)

set(PYTHON_EXECUTABLE "/usr/bin/python3.8")
set(PYTHON_INCLUDE_DIR "/usr/include/python3.8")
set(PYTHON_LIBRARIES "/usr/lib/x86_64-linux-gnu/libpython3.8m.so")

link_directories(
    /usr/local/lib
)
find_package(PythonLibs REQUIRED)
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${PYTHON_INCLUDE_DIR}
)
# define pybind11 as a submodule
add_subdirectory(pybind11)
pybind11_add_module(CppAcceleration38 GetAllValidPositions.cpp)
target_link_libraries(${PYTHON_LIBRARIES})
