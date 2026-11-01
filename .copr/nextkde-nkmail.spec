%global commit 483a664317cd1efa43b10ae6d461caa53182ce30
%global ui_commit e2592b2742c58c1bd797a8bcfa2a3ae7da4affd8
Name:           nextkde-nkmail
Version:        0.1.0
Release:        0.4.git483a664%{?dist}
Summary:        Native NkMail application from NextKDE
License:        GPL-3.0-or-later AND BSD-2-Clause
URL:            https://github.com/NextKde/NkMail
Source0:        https://codeload.github.com/NextKde/NkMail/tar.gz/%{commit}#/nkmail-%{commit}.tar.gz
Source1:        https://codeload.github.com/NextKde/nextkdeAppDemo/tar.gz/%{ui_commit}#/kos-ui-%{ui_commit}.tar.gz
ExclusiveArch:  aarch64
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtshadertools
BuildRequires:  qt6-qt5compat
BuildRequires:  qt6-qtsvg
BuildRequires:  qtkeychain-qt6-devel
BuildRequires:  boost-devel
BuildRequires:  openssl-devel
BuildRequires:  openssl
# Unmodified upstream loopback/CLI test fixtures run only in the COPR builder.
BuildRequires:  python3
BuildRequires:  desktop-file-utils
Requires:       qt6-qt5compat%{?_isa}
Requires:       qt6-qtsvg%{?_isa}
Provides:       bundled(mailio) = 0.26.1

%description
The independent upstream NkMail application using its fixed Kos.Ui gitlink
and vendored mailio with the upstream TLS/PEEK fixes. Passwords use the
platform keychain. This development snapshot is not qualified for real mail
providers; local tests use synthetic data and non-relaying loopback services.

%prep
%autosetup -n NkMail-%{commit}
tar -xf %{SOURCE1} -C third_party/nextkdeAppDemo --strip-components=1
grep -q '%{ui_commit}' third_party/kos-ui.lock.json

%build
%cmake -GNinja -DCMAKE_SKIP_RPATH=ON -DNKMAIL_BUILD_TESTS=ON -DBUILD_SHARED_LIBS=OFF
%cmake_build

%install
%cmake_install
install -d %{buildroot}%{_licensedir}/%{name}
cp third_party/mailio/LICENSE %{buildroot}%{_licensedir}/%{name}/mailio-LICENSE
cp third_party/nextkdeAppDemo/LICENSE %{buildroot}%{_licensedir}/%{name}/Kos.Ui-LICENSE
cp third_party/nextkdeAppDemo/NOTICE.md %{buildroot}%{_licensedir}/%{name}/Kos.Ui-NOTICE

%check
export QT_QPA_PLATFORM=offscreen QT_QUICK_BACKEND=software
%ctest --timeout 180
desktop-file-validate %{buildroot}%{_datadir}/applications/nkmail.desktop
test -x %{buildroot}%{_bindir}/nkmail
test -z "$(find %{buildroot} -type f \( -name '*.py' -o -name '*.pyc' \) -print -quit)"

%files
%license LICENSE
%license %{_licensedir}/%{name}/mailio-LICENSE
%license %{_licensedir}/%{name}/Kos.Ui-LICENSE
%license %{_licensedir}/%{name}/Kos.Ui-NOTICE
%doc NOTICE.md
%{_bindir}/nkmail
%{_datadir}/applications/nkmail.desktop
%{_datadir}/icons/hicolor/scalable/apps/nkmail.svg

%changelog
* Sun Nov 01 2026 mcc45tr - 0.1.0-0.4.git483a664
- Preserve upstream static mailio against Fedora shared-library defaults

* Sun Nov 01 2026 mcc45tr - 0.1.0-0.3.git483a664
- Use the SQLite driver provided by Fedora qt6-qtbase

* Sun Nov 01 2026 mcc45tr - 0.1.0-0.2.git483a664
- Include QML compatibility modules and SQLite in the isolated test buildroot

* Sun Nov 01 2026 mcc45tr - 0.1.0-0.1.git483a664
- Package the upstream snapshot with its exact UI gitlink and loopback tests
