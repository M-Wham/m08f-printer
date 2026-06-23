Name:           m08f-printer
Version:        0.1.0
Release:        1%{?dist}
Summary:        Linux driver and CUPS backend for the M08F A4 thermal printer

License:        MIT
URL:            https://github.com/M-Wham/m08f-printer
Source0:        %{url}/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

Requires:       python3-pyserial
Requires:       python3-pillow
Requires:       ghostscript
Requires:       cups

%description
Provides a CLI (m08f print/probe/calibrate/status) and a CUPS backend so the
M08F A4 thermal printer (sold as Phomemo / COLORWING / AIMO) appears as a normal
printer in any Linux application. Communicates over USB CDC/ACM in solid-red mode
using the ESC/POS protocol.

%prep
%autosetup -n %{name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files m08f

install -Dm700 cups/m08f-backend %{buildroot}%{_prefix}/lib/cups/backend/m08f
install -Dm644 cups/m08f.ppd %{buildroot}%{_datadir}/cups/model/m08f.ppd
install -Dm644 udev/99-m08f.rules %{buildroot}%{_prefix}/lib/udev/rules.d/99-m08f.rules

%files -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/m08f
%{_prefix}/lib/cups/backend/m08f
%{_datadir}/cups/model/m08f.ppd
%{_prefix}/lib/udev/rules.d/99-m08f.rules

%post
/usr/bin/udevadm control --reload-rules >/dev/null 2>&1 || :
/usr/bin/udevadm trigger >/dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    /usr/sbin/lpadmin -x M08F >/dev/null 2>&1 || :
fi

%changelog
* Tue Jun 23 2026 mwham <mwams-mail@proton.me> - 0.1.0-1
- Initial RPM packaging.
