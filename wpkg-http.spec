#TODO:
#- config for apache
Summary:	WPKG - HTTP backend
Summary(pl):	WPKG - Interfejs Webowy
Name:		wpkg-http
Version:	06062005
Release:	0.1
License:	GPL v.2
Group:		Applications
Source0:	http://dl.sourceforge.net/wpkg/%{name}-%{version}.tar.gz
# Source0-md5:	033e6251fb80db3ec1207f83155a5b6b
Source1:	%{name}_apache.conf
#Source2:	%{name}-
URL:		http://wpkg.sourceforge.net/
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:	wpkg
Requires:	httpd
Requires:	php

%description
Web backend for configuration WPKG.

%description -l pl
Webowy konfigurator dla WPKG
%prep
%setup -q -n wpkg

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name}/{classes,config,libs,locale,packages,root,smarty,xml},%{_sysconfdir}/{%{name},httpd/httpd.conf}}

rm INSTALL xml/{hosts.xml,packages.xml,profiles.xml} root/wpkg.tar.gz
cp -Rv *		$RPM_BUILD_ROOT%{_datadir}/%{name}/
#install hosts.xml 	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/hosts.xml
#install packages.xml	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/packages.xml

install %{SOURCE1}	$RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/98_wpkg-http.conf

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/config/* $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cd $RPM_BUILD_ROOT%{_datadir}/%{name}/config
ln -s %{_sysconfdir}/%{name}/config.xml	config.xml
cd $RPM_BUILD_ROOT%{_datadir}/%{name}/xml
ln -s %{_sysconfdir}/%{name}/hosts.xml	hosts.xml
ln -s %{_sysconfdir}/%{name}/packages.xml packages.xml 
ln -s %{_sysconfdir}/%{name}/profiles.xml profiles.xml 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
#%doc README TODO GPL-2 LICENSE
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd/httpd.conf/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
#%attr(755,root,root) %{_datadir}/%{name}/wpkg.js
#%{_datadir}/%{name}/*.xml
