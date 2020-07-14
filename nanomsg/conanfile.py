from conans import ConanFile, CMake, tools
import os
import shutil

class NanomsgConan(ConanFile):
    name = "nanomsg"
    version = "1.1.5"
    description = "Simple high-performance implementation of several scalability protocols"
    topics = ("conan", "nanomsg", "communication", "messaging", "protocols")
    url = "https://github.com/bincrafters/conan-nanomsg"
    homepage = "https://github.com/nanomsg/nanomsg"
    license = "MIT"
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    short_paths = True
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "enable_doc": [True, False],
        "enable_getaddrinfo_a": [True, False],
        "enable_tests": [True, False],
        "enable_tools": [True, False],
        "enable_nanocat": [True, False],
    }
    default_options = {
        'shared': True,
        'fPIC': True,
        'enable_doc': False,
        'enable_getaddrinfo_a': True,
        'enable_tests': False,
        'enable_tools': True,
        'enable_nanocat': True
    }
    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        sha256 = "218b31ae1534ab897cb5c419973603de9ca1a5f54df2e724ab4a188eb416df5a"
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)
        os.rename(os.path.join(self._source_subfolder, 'CMakeLists.txt'), 'CMakeListsOriginal.txt')
        for f in os.listdir(self._source_subfolder):
            shutil.move(os.path.join(self._source_subfolder, f), '.')

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["NN_STATIC_LIB"] = not self.options.shared
        cmake.definitions["NN_ENABLE_DOC"] = self.options.enable_doc
        cmake.definitions["NN_ENABLE_GETADDRINFO_A"] = self.options.enable_getaddrinfo_a
        cmake.definitions["NN_TESTS"] = self.options.enable_tests
        cmake.definitions["NN_TOOLS"] = self.options.enable_tools
        cmake.definitions["NN_ENABLE_NANOCAT"] = self.options.enable_nanocat
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        if not self.options.shared:
            self.cpp_info.defines.append("NN_STATIC_LIB=ON")

        if self.settings.os == "Windows" and not self.options.shared:
            self.cpp_info.libs.extend(['mswsock', 'ws2_32'])
        elif self.settings.os == "Linux":
            self.cpp_info.libs.extend(['anl', 'pthread'])
