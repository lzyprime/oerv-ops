#！/usr/bin/env bash
set -e
set -x

repo_name=$(echo ${REPO##h*/} | awk -F'.' '{print $1}')
qemu_job_name=${repo_name}_pr_${ISSUE_ID}
lava_template=lava-job-template/qemu/qemu-ltp.yaml
device_type=$(yq .device_type ${lava_template})
testcase_name=$(echo ${testcase_url} | awk -F'/' '{print $2}')
testitem_name=${repo_name}_${testcase_name}_${device_type}
testcase_repo=${GIT_URL}
ssh_port=$(od -An -N2 -i /dev/urandom | awk -v min=10000 -v max=20000 '{print min + ($1 % (max - min + 1))}')
lava_server=lava.oerv.ac.cn

lavacli_admim(){
    command=$1
    option=$2
    if [ ${option} = "show" ];then
    	option=${option}" --yaml"
    fi
    jobid=$3
    lavacli --uri https://${lava_admin_token}@${lava_server}/RPC2/ ${command} ${option} ${jobid}
}

yq e ".job_name |= sub(\"\\\${qemu_job_name}\",\"${qemu_job_name}\")" -i ${lava_template}
yq e ".context.extra_options[] |=  sub(\"hostfwd=tcp::10001-:22\", \"hostfwd=tcp::${ssh_port}-:22\")" -i ${lava_template}
yq e ".actions[0].deploy.images.kernel.url |= sub(\"\\\${qemu_kernel_image_url}\", \"${kernel_download_url}\")" -i ${lava_template}
yq e ".actions[0].deploy.images.rootfs.url |= sub(\"\\\${qemu_rootfs_image_url}\", \"${rootfs_download_url}\")" -i ${lava_template}
yq e ".actions[2].test.definitions[0].name |= sub(\"\\\${testitem_name}\",\"${testitem_name}\")" -i ${lava_template}
yq e ".actions[2].test.definitions[0].path |= sub(\"\\\${testcase_url}\",\"${testcase_url}\")" -i ${lava_template}
yq e ".actions[2].test.definitions[0].repository |= sub(\"\\\${testcase_repo}\",\"${testcase_repo}\")" -i ${lava_template}
yq e ".actions[2].test.definitions[0].parameters.TST_CMDFILES |= sub(\"\\\${ltp_testsuite}\",\"${testcase}\")" -i ${lava_template}


lava_jobid=$(lavacli_admim jobs submit ${lava_template})
lavacli_admim jobs wait ${lava_jobid}
sleep 5
lava_result_url=https://${lava_server}/scheduler/job/${lava_jobid}
lava_result=$(lavacli_admim jobs show ${lava_jobid} | yq .health)

if [ ${lava_result} = "Complete" ];then
	echo "Lava check pass! result url: ${lava_result_url}" > COMMENT_CONTENT
else
	echo "Lava check fail! result url: ${lava_result_url}" > COMMENT_CONTENT
	exit 1
fi
