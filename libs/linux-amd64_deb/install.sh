#!/bin/sh

# Copyright(C) 2005-2017
#
# Этот файл содержит информацию, являющуюся
# собственностью компании Крипто-Про.
#
# Любая часть этого файла не может быть скопирована,
# исправлена, переведена на другие языки,
# локализована или модифицирована любым способом,
# откомпилирована, передана по сети с или на
# любую компьютерную систему без предварительного
# заключения соглашения с компанией Крипто-Про.
#
# This is proprietary information of
# Crypto-Pro company.
#
# Any part of this file can not be copied,
# corrected, translated into other languages,
# localized or modified by any means,
# compiled, transferred over a network from or to
# any computer system without preliminary
# agreement with Crypto-Pro company

# IMPORTANT NOTE
# echo's to stdout are redirected to gui-notifications,
# so don't change output stream if not necessary.

COMPAT_VERSION="1.0.0-1"
VERSION="[25.0].*-[16]"
PACKAGE_NAMES=""
FROM_REPO=0

# Exit codes.
SUCCESS=0
FAILURE=1
PACKAGES_NOT_AVAILABLE=2

localize() {
    if test "$LANG" = "ru_RU.UTF-8" || test "$LANG" = "ru_RU.utf8"; then
        PRODUCT_NAME="КриптоПро CSP"
	ERROR_root="Ошибка: этот скрипт надо запускать от имени root или с помощью sudo"
	ERROR_lsb="Ошибка: установка завершилась неуспехом. Возможно, не хватает пакета LSB из
состава ОС. Попробуйте установить пакет LSB и переустановить ${PRODUCT_NAME}.
Если вы всё ещё испытываете проблемы, обратитесь к документации
или на портал техподдержки: https://support.cryptopro.ru"
	ERROR_debian="Ошибка: вы пытаетесь установить debian-дистрибутив на не-debian систему"
	ERROR_missing="Ошибка: следующие пакеты не найдены:"
	SUCCESS_install="Пакеты ${PRODUCT_NAME} успешно установлены"
	MSG_installing="Установка"
	TEXT_help="Использование: ./install.sh [kc1|kc2] [пакет [...]]
  kc1: установить конфигурацию kc1 (по умолчанию)
  kc2: установить конфигурацию kc2 (не используйте без необходимости)
  [пакет [...]]: список имён дополнительных пакетов
Примеры:
  ./install.sh kc1
  ./install.sh kc1 lsb-cprocsp-pkcs11 cprocsp-rdr-pcsc"
    else	
        PRODUCT_NAME="CryptoPro CSP"
	ERROR_root="Error: this script must be run as root or via sudo"
	ERROR_lsb="Error: installation failed. Maybe system LSB package is missing.
Install LSB package and reinstall ${PRODUCT_NAME}. If it does not help, please
read documentation or visit support: https://support.cryptopro.ru"
	ERROR_debian="Error: you are trying to install debian packages on not debian package system"
	ERROR_missing="Error: the following packages are missing:"
	SUCCESS_install="${PRODUCT_NAME} packages have been successfully installed"
	MSG_installing="Installing"
	TEXT_help="Usage: ./install.sh [kc1|kc2] [package [...]]
  kc1: install kc1 packages (by default)
  kc2: install kc2 packages (skip if not necessary)
  [package [...]]: list of additional packages
Examples:
  ./install.sh kc1
  ./install.sh kc1 lsb-cprocsp-pkcs11 cprocsp-rdr-pcsc"
    fi
}

parse_args() {
    _enclosure="kc1"
    while ! [ -z "$1" ] ; do
        case "$1" in
            "kc1")
                ;;
            "kc2")
                _enclosure="kc2"
                ;;
            "--from-repo")
                FROM_REPO=1
                ;;
            "-help"|"--help")
                show_help
                exit "${SUCCESS}"
                ;;
            *)
                _additional_packages="$*"
                break
                ;;
        esac
        shift
    done
    PACKAGE_NAMES="lsb-cprocsp-base \
lsb-cprocsp-rdr lsb-cprocsp-${_enclosure} lsb-cprocsp-capilite cprocsp-curl \
lsb-cprocsp-ca-certs \
${_additional_packages}"
}

show_help() {
    echo "$TEXT_help"
}

which_architecture() {
    machine_architecture="$(uname -m)"
    case "${machine_architecture}" in
        *64*|"e2k")
            bits_postfix="-64"
            ;;
        *)
            bits_postfix=""
            ;;
    esac
    case "${machine_architecture}" in
        arm*|"aarch64")
            is_arm=1
            ;;
        *)
            is_arm=0
            ;;
    esac
}

check_if_debian_system() {
    if [ -f /etc/debian_version ] ||
       [ -f /etc/mcst_version ] ||
        grep Ubuntu /etc/lsb-release > /dev/null 2>&1
    then
        is_debian_system=1
    else
        is_debian_system=0
    fi
}

check_release_attributes() {
    if ls ./lsb-cprocsp-base*.deb > /dev/null 2>&1 ; then
        is_debian_release=1
    else
        is_debian_release=0
    fi
    if ls ./lsb-cprocsp-base*.rpm > /dev/null 2>&1 ; then
        is_rpm_release=1
    else
        is_rpm_release=0
    fi
    if ls ./lsb-cprocsp-rdr-64* > /dev/null 2>&1 ; then
        is_64_release=1
    else
        is_64_release=0
    fi
}

# Use dpkg or alien on debian systems, otherwise use rpm.
set_inst_cmd() {
    if [ "${is_debian_system}" -eq 1 ] ; then
        if [ "${is_debian_release}" -eq 1 ] ; then
            inst_cmd="dpkg -i"
        else
            inst_cmd="alien -kci"
        fi
    else
        if [ "${is_rpm_release}" -eq 1 ] ; then
            inst_cmd="rpm -i"
        else
            echo "$ERROR_debian"
            exit "${FAILURE}"
        fi
    fi
}

# The release variables are used to construct full names of packages.
set_release_variables() {
    if [ "${is_debian_system}" -eq 1 ] &&
        [ "${is_debian_release}" -eq 1 ]
    then
        first_delimiter="_"
        noarch="all"
        second_delimiter="_"
        extension=".deb"
    else
        first_delimiter="-"
        noarch="noarch"
        second_delimiter="."
        extension=".rpm"
    fi
    alt_arch="dummy_arch"
    case "${machine_architecture}" in
        # Enforce to install 64-bit packages on 64-bit system.
        "x86_64"|"amd64")
            if [ "${is_debian_system}" -eq 1 ] &&
                [ "${is_debian_release}" -eq 1 ]
            then
                arch="amd64"
            else
                arch="x86_64"
                alt_arch="amd64"
            fi
            ;;
        "ppc64"|"ppc64le")
            arch="${machine_architecture}"
            ;;
        "aarch64")
            arch="${noarch}"
            if [ "${is_debian_system}" -eq 1 ] &&
                [ "${is_debian_release}" -eq 1 ]
            then
                alt_arch="aarch64"
            else
                alt_arch="arm64"
            fi
            ;;
        arm*)
            arch="${noarch}"
            alt_arch="armhf"
            ;;
        "mips")
            arch="${noarch}"
            alt_arch="mips"
            ;;
        "e2k")
	    if test -f /etc/altlinux-release ; then
		if cat /proc/cpuinfo | grep -q E2S ; then
		    arch="e2k"
		else
		    arch="e2kv4"
		fi
	    else	
		if [ "`uname -p`" = "E2S" ] ; then
		    arch="e2k-4c"
		else
		    arch="e2k-8c"
		fi
	    fi
            ;;
        *)
            if [ "${is_debian_system}" -eq 1 ] &&
                [ "${is_debian_release}" -eq 1 ]
            then
                arch="i386"
            elif ls ./*.i686.rpm > /dev/null 2>&1 ; then
                arch="i686"
                alt_arch="i386"
            else
                arch="i486"
            fi
            ;;
    esac
}

construct_compat_package() {
    compat_package=''
    # Return if lsb package is installed.
    if [ "${is_debian_system}" -eq 1 ] ; then
        if dpkg -s lsb-base >/dev/null 2>&1 ; then
            return
        fi
    elif rpm -q lsb-core >/dev/null 2>&1 ; then
        return
    fi
    # Не ставить compat на arm64.
    if [ "${is_arm}" -eq 1 ] && [ "${bits_postfix}" = "-64" ] ; then
        return
    fi
    if [ "${is_arm}" -eq 1 ] ; then
        _distr='armhf'
    elif [ -f /etc/mcst_version ] ; then
        _distr='mcst'
    elif [ -f /etc/cp-release ] ; then
        if grep Gaia /etc/cp-release >/dev/null 2>&1 ; then
            _distr='gaia'
        else
            _distr='splat'
        fi
    elif [ -f /etc/altlinux-release ] ; then
        _distr="altlinux${bits_postfix}"
    elif [ -f /etc/os-rt-release ] ; then
        _distr="osrt${bits_postfix}"
    elif [ -f /etc/os-release ] && grep -q SUSE /etc/os-release ; then
        if rpm -q --whatprovides lsb-core-noarch >/dev/null 2>&1 ; then
            return
        else
            _distr='suse'
        fi
    else
        return
    fi
    compat_package="cprocsp-compat-\
${_distr}\
${first_delimiter}\
${COMPAT_VERSION}\
${second_delimiter}\
${noarch}\
${extension}"
}

construct_other_packages() {
    other_packages=""
    _absent=""
    for _name in ${PACKAGE_NAMES} ; do
        _package="${_name}"
        if [ "${is_64_release}" -eq 1 ] ; then
            _package="${_package}${bits_postfix}"
        fi
        _package="${_package}\
${first_delimiter}\
${VERSION}\
${second_delimiter}\
${arch}\
${extension}"
        if ! [ -f ${_package} ] ; then
            _package="${_name}"
            if [ "${is_64_release}" -eq 1 ] ; then
                _package="${_package}${bits_postfix}"
            fi
            _package="${_package}\
${first_delimiter}\
${VERSION}\
${second_delimiter}\
${alt_arch}\
${extension}"
        fi
        # There are several packages which are NOT architecture-specific,
        # e.g. lsb-cprocsp-base, lsb-cprocsp-ca-certs and devel-packages.
        # If the architecture-specific package is not found, try to install
        # the noarch package.
        # shellcheck disable=SC2086
        if ! [ -f ${_package} ] ; then
            _package="${_name}\
${first_delimiter}\
${VERSION}\
${second_delimiter}\
${noarch}\
${extension}"
        fi
        # Even the noarch package wasn't found.
        # shellcheck disable=SC2086
        if ! [ -f ${_package} ] ; then
            _absent="${_absent} ${_name}"
        else
            other_packages="${other_packages} ${_package}"
        fi
    done
    if ! [ -z "${_absent}" ] ; then
        echo "$ERROR_missing"
        echo "${_absent}" | xargs -n1 echo "*"
        exit "${PACKAGES_NOT_AVAILABLE}"
    fi
}


construct_list_of_packages() {
    packages=""
    construct_compat_package
    packages="${packages} ${compat_package}"
    # Other packages are the base packages and additional packages
    # specified by command-line arguments.
    construct_other_packages
    packages="${packages} ${other_packages}"
    # Remove duplicate packages.
    packages="$(
        echo "${packages}" \
            | awk '{for(i=1;i<=NF;i++)if(!a[$i]++)print $i}' | xargs
    )"
}

check_fail() {
    echo "$ERROR_lsb"
    exit "$1"
}

# Install packages one at a time before capilite, then batch install.
install_packages() {
    while ! [ -z "${packages}" ] ; do
        _head="$(echo "${packages}" | awk '{print $1}')"
        _tail="$(echo "${packages}" | awk '{for(i=2;i<=NF;i++)print $i}' | xargs)"
        eval "echo $MSG_installing ${_head} '...'" >&2
        eval "${inst_cmd} ${_head}" >&2 || check_fail "$?"
        if echo "${_head}" | grep capilite > /dev/null 2>&1 &&
            ! [ -z "${_tail}" ]
        then
            eval "echo $MSG_installing ${_tail} '...'" >&2
            eval "${inst_cmd} ${_tail}" >&2 || check_fail "$?"
            return
        fi
        packages="${_tail}"
    done
}

construct_list_of_packages_from_repository() {
    _tmp_repo="$(mktemp)"
    apt-cache dumpavail | grep -F 'Package: ' > "${_tmp_repo}"
    packages=""
    _absent=""
    for _name in ${PACKAGE_NAMES} ; do
        _package="${_name}${bits_postfix}"
        if ! grep -F "Package: ${_package}" "${_tmp_repo}" > /dev/null 2>&1
        then
            _package="${_name}"
        fi
        if grep -F "Package: ${_package}" "${_tmp_repo}" > /dev/null 2>&1
        then
            packages="${packages} ${_package}"
        else
            _absent="${_absent} ${_name}"
        fi
    done
    rm -f "${_tmp_repo}"
    if ! [ -z "${_absent}" ] ; then
        echo "$ERROR_missing"
        echo "${_absent}" | xargs -n1 echo "*"
        exit "${PACKAGES_NOT_AVAILABLE}"
    fi
    # Remove duplicate packages.
    packages="$(
        echo "${packages}" \
            | awk '{for(i=1;i<=NF;i++)if(!a[$i]++)print $i}' | xargs
    )"
}

main() {
    export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    localize
    if [ "$(id -u)" -ne 0 ] ; then
        echo "$ERROR_root"
        exit "${FAILURE}"
    fi
    cd "$(dirname "$0")" || check_fail "$?"
    parse_args "$@"
    which_architecture
    if [ "${FROM_REPO}" -eq 1 ] ; then
        construct_list_of_packages_from_repository
        sh ./uninstall.sh >&2 || check_fail "$?"
        eval "apt-get --yes install ${packages}" >&2 || check_fail "$?"
        echo "$SUCCESS_install"
        exit "${SUCCESS}"
    fi
    check_if_debian_system
    check_release_attributes
    set_inst_cmd
    set_release_variables
    construct_list_of_packages
    sh ./uninstall.sh >&2 || check_fail "$?"
    install_packages
    echo "$SUCCESS_install"
    exit "${SUCCESS}"
}

main "$@"
