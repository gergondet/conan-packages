from conans import ConanFile, CMake, tools

import os
import shutil

class HPPSplineConan(ConanFile):
    name = "hpp-spline"
    homepage = "https://github.com/humanoid-path-planner/hpp-spline"
    description = "Library for creating smooth cubic splines"
    topics = ("conan", "splines", "robotics")
    url = "https://github.com/humanoid-path-planner/hpp-spline"
    license = "BSD-2-Clause"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    version = "4.8.2"

    _cmake = None

    requires = (
        "eigen/3.3.4@conan/stable"
    )

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("hpp-spline-v{}-{}".format(self.version, "debian.1"), self._source_subfolder)
        os.rename(os.path.join(self._source_subfolder, 'CMakeLists.txt'), 'CMakeListsOriginal.txt')
        for f in os.listdir(self._source_subfolder):
            shutil.move(os.path.join(self._source_subfolder, f), '.')

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['BUILD_TESTING'] = False
        cmake.definitions['BUILD_PYTHON_INTERFACE'] = False
        cmake.definitions['INSTALL_DOCUMENTATION'] = False
        cmake.definitions['INSTALL_PKG_CONFIG_FILE'] = False
        cmake.configure()
        return cmake

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_id(self):
        self.info.header_only()
