%define pkgname	elgg
%define gettext	1

Summary:	A powerful open source social networking engine
Name:		elgg
Version:	1.8.15
Release:	1%{?dist}
License:	GPLv2+
Group:		Applications/Internet
URL:		http://www.elgg.org/
Source0:	http://elgg.org/getelgg.php?forward=%{pkgname}-%{version}.tar.gz
Source1:	elgg.conf
#Source1:	phpMyAdmin-config.inc.php
#Source2:	phpMyAdmin.htaccess
%if 0%{?rhel} != 5
Requires:	httpd, php >= 5.2.0, php-mysql >= 5.2.0, php-xml >= 5.4
Requires:	php-mbstring >= 5.2.0, php-gd >= 5.2.0
%if %{gettext}
Requires:	php-php-gettext
%endif
%else
Requires:	httpd, php53, php53-mysql, php53-mbstring, php53-gd, php53-xml
%if %{gettext}
Requires:	php53-php-gettext
%endif
Provides:	elgg = %{version}-%{release}
%endif
Provides:	elgg = %{version}-%{release}
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Elgg is an award-winning open source social networking engine that provides
a robust framework on which to build all kinds of social environments, from
a campus wide social network for your university, school or college or an
internal collaborative platform for your organization through to a
brand-building communications tool for your company and its clients.

%prep
#%setup -q -n %{pkgname}-%{version}-all-languages

# Setup vendor config file
#sed -e "/'CHANGELOG_FILE'/s@./ChangeLog@%{_datadir}/doc/%{name}-%{version}/ChangeLog@" \
#    -e "/'LICENSE_FILE'/s@./LICENSE@%{_datadir}/doc/%{name}-%{version}/LICENSE@" \
#    -e "/'CONFIG_DIR'/s@'./'@'%{_sysconfdir}/%{pkgname}/'@" \
#    -e "/'SETUP_CONFIG_FILE'/s@./config/config.inc.php@%{_localstatedir}/lib/%{pkgname}/config/config.inc.php@" \
#%if %{gettext}
#    -e "/'GETTEXT_INC'/s@./libraries/php-gettext/gettext.inc@%{_datadir}/php/gettext/gettext.inc@" \
#%endif
#    -i libraries/vendor_config.php

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT{%{_datadir}/%{pkgname},%{_sysconfdir}/httpd/conf.d}


#mkdir -p $RPM_BUILD_ROOT{%{_datadir}/%{pkgname}}
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/%{pkgname}
#mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/%{pkgname}/{upload,save,config}
cp -ad * $RPM_BUILD_ROOT%{_datadir}/%{pkgname}
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{pkgname}.conf
#install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{pkgname}/config.inc.php

rm -f $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/{[CIRLT]*,*txt}
rm -f $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/{libraries,setup/{lib,frames}}/.htaccess
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/contrib

%if %{gettext}
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/libraries/php-gettext/
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
#%doc ChangeLog CHANGES.txt CODING.txt CONTRIBUTORS.txt COPYRIGHT.txt LICENSE.txt README.txt INSTALL INSTALL.fedora UPGRADE.txt
%{_datadir}/%{pkgname}/
#%dir %{_sysconfdir}/%{pkgname}/
#%config(noreplace) %{_sysconfdir}/%{pkgname}/config.inc.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{pkgname}.conf
%dir %{_sharedstatedir}/%{pkgname}/
%dir %attr(0755,apache,apache) %{_sharedstatedir}/%{pkgname}
#%dir %attr(0755,apache,apache) %{_localstatedir}/lib/%{pkgname}/upload
#%dir %attr(0755,apache,apache) %{_localstatedir}/lib/%{pkgname}/save
#%dir %attr(0755,apache,apache) %{_localstatedir}/lib/%{pkgname}/config

%changelog
* Tue May 14 2013 Andrew Hatfield <andrew.hatfield@cynosureservices.com> 1.8.15-1
- Created RPM package for Fedora 18

