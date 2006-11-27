# TODO
# - smarty cache dirs to /var/cache
%define	_snap 06062005
Summary:	WPKG - HTTP backend
Summary(pl):	WPKG - Interfejs WWW
Name:		wpkg-http
Version:	0.0.%{_snap}
Release:	0.7
License:	GPL v2
Group:		Applications
Source0:	http://dl.sourceforge.net/wpkg/%{name}-%{_snap}.tar.gz
# Source0-md5:	033e6251fb80db3ec1207f83155a5b6b
Source1:	%{name}_apache.conf
Patch0:		%{name}-config.patch
URL:		http://wpkg.sourceforge.net/
Requires:	Smarty >= 2.6.10-4
Requires:	webserver = apache
Requires:	webserver(php)
Requires:	wpkg
Conflicts:	apache1 < 1.3.33-2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_appdir		%{_datadir}/%{name}

%description
Web backend for configuration WPKG.

%description -l pl
Konfigurator WWW dla WPKG.

%prep
%setup -q -n wpkg
%patch0 -p1
rm INSTALL xml/{hosts.xml,packages.xml,profiles.xml} root/wpkg.tar.gz

rm -rf libs/smarty

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}

cp -Rv *		$RPM_BUILD_ROOT%{_appdir}
#install hosts.xml 	$RPM_BUILD_ROOT%{_sysconfdir}/hosts.xml
#install packages.xml	$RPM_BUILD_ROOT%{_sysconfdir}/packages.xml

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf

mv $RPM_BUILD_ROOT%{_appdir}/config/* $RPM_BUILD_ROOT%{_sysconfdir}
cd $RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_sysconfdir}/config.xml	config.xml
cd $RPM_BUILD_ROOT%{_appdir}/xml
ln -s %{_sysconfdir}/hosts.xml	hosts.xml
ln -s %{_sysconfdir}/packages.xml packages.xml
ln -s %{_sysconfdir}/profiles.xml profiles.xml
touch $RPM_BUILD_ROOT%{_sysconfdir}/htpasswd

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%apache_config_install -v 1 -c %{_sysconfdir}/apache.conf -n 98

%triggerun -- apache1 < 1.3.37-3, apache1-base
%apache_config_uninstall -v 1 -n 98

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache.conf -n 98

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2 -n 98

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.xml
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/htpasswd

%dir %{_appdir}
%{_appdir}/*
