### RPM cms PHEDEX-webapp WEBAPP_BETA_0_9
# note: trailing letters in version are ignored when fetching from cvs
## INITENV +PATH PERL5LIB %i/perl_lib
%define downloadn %(echo %n | cut -f1 -d-)
%define nversion %(echo %v | sed 's|APPSERV_||' | sed 's|_|.|g')
%define cvsversion %(echo %v | sed 's/[a-z]$//')
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
%define deployutil WTDeployUtil.pm
%define deployutilrev 1.6
%define deployutilurl http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/COMP/WEBTOOLS/Configuration/%{deployutil}?revision=%{deployutilrev}

Source: %cvsserver&strategy=checkout&module=%{downloadn}&export=%{downloadn}&&tag=-r%{cvsversion}&output=/%{n}.tar.gz
Requires: protovis yui PHEDEX-datasvc

# We obsolete each previous release to force them to be removed
# Prior to BETA_0_9, WEBAPP was known as APPSERV
Obsoletes: cms+PHEDEX-appserv+APPSERV_BETA_0_8
Obsoletes: cms+PHEDEX-appserv+APPSERV_BETA_0_7
Obsoletes: cms+PHEDEX-appserv+APPSERV_BETA_0_5
Obsoletes: cms+PHEDEX-appserv+APPSERV_BETA_0_4
Obsoletes: cms+PHEDEX-appserv+APPSERV_BETA_0_2
Obsoletes: cms+PHEDEX-appserv+APPSERV_BETA_0_1

%prep
%setup -n PHEDEX
wget -O %{deployutil} '%{deployutilurl}'

%build
echo 'now in the build section'
pwd
cd %_builddir
sh %_builddir/PHEDEX/PhEDExWeb/ApplicationServer/util/phedex-minify.sh
rm -rf %_builddir/PHEDEX/PhEDExWeb/{ApplicationServer/{js,css,util},yuicompressor*}
mv %_builddir/PHEDEX/PhEDExWeb/ApplicationServer/{build/*,}
rmdir %_builddir/PHEDEX/PhEDExWeb/ApplicationServer/build

%install
mkdir -p %i/etc
tar -cf - * | (cd %i && tar -xf -)
echo 'manifest of installation'
find %i -type f

rm -f %instroot/apache2/apps.d/appserv-httpd.conf

# Set template variables in deployment files
export DOCUMENT_ROOT=%i/PhEDExWeb/ApplicationServer
export VERSION=%nversion
perl -I  $RPM_INSTALL_PREFIX/%{pkgrel} -MWTDeployUtil -p -i -e '
  s|\@SERVER_ROOT\@|%instroot/apache2|g;
  s|\@DOCUMENT_ROOT\@|$ENV{DOCUMENT_ROOT}|g;
  s|\@YUI_ROOT\@|$ENV{YUI_ROOT}|g; \
  s|\@PROTOVIS_ROOT\@|$ENV{PROTOVIS_ROOT}|g;' \
  %i/PhEDExWeb/ApplicationServer/conf/appserv-httpd.conf

export APPSERV_BASEURL='/phedex/datasvc/app'
perl -p -i -e "s|\@APPSERV_VERSION\@|$VERSION|g; \
               s|\@APPSERV_BASEURL\@|$APPSERV_BASEURL|g;" \
  %i/PhEDExWeb/ApplicationServer/js/phedex-base{,-loader}{,-min}.js
cp %i/PhEDExWeb/ApplicationServer/html/phedex{,-debug}.html
# Replace the base and loader files with the rollup, and switch everything to minified files.
# Also explicitly turn off combo-serving, for now.
perl -p -i -e 's|phedex-base.js|phedex-base-loader.js|; \
	      s|^.*phedex-loader.js.*||; \
	      s|phedex([a-z,-]+).js|phedex\1-min.js|g; \
	      s|PHEDEX.Appserv.combineRequests.*$|PHEDEX.Appserv.combineRequests = false;|g;' \
  %i/PhEDExWeb/ApplicationServer/html/phedex.html

%post
perl -I  $RPM_INSTALL_PREFIX/%{pkgrel} -MWTDeployUtil -p -i -e '
  $hosts = join(",", &WTDeployUtil::frontend_hosts());
  s|\@FRONTEND_HOSTS\@|$hosts|g;' \
  $RPM_INSTALL_PREFIX/%{pkgrel}/PhEDExWeb/ApplicationServer/conf/appserv-httpd.conf

SERVER_CONF=$RPM_INSTALL_PREFIX/apache2/apps.d
INSTALL_CONF=PhEDExWeb/ApplicationServer/conf
FULL_INSTALL_CONF=$RPM_INSTALL_PREFIX/%{pkgrel}/$INSTALL_CONF
%{relocateConfig}$INSTALL_CONF/appserv-httpd.conf

# copy to apps.d/ directory.  Note: we must ensure that this config is
# sourced after datasvc-httpd.conf, so we give it a similar name
cp -p $FULL_INSTALL_CONF/appserv-httpd.conf $SERVER_CONF/datasvc-xappserv.conf

# Provide helpful symlink
ln -s $RPM_INSTALL_PREFIX/PHEDEX-webapp .

%files
%i/
# does not work.  
#%instroot/apache2/apps.d/datasvc-httpd.conf.02-appserv
#%attr(444,-,-) %config %instroot/apache2/apps.d/datasvc-httpd.conf.02-appserv
