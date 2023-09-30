from conan import ConanFile

from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, patch
from conan.tools.scm import Git, Version

from typing import Dict

required_conan_version = ">=2.0.0"

class MyProjectConanFile(ConanFile):
    name = "mavsdk"
    version = "0.0.1"
    license = "BSD 3-Clause"
    author = "Martin Kvisvik Larsen"
    description = "A cpptemp for C++ projects."
    url = "https://github.com/mavlink/MAVSDK"
    homepage = "https://github.com/mavlink/MAVSDK"

    settings = ["os", "compiler", "build_type", "arch"]
    
    options = {
        "shared" : [True, False], 
        "fPIC" : [True, False],
    }

    default_options = {
        "shared" : False, 
        "fPIC" : True,
    }

    exports_sources = [
        "CMakeLists.txt", 
        "examples/*",
        "proto/*",
        "src/*",
        "templates/*", 
        "tools/*",
    ]
    
    @property
    def _min_cppstd(self):
        return "17"

    @property
    def _compilers_minimum_version(self):
        return {
            "Visual Studio": "15.9",
            "msvc"         : "16",
            "gcc"          : "7",
            "clang"        : "8",
            "apple-clang"  : "10",
        }

    def config_options(self):
        """ Configure project options. """
        if self.settings.os == "Windows":
            del self.options.fPIC
        if self.options.shared:
            del self.options.fPIC

    def configure(self):
        """ Configures the project settings. """
        if self.options.shared:
            del self.options.fPIC

    def requirements(self):
        """ Specifies the project requirements. """
        self.requires("jsoncpp/[>=1.9.5]")
        self.requires("tinyxml2/[>=9.0.0]")
        self.requires("openssl/[>=3.1.3]")
        self.requires("protobuf/[>=3.21.12]")
        # TODO: Check if primary or secondary dependency
        # self.requires("re2/[>=20230301]")
        self.requires("grpc/[>=1.54.3]")

    def build_requirements(self):
        """ Specifies requirements for building the package. """
        self.tool_requires("cmake/[>=3.19]")

    def validate(self):
        """ Validates the project configuration. """
        # Check C++ standard
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._min_cppstd)

        # Check compiler version
        compiler = str(self.settings.compiler)
        compiler_version = Version(self.settings.compiler.version)
        minimum_version = Version(
            self._compilers_minimum_version.get(compiler)
        )
        if minimum_version and minimum_version > compiler_version:
            raise ConanInvalidConfiguration(
                f"{self.ref} requires C++{self._min_cppstd}, which your "
                "compiler does not support.",
            )

    def layout(self):
        """ Defines the project layout. """
        self.folders.root = "."
        self.folders.source = "."
        self.folders.build = "build"
        cmake_layout(self)

    def source(self):
        """ Retrieves and prepares source code for the package. """
        # NOTE: For reference
        # git = tools.Git(folder=self.folders.source)
        # git.clone("https://github.om/myuser/mypackage.git")
        # git.checkout("v1.0")
        pass

    def _get_cmake_variables(self) -> Dict:
        """ Internal methods to get CMake variables based on options. """
        return {
            "MAVSDK_BUILD_SHARED" : 
                "ON" if self.options.shared else "OFF",
        }

    def generate(self):
        """ Generates files necessary for build the package. """
        # Create dependency graph
        deps = CMakeDeps(self)
        deps.generate()

        # Set up toolchain
        tc = CMakeToolchain(self)

        # Add variables to toolchain
        variables = self._get_cmake_variables()
        for name, value in variables.items():
            tc.variables[name] = value
        
        # NOTE: For reference
        # tc.preprocessor_definitions
        # tc.cache_variables
        # tc.variables

        tc.generate()

    def build(self):
        """ Builds the library. """
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        """ Packages the library. """
        copy(self, pattern="LICENSE*", dst="licenses", src=self.source_folder)
        cmake = CMake(self)
        variables = self._get_cmake_variables()
        cmake.configure(variables=variables)
        cmake.install()

    def package_info(self):
        """ Configures the package information. """
        # Set up component and properties
        mavsdk = self.cpp_info.components["mavsdk"]
        mavsdk.set_property("cmake_file_name", "cpptemp")
        mavsdk.set_property("cmake_target_name", "cpptemp::cpptemp")
        mavsdk.set_property("pkg_config_name", "cpptemp-config.cmake")

        # Component attributes
        mavsdk.libs = ["mavsdk"]
        #mavsdk.resdirs = ["resource"]
        mavsdk.requires = ["JsonCpp::JsonCpp", "tinyxml2::tinyxml2"]

        """
        # Architecture definitions
        if self.settings.os == "Windows":
            self.cpp_info.components["cpptemp"].defines \
                .append("CPPTEMP_PLATFORM_WINDOWS")
        elif self.settings.os == "Linux":
            self.cpp_info.components["cpptemp"].defines \
                .append("CPPTEMP_PLATFORM_LINUX")

        # Build type definitions
        if self.settings.build_type == "Debug":
            self.cpp_info.components["cpptemp"].defines \
                .append("CPPTEMP_DEBUG_DEFINITION")
        elif self.settings.build_type == "Release":
            self.cpp_info.components["cpptemp"].defines \
                .append("CPPTEMP_RELEASE_DEFINITION")
        """

    def export(self):
        """ Responsible for capturing the coordinates of the current URL and 
        commit. """
        # TODO: Implement
        pass
