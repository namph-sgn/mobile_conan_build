from conans import ConanFile, CMake
from conan.tools.files import save
from conans.model import Generator
from conans.tools import Version
from itertools import chain
from pathlib import Path

required_conan_version = ">=1.53.0"

# Conan does not provide a generator which makes it possible to easily access package folders for
# packages in both host and build contexts. This is the replacement.
def generate_conan_package_paths(conanfile):
    def toPosixPath(path):
        return path.replace("\\", "/")

    packages = {reference.ref.name: toPosixPath(package.package_folder) \
        for reference, package in chain(
            conanfile.dependencies.build.items(),
            conanfile.dependencies.host.items())}

    content = "set(CONAN_DEPENDENCIES {})\n\n".format(" ".join(name for name in packages.keys()))

    for name, path in packages.items():
        content += f"set(CONAN_{name.upper()}_ROOT \"{path}\")\n"

    save(conanfile, "conan_paths.cmake", content)


def generate_conan_package_refs(conanfile):
    refs = [package.pref.full_str() \
        for _, package in chain(
                conanfile.dependencies.build.items(),
                conanfile.dependencies.host.items())]

    save(conanfile, "conan_refs.txt", "\n".join(refs))

class OryzaPluginConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    
    options = {"shared": [True, False]}
    
    default_options = {"shared": False}
    
    generators = "cmake_find_package", "virtualrunenv"

    requires = (
        "opencv/4.5.5"
    )

    def generate(self):
        generate_conan_package_paths(self)
        generate_conan_package_refs(self)

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["opencv"]

    def requirements(self):
        # if self.isLinux or self.isWindows or self.isAndroid:
        #     self.requires("openal-soft/1.19.1")
        pass


    def imports(self):
        copy_packages = [
            "opencv"
        ]
        self._copy_packages(copy_packages)

    def _copy_packages(self, packages):
        for package in packages:
            if package in self.deps_cpp_info.deps:
                if self.isLinux or self.isAndroid:
                    self.copy("*.so*", "lib", "lib", root_package=package)
                if self.isMacos:
                    self.copy("*.dylib", "lib", "lib", root_package=package)
                if self.isWindows:
                    self.copy("*.dll", "bin", "bin", root_package=package)
                    self.copy("*.pdb", "bin", "bin", root_package=package)

        self.fixLibraryPermissions()


    # Temporary workaround for conan issue 6470.
    def fixLibraryPermissions(self):
        if self.isWindows:
            return

        if self._lib_path.is_dir():
            self.run(f"chmod -R u+w {self._lib_path}")


    @property
    def isLinux(self):
        return self.settings.os == "Linux"

    @property
    def isWindows(self):
        return self.settings.os == "Windows"

    @property
    def isMacos(self):
        return self.settings.os == "Macos"

    @property
    def isAndroid(self):
        return self.settings.os == "Android"

    @property
    def isLinux(self):
        return self.settings.os == "Linux"

    @property
    def isArm32(self):
        return self.settings.arch in ("armv7", "armv7hf")

    @property
    def isArm64(self):
        return self.settings.arch == "armv8"

    @property
    def isEdge1(self):
        return self.options.targetDevice == "edge1"

    @property
    def isIos(self):
        return self.settings.os == "iOS"

    @property
    def haveMediaserver(self):
        return not (self.isAndroid or self.isIos)

    @property
    def haveDesktopClient(self):
        return self.isWindows or self.isMacos \
               or (self.isLinux and (self.settings.arch in ("x86_64", "armv8")))

    @property
    def haveMobileClient(self):
        return self.isAndroid or self.isIos

    @property
    def _lib_path(self):
        return Path(self.install_folder) / "lib"
