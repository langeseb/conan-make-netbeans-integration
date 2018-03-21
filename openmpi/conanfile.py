#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment, RunEnvironment
import os


class OpenMPIConan(ConanFile):
    name = "openmpi"
    version = "3.0.0"
    description = "A High Performance Message Passing Library"
    url="http://stash01.dev.sarah/projects/RDK/repos/openmpi/"
    license = "https://www.open-mpi.org/community/license.php"
    settings = {"os": ["Linux"], "arch": ["x86_64"], "compiler": ["gcc"] , "build_type": None}
    options = {"shared": [True,False]}
    default_options = "shared=True"
#    generators  = "txt"
    tarfile = name + "-" + version + ".tar.gz"
    build_dir  = name + "-" + version 
    exports_sources = tarfile

#    def requirements(self):
#        self.requires.add("zlib/1.2.11@conan/stable")

#   def system_requirements(self):
#       if self.settings.os == "Linux":
#           if tools.os_info.linux_distro == "ubuntu" or tools.os_info.linux_distro == "debian":
#               installer = tools.SystemPackageTool()
#               installer.install('openssh-client')

#    def source(self):
#        version_tokens = self.version.split('.')
#        version_short = 'v%s.%s' % (version_tokens[0], version_tokens[1])
#        source_url = "https://www.open-mpi.org/software/ompi"
#        tools.get("{0}/{1}/downloads/{2}-{3}.tar.bz2".format(source_url, version_short, self.name, self.version))
#        extracted_dir = self.name + "-" + self.version
#        os.rename(extracted_dir, "sources")

    def build(self):
        env = RunEnvironment(self)
        with tools.environment_append(env.vars):
            tools.unzip(self.tarfile)
            with tools.chdir(self.build_dir):
              env_build = AutoToolsBuildEnvironment(self)
              args = ['--disable-wrapper-rpath',
                      'prefix=%s' % self.package_folder]
              if self.settings.build_type == 'Debug':
                  args.append('--enable-debug')
              if self.options.shared == 'True':
                  args.extend(['--enable-shared', '--disable-static'])
              else:
                  args.extend(['--enable-static', '--disable-shared'])
              args.append('--with-slurm')
              env_build.configure(args=args)
              env_build.make()
              env_build.make(args=['install'])

    def package(self):
        with tools.chdir(self.build_dir):
            self.copy("*.h", dst="include", src="include", keep_path=True)
            self.copy("*", dst="bin", src="bin", keep_path=True)
            self.copy("*", dst="lib", src="lib", keep_path=True, symlinks=True)

    def package_info(self):
        self.cpp_info.libs = ['mpi', 'open-rte', 'open-pal']
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(['dl', 'pthread', 'rt', 'util'])
        self.env_info.MPI_HOME = self.package_folder
        self.env_info.MPI_BIN = os.path.join(self.package_folder, 'bin')

    def deploy(self):
        self.copy("*.h", dst="include", src="include", keep_path=True)
        self.copy("*", dst="bin", src="bin", keep_path=True)
        self.copy("*", dst="lib", src="lib", keep_path=True, symlinks=True)


