diff --git a/Makefile.am b/Makefile.am
index e665b8f..64a4442 100644
--- a/Makefile.am.save
+++ b/Makefile.am
@@ -1,13 +1,10 @@
 ACLOCAL_AMFLAGS = -I m4
-SUBDIRS = src pyext data include bin doc test
+SUBDIRS = src pyext data include bin test
 
 #dist_pkgdata_DATA = rivetenv.sh rivetenv.csh
 EXTRA_DIST = GUIDELINES
 
-doc:
-	cd doc && $(MAKE) doc
-
-.PHONY : doc dox pyclean
+.PHONY : dox pyclean
 
 clean-local:
 	@rm -rf a.out
diff --git a/Makefile.in b/Makefile.in
index 8cf62fd..85fb528 100644
--- a/Makefile.in.save
+++ b/Makefile.in
@@ -325,7 +325,7 @@ top_build_prefix = @top_build_prefix@
 top_builddir = @top_builddir@
 top_srcdir = @top_srcdir@
 ACLOCAL_AMFLAGS = -I m4
-SUBDIRS = src pyext data include bin doc test
+SUBDIRS = src pyext data include bin test
 
 #dist_pkgdata_DATA = rivetenv.sh rivetenv.csh
 EXTRA_DIST = GUIDELINES
@@ -870,10 +870,7 @@ uninstall-am: uninstall-local
 	uninstall-local
 
 
-doc:
-	cd doc && $(MAKE) doc
-
-.PHONY : doc dox pyclean
+.PHONY : dox pyclean
 
 clean-local:
 	@rm -rf a.out
