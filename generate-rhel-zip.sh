#!/bin/sh

# Untar openjdk source tarball.
mkdir openjdk
tar xzf $1 -C openjdk

# PRx denotes bug x in the IcedTea bug database (http://icedtea.classpath.org/bugzilla/show_bug.cgi?id=x)
# Sx denotes bug x in the Sun bug database (http://bugs.sun.com/bugdatabase/view_bug.do?bug_id=x)

# PR146/S6713083
# Remove binaries
rm -f \
  openjdk/jdk/test/sun/management/windows/revokeall.exe \
  openjdk/jdk/test/sun/management/jmxremote/bootstrap/linux-i586/launcher \
  openjdk/jdk/test/sun/management/jmxremote/bootstrap/solaris-sparc/launcher \
  openjdk/jdk/test/sun/management/jmxremote/bootstrap/solaris-i586/launcher

rm -f \
  openjdk/jdk/test/java/nio/channels/spi/SelectorProvider/inheritedChannel/lib/linux-i586/libLauncher.so \
  openjdk/jdk/test/java/nio/channels/spi/SelectorProvider/inheritedChannel/lib/solaris-i586/libLauncher.so \
  openjdk/jdk/test/java/nio/channels/spi/SelectorProvider/inheritedChannel/lib/solaris-sparc/libLauncher.so \
  openjdk/jdk/test/java/nio/channels/spi/SelectorProvider/inheritedChannel/lib/solaris-sparcv9/libLauncher.so \
  openjdk/jdk/test/tools/launcher/lib/i386/lib32/lib32/liblibrary.so \
  openjdk/jdk/test/tools/launcher/lib/i386/lib32/liblibrary.so \
  openjdk/jdk/test/tools/launcher/lib/sparc/lib32/lib32/liblibrary.so \
  openjdk/jdk/test/tools/launcher/lib/sparc/lib32/liblibrary.so \
  openjdk/jdk/test/tools/launcher/lib/sparc/lib64/lib64/liblibrary.so \
  openjdk/jdk/test/tools/launcher/lib/sparc/lib64/liblibrary.so

rm -f \
  openjdk/jdk/test/java/util/Locale/data/deflocale.exe \
  openjdk/jdk/test/java/util/Locale/data/deflocale.jds3 \
  openjdk/jdk/test/java/util/Locale/data/deflocale.rhel4 \
  openjdk/jdk/test/java/util/Locale/data/deflocale.sh \
  openjdk/jdk/test/java/util/Locale/data/deflocale.sol10 \
  openjdk/jdk/test/java/util/Locale/data/deflocale.winvista \
  openjdk/jdk/test/java/util/Locale/data/deflocale.winxp \

# Remove test sources with questionable license headers.
rm -f \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4168625Resource3.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4168625Resource3_en_IE.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4165815Test.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4177489_Resource_jf.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4168625Resource3_en_CA.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4168625Getter.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4177489Test.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4168625Resource.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4168625Resource2.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4168625Resource3_en_US.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4083270Test.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4168625Resource3_en.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4177489_Resource.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4168625Test.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4168625Resource2_en_US.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4168625Class.java \
   openjdk/jdk/test/java/util/Locale/Bug4175998Test.java \
   openjdk/jdk/test/java/util/ResourceBundle/RBTestFmwk.java \
   openjdk/jdk/test/java/util/ResourceBundle/TestResource_fr.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4179766Resource.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4179766Getter.java \
   openjdk/jdk/test/java/util/ResourceBundle/Bug4179766Class.java \
   openjdk/jdk/test/java/util/ResourceBundle/TestResource.java \
   openjdk/jdk/test/java/util/ResourceBundle/FakeTestResource.java \
   openjdk/jdk/test/java/util/ResourceBundle/TestResource_de.java \
   openjdk/jdk/test/java/util/ResourceBundle/TestBug4179766.java \
   openjdk/jdk/test/java/util/ResourceBundle/TestResource_fr_CH.java \
   openjdk/jdk/test/java/util/ResourceBundle/ResourceBundleTest.java \
   openjdk/jdk/test/java/util/ResourceBundle/TestResource_it.java \
   openjdk/jdk/test/java/util/Locale/PrintDefaultLocale.java \
   openjdk/jdk/test/java/util/Locale/LocaleTest.java \
   openjdk/jdk/test/java/util/Locale/LocaleTestFmwk.java \
   openjdk/jdk/test/java/util/Locale/Bug4184873Test.java \
   openjdk/jdk/test/sun/text/resources/LocaleDataTest.java

# Remove J2DBench sources, some of which have questionable license
# headers.
rm -rf \
  openjdk/jdk/src/share/demo/java2d/J2DBench


# Create new tarball with new name.
pushd openjdk > /dev/null
  tar czf ../$(basename $1 .tar.gz)-rhel.tar.gz *
popd > /dev/null

# Remove old unzipped openjdk dir.
rm -rf openjdk
