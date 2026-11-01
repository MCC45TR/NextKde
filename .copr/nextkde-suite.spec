Name:           nextkde-suite
Version:        0.1.1
Release:        1%{?dist}
Summary:        Complete NextKDE desktop and official application family
License:        GPL-3.0-only
URL:            https://github.com/MCC45TR/NextKde
Source0:        nextkde-LICENSE
BuildArch:      noarch
Requires:       nextkde-full >= 0.1.1
Requires:       nextkde-kmusic >= 0.1.0
Requires:       nextkde-nkmail >= 0.1.0

%description
Select every packaged component from the NextKDE release and the independent
official KMusic and NkMail applications. Installing this metapackage does not
activate the shell, effects, login theme or lock screen.

%prep
%build
%install

%files
%license %{SOURCE0}

%changelog
* Sun Nov 01 2026 mcc45tr - 0.1.1-1
- Select the complete NextKDE release plus the official standalone applications
