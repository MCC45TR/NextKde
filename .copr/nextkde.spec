%global commit 2ca59a1fbe7cd8c4b9c0b9fd960edca6788425c5
%global kwin_version 6.8.2

Name:           nextkde
Version:        0.1.1
Release:        8%{?dist}
Summary:        Quickshell desktop shell for KDE Plasma Wayland
License:        GPL-3.0-only AND GPL-2.0-or-later AND MIT AND BSD-3-Clause AND Apache-2.0
URL:            https://github.com/NextKde/NextKde
Source0:        https://codeload.github.com/MCC45TR/NextKde/tar.gz/%{commit}#/nextkde-%{commit}.tar.gz
Source1:        nextkde-vendor.tar.gz
# License of the Material Color Utilities code ported in Cam16Hct.mjs.
Source2:        material-color-utilities-LICENSE
Patch0:         nextkde-system-paths.patch
ExclusiveArch:  aarch64

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  golang >= 1.26
BuildRequires:  extra-cmake-modules
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  python3
BuildRequires:  systemd-rpm-macros
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtwayland-devel
BuildRequires:  qt6-qtshadertools
BuildRequires:  qt6-qtquick3d-devel
BuildRequires:  kf6-kcalendarcore-devel
BuildRequires:  onnxruntime-devel
BuildRequires:  opencv-devel
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(taglib)
BuildRequires:  dbus-daemon
BuildRequires:  nodejs
BuildRequires:  kwin-devel = %{kwin_version}
BuildRequires:  kdecoration-devel
BuildRequires:  libplasma-devel
BuildRequires:  kf6-kcoreaddons-devel
BuildRequires:  kf6-kconfig-devel
BuildRequires:  kf6-kiconthemes-devel
BuildRequires:  kf6-kglobalaccel-devel
BuildRequires:  kf6-kio-devel
BuildRequires:  kf6-ki18n-devel
BuildRequires:  kf6-kguiaddons-devel
BuildRequires:  kf6-kcmutils-devel
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  vulkan-loader-devel
BuildRequires:  kf6-kwindowsystem-devel
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)

Requires:       %{name}-data%{?_isa} = %{version}-%{release}
Requires:       quickshell%{?_isa} >= 0.3.2
Requires:       quickshell%{?_isa} < 0.4
# KWin plugins use its private ABI; rebuild for each KWin version.
Requires:       kwin%{?_isa} = %{kwin_version}
Requires:       plasma-workspace%{?_isa}
Requires:       qt6-qt5compat%{?_isa}
Requires:       qt6-qtquick3d%{?_isa}
Requires:       qt6-qtsvg%{?_isa}
Requires:       qt6-qtimageformats%{?_isa}
Requires:       kpipewire%{?_isa}
Requires:       pulseaudio-utils
Requires:       wireplumber
Requires:       wl-clipboard
Requires:       cliphist
Requires:       systemd
Recommends:     spectacle
Recommends:     NetworkManager
Recommends:     bluez


%description
NextKDE (KOS Desktop Shell) provides a top bar, dock, launcher, search,
notifications and settings on KDE Plasma Wayland. This is independent
downstream packaging of upstream NextKDE, using Fedora's Plasma packages.

User services are installed but are not enabled or started by the RPM.
Independent applications, shared services, themes and the native spatial
wallpaper engine are available as separate subpackages. The full metapackage
selects every packaged component.


%package data
Summary: Persistent desktop and weather data service for NextKDE
Requires: systemd
Provides: bundled(golang(github.com/fsnotify/fsnotify)) = 1.10.1
Provides: bundled(golang(golang.org/x/sys)) = 0.13.0
%description data
Upstream Go data service shared by the desktop shell and Weather application.
Its user unit is installed without enabling or starting it.

%package pim
Summary: NextKDE calendar and reminder service
Requires: systemd
%description pim
D-Bus-activated calendar and reminder service shared by Calendar and Todo.

%package calculator
Summary: NextKDE calculator
Requires: qt6-qt5compat%{?_isa}
Requires: qt6-qtsvg%{?_isa}
%description calculator
Standalone upstream Qt Quick calculator and unit converter.

%package calendar
Summary: NextKDE calendar
Requires: %{name}-pim%{?_isa} = %{version}-%{release}
Requires: qt6-qt5compat%{?_isa}
Requires: qt6-qtsvg%{?_isa}
%description calendar
Standalone upstream calendar with events and reminders.

%package todo
Summary: NextKDE task manager
Requires: %{name}-pim%{?_isa} = %{version}-%{release}
Requires: qt6-qt5compat%{?_isa}
Requires: qt6-qtsvg%{?_isa}
%description todo
Standalone upstream Todo application using the shared PIM service.

%package weather
Summary: NextKDE weather application
Requires: %{name}-data%{?_isa} = %{version}-%{release}
Requires: qt6-qt5compat%{?_isa}
Requires: qt6-qtsvg%{?_isa}
%description weather
Standalone upstream weather application using the shared data service.

%package music
Summary: Legacy NextKDE music player
Requires: qt6-qt5compat%{?_isa}
Requires: qt6-qtsvg%{?_isa}
Requires: nodejs
Requires: gstreamer1-plugins-base%{?_isa}
Requires: gstreamer1-plugins-good%{?_isa}
%description music
The legacy upstream KOS Music player retained in the selected release.
It coexists with ListenFree without changing existing media associations.

%package spatial
Summary: Native NextKDE depth and spatial wallpaper engine
Requires: %{name}%{?_isa} = %{version}-%{release}
%description spatial
AArch64 depth-inference worker and Qt Quick 3D mesh plugin built with Fedora's
ONNX Runtime and OpenCV. Models are downloaded and verified by upstream only
when the user explicitly enables spatial wallpaper; models are not bundled.

%package lockscreen
Summary: NextKDE Plasma lock screen theme
BuildArch: noarch
Requires: plasma-workspace
Requires: kscreenlocker
%description lockscreen
Upstream Plasma look-and-feel and shell theme. Installation does not select
the theme or change authentication configuration.

%package sddm
Summary: NextKDE SDDM sign-in theme
BuildArch: noarch
Requires: sddm
Requires: qt6-qtdeclarative
%description sddm
Upstream SDDM sign-in theme. Installation does not select the theme or enable
a display manager.

%package apps
Summary: All standalone applications from the NextKDE release
BuildArch: noarch
Requires: %{name}-calculator = %{version}-%{release}
Requires: %{name}-calendar = %{version}-%{release}
Requires: %{name}-todo = %{version}-%{release}
Requires: %{name}-weather = %{version}-%{release}
Requires: %{name}-music = %{version}-%{release}
Requires: %{name}-listenfree >= 0.3.8
%description apps
Metapackage selecting every standalone application in the pinned NextKDE
release, including the retained legacy Music player and ListenFree.

%package full
Summary: Every packaged component from the NextKDE release
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
Requires: %{name}-apps = %{version}-%{release}
Requires: %{name}-spatial = %{version}-%{release}
Requires: %{name}-lockscreen = %{version}-%{release}
Requires: %{name}-sddm = %{version}-%{release}
%description full
Metapackage selecting the desktop, applications, shared services, spatial
engine and optional login/lock themes. Components remain opt-in at runtime.

%prep
%autosetup -n NextKde-%{commit} -p1
tar -xf %{SOURCE1} -C services/data-service

%build
export GOPROXY=off GOSUMDB=off GOTOOLCHAIN=local
export GOFLAGS='-mod=vendor -trimpath -buildvcs=false'
export GOCACHE="$PWD/.go-cache"
# Qt Quick 3D custom materials compile source shaders at runtime.
find shell shared/qml -type f \( -name '*.frag' -o -name '*.vert' \) | while IFS= read -r shader; do
    if [ -f "$shader.qsb" ]; then
        %{_libdir}/qt6/bin/qsb --qsbversion 64 --glsl '330,300 es' --hlsl 50 --msl 12 -o "$shader.qsb" "$shader"
    fi
done
%cmake -GNinja \
    -DBUILD_TESTING=OFF \
    -DKOS_BUILD_SPATIAL=ON \
    -DKOS_BUILD_CALENDAR=ON \
    -DKOS_BUILD_TODO=ON \
    -DKOS_BUILD_WEATHER=ON \
    -DKOS_BUILD_MUSIC=ON \
    -DKOS_BUILD_CALCULATOR=ON \
    -DKOS_BUILD_KWIN_PLUGINS=ON \
    -DCMAKE_SKIP_RPATH=ON
%cmake_build
cmake -S kwin/glass-effect -B glass-build -GNinja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DCMAKE_SKIP_RPATH=ON -DGLASS_X11=OFF
cmake --build glass-build --parallel %{_smp_build_ncpus}
(cd services/data-service && CGO_ENABLED=0 go build -ldflags="-B gobuildid" -o kos-data-service .)

%install
%cmake_install
DESTDIR=%{buildroot} cmake --install glass-build
install -Dm0755 services/data-service/kos-data-service %{buildroot}%{_libexecdir}/kos-data-service
# Fedora user units live under /usr/lib, including the units installed by CMake.
install -d %{buildroot}%{_userunitdir}
rm -f %{buildroot}%{_datadir}/systemd/user/kos-data.service
mv %{buildroot}%{_datadir}/systemd/user/kos-pim-service.service %{buildroot}%{_userunitdir}/
install -d %{buildroot}%{_datadir}/plasma/look-and-feel/org.kos.desktop %{buildroot}%{_datadir}/plasma/shells
cp -a apps/lockscreen/contents apps/lockscreen/metadata.json %{buildroot}%{_datadir}/plasma/look-and-feel/org.kos.desktop/
ln -s ../look-and-feel/org.kos.desktop %{buildroot}%{_datadir}/plasma/shells/org.kos.desktop
install -d %{buildroot}%{_datadir}/sddm/themes/kos
cp -a apps/sddm/*.qml apps/sddm/metadata.desktop apps/sddm/theme.conf %{buildroot}%{_datadir}/sddm/themes/kos/

mkdir -p %{buildroot}%{_datadir}/nextkde
cp -a shell %{buildroot}%{_datadir}/nextkde/
mkdir -p %{buildroot}%{_datadir}/nextkde/shared
cp -a shared/qml %{buildroot}%{_datadir}/nextkde/shared/
rm -rf %{buildroot}%{_datadir}/nextkde/shell/native
find %{buildroot}%{_datadir}/nextkde \
    \( -name CMakeLists.txt -o -name 'test_*.mjs' -o -name '*.test.mjs' -o -name '*.py' -o -name '*.sh' -o -name '*test*.cpp' \) -delete

install -d %{buildroot}%{_userunitdir} %{buildroot}%{_datadir}/applications
sed -e 's|%%h/.local/libexec|%{_libexecdir}|g' \
    -e 's|%%h/.local/share|%{_datadir}|g' \
    packaging/systemd/kos-platform.service > %{buildroot}%{_userunitdir}/kos-platform.service
sed 's|@CMAKE_INSTALL_FULL_LIBEXECDIR@|%{_libexecdir}|g' \
    services/data-service/systemd/kos-data.service.in > %{buildroot}%{_userunitdir}/kos-data.service
sed -e 's|@QS_EXEC@ --no-duplicate -c kos|%{_bindir}/quickshell --no-duplicate --path %{_datadir}/nextkde/shell|g' \
    -e 's|^Environment=QML2_IMPORT_PATH=.*|Environment=QML2_IMPORT_PATH=%{_datadir}/nextkde/shell:%{_libdir}/qt6/qml|' \
    packaging/systemd/kos-shell.service.in > %{buildroot}%{_userunitdir}/kos-shell.service
sed -i '/^\[Service\]/a Environment=KOS_SHELL_DIR=%{_datadir}/nextkde/shell' \
    %{buildroot}%{_userunitdir}/kos-platform.service
cp packaging/desktop/kos-settings.desktop.in %{buildroot}%{_datadir}/applications/kos-settings.desktop
sed 's|@KOS_PLATFORM_EXEC@|%{_libexecdir}/kos-platform|g' \
    packaging/desktop/org.kos.Platform.desktop.in > %{buildroot}%{_datadir}/applications/org.kos.Platform.desktop
cat > %{buildroot}%{_datadir}/nextkde/release.json <<'EOF'
{"version":"%{version}","revision":"%{commit}","dirty":false,"tag":"v%{version}"}
EOF
install -d %{buildroot}%{_licensedir}/%{name}/bundled
install -d %{buildroot}%{_licensedir}/%{name}-data
cp services/data-service/vendor/github.com/fsnotify/fsnotify/LICENSE %{buildroot}%{_licensedir}/%{name}-data/fsnotify-LICENSE
cp services/data-service/vendor/golang.org/x/sys/LICENSE %{buildroot}%{_licensedir}/%{name}-data/x-sys-LICENSE
cp shared/qml/wallpapers/vendor/flow/LICENSE %{buildroot}%{_licensedir}/%{name}/bundled/flow-LICENSE
cp shared/qml/wallpapers/vendor/black-hole/LICENSE %{buildroot}%{_licensedir}/%{name}/bundled/black-hole-LICENSE
cp kwin/glass-effect/LICENSE %{buildroot}%{_licensedir}/%{name}/bundled/glass-LICENSE
cp %{SOURCE2} %{buildroot}%{_licensedir}/%{name}/bundled/material-color-utilities-LICENSE

%check
mkdir packaging-check
cat > packaging-check/CMakeLists.txt <<'EOF'
cmake_minimum_required(VERSION 3.21)
project(nextkde_packaging_check LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_AUTOMOC ON)
find_package(Qt6 REQUIRED COMPONENTS Core Gui Test)
add_executable(backend
    ../apps/settings/tests/backend/ModulesTest.cpp
    ../apps/settings/src/SettingsProbeTasks.cpp
    ../apps/settings/src/ShellIpcClient.cpp
    ../apps/settings/src/WallpaperLibrary.cpp)
target_include_directories(backend PRIVATE ../apps/settings/src)
target_compile_definitions(backend PRIVATE SETTINGS_SHELL_DIR="/usr/share/nextkde/shell")
target_link_libraries(backend PRIVATE Qt6::Core Qt6::Gui Qt6::Test)
EOF
cmake -S packaging-check -B packaging-check/build -GNinja
cmake --build packaging-check/build --parallel %{_smp_build_ncpus}
packaging-check/build/backend
export GOPROXY=off GOSUMDB=off GOTOOLCHAIN=local
export GOFLAGS='-mod=vendor -trimpath -buildvcs=false'
export GOCACHE="$PWD/.go-cache"
(cd services/data-service && go test ./...)
export QT_QPA_PLATFORM=offscreen QT_QUICK_BACKEND=software
export KOS_WEATHER_DISABLE_SERVICE_AUTOSTART=1 KOS_MUSIC_FAKE_AUDIO=1
for app in calculator calendar todo weather music; do
    %{buildroot}%{_bindir}/kos-$app --version
done
for app in calculator calendar todo weather; do
    dbus-run-session -- %{buildroot}%{_bindir}/kos-$app --smoke-test
done
test -x %{buildroot}%{_libexecdir}/kos-ai-worker
test -f %{buildroot}%{_libdir}/qt6/qml/Kos/Spatial3D/libkos_spatial3d.so

desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
grep -q '"EnabledByDefault": false' kwin/kos-bridge/metadata.json
test -x %{buildroot}%{_libexecdir}/kos-platform
test -x %{buildroot}%{_libexecdir}/kos-data-service
test -x %{buildroot}%{_bindir}/kos-settings
test -f %{buildroot}%{_libdir}/qt6/qml/Kos/SurfaceShape/libkos_surface_shape.so
test -f %{buildroot}%{_libdir}/qt6/plugins/kwin/effects/plugins/glass.so
test -f %{buildroot}%{_datadir}/nextkde/shell/Kos/Ui/foundation/AppTheme.qml
test -f %{buildroot}%{_datadir}/nextkde/apps/settings/main.qml
test -z "$(find %{buildroot} -xtype l -print -quit)"
! grep -R -E '@QS_EXEC@|@KOS_PLATFORM_EXEC@|%%h/\.local|%%h/\.config' \
    %{buildroot}%{_userunitdir}/kos-*.service %{buildroot}%{_datadir}/applications/*.desktop

%files
%license LICENSE
%license %{_licensedir}/%{name}/bundled/
%doc README.md
%{_bindir}/kos-settings
%{_libexecdir}/kos-platform
%{_libdir}/qt6/qml/Kos/SurfaceShape/
%{_libdir}/qt6/plugins/kwin/effects/plugins/*.so
%{_libdir}/qt6/plugins/kwin/effects/configs/*.so
%{_libdir}/qt6/plugins/org.kde.kdecoration3/*.so
%{_datadir}/nextkde/
%{_datadir}/kos/platform/
%{_datadir}/applications/kos-settings.desktop
%{_datadir}/applications/org.kos.Platform.desktop
%{_userunitdir}/kos-platform.service
%{_userunitdir}/kos-shell.service
%{_datadir}/locale/*/LC_MESSAGES/kwin_effects_glass.mo


%files data
%license LICENSE
%license %{_licensedir}/%{name}-data/
%{_libexecdir}/kos-data-service
%{_userunitdir}/kos-data.service

%files pim
%license LICENSE
%{_bindir}/kos-pim-service
%{_datadir}/dbus-1/services/org.nextkde.Kos.Pim1.service
%{_userunitdir}/kos-pim-service.service

%files calculator
%license LICENSE
%{_bindir}/kos-calculator
%{_datadir}/applications/kos-calculator.desktop
%{_datadir}/icons/hicolor/scalable/apps/kos-calculator.svg
%{_datadir}/metainfo/org.nextkde.Kos.Calculator.metainfo.xml

%files calendar
%license LICENSE
%{_bindir}/kos-calendar
%{_datadir}/applications/kos-calendar.desktop
%{_datadir}/icons/hicolor/scalable/apps/kos-calendar.svg
%{_datadir}/metainfo/org.nextkde.Kos.Calendar.metainfo.xml

%files todo
%license LICENSE
%{_bindir}/kos-todo
%{_datadir}/applications/kos-todo.desktop
%{_datadir}/icons/hicolor/scalable/apps/kos-todo.svg
%{_datadir}/metainfo/org.nextkde.Kos.Todo.metainfo.xml

%files weather
%license LICENSE
%{_bindir}/kos-weather
%{_datadir}/applications/kos-weather.desktop
%{_datadir}/icons/hicolor/scalable/apps/kos-weather.svg
%{_datadir}/metainfo/org.nextkde.Kos.Weather.metainfo.xml

%files music
%license LICENSE
%{_bindir}/kos-music
%{_datadir}/applications/kos-music.desktop
%{_datadir}/icons/hicolor/scalable/apps/kos-music.svg
%{_datadir}/metainfo/org.nextkde.Kos.Music.metainfo.xml
%{_bindir}/kos-music-lx-source-host
%{_bindir}/kos-music-lx-source-host.js

%files spatial
%license LICENSE
%{_libexecdir}/kos-ai-worker
%{_libdir}/qt6/qml/Kos/Spatial3D/

%files lockscreen
%license LICENSE
%{_datadir}/plasma/look-and-feel/org.kos.desktop/
%{_datadir}/plasma/shells/org.kos.desktop

%files sddm
%license LICENSE
%{_datadir}/sddm/themes/kos/

%files apps
%files full

%changelog
* Sun Nov 01 2026 mcc45tr - 0.1.1-8
- Build all release applications, shared services, spatial engine and themes
- Maintain downstream packaging in the MCC45TR/NextKde fork

* Sun Nov 01 2026 mcc45tr - 0.1.1-7
- Add the Plasma version header required by the bundled Glass effect

* Sun Nov 01 2026 mcc45tr - 0.1.1-6
- Rebuild QSB resources for GLSL 330 and GLES 3.0; retain Quick 3D sources

* Sun Nov 01 2026 mcc45tr - 0.1.1-5
- Match KDE module naming and retain a GNU build ID for the Go service

* Sun Nov 01 2026 mcc45tr - 0.1.1-4
- Retain the Material Color Utilities Apache license and rebuild QSB shaders

* Sun Nov 01 2026 mcc45tr - 0.1.1-3
- Keep KOS Bridge disabled by default until the user enables it

* Sun Nov 01 2026 mcc45tr - 0.1.1-2
- Limit shared payload to runtime QML and retain the Glass translation catalog

* Sun Nov 01 2026 mcc45tr - 0.1.1-1
- Package upstream v0.1.1 for Fedora Rawhide AArch64, with opt-in user services
