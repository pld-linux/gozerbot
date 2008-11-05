# TODO
# - user and initscript
Summary:	gozerbot is the Python IRC bot and Jabber bot in one
Name:		gozerbot
Version:	0.8.1.1
Release:	0.2
License:	BSD
Group:		Applications/Communications
Source0:	http://www.gozerbot.org/media/tarball/%{name}-%{version}.tar.gz
# Source0-md5:	f94037651700737f655f28244662c5a0
URL:		http://www.gozerbot.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
Requires:	python >= 1:2.4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python IRC bot and Jabber bot in one.

%prep
%setup -q
%{__grep} -rl '#!/usr/bin/env python' . | xargs %{__sed} -i -e '1s,#!.*bin/env python,#!%{__python}',

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

# some merge tool. likely don't need it
rm -f $RPM_BUILD_ROOT%{_bindir}/gozerbot-merc
rm -f $RPM_BUILD_ROOT%{_bindir}/gozerupgrade06
# we'll have initscript
rm -f $RPM_BUILD_ROOT%{_bindir}/gozerbot-{start,stop}
rm -f $RPM_BUILD_ROOT%{_datadir}/gozerbot/gozerbot.cron
# if needed, move to datadir
rm -f $RPM_BUILD_ROOT%{_bindir}/gozerinit
# if need, package it, likely some subpkg, initially won't pkg trash
rm -f $RPM_BUILD_ROOT%{_datadir}/gozerbot/mailudp.py
rm -f $RPM_BUILD_ROOT%{_datadir}/gozerbot/nagios-udp
rm -f $RPM_BUILD_ROOT%{_datadir}/gozerbot/onconnect
rm -f $RPM_BUILD_ROOT%{_datadir}/gozerbot/pickletodb.py
rm -f $RPM_BUILD_ROOT%{_datadir}/gozerbot/toudp.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/gozerbot
%dir %{_datadir}/gozerbot
%{_datadir}/gozerbot/gb_db
%{_datadir}/gozerbot/postgres_db
%{_datadir}/gozerbot/sqlite_db
%{py_sitescriptdir}/gozerbot
%{py_sitescriptdir}/gozerplugs
