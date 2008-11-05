# TODO
# - initscript
# - patch code to support output logging
# - patch code to support daemonizing
# - patch code to switch uid
# - config from /etc when ran as service
Summary:	gozerbot is the Python IRC bot and Jabber bot in one
Name:		gozerbot
Version:	0.8.1.1
Release:	0.5
License:	BSD
Group:		Applications/Communications
Source0:	http://www.gozerbot.org/media/tarball/%{name}-%{version}.tar.gz
# Source0-md5:	f94037651700737f655f28244662c5a0
Source1:	%{name}.init
Patch0:		%{name}-pyc.patch
URL:		http://www.gozerbot.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	python >= 1:2.4
Provides:	group(gozerbot)
Provides:	user(gozerbot)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_rundir		/var/lib/%{name}

%description
Python IRC bot and Jabber bot in one.

%prep
%setup -q
%patch0 -p1
%{__grep} -rl '#!/usr/bin/env python' . | xargs %{__sed} -i -e '1s,#!.*bin/env python,#!%{__python}',

%build
%{__python} setup.py build

# build datadir
./bin/gozerinit

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_rundir},%{_mandir}/man1}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/gozerbot
cp -a man/gozerbot.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -a gozerdata $RPM_BUILD_ROOT%{_rundir}

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

%pre
%groupadd -g 205 -r -f gozerbot
%useradd -u 205 -r -d %{_rundir} -s /bin/sh -c "gozerbot" -g gozerbot gozerbot

%post
/sbin/chkconfig --add gozerbot
%service gozerbot restart

%preun
if [ "$1" = "0" ]; then
	%service -q gozerbot stop
	/sbin/chkconfig --del gozerbot
fi

%postun
if [ "$1" = "0" ]; then
	%userremove gozerbot
	%groupremove gozerbot
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(754,root,root) /etc/rc.d/init.d/gozerbot
%attr(755,root,root) %{_bindir}/gozerbot
%{_mandir}/man1/gozerbot.1*
%dir %{_datadir}/gozerbot
%{_datadir}/gozerbot/gb_db
%{_datadir}/gozerbot/postgres_db
%{_datadir}/gozerbot/sqlite_db
%{py_sitescriptdir}/gozerbot
%{py_sitescriptdir}/gozerplugs

%dir %attr(775,root,gozerbot) %{_rundir}
%dir %attr(775,root,gozerbot) %{_rundir}/gozerdata
%dir %attr(775,root,gozerbot) %{_rundir}/gozerdata/userstates
# XXX: move to %{_sysconfdir}
%attr(660,root,gozerbot) %config(noreplace) %verify(not md5 mtime size) %{_rundir}/gozerdata/config
