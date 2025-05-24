%{!?python_sitelib: %global python_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           voktrainer
Version:        1.1.3
Release:        2%{?dist}
Summary:        A vocabulary trainer for Linux

Group:          Applications/Productivity
License:        GPLv3
URL:            https://framagit.org/tuxor1337/voktrainer
Source0:        https://framagit.org/tuxor1337/%{name}/-/archive/v%{version}/%{name}-v%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  desktop-file-utils
Requires:	    python3
Requires:	    gobject-introspection

%description
Linux application aimed at helping users to learn vocabulary from any foreign
language(s) written in Python with GTK+ user interface.

%prep
%autosetup -n %{name}-v%{version}

%install
python3 setup.py install --root=%{buildroot} --prefix=%{_prefix}

desktop-file-install --vendor fedora                            \
        --dir %{buildroot}%{_datadir}/applications              \
        --delete-original										\
        %{buildroot}%{_datadir}/applications/voktrainer.desktop

%clean
rm -rf %{buildroot}

%files
%{_bindir}/voktrainer
%{_datadir}/applications/fedora-voktrainer.desktop
%{_datadir}/pixmaps/voktrainer.svg
%{python3_sitelib}/vok/
%{python3_sitelib}/Vokabeltrainer_f_r_Linux-%{version}-py%{python3_version}.egg-info

%changelog
* Wed Apr 20 2022 Thomas Vogt <admin@tovotu.de> - 1.1.2-2
- Explictly require python3-setuptools
* Thu Nov 29 2018 Thomas Vogt <admin@tovotu.de> - 1.1.2
- Upgrade to 1.1.2
* Mon Nov 26 2018 Thomas Vogt <admin@tovotu.de> - 1.1.1
- Upgrade to 1.1.1
* Sat Nov 24 2018 Thomas Vogt <admin@tovotu.de> - 1.1
- Fix python version in egg-info
* Mon Aug 6 2018 Thomas Vogt <admin@tovotu.de> - 1.1
- Upgrade to 1.1
* Sun Oct 26 2014 Thomas Vogt <admin@tovotu.de> - 1.0.1
- First version for copr
* Mon Dec 24 2012 Thomas Vogt <admin@tovotu.de> - 1.0
- First version for myself
