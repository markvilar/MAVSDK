cmake_minimum_required(VERSION 3.10.2)

project(third_party)

include(cmake/build_target.cmake)

if (SUPERBUILD)
    list(APPEND CMAKE_PREFIX_PATH "${DEPS_INSTALL_PATH}")
    set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} PARENT_SCOPE)

    build_target(mavlink)
    build_target(jsoncpp)           # conan
    build_target(tinyxml2)          # conan

    if(NOT IOS)
        build_target(zlib)
    endif()

    build_target(curl)

    if(BUILD_MAVSDK_SERVER)
        build_target(openssl)       # conan
        build_target(cares)
        build_target(absl)
        build_target(protobuf)      # conan
        build_target(re2)           # conan
        build_target(grpc)          # conan
    endif()
endif()

