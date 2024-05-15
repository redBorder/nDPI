# 
# RPM Build Process
#
APPL=libndpi
PLATFORM=x86_64
GIT_REVISION=4764
PACKAGE_VERSION=3.4.0
PACKAGE=$(APPL)-$(PACKAGE_VERSION)-$(GIT_REVISION).$(PLATFORM).rpm
DEV_PACKAGE=$(APPL)-dev-$(PACKAGE_VERSION)-$(GIT_REVISION).$(PLATFORM).rpm
PACKAGE_PATH=$(HOME)/rpmbuild/RPMS/$(PLATFORM)/$(PACKAGE)
PACKAGE_NAME?=	$(APPL)

PACKAGE_NAME?=	$(APPL)
VERSION?=	$(PACKAGE_VERSION)
BUILD_NUMBER?= 1
MOCK_CONFIG?=default
RESULT_DIR?=pkgs

all: rpm

package: rpm

build-src:
	cd ../..; ./autogen.sh; ./configure; make clean; make

cleanup-rpm:
	rm -rf $(HOME)/rpmbuild/BUILD/ndpi* $(HOME)/rpmbuild/SOURCES/ndpi*

build-rpm: build-src cleanup-rpm
	-rm -rf ndpi-3.4.0
	mkdir -p ndpi-3.4.0/packages
	cp ndpi.spec.in ndpi-3.4.0/packages
	cp ../../Makefile.* ../../libtool ../../configure* ../../config.* ../../install-sh ../../autogen.sh ndpi-3.4.0
	cp -rf ../../src ndpi-3.4.0 
	cp ../../CHANGELOG.md ../../COPYING ndpi-3.4.0 
	\rm -f ndpi-3.4.0/config.status
	mkdir -p $(HOME)/rpmbuild/SOURCES
	tar cvfz $(HOME)/rpmbuild/SOURCES/ndpi-3.4.0.tgz ndpi-3.4.0
	@rm -f $(HOME)/rpmbuild/RPMS/$(PLATFORM)/$(PACKAGE)
	@rpmbuild -bb ./$(APPL).spec --define "buildnumber $(GIT_REVISION)"
	@if [[ $EUID -ne 0 ]]; then ./rpm-sign.exp $(HOME)/rpmbuild/RPMS/$(PLATFORM)/$(PACKAGE); fi
	@if [[ $EUID -ne 0 ]]; then ./rpm-sign.exp $(HOME)/rpmbuild/RPMS/$(PLATFORM)/$(DEV_PACKAGE); fi
	@echo ""
	@echo "Package contents:"
	@rpm -qpl $(HOME)/rpmbuild/RPMS/$(PLATFORM)/$(PACKAGE)
	@echo "The package is now available in $(HOME)/rpmbuild/RPMS/$(PLATFORM)/$(PACKAGE)"

SOURCES:
	mkdir -p SOURCES

archive: SOURCES
	rm -rf libndpi-3.4.0
	mkdir -p libndpi-3.4.0/packages
	cp libndpi-mock.spec.in libndpi-3.4.0/packages
	cp ../../Makefile.* ../../libtool ../../configure* ../../config.* ../../install-sh ../../autogen.sh ../../libndpi.pc.in libndpi-3.4.0
	cp -rf ../../src libndpi-3.4.0 
	cp -rf ../../example libndpi-3.4.0 
	cp -rf ../../tests libndpi-3.4.0 
	cp -rf ../../python libndpi-3.4.0 
	cp -rf ../../fuzz libndpi-3.4.0 
	cp -rf ../../packages/etc libndpi-3.4.0/packages
	cp ../../CHANGELOG.md ../../COPYING libndpi-3.4.0 
	\rm -f libndpi-3.4.0/config.status
	tar cvfz SOURCES/libndpi-3.4.0.tgz libndpi-3.4.0

build_prepare: archive
	mkdir -p $(RESULT_DIR)
	rm -f $(RESULT_DIR)/$(PACKAGE_NAME)*.rpm

srpm: build_prepare
	/usr/bin/mock \
		-r $(MOCK_CONFIG) \
		--define "__version $(VERSION)" \
		--define "__release $(BUILD_NUMBER)" \
		--resultdir=$(RESULT_DIR) \
		--buildsrpm \
		--spec=${PACKAGE_NAME}-mock.spec \
		--sources=SOURCES
	@echo "======= Source RPM now available in $(RESULT_DIR) ======="

rpm: srpm
	/usr/bin/mock \
		-r $(MOCK_CONFIG) \
		--define "__version $(VERSION)"\
		--define "__release $(BUILD_NUMBER)"\
		--resultdir=$(RESULT_DIR) \
		--rebuild $(RESULT_DIR)/$(PACKAGE_NAME)*.src.rpm
	@echo "======= Binary RPMs now available in $(RESULT_DIR) ======="

clean:
	rm -rf SOURCES pkgs

distclean: clean
	rm -f build.log root.log state.log available_pkgs installed_pkgs \
		*.rpm *.tar.gz
