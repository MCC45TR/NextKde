%global commit 2ca59a1fbe7cd8c4b9c0b9fd960edca6788425c5
%global private_dir %{_libexecdir}/nextkde/listenfree
%global __provides_exclude_from ^%{private_dir}/.*\\.so.*$
%global __requires_exclude ^lib(qmmp|qmmpui|tag)\\.so.*$

Name:           nextkde-listenfree
Version:        0.3.8
Release:        4%{?dist}
Summary:        ListenFree music player from NextKDE
License:        GPL-3.0-or-later AND AGPL-3.0-or-later AND GPL-2.0-or-later AND LGPL-2.1-or-later AND MIT AND MIT-0 AND BSD-3-Clause AND Apache-2.0 AND BSL-1.0
URL:            https://github.com/NextKde/NextKde
Source0:        https://codeload.github.com/MCC45TR/NextKde/tar.gz/%{commit}#/nextkde-%{commit}.tar.gz
Source1:        https://codeload.github.com/quickjs-ng/quickjs/tar.gz/refs/tags/v0.16.2#/quickjs-0.16.2.tar.gz
Source2:        https://downloads.sourceforge.net/project/qmmp-dev/qmmp/2.4/qmmp-2.4.1.tar.bz2
Source3:        https://codeload.github.com/taglib/taglib/tar.gz/refs/tags/v2.3.1#/taglib-2.3.1.tar.gz
ExclusiveArch:  aarch64

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  utf8cpp-devel
BuildRequires:  ninja-build
BuildRequires:  patch
BuildRequires:  ripgrep
BuildRequires:  pkgconf-pkg-config
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  qt6-qtmultimedia-devel
BuildRequires:  cmake(Qt6ShaderTools)
BuildRequires:  qt6-qtwebengine-devel
BuildRequires:  kf6-kwindowsystem-devel
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  desktop-file-utils
BuildRequires:  dbus-daemon
Requires:       qt6-qtimageformats%{?_isa}
Requires:       qt6-qtsvg%{?_isa}
Requires:       qt6-qt5compat%{?_isa}
Provides:       bundled(qmmp) = 2.4.1
Provides:       bundled(quickjs-ng) = 0.16.2
Provides:       bundled(taglib) = 2.3.1

%description
The upstream NextKDE ListenFree application with its matching patched audio
backend. Private Qmmp, QuickJS-ng and TagLib sources are built natively for
AArch64. Fedora provides Qt, WebEngine, FFmpeg, OpenSSL and other platform
libraries. This package does not change media associations or remove players.

%prep
%autosetup -n NextKde-%{commit}
mkdir -p sdk/vendor
tar -xf %{SOURCE1} -C sdk/vendor
tar -xf %{SOURCE2} -C sdk/vendor
tar -xf %{SOURCE3} -C sdk/vendor
patch_root="$PWD/apps/listenfree/patches/qmmp"
for patch_file in "$patch_root/2.4.1/0001-enable-https-verification.patch" \
    "$patch_root/2.4.1/0003-propagate-http-end-of-stream.patch" "$patch_root"/00{04..20}-*.patch; do
    patch --batch --forward --fuzz=0 -p1 -d sdk/vendor/qmmp-2.4.1 < "$patch_file"
done
sed -i 's|set(_listenfree_install_dir opt/listenfree)|set(_listenfree_install_dir libexec/nextkde/listenfree)|' apps/listenfree/packaging/linux/install.cmake
sed -i 's|@CMAKE_INSTALL_PREFIX@/opt/listenfree|@CMAKE_INSTALL_PREFIX@/libexec/nextkde/listenfree|' apps/listenfree/packaging/linux/listenfree.in

%build
%set_build_flags
sdk="$PWD/sdk"
cmake -S sdk/vendor/quickjs-0.16.2 -B sdk/build/quickjs -GNinja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_PREFIX="$sdk/prefix" \
    -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DBUILD_SHARED_LIBS=OFF -DQJS_BUILD_EXAMPLES=OFF
cmake --build sdk/build/quickjs --parallel %{_smp_build_ncpus}
cmake --install sdk/build/quickjs
cmake -S sdk/vendor/taglib-2.3.1 -B sdk/build/taglib -GNinja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_PREFIX="$sdk/prefix" \
    -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=OFF -DBUILD_BINDINGS=OFF -DBUILD_EXAMPLES=OFF
cmake --build sdk/build/taglib --parallel %{_smp_build_ncpus}
cmake --install sdk/build/taglib
export PKG_CONFIG_PATH="$sdk/prefix/lib/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"
qmmp_options=""
for option in $(rg --no-filename -o 'option\(USE_[A-Z0-9_]+' sdk/vendor/qmmp-2.4.1 -g CMakeLists.txt | sed 's/^option(//' | sort -u); do
    case "$option" in
        USE_FFMPEG|USE_CURL|USE_PULSE|USE_NULL|USE_CROSSFADE) value=ON ;;
        *) value=OFF ;;
    esac
    qmmp_options="$qmmp_options -D$option=$value"
done
test -n "$qmmp_options"
cmake -S sdk/vendor/qmmp-2.4.1 -B sdk/build/qmmp -GNinja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_PREFIX="$sdk/prefix" \
    -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_PREFIX_PATH="$sdk/prefix" \
    -DCMAKE_INSTALL_RPATH='$ORIGIN' $qmmp_options
cmake --build sdk/build/qmmp --parallel %{_smp_build_ncpus}
cmake --install sdk/build/qmmp
cmake -S apps/listenfree -B listenfree-build -GNinja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DKOS_LISTENFREE_SDK="$sdk" -DLISTENFREE_LIVE_FFMPEG_ROOT=%{_prefix} \
    -DLISTENFREE_LIVE_FFMPEG_INCLUDE="$(pkg-config --variable=includedir libavformat)" \
    -DLISTENFREE_BUILD_TESTS=ON
cmake --build listenfree-build --parallel %{_smp_build_ncpus} --target \
    listenfree listenfree-sourcehost listenfree_language_tests \
    listenfree_nextkde_tests listenfree_single_instance_tests

%install
DESTDIR=%{buildroot} cmake --install listenfree-build
find %{buildroot}%{private_dir} -type f -name '*.so*' -exec chmod 0755 {} +

%check
export QT_QPA_PLATFORM=offscreen QT_QUICK_BACKEND=software
sdk="$PWD/sdk"
export LD_LIBRARY_PATH="$sdk/prefix/lib"
export QMMP_PLUGINS="$sdk/prefix/lib/qmmp-2.4"
export LISTENFREE_QMMP_OUTPUT=null
ctest --test-dir listenfree-build --output-on-failure \
    -R '^(listenfree\.language\.|listenfree_nextkde_tests$|listenfree_single_instance_tests$)' \
    --timeout 60
desktop-file-validate %{buildroot}%{_datadir}/applications/listenfree.desktop
test -x %{buildroot}%{private_dir}/listenfree
test -x %{buildroot}%{private_dir}/listenfree-sourcehost
test -f %{buildroot}%{private_dir}/qmmp/Input/libffmpeg.so
test -f %{buildroot}%{private_dir}/qmmp/Transports/libhttp.so
test -f %{buildroot}%{private_dir}/qmmp/Output/libpulseaudio.so
test -z "$(find %{buildroot} -xtype l -print -quit)"
if find %{buildroot} -type f \( -name '*.py' -o -name '*.pyc' \) | read -r unwanted; then
    exit 1
fi

%files
%license LICENSE
%{_bindir}/listenfree
%{private_dir}/
%{_datadir}/applications/listenfree.desktop
%{_datadir}/icons/hicolor/scalable/apps/listenfree.svg

%changelog
* Sun Nov 01 2026 mcc45tr - 0.3.8-4
- Use the FFmpeg include directory declared by Fedora pkg-config metadata

* Sun Nov 01 2026 mcc45tr - 0.3.8-3
- Require the Qt ShaderTools CMake development module

* Sun Nov 01 2026 mcc45tr - 0.3.8-2
- Add TagLib header dependencies and retain normal browser sandbox settings

* Sun Nov 01 2026 mcc45tr - 0.3.8-1
- Package upstream ListenFree and its matching private native audio SDK
