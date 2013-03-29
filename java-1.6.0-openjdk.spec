# If gcjbootstrap is 1 IcedTea is bootstrapped against
# java-1.5.0-gcj-devel.  If gcjbootstrap is 0 IcedTea is built against
# java-1.6.0-openjdk-devel.
%define gcjbootstrap 0

#remove with %ifdef in postun
%define NO_PLUGIN 1

# If debug is 1, IcedTea is built with all debug info present.
%define debug 0

# If runtests is 0 test suites will not be run.
%define runtests 0

%define icedteaver 1.7.5
%define icedteasnapshot %{nil}
%define openjdkver b17
%define openjdkdate 14_oct_2009

%define genurl http://cvs.fedoraproject.org/viewcvs/devel/java-1.6.0-openjdk/

%define icedteaurl http://icedtea.classpath.org/

%define accessmajorver 1.23
%define accessminorver 0
%define accessver %{accessmajorver}.%{accessminorver}
%define accessurl http://ftp.gnome.org/pub/GNOME/sources/java-access-bridge/

%define hotspoturl  http://hg.openjdk.java.net/jdk6/hotspot/hotspot/archive/

%define openjdkurlbase http://www.java.net/download/openjdk/jdk6/promoted/
%define openjdkurl %{openjdkurlbase}%{openjdkver}/
%define rhelzip  openjdk-6-src-%{openjdkver}-%{openjdkdate}-rhel.tar.gz

%define mauvedate 2008-10-22

%define multilib_arches ppc64 sparc64 x86_64

%define jit_arches %{ix86} x86_64 sparcv9 sparc64

%ifarch x86_64
%define archbuild amd64
%define archinstall amd64
%endif
%ifarch ppc
%define archbuild ppc
%define archinstall ppc
%endif
%ifarch ppc64
%define archbuild ppc64
%define archinstall ppc64
%endif
%ifarch i386
%define archbuild i586
%define archinstall i386
%endif
%ifarch i686
%define archbuild i586
%define archinstall i386
%endif
%ifarch ia64
%define archbuild ia64
%define archinstall ia64
%endif
%ifarch s390
%define archbuild s390x
%define archinstall s390x
%endif
# 32 bit sparc, optimized for v9
%ifarch sparcv9
%define archbuild sparc
%define archinstall sparc
%endif
# 64 bit sparc
%ifarch sparc64
%define archbuild sparcv9
%define archinstall sparcv9
%endif
%ifnarch %{jit_arches}
%define archbuild %{_arch}
%define archinstall %{_arch}
%endif

# Reduce build time from 27 hours to 12 hours by only running test
# suites on JIT architectures.
#%%ifnarch %{jit_arches}
#%%define runtests 0
#%%endif

%if %{debug}
%define debugbuild icedtea-debug
%define buildoutputdir openjdk/build/linux-%{archbuild}-debug
%else
%define debugbuild %{nil}
%define buildoutputdir openjdk/build/linux-%{archbuild}
%endif

%if %{gcjbootstrap}

%ifarch %{jit_arches}
%define icedteaopt --enable-systemtap
%else
%define icedteaopt %{nil}
%endif

%else

%ifarch %{jit_arches}
%define icedteaopt --with-openjdk --enable-systemtap
%else
%define icedteaopt --with-openjdk
%endif

%endif

# Convert an absolute path to a relative path.  Each symbolic link is
# specified relative to the directory in which it is installed so that
# it will resolve properly within chrooted installations.
%define script 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])'
%define abs2rel %{__perl} -e %{script}

# Hard-code libdir on 64-bit architectures to make the 64-bit JDK
# simply be another alternative.
%ifarch %{multilib_arches}
%define syslibdir       %{_prefix}/lib64
%define _libdir         %{_prefix}/lib
%define archname        %{name}.%{_arch}
%define javaplugin      libjavaplugin.so.%{_arch}
%else
%define syslibdir       %{_libdir}
%define archname        %{name}
%define javaplugin      libjavaplugin.so
%endif

# Standard JPackage naming and versioning defines.
%define origin          openjdk
%define priority        16000
%define javaver         1.6.0
%define buildver        0

# Standard JPackage directories and symbolic links.
# Make 64-bit JDKs just another alternative on 64-bit architectures.
%ifarch %{multilib_arches}
%define sdklnk          java-%{javaver}-%{origin}.%{_arch}
%define jrelnk          jre-%{javaver}-%{origin}.%{_arch}
%define sdkdir          %{name}-%{version}.%{_arch}
%else
%define sdklnk          java-%{javaver}-%{origin}
%define jrelnk          jre-%{javaver}-%{origin}
%define sdkdir          %{name}-%{version}
%endif
%define jredir          %{sdkdir}/jre
%define sdkbindir       %{_jvmdir}/%{sdklnk}/bin
%define jrebindir       %{_jvmdir}/%{jrelnk}/bin
%ifarch %{multilib_arches}
%define jvmjardir       %{_jvmjardir}/%{name}-%{version}.%{_arch}
%else
%define jvmjardir       %{_jvmjardir}/%{name}-%{version}
%endif

%ifarch %{jit_arches}
# Where to install systemtap tapset (links)
# We would like these to be in a package specific subdir,
# but currently systemtap doesn't support that, so we have to
# use the root tapset dir for now. To distinquish between 64
# and 32 bit architectures we place the tapsets under the arch
# specific dir (note that systemtap will only pickup the tapset
# for the primary arch for now). Systemtap uses the machine name
# aka build_cpu as architecture specific directory name.
#%define tapsetdir	/usr/share/systemtap/tapset/%{sdkdir}
%define tapsetdir	/usr/share/systemtap/tapset/%{_build_cpu}
%endif

# Prevent brp-java-repack-jars from being run.
%define __jar_repack 0

Name:    java-%{javaver}-%{origin}
Version: %{javaver}.%{buildver}
Release: 1.31.%{openjdkver}%{?dist}
# java-1.5.0-ibm from jpackage.org set Epoch to 1 for unknown reasons,
# and this change was brought into RHEL-4.  java-1.5.0-ibm packages
# also included the epoch in their virtual provides.  This created a
# situation where in-the-wild java-1.5.0-ibm packages provided "java =
# 1:1.5.0".  In RPM terms, "1.6.0 < 1:1.5.0" since 1.6.0 is
# interpreted as 0:1.6.0.  So the "java >= 1.6.0" requirement would be
# satisfied by the 1:1.5.0 packages.  Thus we need to set the epoch in
# JDK package >= 1.6.0 to 1, and packages referring to JDK virtual
# provides >= 1.6.0 must specify the epoch, "java >= 1:1.6.0".
Epoch:   1
Summary: OpenJDK Runtime Environment
Group:   Development/Languages

License:  ASL 1.1, ASL 2.0, GPL+, GPLv2, GPLv2 with exceptions, LGPL+, LGPLv2, MPLv1.0, MPLv1.1, Public Domain, W3C
URL:      http://icedtea.classpath.org/
Source0:  %{icedteaurl}download/source/icedtea6-%{icedteaver}%{icedteasnapshot}.tar.gz
# To generate, download OpenJDK tarball from %{openjdkurl},
# and run %{SOURCE3} on the tarball.
Source1:  %{rhelzip}
Source2:  %{accessurl}%{accessmajorver}/java-access-bridge-%{accessver}.tar.bz2
Source3:  %{genurl}generate-rhel-zip.sh
Source4:  README.src
Source5:  mauve-%{mauvedate}.tar.gz
Source6:  mauve_tests
# FIXME: This patch needs to be fixed. optflags argument
# -mtune=generic is being ignored because it breaks several graphical
# applications.
Patch0:   java-1.6.0-openjdk-optflags.patch
Patch1:   java-1.6.0-openjdk-java-access-bridge-tck.patch
Patch2:   java-1.6.0-openjdk-java-access-bridge-idlj.patch
Patch3:	  java-1.6.0-openjdk-java-access-bridge-security.patch
Patch4:   java-1.6.0-openjdk-accessible-toolkit.patch
Patch5:   java-1.6.0-openjdk-debugdocs.patch
Patch6:   %{name}-debuginfo.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: alsa-lib-devel
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: giflib-devel
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: libXp-devel
BuildRequires: libXt-devel
BuildRequires: libXtst-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: wget
BuildRequires: xalan-j2
BuildRequires: xerces-j2
BuildRequires: xorg-x11-proto-devel
BuildRequires: mercurial
BuildRequires: ant
BuildRequires: libXinerama-devel
BuildRequires: rhino
%if %{gcjbootstrap}
BuildRequires: java-1.5.0-gcj-devel
%else
BuildRequires: java-1.6.0-openjdk-devel
%endif
# Mauve build requirements.
BuildRequires: xorg-x11-server-Xvfb
BuildRequires: xorg-x11-fonts-Type1
BuildRequires: xorg-x11-fonts-misc
BuildRequires: freetype-devel >= 2.3.0
BuildRequires: fontconfig
BuildRequires: ecj
# Java Access Bridge for GNOME build requirements.
BuildRequires: at-spi-devel
BuildRequires: gawk
BuildRequires: libbonobo-devel
BuildRequires: pkgconfig >= 0.9.0
BuildRequires: xorg-x11-utils
# IcedTeaPlugin build requirements.
#BuildRequires: gecko-devel
#BuildRequires: glib2-devel
#BuildRequires: gtk2-devel
#BuildRequires: xulrunner-devel
# PulseAudio build requirements.
BuildRequires: pulseaudio-libs-devel >= 0.9.11
BuildRequires: pulseaudio >= 0.9.11
# Zero-assembler build requirement.
%ifnarch %{jit_arches}
BuildRequires: libffi-devel
%endif

ExclusiveArch: x86_64 i686

# cacerts build requirement.
BuildRequires: openssl
# execstack build requirement.
BuildRequires: prelink
%ifarch %{jit_arches}
#systemtap build requirement.
BuildRequires: systemtap-sdt-devel
%endif
# visualvm build requirements.
BuildRequires: jakarta-commons-logging

Requires: rhino
Requires: libjpeg = 6b
# Require /etc/pki/java/cacerts.
Requires: ca-certificates
# Require jpackage-utils for ant.
Requires: jpackage-utils >= 1.7.3-1jpp.2
# Require zoneinfo data provided by tzdata-java subpackage.
Requires: tzdata-java
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

# Standard JPackage base provides.
Provides: jre-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides: jre-%{origin} = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver} = %{epoch}:%{version}-%{release}
Provides: jre = %{javaver}
Provides: java-%{origin} = %{epoch}:%{version}-%{release}
Provides: java = %{epoch}:%{javaver}
# Standard JPackage extensions provides.
Provides: jndi = %{epoch}:%{version}
Provides: jndi-ldap = %{epoch}:%{version}
Provides: jndi-cos = %{epoch}:%{version}
Provides: jndi-rmi = %{epoch}:%{version}
Provides: jndi-dns = %{epoch}:%{version}
Provides: jaas = %{epoch}:%{version}
Provides: jsse = %{epoch}:%{version}
Provides: jce = %{epoch}:%{version}
Provides: jdbc-stdext = 3.0
Provides: java-sasl = %{epoch}:%{version}
Provides: java-fonts = %{epoch}:%{version}


Obsoletes: java-1.6.0-openjdk-plugin <= %{epoch}:%{version}-%{release}


%description
The OpenJDK runtime environment.

%package devel
Summary: OpenJDK Development Environment
Group:   Development/Tools

# Require base package.
Requires:         %{name} = %{epoch}:%{version}-%{release}
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

# Standard JPackage devel provides.
Provides: java-sdk-%{javaver}-%{origin} = %{epoch}:%{version}
Provides: java-sdk-%{javaver} = %{epoch}:%{version}
Provides: java-sdk-%{origin} = %{epoch}:%{version}
Provides: java-sdk = %{epoch}:%{javaver}
Provides: java-%{javaver}-devel = %{epoch}:%{version}
Provides: java-devel-%{origin} = %{epoch}:%{version}
Provides: java-devel = %{epoch}:%{javaver}


%description devel
The OpenJDK development tools.

%package demo
Summary: OpenJDK Demos
Group:   Development/Languages

Requires: %{name} = %{epoch}:%{version}-%{release}

%description demo
The OpenJDK demos.

%package src
Summary: OpenJDK Source Bundle
Group:   Development/Languages

Requires: %{name} = %{epoch}:%{version}-%{release}

%description src
The OpenJDK source bundle.

%package javadoc
Summary: OpenJDK API Documentation
Group:   Documentation

# Post requires alternatives to install javadoc alternative.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall javadoc alternative.
Requires(postun): %{_sbindir}/alternatives

# Standard JPackage javadoc provides.
Provides: java-javadoc = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-javadoc = %{epoch}:%{version}-%{release}

%description javadoc
The OpenJDK API documentation.

#%package plugin
#Summary: OpenJDK Web Browser Plugin
#Group:   Applications/Internet
#
#Requires: %{name} = %{epoch}:%{version}-%{release}
#Requires: %{syslibdir}/mozilla/plugins
## Post requires alternatives to install plugin alternative.
#Requires(post):   %{_sbindir}/alternatives
## Postun requires alternatives to uninstall plugin alternative.
#Requires(postun): %{_sbindir}/alternatives
#
## java-1.6.0-openjdk-plugin replaces java-1.7.0-icedtea-plugin.
##Provides: java-1.7.0-icedtea-plugin = 0:1.7.0.0-0.999
##Obsoletes: java-1.7.0-icedtea-plugin < 0:1.7.0.0-0.999
#
## Standard JPackage plugin provides.
#Provides: java-plugin = %{javaver}
#Provides: java-%{javaver}-plugin = %{epoch}:%{version}
#
#%description plugin
#The OpenJDK web browser plugin.

%prep
%setup -q -n icedtea6-%{icedteaver}
%setup -q -n icedtea6-%{icedteaver} -T -D -a 5
%setup -q -n icedtea6-%{icedteaver} -T -D -a 2
%patch0
cp %{SOURCE4} .
cp %{SOURCE6} .

%build
# How many cpu's do we have?
export NUM_PROC=`/usr/bin/getconf _NPROCESSORS_ONLN 2> /dev/null || :`
export NUM_PROC=${NUM_PROC:-1}

# Build IcedTea and OpenJDK.
%ifarch sparc64 alpha
export ARCH_DATA_MODEL=64
%endif
%ifarch alpha
export CFLAGS="$CFLAGS -mieee"
%endif
./autogen.sh
./configure %{icedteaopt} --with-openjdk-src-zip=%{SOURCE1} \
  --with-pkgversion=rhel-%{release}-%{_arch} --enable-pulse-java \
  --with-abs-install-dir=%{_jvmdir}/%{sdkdir} \
  --with-rhino --disable-npplugin \
  --with-parallel-jobs=$NUM_PROC
make patch
patch -l -p0 < %{PATCH3}
patch -l -p0 < %{PATCH4}

%if %{debug}
patch -l -p0 < %{PATCH5}
patch -l -p0 < %{PATCH6}
%endif

%if %{gcjbootstrap}
make stamps/patch-ecj.stamp
%endif
make %{debugbuild}

export JAVA_HOME=$(pwd)/%{buildoutputdir}/j2sdk-image

# Build Java Access Bridge for GNOME.
pushd java-access-bridge-%{accessver}
  patch -l -p1 < %{PATCH1}
  patch -l -p1 < %{PATCH2}
  OLD_PATH=$PATH
  export PATH=$JAVA_HOME/bin:$OLD_PATH
  ./configure
  make
  export PATH=$OLD_PATH
  cp -a bridge/accessibility.properties $JAVA_HOME/jre/lib
  cp -a gnome-java-bridge.jar $JAVA_HOME/jre/lib/ext
popd

%if %{runtests}
# Run jtreg test suite.
{
  echo ====================JTREG TESTING========================
  export DISPLAY=:20
  Xvfb :20 -screen 0 1x1x24 -ac&
  echo $! > Xvfb.pid
  make jtregcheck -k
  kill -9 `cat Xvfb.pid`
  unset DISPLAY
  rm -f Xvfb.pid
  echo ====================JTREG TESTING END====================
} || :

# Run Mauve test suite.
{
  pushd mauve-%{mauvedate}
    ./configure
    make
    echo ====================MAUVE TESTING========================
    export DISPLAY=:20
    Xvfb :20 -screen 0 1x1x24 -ac&
    echo $! > Xvfb.pid
    $JAVA_HOME/bin/java Harness -vm $JAVA_HOME/bin/java \
      -file %{SOURCE6} -timeout 30000 2>&1 | tee mauve_output
    kill -9 `cat Xvfb.pid`
    unset DISPLAY
    rm -f Xvfb.pid
    echo ====================MAUVE TESTING END====================
  popd
} || :
%endif

%install
rm -rf $RPM_BUILD_ROOT
STRIP_KEEP_SYMTAB=libjvm*

pushd %{buildoutputdir}/j2sdk-image

  # Install main files.
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  cp -a bin include lib src.zip $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
  cp -a jre/bin jre/lib $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}

%ifarch %{jit_arches}
  # Install systemtap support files.
  cp -a tapset $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  install -d -m 755 $RPM_BUILD_ROOT%{tapsetdir}
  pushd $RPM_BUILD_ROOT%{tapsetdir}
    RELATIVE=$(%{abs2rel} %{_jvmdir}/%{sdkdir}/tapset %{tapsetdir})
    ln -sf $RELATIVE/*.stp .
  popd
%endif

  # Install cacerts symlink.
  rm -f $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/cacerts
  pushd $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security
    RELATIVE=$(%{abs2rel} %{_sysconfdir}/pki/java \
      %{_jvmdir}/%{jredir}/lib/security)
    ln -sf $RELATIVE/cacerts .
  popd

  # Install extension symlinks.
  install -d -m 755 $RPM_BUILD_ROOT%{jvmjardir}
  pushd $RPM_BUILD_ROOT%{jvmjardir}
    RELATIVE=$(%{abs2rel} %{_jvmdir}/%{jredir}/lib %{jvmjardir})
    ln -sf $RELATIVE/jsse.jar jsse-%{version}.jar
    ln -sf $RELATIVE/jce.jar jce-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-ldap-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-cos-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-rmi-%{version}.jar
    ln -sf $RELATIVE/rt.jar jaas-%{version}.jar
    ln -sf $RELATIVE/rt.jar jdbc-stdext-%{version}.jar
    ln -sf jdbc-stdext-%{version}.jar jdbc-stdext-3.0.jar
    ln -sf $RELATIVE/rt.jar sasl-%{version}.jar
    for jar in *-%{version}.jar
    do
      if [ x%{version} != x%{javaver} ]
      then
        ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|-%{javaver}.jar|g")
      fi
      ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|.jar|g")
    done
  popd

  # Install JCE policy symlinks.
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmprivdir}/%{archname}/jce/vanilla

  # Install versionless symlinks.
  pushd $RPM_BUILD_ROOT%{_jvmdir}
    ln -sf %{jredir} %{jrelnk}
    ln -sf %{sdkdir} %{sdklnk}
  popd

  pushd $RPM_BUILD_ROOT%{_jvmjardir}
    ln -sf %{sdkdir} %{jrelnk}
    ln -sf %{sdkdir} %{sdklnk}
  popd

  # Remove javaws man page.
  rm -f man/man1/javaws.1

  # Install man pages.
  install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man1
  for manpage in man/man1/*
  do
    # Convert man pages to UTF8 encoding.
    iconv -f ISO_8859-1 -t UTF8 $manpage -o $manpage.tmp
    mv -f $manpage.tmp $manpage
    install -m 644 -p $manpage $RPM_BUILD_ROOT%{_mandir}/man1/$(basename \
      $manpage .1)-%{name}.1
  done

  # Install demos and samples.
  cp -a demo $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  mkdir -p sample/rmi
  mv bin/java-rmi.cgi sample/rmi
  cp -a sample $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}

  # Run execstack on libjvm.so.
  %ifarch i386 i686
    execstack -c $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/%{archinstall}/client/libjvm.so
  %endif
  execstack -c $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/%{archinstall}/server/libjvm.so

popd

# Install Javadoc documentation.
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}
cp -a %{buildoutputdir}/docs $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# Install icons and menu entries.
for s in 16 24 32 48 ; do
  install -D -p -m 644 \
    openjdk/jdk/src/solaris/classes/sun/awt/X11/java-icon${s}.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/java.png
done

# Install desktop files.
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
#cp javaws.png $RPM_BUILD_ROOT%{_datadir}/pixmaps
#desktop-file-install --vendor ''\
#  --dir $RPM_BUILD_ROOT%{_datadir}/applications javaws.desktop
for e in jconsole policytool ; do
    desktop-file-install --vendor=%{name} --mode=644 \
        --dir=$RPM_BUILD_ROOT%{_datadir}/applications $e.desktop
done

# Find JRE directories.
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type d \
  | grep -v jre/lib/security \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' \
  > %{name}.files
# Find JRE files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type f -o -type l \
  | grep -v jre/lib/security \
  | grep -v IcedTeaNPPlugin.so \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  >> %{name}.files
# Find demo directories.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample -type d \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' \
  > %{name}-demo.files

# FIXME: remove SONAME entries from demo DSOs.  See
# https://bugzilla.redhat.com/show_bug.cgi?id=436497

# Find non-documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample \
  -type f -o -type l | sort \
  | grep -v README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  >> %{name}-demo.files
# Find documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample \
  -type f -o -type l | sort \
  | grep README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  | sed 's|^|%doc |' \
  >> %{name}-demo.files

%clean
rm -rf $RPM_BUILD_ROOT

# FIXME: identical binaries are copied, not linked. This needs to be
# fixed upstream.
%post
ext=.gz
alternatives \
  --install %{_bindir}/java java %{jrebindir}/java %{priority} \
  --slave %{_jvmdir}/jre jre %{_jvmdir}/%{jrelnk} \
  --slave %{_jvmjardir}/jre jre_exports %{_jvmjardir}/%{jrelnk} \
  --slave %{_bindir}/keytool keytool %{jrebindir}/keytool \
  --slave %{_bindir}/orbd orbd %{jrebindir}/orbd \
  --slave %{_bindir}/pack200 pack200 %{jrebindir}/pack200 \
  --slave %{_bindir}/rmid rmid %{jrebindir}/rmid \
  --slave %{_bindir}/rmiregistry rmiregistry %{jrebindir}/rmiregistry \
  --slave %{_bindir}/servertool servertool %{jrebindir}/servertool \
  --slave %{_bindir}/tnameserv tnameserv %{jrebindir}/tnameserv \
  --slave %{_bindir}/unpack200 unpack200 %{jrebindir}/unpack200 \
  --slave %{_mandir}/man1/java.1$ext java.1$ext \
  %{_mandir}/man1/java-%{name}.1$ext \
  --slave %{_mandir}/man1/keytool.1$ext keytool.1$ext \
  %{_mandir}/man1/keytool-%{name}.1$ext \
  --slave %{_mandir}/man1/orbd.1$ext orbd.1$ext \
  %{_mandir}/man1/orbd-%{name}.1$ext \
  --slave %{_mandir}/man1/pack200.1$ext pack200.1$ext \
  %{_mandir}/man1/pack200-%{name}.1$ext \
  --slave %{_mandir}/man1/rmid.1$ext rmid.1$ext \
  %{_mandir}/man1/rmid-%{name}.1$ext \
  --slave %{_mandir}/man1/rmiregistry.1$ext rmiregistry.1$ext \
  %{_mandir}/man1/rmiregistry-%{name}.1$ext \
  --slave %{_mandir}/man1/servertool.1$ext servertool.1$ext \
  %{_mandir}/man1/servertool-%{name}.1$ext \
  --slave %{_mandir}/man1/tnameserv.1$ext tnameserv.1$ext \
  %{_mandir}/man1/tnameserv-%{name}.1$ext \
  --slave %{_mandir}/man1/unpack200.1$ext unpack200.1$ext \
  %{_mandir}/man1/unpack200-%{name}.1$ext

alternatives \
  --install %{_jvmdir}/jre-%{origin} \
  jre_%{origin} %{_jvmdir}/%{jrelnk} %{priority} \
  --slave %{_jvmjardir}/jre-%{origin} \
  jre_%{origin}_exports %{_jvmjardir}/%{jrelnk}

alternatives \
  --install %{_jvmdir}/jre-%{javaver} \
  jre_%{javaver} %{_jvmdir}/%{jrelnk} %{priority} \
  --slave %{_jvmjardir}/jre-%{javaver} \
  jre_%{javaver}_exports %{_jvmjardir}/%{jrelnk}

# Update for jnlp handling.
update-desktop-database %{_datadir}/applications &> /dev/null || :

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

exit 0

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove java %{jrebindir}/java
  alternatives --remove jre_%{origin} %{_jvmdir}/%{jrelnk}
  alternatives --remove jre_%{javaver} %{_jvmdir}/%{jrelnk}
fi

# Update for jnlp handling.
update-desktop-database %{_datadir}/applications &> /dev/null || :

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

exit 0

%post devel
ext=.gz
alternatives \
  --install %{_bindir}/javac javac %{sdkbindir}/javac %{priority} \
  --slave %{_jvmdir}/java java_sdk %{_jvmdir}/%{sdklnk} \
  --slave %{_jvmjardir}/java java_sdk_exports %{_jvmjardir}/%{sdklnk} \
  --slave %{_bindir}/appletviewer appletviewer %{sdkbindir}/appletviewer \
  --slave %{_bindir}/apt apt %{sdkbindir}/apt \
  --slave %{_bindir}/extcheck extcheck %{sdkbindir}/extcheck \
  --slave %{_bindir}/jar jar %{sdkbindir}/jar \
  --slave %{_bindir}/jarsigner jarsigner %{sdkbindir}/jarsigner \
  --slave %{_bindir}/javadoc javadoc %{sdkbindir}/javadoc \
  --slave %{_bindir}/javah javah %{sdkbindir}/javah \
  --slave %{_bindir}/javap javap %{sdkbindir}/javap \
  --slave %{_bindir}/jconsole jconsole %{sdkbindir}/jconsole \
  --slave %{_bindir}/jdb jdb %{sdkbindir}/jdb \
  --slave %{_bindir}/jhat jhat %{sdkbindir}/jhat \
  --slave %{_bindir}/jinfo jinfo %{sdkbindir}/jinfo \
  --slave %{_bindir}/jmap jmap %{sdkbindir}/jmap \
  --slave %{_bindir}/jps jps %{sdkbindir}/jps \
  --slave %{_bindir}/jrunscript jrunscript %{sdkbindir}/jrunscript \
  --slave %{_bindir}/jsadebugd jsadebugd %{sdkbindir}/jsadebugd \
  --slave %{_bindir}/jstack jstack %{sdkbindir}/jstack \
  --slave %{_bindir}/jstat jstat %{sdkbindir}/jstat \
  --slave %{_bindir}/jstatd jstatd %{sdkbindir}/jstatd \
  --slave %{_bindir}/native2ascii native2ascii %{sdkbindir}/native2ascii \
  --slave %{_bindir}/policytool policytool %{sdkbindir}/policytool \
  --slave %{_bindir}/rmic rmic %{sdkbindir}/rmic \
  --slave %{_bindir}/schemagen schemagen %{sdkbindir}/schemagen \
  --slave %{_bindir}/serialver serialver %{sdkbindir}/serialver \
  --slave %{_bindir}/wsgen wsgen %{sdkbindir}/wsgen \
  --slave %{_bindir}/wsimport wsimport %{sdkbindir}/wsimport \
  --slave %{_bindir}/xjc xjc %{sdkbindir}/xjc \
  --slave %{_mandir}/man1/appletviewer.1$ext appletviewer.1$ext \
  %{_mandir}/man1/appletviewer-%{name}.1$ext \
  --slave %{_mandir}/man1/apt.1$ext apt.1$ext \
  %{_mandir}/man1/apt-%{name}.1$ext \
  --slave %{_mandir}/man1/extcheck.1$ext extcheck.1$ext \
  %{_mandir}/man1/extcheck-%{name}.1$ext \
  --slave %{_mandir}/man1/jar.1$ext jar.1$ext \
  %{_mandir}/man1/jar-%{name}.1$ext \
  --slave %{_mandir}/man1/jarsigner.1$ext jarsigner.1$ext \
  %{_mandir}/man1/jarsigner-%{name}.1$ext \
  --slave %{_mandir}/man1/javac.1$ext javac.1$ext \
  %{_mandir}/man1/javac-%{name}.1$ext \
  --slave %{_mandir}/man1/javadoc.1$ext javadoc.1$ext \
  %{_mandir}/man1/javadoc-%{name}.1$ext \
  --slave %{_mandir}/man1/javah.1$ext javah.1$ext \
  %{_mandir}/man1/javah-%{name}.1$ext \
  --slave %{_mandir}/man1/javap.1$ext javap.1$ext \
  %{_mandir}/man1/javap-%{name}.1$ext \
  --slave %{_mandir}/man1/jconsole.1$ext jconsole.1$ext \
  %{_mandir}/man1/jconsole-%{name}.1$ext \
  --slave %{_mandir}/man1/jdb.1$ext jdb.1$ext \
  %{_mandir}/man1/jdb-%{name}.1$ext \
  --slave %{_mandir}/man1/jhat.1$ext jhat.1$ext \
  %{_mandir}/man1/jhat-%{name}.1$ext \
  --slave %{_mandir}/man1/jinfo.1$ext jinfo.1$ext \
  %{_mandir}/man1/jinfo-%{name}.1$ext \
  --slave %{_mandir}/man1/jmap.1$ext jmap.1$ext \
  %{_mandir}/man1/jmap-%{name}.1$ext \
  --slave %{_mandir}/man1/jps.1$ext jps.1$ext \
  %{_mandir}/man1/jps-%{name}.1$ext \
  --slave %{_mandir}/man1/jrunscript.1$ext jrunscript.1$ext \
  %{_mandir}/man1/jrunscript-%{name}.1$ext \
  --slave %{_mandir}/man1/jsadebugd.1$ext jsadebugd.1$ext \
  %{_mandir}/man1/jsadebugd-%{name}.1$ext \
  --slave %{_mandir}/man1/jstack.1$ext jstack.1$ext \
  %{_mandir}/man1/jstack-%{name}.1$ext \
  --slave %{_mandir}/man1/jstat.1$ext jstat.1$ext \
  %{_mandir}/man1/jstat-%{name}.1$ext \
  --slave %{_mandir}/man1/jstatd.1$ext jstatd.1$ext \
  %{_mandir}/man1/jstatd-%{name}.1$ext \
  --slave %{_mandir}/man1/native2ascii.1$ext native2ascii.1$ext \
  %{_mandir}/man1/native2ascii-%{name}.1$ext \
  --slave %{_mandir}/man1/policytool.1$ext policytool.1$ext \
  %{_mandir}/man1/policytool-%{name}.1$ext \
  --slave %{_mandir}/man1/rmic.1$ext rmic.1$ext \
  %{_mandir}/man1/rmic-%{name}.1$ext \
  --slave %{_mandir}/man1/schemagen.1$ext schemagen.1$ext \
  %{_mandir}/man1/schemagen-%{name}.1$ext \
  --slave %{_mandir}/man1/serialver.1$ext serialver.1$ext \
  %{_mandir}/man1/serialver-%{name}.1$ext \
  --slave %{_mandir}/man1/wsgen.1$ext wsgen.1$ext \
  %{_mandir}/man1/wsgen-%{name}.1$ext \
  --slave %{_mandir}/man1/wsimport.1$ext wsimport.1$ext \
  %{_mandir}/man1/wsimport-%{name}.1$ext \
  --slave %{_mandir}/man1/xjc.1$ext xjc.1$ext \
  %{_mandir}/man1/xjc-%{name}.1$ext

alternatives \
  --install %{_jvmdir}/java-%{origin} \
  java_sdk_%{origin} %{_jvmdir}/%{sdklnk} %{priority} \
  --slave %{_jvmjardir}/java-%{origin} \
  java_sdk_%{origin}_exports %{_jvmjardir}/%{sdklnk}

alternatives \
  --install %{_jvmdir}/java-%{javaver} \
  java_sdk_%{javaver} %{_jvmdir}/%{sdklnk} %{priority} \
  --slave %{_jvmjardir}/java-%{javaver} \
  java_sdk_%{javaver}_exports %{_jvmjardir}/%{sdklnk}

exit 0

%postun devel
if [ $1 -eq 0 ]
then
  alternatives --remove javac %{sdkbindir}/javac
  alternatives --remove java_sdk_%{origin} %{_jvmdir}/%{sdklnk}
  alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdklnk}
fi

exit 0

%post javadoc
alternatives \
  --install %{_javadocdir}/java javadocdir %{_javadocdir}/%{name}/api \
  %{priority}

exit 0

%postun javadoc
if [ $1 -eq 0 ]
then
  alternatives --remove javadocdir %{_javadocdir}/%{name}/api
fi

exit 0


%if %{NO_PLUGIN}
#garbage
%endif

%files -f %{name}.files
%defattr(-,root,root,-)
%doc %{buildoutputdir}/j2sdk-image/jre/ASSEMBLY_EXCEPTION
%doc %{buildoutputdir}/j2sdk-image/jre/LICENSE
%doc %{buildoutputdir}/j2sdk-image/jre/THIRD_PARTY_README
# FIXME: The TRADEMARK file should be in j2sdk-image.
%doc openjdk/TRADEMARK
%doc AUTHORS
%doc COPYING
%doc ChangeLog
%doc NEWS
%doc README
%dir %{_jvmdir}/%{sdkdir}
%{_jvmdir}/%{jrelnk}
%{_jvmjardir}/%{jrelnk}
%{_jvmprivdir}/*
%{jvmjardir}
%dir %{_jvmdir}/%{jredir}/lib/security
%{_jvmdir}/%{jredir}/lib/security/cacerts
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.policy
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.security
%{_datadir}/icons/hicolor/*x*/apps/java.png
%{_mandir}/man1/java-%{name}.1*
%{_mandir}/man1/keytool-%{name}.1*
%{_mandir}/man1/orbd-%{name}.1*
%{_mandir}/man1/pack200-%{name}.1*
%{_mandir}/man1/rmid-%{name}.1*
%{_mandir}/man1/rmiregistry-%{name}.1*
%{_mandir}/man1/servertool-%{name}.1*
%{_mandir}/man1/tnameserv-%{name}.1*
%{_mandir}/man1/unpack200-%{name}.1*
#%{_datadir}/pixmaps/javaws.png
#%{_datadir}/applications/javaws.desktop
%exclude  %{_jvmdir}/%{jredir}/bin/javaws

%files devel
%exclude  %{_jvmdir}/%{sdkdir}/bin/javaws

%defattr(-,root,root,-)
%doc %{buildoutputdir}/j2sdk-image/ASSEMBLY_EXCEPTION
%doc %{buildoutputdir}/j2sdk-image/LICENSE
#%doc %{buildoutputdir}/j2sdk-image/README.html
%doc %{buildoutputdir}/j2sdk-image/THIRD_PARTY_README
# FIXME: The TRADEMARK file should be in j2sdk-image.
%doc openjdk/TRADEMARK
%dir %{_jvmdir}/%{sdkdir}/bin
%dir %{_jvmdir}/%{sdkdir}/include
%dir %{_jvmdir}/%{sdkdir}/lib
%ifarch %{jit_arches}
%dir %{_jvmdir}/%{sdkdir}/tapset
%endif
%{_jvmdir}/%{sdkdir}/bin/*
%{_jvmdir}/%{sdkdir}/include/*
%{_jvmdir}/%{sdkdir}/lib/*
%ifarch %{jit_arches}
%{_jvmdir}/%{sdkdir}/tapset/*.stp
%endif
%{_jvmdir}/%{sdklnk}
%{_jvmjardir}/%{sdklnk}
%{_datadir}/applications/*jconsole.desktop
%{_datadir}/applications/*policytool.desktop
%{_mandir}/man1/appletviewer-%{name}.1*
%{_mandir}/man1/apt-%{name}.1*
%{_mandir}/man1/extcheck-%{name}.1*
%{_mandir}/man1/idlj-%{name}.1*
%{_mandir}/man1/jar-%{name}.1*
%{_mandir}/man1/jarsigner-%{name}.1*
%{_mandir}/man1/javac-%{name}.1*
%{_mandir}/man1/javadoc-%{name}.1*
%{_mandir}/man1/javah-%{name}.1*
%{_mandir}/man1/javap-%{name}.1*
%{_mandir}/man1/jconsole-%{name}.1*
%{_mandir}/man1/jdb-%{name}.1*
%{_mandir}/man1/jhat-%{name}.1*
%{_mandir}/man1/jinfo-%{name}.1*
%{_mandir}/man1/jmap-%{name}.1*
%{_mandir}/man1/jps-%{name}.1*
%{_mandir}/man1/jrunscript-%{name}.1*
%{_mandir}/man1/jsadebugd-%{name}.1*
%{_mandir}/man1/jstack-%{name}.1*
%{_mandir}/man1/jstat-%{name}.1*
%{_mandir}/man1/jstatd-%{name}.1*
%{_mandir}/man1/native2ascii-%{name}.1*
%{_mandir}/man1/policytool-%{name}.1*
%{_mandir}/man1/rmic-%{name}.1*
%{_mandir}/man1/schemagen-%{name}.1*
%{_mandir}/man1/serialver-%{name}.1*
%{_mandir}/man1/wsgen-%{name}.1*
%{_mandir}/man1/wsimport-%{name}.1*
%{_mandir}/man1/xjc-%{name}.1*
%ifarch %{jit_arches}
%{tapsetdir}/*.stp
%endif

%files demo -f %{name}-demo.files
%defattr(-,root,root,-)

%files src
%defattr(-,root,root,-)
%doc README.src
%{_jvmdir}/%{sdkdir}/src.zip
%if %{runtests}
# FIXME: put these in a separate testresults subpackage.
%doc mauve_tests
%doc mauve-%{mauvedate}/mauve_output
%doc test/jtreg-summary.log
%endif

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}

#%files plugin
#%defattr(-,root,root,-)
#%{_jvmdir}/%{jredir}/lib/%{archinstall}/IcedTeaNPPlugin.so

%changelog
* Mon Nov 1 2010 Jiri Vanek <jvanek@redhat.com> - 1.6.0.0-1.31.b17
- excluded bin/javaws files
		exclude  %{_jvmdir}/%{jredir}/bin/javaws
		files devel
		exclude  %{_jvmdir}/%{sdkdir}/bin/javaws

- garbage removed to separated file
- Resolves: rhbz#639954

* Wed Oct 27 2010 Jiri Vanek <jvanek@redhat.com> - 1.6.0.0-1.30.b17
- javaws again removed, sorry for confusion (QA!-)
- Resolves: rhbz#639954


* Wed Oct 27 2010 Jiri Vanek <jvanek@redhat.com> - 1.6.0.0-1.28.b17
- removed garbage from plugin postun
- again added javaws
- Resolves: rhbz#639954


* Mon Oct 20 2010 Jiri Vanek <jvanek@redhat.com> - 1.6.0.0-1.27.b17
- obsoleting plugin, aded versioning
- Resolves: rhbz#639954

* Mon Oct 20 2010 Jiri Vanek <jvanek@redhat.com> - 1.6.0.0-1.26.b17
- obsoleting plugin
- Resolves: rhbz#639954

* Fri Oct 15 2010 Jiri Vanek <jvanek@redhat.com> - 1.6.0.0-1.25.b17
-  obsoleting plugin


* Thu Oct 14 2010 Deepak Bhole <dbhole@redhat.com> - 1.6.0.0-1.24.b17
- Resolves: bz643095
- Disable Web Plugin and Webstart

* Tue Oct 12 2010 Deepak Bhole <dbhole@redhat.com> - 1.6.0.0-1.23.b17
- Updated 1.7.5 tarball (contains additional security fixes)
- Resolves: bz639954

* Tue Oct 05 2010 Deepak Bhole <dbhole@redhat.com> - 1.6.0.0-1.22.b17
- Update to IcedTea 1.7.5
- Import debuginfo patch from el5
- Parallelize build
- Removed systemtap probepoint patch (now upstream)
- Resolves: bz#639954

* Tue Jul 27 2010 Deepak Bhole <dbhole@redhat.com> - 1.6.0.0-1.21.b17
- Updated to IcedTea 1.7.4
- Resolves: rhbz#537121
- Resolves: rhbz#612467
- Resolves: rhbz#613824
- Additionally, fixed rh bugs 616893 and 616895

* Tue May 25 2010 Martin Matejovic <mmatejov@redhat.com> - 1.6.0.0-1.20.b17
- Fixed brew build for i686
- Removed Files:
    java-1.6.0-openjdk-securitypatches-20091103.patch
    java-1.6.0-openjdk-securitypatches-20100323.patch
    java-1.6.0-openjdk-sparc-fixes.patch
    java-1.6.0-openjdk-sparc-hotspot.patch
	

* Mon May 24 2010 Martin Matejovic <mmatejov@redhat.com> - 1.6.0.0-1.19.b17
- Added icedtea6-1.7.3
- Added openjdk b17
- Enabled NPPlugin
- Removed Files:
    java-1.6.0-openjdk-icedtea-gcc-stack-markings.patch
    java-1.6.0-openjdk-jar-misc.patch
    java-1.6.0-openjdk-linux-separate-debuginfo.patch
    java-1.6.0-openjdk-memory-barriers.patch
    java-1.6.0-openjdk-rhino-rewrite.patch
    java-1.6.0-openjdk-s390-optimizer-failure.patch
    java-1.6.0-openjdk-s390-serializer.patch
    java-1.6.0-openjdk-systemtap-fixes-jni-jstack.patch
    java-1.6.0-openjdk-x11.patch
- Resolves: rhbz#593135
- Resolves: rhbz#572675


* Tue Mar 30 2010 Deepak Bhole <dbhole@redhat.com> 1.6.0.0-1.18.b16
- Build only on x86 and x86_64
- Added STRIP_KEEP_SYMTAB=libjvm* to install section, fix bz530402
- Added java-1.6.0-openjdk-jar-misc.patch
- Added java-1.6.0-openjdk-linux-separate-debuginfo.patch to separate debuginfo
- Added patch for March 2010 security issues (java-1.6.0-openjdk-securitypatches-20100323.patch)

* Mon Mar 13 2010 Deepak Bhole <dbhole@redhat.com> 1.6.0.0-1.17.b16
- Added missing autoconf and automake BRs

* Thu Mar 11 2010 Deepak Bhole <dbhole@redhat.com> 1.6.0.0-1.16.b16
- Added a memory barrier patch that prevents wake up losses and hangs

* Mon Feb 22 2010 Deepak Bhole <dbhole@redhat.com> - 1:1.6.0.0-1.15.b16
- Imported rhino related patches from mainline to fix icedtea bz#179

* Thu Jan 28 2010 Deepak Bhole <dbhole@redhat.com> - 1:1.6.0.0-1.14.b16
- Fixed license field

* Wed Jan 20 2010 Deepak Bhole <dbhole@redhat.com> - 1:1.6.0.0-1.13.b16
- Build in non-bootstrap
- Run tests during build

* Wed Jan 20 2010 Deepak Bhole <dbhole@redhat.com> - 1:1.6.0.0-1.12.b16
- Re-enable s390

* Thu Jan 14 2010 Deepak Bhole <dbhole@redhat.com> - 1:1.6.0.0-1.11.b16
- Build with ecj
- Resolves: rhbz#553446
- Exclude s390 build
- Added optimizer patch from Gary Benson to prevent s390x build failure
- Remove pre-applied zero native sacope patch
    From Mark Wielaard <mjw@redhat.com>:
    - Backport systemtap fixes, jni support and jstack from IcedTea6 1.7
    - Backport icedtea-gcc-stack-markings patch from IcedTea6 1.7

* Thu Jan 14 2010 Deepak Bhole <dbhole@redhat.com> - 1:1.6.0.0-1.10.b16
- Merge from alpha branch and F12

* Thu Nov 12 2009 Martin Matejovic <mmatejov@redhat.com> - 1:1.6.0-33.b16
- Updated release
- Fixed applying patches

* Mon Nov 09 2009 Martin Matejovic <mmatejov@redhat.com> - 1:1.6.0-32.b16
- Added java-1.6.0-openjdk-securitypatches-20091103.patch
- Removed BuildRequirement: openmotif-devel, lesstif-devel
- Resolves: rhbz#510197
- Resolves: rhbz#530053
- Resolves: rhbz#530057
- Resolves: rhbz#530061
- Resolves: rhbz#530062
- Resolves: rhbz#530063
- Resolves: rhbz#530067
- Resolves: rhbz#530098
- Resolves: rhbz#530173
- Resolves: rhbz#530175
- Resolves: rhbz#530296
- Resolves: rhbz#530297
- Resolves: rhbz#530300

* Thu Sep  9 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-31.b16
- Added java-1.6.0-openjdk-netbeans.patch.
- Reenabled visualvm.

* Thu Sep  9 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-30.b16
- Temporarily removed building of visualvm.

* Thu Sep  9 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-30.b16
- Removed unneeded patches.
- Updated icedteaver to 1.6
- Resolves: rhbz#484858
- Resolves: rhbz#497408
- Resolves: rhbz#489414

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 1:1.6.0-29.b16
- Use bzipped java-access-bridge tarball.

* Tue Aug  4 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-28.b16
- Updated java-1.6.0-openjdk-netx.patch, and renamed to
java-1.6.0-openjdk-netxandplugin.patch.
- Added java-1.6.0-openjdk-securitypatches.patch.
- Resolves: rhbz#512101
- Resolves: rhbz#512896
- Resolves: rhbz#512914
- Resolves: rhbz#512907
- Resolves: rhbz#512921
- Resolves: rhbz#511915
- Resolves: rhbz#512915
- Resolves: rhbz#512920
- Resolves: rhbz#512714
- Resolves: rhbz#513215
- Resolves: rhbz#513220
- Resolves: rhbz#513222
- Resolves: rhbz#513223
- Resolves: rhbz#503794

* Thu Jul 30 2009 Lillian Angel  <langel@redhat.com> - 1:1.6.0-27.b16
- java-1.6.0-openjdk-x11.patch updated.

* Wed Jul 29 2009 Lillian Angel  <langel@redhat.com> - 1:1.6.0-27.b16
- Renamed java-1.6.0-openjdk-libx11.patch to java-1.6.0-openjdk-x11.patch 
and updated.

* Wed Jul 29 2009 Lillian Angel  <langel@redhat.com> - 1:1.6.0-26.b16
- Added java-1.6.0-openjdk-libx11.patch.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.0.0-25.b16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-24.b16
- Added java-1.6.0-openjdk-execvpe.patch.

* Thu Jul  9 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-24.b16
- Added java-1.6.0-openjdk-netx.patch
- Moved policytool to devel package.
- Updated release.
- Resolves: rhbz#507870
- Resolves: rhbz#471346

* Fri May 29 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-23.b16
- Fixed abs-install-dir.
- Updated release.

* Fri May 29 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-22.b16
- Set icedteasnapshot to nil.
- Updated release.

* Wed May 21 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-21.b16
- Disable building systemtap on non-jit arches.

* Tue May 19 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-21.b16
- Set icedteasnapshot. Only release candidate.

* Tue May 19 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-21.b16
- Removed java-1.6.0-openjdk-lcms.patch java-1.6.0-openjdk-securitypatches.patch 
java-1.6.0-openjdk-pulsejava.patch.
- Updated visualvm source.
- Updated sparc patches.
- Updated release.
- Updated icedteaver.
- Updated openjdkver.
- Updated openjdkdate.
- Adjusted buildoutputdir.
- Set runtests to 0. Hanging test causing problems.
- Include systemtap support, install hotspot tapset.
- Resolves: rhbz#479041 
- Resolves: rhbz#480075 
- Resolves: rhbz#483095 
- Resolves: rhbz#487872 
- Resolves: rhbz#467591 
- Resolves: rhbz#487452 
- Resolves: rhbz#498109 
- Resolves: rhbz#497191 
- Resolves: rhbz#462876 
- Resolves: rhbz#489586
- Resolves: rhbz#501391

* Wed May 6 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-20.b14
- Added devel requirement for netbeans-platform

* Mon Apr 27 2009 Christopher Aillon <caillon@redhat.com> - 1:1.6.0.0-20.b14
- Rebuild against newer gecko

* Mon Apr  6 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-19.b14
- Updated java-1.6.0-openjdk-lcms.patch

* Thu Apr  2 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-18.b14
- Added java-1.6.0-openjdk-pulsejava.patch.
- Updated release.
- Updated java-1.6.0-openjdk-lcms.patch.
- Resolves: rhbz#492367
- Resolves: rhbz#493276

* Tue Mar 24 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-17.b14
- Updated java-1.6.0-openjdk-lcms.patch.

* Tue Mar 24 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-16.b14
- Added java-1.6.0-openjdk-securitypatches.patch.
- Updated release.

* Fri Mar 20 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-15.b14
- Added java-1.6.0-openjdk-lcms.patch.

* Mon Mar 9 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-14.b14
- Updated sources. 
- Resolves: rhbz#489029

* Mon Mar  2 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-14.b14
- Reverting last change.

* Mon Mar  2 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-14.b14
- Fixed archinstall i386 to i586, since Fedora 11 made the switch.

* Wed Feb 25 2009 Dennis Gilmore <dennis@ausil.us> - 1:1.6.0-13.b14
- fix sparc arch building asm-sparc has gone. we only have asm/ now
- add sparc arches back to the jit arch list

* Wed Feb 25 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-12.b14
- Updated release.
- Updated icedteaver.
- Re-enabled visualvm building.
- Installed jvisualvm appropriately.
- Resolves: rhbz#480487
- Resolves: rhbz#482943  

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.0.0-11.b14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-10.b14
- Updated sources.

* Fri Jan 23 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-10.b14
- Added accessibility patch.

* Thu Jan 22 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-10.b14
- Updated to icedtea-1.4 snapshot.
- Updated release.
- Removed netbeans and visualvm.
- Resolves: rhbz#472953
- Resolves: rhbz#475081 
- Resolves: rhbz#452573
- Resolves: rhbz#477351
- Resolves: rhbz#475109
- Resolves: rhbz#476462

* Sun Jan 11 2009 Lillian Angel <langel@redhat.com> - 1:1.6.0-9.b14
- Removed README.plugin, updated source list.
- Updated release.

* Fri Dec  5 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-8.b14
- Added hotspot source.
- Added --with-hotspot-src-zip build option.
- Set runtests to 1.
- Updated jtreg log.
- Added new patch to add GNOME to java.security.
- Updated icedteasnapshot.
- Updated openjdkver.
- Updated openjdkdate.
- Resolves: rhbz#474431
- Resolves: rhbz#474503
- Resolves: rhbz#472862

* Tue Dec  2 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-7.b13
- Set runtests to 0.

* Tue Dec  2 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-7.b13
- Updated pkgversion to include release and arch.
- Set runtests to 1.
- Updated icedteasnapshot.
- Resolves: rhbz#468484
- Resolves: rhbz#472862
- Resolves: rhbz#472234
- Resolves: rhbz#472233
- Resolves: rhbz#472231
- Resolves: rhbz#472228
- Resolves: rhbz#472224
- Resolves: rhbz#472218
- Resolves: rhbz#472213
- Resolves: rhbz#472212
- Resolves: rhbz#472211
- Resolves: rhbz#472209
- Resolves: rhbz#472208
- Resolves: rhbz#472206
- Resolves: rhbz#472201

* Mon Nov 24 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-6.b13
- Updated icedteasnapshot.
- Updated openjdkver to b13.
- Updated openjdkdate.
- Resolves: rhbz#471987
- Resolves: rhbz#465531
- Resolves: rhbz#470551

* Thu Nov 20 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-6.b12
- Redirect error from removing gcjwebplugin link.
- Resolves: rhbz#471568

* Thu Nov 13 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-5.b12
- Added java-fonts to Provides for base package.
- Resolves: rhbz#469893

* Wed Nov 12 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-4.b12
- Fixed pulse audio build requirements.
- Updated release.
- Resolves: rhbz#471229

* Fri Nov  7 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-3.b12
- Updated icedteasnapshot.
- Resolves: rhbz#453290
- Resolves: rhbz#469361 

* Wed Nov  5 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-3.b12
- Re-enabled pulse java. Fix committed upstream to prevent TCK failures.
- Updated release.
- Updated icedteasnapshot.
- Updated icedteaver.
- Updated visualvm source.

* Thu Oct 30 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-2.b12
- Fixed post plugin scriptlet to work for install, as well as upgrade.

* Wed Oct 29 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-2.b12
- Fixed release string.

* Mon Oct 27 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-2b12
- Updated icedteasnapshot.
- Fixed post scriptlet to remove gcjwebplugin.so.
- Updated jvisualvm requirement.
- Added build option --with-pkgversion=6b12-Fedora-10
- Resolves: rhbz#428503
- Resolves: rhbz#251829
- Resolves: rhbz#415061
- Resolves: rhbz#452188

* Mon Oct 27 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-1.2.b12
- Added netbeans requirement for devel package.
- Fixed removal of gcjwebplugin.so link when installing plugin package.
- Updated Release.
- Resolves: rhbz#468635

* Fri Oct 24 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-1.1.b12
- Removed --enable-pulse-java. Causes some TCK tests to fail.

* Fri Oct 24 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-1.1.b12
- Updated sources to include latest liveconnect fixes.

* Wed Oct 22 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-1.0.b12
- Removed option to build with alternate jar.

* Tue Oct 21 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-1.0.b12
- Updated icedteaver.
- Updated Release.
- Changed to use IcedTeaNPPlugin.so instead of gcjwebplugin.so. Includes 
LiveConnect support.
- Updated mauvedate.
- Added xulrunner-devel and xulrunner-devel-unstable as build requirements.
- Enabled building of pulse-java, not default sound implementation though.
- Added build requirements for pulse-java.
- Resolves: rhbz#468043 
- Resolves: rhbz#375161 
- Resolves: rhbz#432184 
- Resolves: rhbz#302071 
- Resolves: rhbz#457536 
- Resolves: rhbz#460236 
- Resolves: rhbz#460084
- Resolves: rhbz#467794

* Tue Oct 14 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-0.23.b12
- Updated icedteasnapshot to nil.
- Updated release.
- Added jakarta-commons-logging requirement for visualvm.

* Thu Oct  2 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-0.22.b12
- Enabled building of jvisualvm tool.

* Wed Sep 24 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-0.21.b12
- Removed all instances of security jars.

* Wed Sep 24 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-0.21.b12
- Updated icedteasnapshot.
- Updated release.
- Updated openjdkver.
- Updated openjdkdate.

* Mon Sep 22 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-0.20.b11
- Removed update-desktop-database dependency.
- Resolves: rhbz#463046

* Mon Sep 08 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-0.20.b11
- Added rhino requirement.
- Resolves: rhbz#461336

* Tue Aug 05 2008 Lillian Angel <langel@redhat.com> 1:1.6.0-0.20.b11
- Updated icedteasnapshot.

* Thu Jul 31 2008 Lillian Angel <langel@redhat.com> 1:1.6.0-0.20.b11
- Added java-access-bridge idlj patch. Temp workaround for bug similar to:
http://bugs.sun.com/bugdatabase/view_bug.do?bug_id=6708395. 

* Mon Jul 28 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0-0.20.b11
- Removed freetype patch.

* Wed Jul 23 2008 Lubomir Rintel <lkundrak@v3.sk> - 1:1.6.0-0.20.b11
- Specify vendor for javaws desktop entry.
- Merge EPEL-5 and Fedora devel packages.

* Mon Jul 21 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.19.b11
- Updated icedteasnapshot.

* Wed Jul 16 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.18.b10
- Updated icedteasnapshot.
- Updated openjdkver.
- Updated openjdkdate.
- Updated generate-fedora-zip.sh

* Tue Jul 15 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.18.b10
- Updated accessver to 1.23.

* Tue Jul 15 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.18.b10
- Added rhino as a BuildRequirement.

* Tue Jul 15 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.18.b10
- Removed all unneeded patches. Security patches are included in the 
new icedtea source.

* Tue Jul 15 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.18.b10
- Fixed fedorazip.

* Tue Jul 15 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.18.b10
- Updated icedteaver.
- Updated icedteasnapshot.
- Updated openjdkdate.
- Updated openjdkver.
- Updated release.
- Resolves: rhbz#452525
- Resolves: rhbz#369861 

* Thu Jul  9 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.17.b09
- Added sparc/64 patches.

* Wed Jul  8 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.17.b09
- Only apply hotspot security patch of jitarches.

* Wed Jul  2 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.17.b09
- Added OpenJDK security patches.

* Tue Jun  3 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 1:1.6.0.0-0.16.b09
- Add runtests define.
- Provide Xvfb instance to jtreg.
- Run test suites on JIT architectures only.
- Clean up arch handling.

* Fri May 30 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 1:1.6.0.0-0.15.b09
- Remove jhat patch.

* Fri May 30 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 1:1.6.0.0-0.15.b09
- Remove makefile patch.
- Update generate-fedora-zip.sh.

* Fri May 30 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 1:1.6.0.0-0.15.b09
- Formatting cleanups.

* Fri May 30 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 1:1.6.0.0-0.15.b09
- Group all Mauve commands.

* Fri May 30 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 1:1.6.0.0-0.15.b09
- Formatting cleanups.
- Add jtreg_output to src subpackage.

* Wed May 28 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.15.b09
- Updated icedteasnapshot for new release.

* Tue May 27 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 1:1.6.0.0-0.15.b09
- Require ca-certificates.
- Symlink to ca-certificates cacerts.
- Remove cacerts from files list.
- Resolves: rhbz#444260

* Mon May 26 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.14.b09
- Added eclipse-ecj build requirement for mauve.
- Updated icedteasnapshot.

* Fri May 23 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.14.b09
- Fixed jtreg testing.

* Fri May 23 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.14.b09
- Updated icedteasnapshot.
- Updated release.
- Added jtreg testing.

* Thu May 22 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.13.b09
- Added new patch java-1.6.0-openjdk-java-access-bridge-tck.patch.
- Updated release.

* Mon May 05 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.12.b09
- Updated release.
- Updated icedteasnapshot.
- Resolves: rhbz#445182
- Resolves: rhbz#445183

* Tue Apr 29 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.11.b09
- Fixed javaws.desktop installation.

* Tue Apr 29 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.11.b09
- Updated icedteasnapshot.
- Removed java-1.6.0-openjdk-jconsole.desktop and
  java-1.6.0-openjdk-policytool.desktop files.

* Tue Apr 29 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.11.b09
- Updated release.
- Added archbuild and archinstall definitions for ia64.
- Resolves: rhbz#433843

* Mon Apr 28 2008 Lubomir Rintel <lkundrak@v3.sk> - 1:1.6.0.0-0.12.b08
- Merge changes made to build on Red Hat Enterprise Linux 5, to include in EPEL:
- Require Freetype 2.2.0 instead of 2.3.0.
- Build against openmotif instead of lesstif when not on Fedora.

* Mon Apr 28 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.10.b09
- Fixed installation of javaws.desktop and javaws.png.

* Mon Apr 28 2008 Joshua Sumali <jsumali@redhat.com> - 1:1.6.0.0-0.10.b09
- Added javaws menu entry.
- Resolves: rhbz#443851

* Mon Apr 28 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.10.b09
- Updated release.
- Updated icedteasnapshot.
- Added jconsole and policy menu entries.
- Removed all jhat references.
- Resolves: rhbz#435235
- Resolves: rhbz#417501
- Resolves: rhbz#437418
- Resolves: rhbz#443360
- Resolves: rhbz#304031

* Thu Apr 18 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.9.b09
- Updated icedteaver.
- Updated icedteasnapshot.
- Updated openjdkver.
- Updated openjdkdate.
- Updated release.
- Resolves: rhbz#442602
- Resolves: rhbz#442514
- Resolves: rhbz#441437
- Resolves: rhbz#375541

* Thu Apr 17 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.9.b08
- Added javaws to /usr/bin.
- Resolves: rhbz#437929

* Mon Apr 08 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.8.b08
- Updated sources.
- Updated icedteaver.

* Mon Apr 07 2008 Dennis Gilmore <dennis@ausil.us> - 1:1.6.0.0-0.8.b08
- Enable building for all arches using zero where there is not a native port.

* Mon Mar 31 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.7.b08
- Updated icedteasnapshot. Includes sources needed to build xmlgraphics-commons.
- Updated release.
- Resolves: rhbz#439676

* Fri Mar 28 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.6.b08
- Updated icedteasnapshot to fix ppc failure.

* Thu Mar 27 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.6.b08
- Removed iconv of THIRD_PARTY_README.

* Thu Mar 27 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.6.b08
- Updated icedteasnapshot.
- Updated openjdkver and openjdkdate.
- Removed java-1.6.0-openjdk-trademark.patch.
- Updated generate-fedora-zip.sh.
- Resolves: rhbz#438421

* Thu Mar 20 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.5.b06
- Updated icedteasnapshot.
- Updated java-1.6.0-openjdk-optflags.patch.

* Mon Mar 17 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.5.b06
- Updated icedteasnapshot.
- Updated Release.
- Added new patch: java-1.6.0-openjdk-optflags.patch.
- Resolves: rhbz#437331

* Mon Mar 17 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.5.b06
- Added version for freetype-devel requirement.
- Resolves: rhbz#437782

* Fri Mar 14 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.4.b06
- Fixed Provides and Obsoletes for all sub-packages. Should have specified
  java-1.7.0-icedtea < 1.7.0.0-0.999 instead of 1.7.0-0.999.
- Resolves: rhbz#437492

* Wed Mar 12 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 1:1.6.0.0-0.4.b06
- Add FIXME about versionless SONAMEs.

* Wed Mar 12 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.3.b06
- Updated release.
- Updated mauvedate to 2008-03-11.
- Updated accessmajorver to 1.22.
- Updated accessminorver to 0.

* Tue Mar 11 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.2.b06
- Updated snapshot.
- Changed icedteaopt to use --with-openjdk instead of --with-icedtea.

* Tue Mar 11 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.2.b06
- Added Provides and Obsoletes for all subpackages. All sub-packages
  replaces java-1.7.0-icedtea.
- Updated Release.
- Changed BuildRequires from java-1.7.0-icedtea to java-1.6.0-openjdk.
- Added TRADEMARK file to docs.

* Tue Mar 11 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.2.b06
- Added Provides and Obsoletes. This package replaces java-1.7.0-icedtea.

* Fri Feb 15 2008 Lillian Angel <langel@redhat.com> - 1:1.6.0.0-0.1.b06
- Adapted for java-1.6.0-openjdk.

* Wed Feb 13 2008 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.25.b24
- Added libffi requirement for ppc/64.

* Wed Feb 13 2008 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.25.b24
- Updated icedteaver to 1.6.
- Updated release.

* Mon Feb 11 2008 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.24.b24
- Added libjpeg-6b as a requirement.
- Resolves rhbz#432181

* Mon Jan 28 2008 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.24.b24
- Kill Xvfb after it completes mauve tests.

* Mon Jan 21 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.24.b24
- Remove cgibindir macro.
- Remove icedtearelease.
- Remove binfmt_misc support.
- Remove .snapshot from changelog lines wider than 80 columns.

* Tue Jan 08 2008 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.23.b24.snapshot
- Added xorg-x11-fonts-misc as a build requirement for Mauve.
- Updated mauve_tests.

* Mon Jan 07 2008 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.23.b24.snapshot
- Updated Mauve's build requirements.
- Excluding Mauve tests that try to access the network.
- Added Xvfb functionality to mauve tests to avoid display-related failures.
- Resolves rhbz#427614

* Thu Jan 03 2008 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.23.b24.snapshot
- Added mercurial as a Build Requirement.
- Fixed archbuild/archinstall if-block.

* Thu Jan 03 2008 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.23.b24.snapshot
- Removed BuildRequirement firefox-devel.
- Added BuildRequirement gecko-devel.
- Resolves rhbz#427350

* Fri Dec 28 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.23.b24.snapshot
- Updated icedtea source.
- Resolves rhbz#426142

* Thu Dec 13 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.23.b24.snapshot
- Updated icedteaver.
- Updated Release.
- Updated buildoutputdir.
- Removed openjdkdate.
- Updated openjdkver.
- Updated openjdkzip and fedorazip.
- Added Requires: jpackage-utils.
- Removed java-1.7.0-makefile.patch.
- Updated patch list.
- Resolves rhbz#411941
- Resolves rhbz#399221
- Resolves rhbz#318621

* Thu Dec  6 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.22.b23
- Clear bootstrap mode on ppc and ppc64.

* Wed Dec  5 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.21.b23
- Update icedteasnapshot.

* Fri Nov 30 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.21.b23
- Update icedteasnapshot.
- Remove ExclusiveArch.
- Assume i386.
- Add support for ppc and ppc64.
- Bootstrap on ppc and ppc64.

* Thu Nov 15 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.20.b23
- Add giflib-devel build requirement.

* Thu Nov 15 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.20.b23
- Add libjpeg-devel and libpng-devel build requirements.

* Thu Nov 15 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.20.b23.snapshot
- Added gcjbootstrap.
- Updated openjdkver and openjdkdate to new b23 release.
- Updated Release.
- Added gcjbootstrap checks in.
- Resolves: rhbz#333721

* Mon Oct 15 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.19.b21.snapshot
- Updated release.

* Fri Oct 12 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.18.b21.snapshot
- Updated release.

* Fri Oct 12 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.17.b21.snapshot
- Added jhat patch back in.

* Thu Oct 11 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.17.b21.snapshot
- Update icedtearelease.
- Update icedteasnapshot.
- Update openjdkver.
- Update openjdkdate.
- Updated genurl.
- Removed unneeded patches.
- Removed gcjbootstrap.
- Removed icedteaopt.
- Removed all gcj related checks.
- Resolves: rhbz#317041
- Resolves: rhbz#314211
- Resolves: rhbz#314141
- Resolves: rhbz#301691

* Mon Oct 1 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.16.b19.snapshot
- Listed mauve_output as a doc file instead of a source.
- Added mauve_tests to the src files as doc.

* Fri Sep 28 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.16.b19.snapshot
- Fixed testing. Output is stored in a file and passes/debug info is not shown.

* Thu Sep 27 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.16.b19
- Apply patch to use system tzdata.
- Require tzdata-java.
- Fix mauve shell fragment.

* Thu Sep 27 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.15.b19.snapshot
- Removed jtreg setup line.

* Wed Sep 26 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.15.b19.snapshot
- Removed jtreg.  Does not adhere to Fedora guidelines.

* Tue Sep 25 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.15.b19.snapshot
- Fixed running of Xvfb so it does not terminate after a successful
  test.
- Fixed mauve and jtreg test runs to not break the build when an error
  is thrown

* Mon Sep 24 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.15.b19.snapshot
- Added JTreg zip as source.
- Run JTreg tests after build for smoke testing.
- Added Xvfb as build requirement.

* Wed Sep 12 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.15.b19.snapshot
- Added Mauve tarball as source.
- Added mauve_tests as source.
- Run Mauve after build for regression testing.

* Thu Sep  7 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.15.b18
- Do not require openssl for build.
- Require openssl.
- Set gcjbootstrap to 0.
- Remove generate-cacerts.pl.
- Update icedtearelease.
- Update icedteasnapshot.
- Update openjdkver.
- Update openjdkdate.

* Wed Sep  5 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.15.b18
- Rename javadoc master alternative javadocdir.
- Resolves: rhbz#269901

* Wed Sep  5 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.15.b18
- Remove epoch in plugin provides.
- Bump release number.
- Resolves: rhbz#274001

* Mon Aug 27 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.14.b18
- Include idlj man page in files list.

* Mon Aug 27 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.14.b18
- Add documentation for plugin and src subpackages.
- Fix plugin alternative on x86_64.
- Add java-1.7.0-icedtea-win32.patch.
- Rename modzip.sh generate-fedora-zip.sh.
- Keep patches in main directory.
- Namespace patches.
- Add java-1.7.0-icedtea-win32.patch, README.plugin and README.src.
- Bump release number.

* Mon Aug 27 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.13.b18.snapshot
- Added line to run modzip.sh to remove specific files from the openjdk zip.
- Defined new openjdk zip created by modzip.sh as newopenjdkzip.
- Added line to patch the IcedTea Makefile. No need to download openjdk zip.
- Updated genurl.
- Updated icedteasnapshot.

* Fri Aug 24 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.13.b18
- Remove RMI CGI script and subpackage.
- Fix Java Access Bridge for GNOME URL.

* Thu Aug 23 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.12.b18
- Fully qualify Java Access Bridge for GNOME and generate-cacerts
  source paths.
- Fix plugin post alternatives invocation.
- Include IcedTea documentation.
- Update icedteasnapshot.

* Tue Aug 21 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.11.b18
- Revert change to configure macro.

* Mon Aug 20 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.11.b18
- Fix rpmlint errors.

* Mon Aug 20 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.11.b18
- Add missing development alternatives.
- Bump accessver to 1.19.2.
- Bump icedteaver.
- Set icedteasnapshot.
- Define icedtearelease.
- Bump openjdkver.
- Bump openjdkdate.
- Bump release number.
- Add plugin build requirements and subpackage.

* Tue Jul 31 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.10.b16.1.2
- Bump icedteaver.
- Updated icedteasnapshot.
- Updated release to include icedteaver.

* Wed Jul 25 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.9.b16
- Updated icedteasnapshot.
- Bump openjdkver.
- Bump openjdkdate.
- Bump release number.

* Wed Jul 18 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.8.b15
- Only build rmi subpackage on non-x86_64 architectures.

* Wed Jul 18 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.8.b15
- Bump icedteaver.
- Update icedteasnapshot.

* Fri Jul 13 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.8.b15
- Add rmi subpackage.
- Remove name-version javadoc directory.

* Fri Jul 13 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.8.b15
- Set man extension to .gz in base and devel post sections.

* Thu Jul 12 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.7.b15
- Clear icedteasnapshot.
- Bump release number.

* Wed Jul 11 2007 Lillian Angel <langel@redhat.com> - 1.7.0.0-0.6.b15
- Updated icedteasnapshot.
- Bump openjdkver.
- Bump openjdkdate.
- Bump release number.

* Thu Jul  5 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.5.b14
- Define icedteasnapshot.

* Wed Jul  4 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.4.b14
- Prevent jar repacking.

* Wed Jul  4 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.4.b14
- Include generate-cacerts.pl.
- Generate and install cacerts file.

* Tue Jul  3 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.4.b14
- Add javadoc subpackage.
- Add Java Access Bridge for GNOME.
- Add support for executable JAR files.
- Bump alternatives priority to 17000.

* Thu Jun 28 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.4.b14
- Add support for executable jar files.
- Bump icedteaver.
- Bump openjdkver.
- Bump openjdkdate.
- Bump release number.

* Tue Jun 19 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.3.b13
- Import IcedTea 1.1.
- Bump icedteaver.
- Bump openjdkver.
- Bump openjdkdate.
- Bump release number.
- Use --with-openjdk-src-zip.

* Tue Jun 12 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.7.0.0-0.2.b12
- Initial build.
