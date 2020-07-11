cmake_minimum_required(VERSION 3.1.3)
project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

set(PROJECT_VERSION 4.8.2)
include(CMakeListsOriginal.txt)
