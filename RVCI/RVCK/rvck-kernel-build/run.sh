#!/bin/bash
set -e
set -x

# init env
if [ "$REPO" = "" ] || [ "$ISSUE_ID" = "" ] || [ "$FETCH_REF" = "" ]; then
	echo "REPO ISSUE_ID FETCH_REF is required"
	exit 1
fi

repo_name="$(echo "${REPO##h*/}" | awk -F'.' '{print $1}')"
kernel_result_dir="${repo_name}_pr_${ISSUE_ID}"
download_server=10.213.6.54
rootfs_download_url="http://${download_server}/openEuler24.03-LTS-SP1/openeuler-rootfs.img"
kernel_download_url="http://${download_server}/kernel-build-results/${kernel_result_dir}/Image"

# yum install 
sudo yum makecache
sudo yum install -y git make flex bison bc gcc elfutils-libelf-devel openssl-devel dwarves

# git clone
# git clone -b ${dst_pr} --progress --depth=1 ${REPO} work && pushd work
git init work && pushd work
git config user.email rvci@isrc.iscas.ac.cn
git config user.name rvci
git remote add origin "${REPO}"
git fetch origin "${FETCH_REF}":local --depth=1 --progress
git checkout local

# git am patch
# curl -L ${pr_patch} | git am -3 --empty=drop 2>&1

# build 
make openeuler_defconfig
#make th1520_defconfig
make -j"$(nproc)"

# cp Image
mkdir "${kernel_result_dir}"
cp -v arch/riscv/boot/Image "${kernel_result_dir}"


if [ -f "${kernel_result_dir}/Image" ];then
	cp -vr "${kernel_result_dir}" /mnt/kernel-build-results/
	# pass download url
	echo "${kernel_download_url}" > kernel_download_url
	echo "${rootfs_download_url}" > rootfs_download_url
else
	echo "Kernel not found!"
	exit 1
fi
popd
