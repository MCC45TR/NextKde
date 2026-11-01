# Not needed by default
%bcond asan 0
# Not packaged in Fedora yet (cf. rhbz#2372509)
%bcond breakpad 0
# Not available in RHEL
%bcond x11 %[%{undefined rhel}]

%global commit 4f508be500dea6e5732cc3d50382a0048b17e7b1
%global commitdate 20261022
%global shortcommit %{sub %{commit} 1 7}

%global tarversion %{?commit:%{commit}}%{!?commit:v%{version}}
%global tarext tar.gz
%global tarbasename %{name}-%{?commit:%{shortcommit}}%{!?commit:%{version}}


Name:               quickshell
Version:            0.3.2
Release:            2%{?dist}
Summary:            Flexible QtQuick based desktop shell toolkit
# Code is LGPL, Hyprland protocols are BSD-3-Clause, wlr protocols are HPND-sell-variant
License:            LGPL-3.0-or-later and BSD-3-Clause and HPND-sell-variant
URL:                https://quickshell.org/
Source0:            https://codeload.github.com/quickshell-mirror/quickshell/tar.gz/%{commit}#/%{name}-%{commit}.tar.gz


BuildRequires:      cmake
BuildRequires:      pkgconfig(xcb)
BuildRequires:      cmake(Qt6Core)
BuildRequires:      cmake(Qt6Qml)
BuildRequires:      cmake(Qt6CorePrivate)
BuildRequires:      cmake(Qt6QuickPrivate)
BuildRequires:      cmake(Qt6ShaderTools)
BuildRequires:      cmake(Qt6WaylandClient)
BuildRequires:      desktop-file-utils
BuildRequires:      gcc-c++
BuildRequires:      ninja-build
BuildRequires:      pkgconfig(CLI11)
BuildRequires:      pkgconfig(glib-2.0)
BuildRequires:      pkgconfig(gbm)
BuildRequires:      pkgconfig(jemalloc)
BuildRequires:      pkgconfig(libdrm)
BuildRequires:      pkgconfig(libpipewire-0.3)
BuildRequires:      pkgconfig(pam)
BuildRequires:      pkgconfig(polkit-agent-1)
BuildRequires:      pkgconfig(wayland-client)
BuildRequires:      pkgconfig(wayland-protocols)
BuildRequires:      spirv-tools

# Add undetectable runtime dependencies
Requires:           (qt6-qtwayland%{?_isa} if qt6-qtbase%{?_isa} < 6.10)
Requires:           qt6-qtsvg%{?_isa}

%if %{with asan}
BuildRequires:      libasan
%endif

%if %{with breakpad}
BuildRequires:      breakpad-static
BuildRequires:      pkgconfig(breakpad)
%endif

Provides:           desktop-notification-daemon = %{version}-%{release}
Provides:           PolicyKit-authentication-agent = %{version}-%{release}

%description
Quickshell is a toolkit for building status bars, widgets,
lockscreens, and other desktop components using QtQuick.

It can be used alongside a Wayland compositor to build
a complete desktop environment.

%prep
%autosetup -n %{name}-%{commit}

%conf
# shortcut: Fedora cpptrace lacks signal-safe unwinding, enable the crash handler when its libunwind support is available.
%cmake  -GNinja \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DCMAKE_SKIP_INSTALL_RPATH=ON \
        -DDISTRIBUTOR="Fedora COPR (mcc45tr/kdenext)" \
        -DDISTRIBUTOR_DEBUGINFO_AVAILABLE=YES \
        -DINSTALL_QML_PREFIX=%{_lib}/qt6/qml \
        -DASAN=%{?with_asan:ON}%{!?with_asan:OFF} \
        -DCRASH_HANDLER=OFF \
        -DX11=%{?with_x11:ON}%{!?with_x11:OFF} \
        %{?commit:-DGIT_REVISION=%{commit}} \
        %{nil}

%build
%cmake_build

%install
%cmake_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files
%license LICENSE*
%doc BUILD.md CONTRIBUTING.md README.md
%{_bindir}/qs
%{_bindir}/quickshell
%{_datadir}/applications/org.quickshell.desktop
%{_datadir}/icons/hicolor/scalable/apps/org.quickshell.svg
%{_libdir}/qt6/qml/Quickshell/

%changelog
* Sun Nov 01 2026 mcc45tr - 0.3.2-2
- Disable the optional crash handler unsupported by Fedora cpptrace

* Sun Nov 01 2026 mcc45tr - 0.3.2-1
- Build upstream 0.3.2 for the independent NextKDE Rawhide AArch64 COPR

* Fri Oct 23 2026 Jan Grulich <jgrulich@redhat.com> - 0.2.1^git20260209.dacfa9d-6
- Rebuild (qt6)

* Mon Aug 31 2026 Jan Grulich <jgrulich@redhat.com> - 0.2.1^git20260209.dacfa9d-5
- Rebuild (qt6)

* Thu Jul 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1^git20260209.dacfa9d-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Thu May 14 2026 Jan Grulich <jgrulich@redhat.com> - 0.2.1^git20260209.dacfa9d-3
- Rebuild (qt6)

* Thu Apr 16 2026 Jan Grulich <jgrulich@redhat.com> - 0.2.1^git20260209.dacfa9d-2
- Rebuild (qt6)

* Mon Feb 16 2026 Neal Gompa <ngompa@fedoraproject.org> - 0.2.1^git20260209.dacfa9d-1
- Bump to git snapshot

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sun Jan 04 2026 Neal Gompa <ngompa@fedoraproject.org> - 0.2.1-7
- Initial package based on ErrorNoInternet/quickshell COPR version
