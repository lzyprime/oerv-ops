allParams = [
    'REPO': string(description: '指定所属仓库, 用于gh ... -R "$REPO"', name: 'REPO'),
    "FETCH_REF": string(description: '需要拉去的提交，commit_sha或分支名, git fetch $FETCH_REF', name: 'FETCH_REF'),
    'ISSUE_ID': string(description: '需要评论的issue|pr id', name: 'ISSUE_ID', trim: true),
    
    'kernel_download_url': string(description: '内核下载链接', name: 'kernel_download_url', trim: true), 
    'rootfs_download_url': string(description: 'rootfs下载链接', name: 'rootfs_download_url', trim: true),
    'lava_template': string(defaultValue: 'lava-job-template/qemu/qemu-ltp.yaml', description: 'lava测试模板', name: 'lava_template'),
    'testcase_url': string(defaultValue: 'lava-testcases/common-test/ltp/ltp.yaml', description: '需要执行的用例yaml 文件路径', name: 'testcase_url'),
    'testcase': string(defaultValue: 'math', description: 'ltp测试时，指定测试套', name: 'testcase'),

    'COMMENT_CONTENT': text(description: '评论内容, 用于 gh issue $ISSUE_ID -b "$COMMENT_CONTENT"', name: 'COMMENT_CONTENT'),
    'SET_LABEL': string(description: '清空所有标签并设置新LABEL, 多个以英文逗号 \',\' 分割, 不能与ADD_LABEL,REMOVE_LABEL混用', name: 'SET_LABEL', trim: true),
    'ADD_LABEL': string(description: '添加标签，多个以英文逗号 \',\' 分割 ', name: 'ADD_LABEL', trim: true),
    'REMOVE_LABEL': string(description: '添加标签，多个以英文逗号 \',\' 分割 ', name: 'REMOVE_LABEL', trim: true),
]

kernel_build_params_keys = [
    "REPO",
    "ISSUE_ID",
    "FETCH_REF",
    'lava_template',
    'testcase_url',
    'testcase',
]

gh_actions_params_keys = [
    "REPO",
    "ISSUE_ID",
    "COMMENT_CONTENT",
    "SET_LABEL",
    "ADD_LABEL",
    "REMOVE_LABEL",
]

lava_trigger_params_keys = [
    "REPO",
    "ISSUE_ID",
    "kernel_download_url",
    "rootfs_download_url",
    "lava_template",
    "testcase_url",
    "testcase",
]

return this