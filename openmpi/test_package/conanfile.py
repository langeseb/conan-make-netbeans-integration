#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools, RunEnvironment
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        mpiexec = os.path.join(os.environ['MPI_BIN'], 'mpiexec')
        command = '%s %s' % (mpiexec, os.path.join("bin", "test_package"))
        with tools.environment_append(RunEnvironment(self).vars):
            if self.settings.os == "Windows":
                self.run(command)
            elif self.settings.os == "Macos":
                self.run("DYLD_LIBRARY_PATH=%s %s" % (os.environ.get('DYLD_LIBRARY_PATH', ''), command))
            else:
                self.run("LD_LIBRARY_PATH=%s %s" % (os.environ.get('LD_LIBRARY_PATH', ''), command))
