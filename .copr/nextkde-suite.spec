Name:           nextkde-suite
Version:        0.1.1
Release:        3%{?dist}
Summary:        Complete NextKDE desktop and official application family
License:        GPL-3.0-only
URL:            https://github.com/MCC45TR/NextKde
Source0:        nextkde-LICENSE
BuildArch:      noarch
Requires:       nextkde-full >= 0.1.1
Requires:       nextkde-kmusic >= 0.1.0
Requires:       nextkde-nkmail >= 0.1.0
Requires:       plasma-desktop plasma-systemsettings dolphin konsole
Requires:       xdg-desktop-portal-kde polkit-kde

%description
Select every packaged component from the NextKDE release and the independent
official KMusic and NkMail applications, together with the original Fedora
Plasma desktop, file manager, terminal, settings and desktop portal.
Installing this metapackage does not
activate the shell, effects, login theme or lock screen.

%prep
cp %{SOURCE0} LICENSE
%build
%install

%files
%license LICENSE

%changelog
* Sun Nov 01 2026 mcc45tr - 0.1.1-3
- Include the original Fedora Plasma desktop and its standard integration

* Sun Nov 01 2026 mcc45tr - 0.1.1-2
- Copy the source license before using the relative RPM license directive

* Sun Nov 01 2026 mcc45tr - 0.1.1-1
- Select the complete NextKDE release plus the official standalone applications
