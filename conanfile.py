# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools


class CppastConan(ConanFile):
    name = "cppast"
    version = "0.1"
    license = "MIT License"
    author = "Jonathan Müller <git@foonathan.net>"
    url = "https://github.com/BlueSolei/cppast"
    description = "Library to parse and work with the C++ AST"
    topics = ("cplusplus", "ast", "parser-library", "libclang")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"

    def source(self):
        repo = tools.Git()
        repo.clone(self.url, shallow=True)
        
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("CMakeLists.txt", "project(cppast VERSION 0.0)",
                              '''project(cppast VERSION 0.0)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="cppast/include")
        self.copy("*cppast.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["cppast"]

