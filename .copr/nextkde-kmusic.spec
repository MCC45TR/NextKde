%global commit ad0222d4404a166a1607e2967f3201cea64111c5
Name:           nextkde-kmusic
Version:        0.1.0
Release:        0.3.gitad0222d%{?dist}
Summary:        Native KMusic application from NextKDE
License:        GPL-3.0-only AND AGPL-3.0-only
URL:            https://github.com/NextKde/KMusic
Source0:        https://codeload.github.com/NextKde/KMusic/tar.gz/%{commit}#/kmusic-%{commit}.tar.gz
ExclusiveArch:  aarch64
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtshadertools
BuildRequires:  qtkeychain-qt6-devel
BuildRequires:  pkgconfig(libqrencode)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(taglib)
BuildRequires:  desktop-file-utils
Requires:       nodejs
Requires:       qt6-qt5compat%{?_isa}
Requires:       qt6-qtsvg%{?_isa}
Requires:       gstreamer1-plugins-base%{?_isa}
Requires:       gstreamer1-plugins-good%{?_isa}

%description
The independent upstream KMusic application, with local music, supported
online providers and a user-selected media server. The pinned portable UI
snapshot and JavaScript provider are retained with their original notices.
This is a development snapshot; no real-account or service qualification is
claimed by this package.

%prep
%autosetup -n KMusic-%{commit}

%build
%cmake -GNinja -DCMAKE_SKIP_RPATH=ON
%cmake_build
cmake -S tests/providers -B provider-tests -GNinja -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build provider-tests --parallel %{_smp_build_ncpus}

%install
%cmake_install
install -d %{buildroot}%{_licensedir}/%{name}
cp providers/netease/LICENSE %{buildroot}%{_licensedir}/%{name}/netease-LICENSE
cp vendor/nextkdeAppDemo/LICENSE %{buildroot}%{_licensedir}/%{name}/Kos.Ui-LICENSE
cp vendor/nextkdeAppDemo/NOTICE.md %{buildroot}%{_licensedir}/%{name}/Kos.Ui-NOTICE

%check
export QT_QPA_PLATFORM=offscreen QT_QUICK_BACKEND=software
ctest --test-dir provider-tests --output-on-failure --timeout 60
desktop-file-validate %{buildroot}%{_datadir}/applications/kmusic.desktop
test -x %{buildroot}%{_bindir}/kmusic
test -s %{buildroot}%{_datadir}/kmusic/providers/runtime/helper.js
test -z "$(find %{buildroot} -type f \( -name '*.py' -o -name '*.pyc' \) -print -quit)"

%files
%license LICENSE
%license %{_licensedir}/%{name}/netease-LICENSE
%license %{_licensedir}/%{name}/Kos.Ui-LICENSE
%license %{_licensedir}/%{name}/Kos.Ui-NOTICE
%doc NOTICE.md
%{_bindir}/kmusic
%{_datadir}/applications/kmusic.desktop
%{_datadir}/icons/hicolor/scalable/apps/kmusic.svg
%{_datadir}/kmusic/

%changelog
* Sun Nov 01 2026 mcc45tr - 0.1.0-0.3.gitad0222d
- Use the SQLite driver provided by Fedora qt6-qtbase

* Sun Nov 01 2026 mcc45tr - 0.1.0-0.2.gitad0222d
- Preserve distinct application, provider and shared UI license filenames

* Sun Nov 01 2026 mcc45tr - 0.1.0-0.1.gitad0222d
- Package the pinned upstream KMusic application and provider contract tests
