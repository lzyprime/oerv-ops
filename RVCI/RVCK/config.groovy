
all_params = [
    string(description: '指定所属仓库, 用于gh ... -R "$REPO"', name: 'REPO'),
    string(description: 'PR发起的ID号', name: 'pr_id'),
    string(description: 'PR发起的链接', name: 'pr_id_url'),
    string(defaultValue: 'lava-testcases/common/ltp/ltp.yaml', description: '需要执行的用例yaml 文件路径', name: 'testcase_url'),
    string(defaultValue: 'math', description: 'ltp测试时，指定测试套', name: 'testcase'), 
    string(description: '目标PR分支', name: 'dst_pr'),
    string(description: '目标分支上的commit提交 哈希值', name: 'dst_pr_sha'),
    
    string(description: '需要评论的issue|pr id', name: 'ISSUE_ID', trim: true),
    text(description: '评论内容, 用于 gh issue $ISSUE_ID -b "$COMMENT_CONTENT"', name: 'COMMENT_CONTENT'),
    string(description: '清空所有标签并设置新LABEL, 多个以英文逗号 \',\' 分割, 不能与ADD_LABEL,REMOVE_LABEL混用', name: 'SET_LABEL', trim: true),
    string(description: '添加标签，多个以英文逗号 \',\' 分割 ', name: 'ADD_LABEL', trim: true),
    string(description: '添加标签，多个以英文逗号 \',\' 分割 ', name: 'REMOVE_LABEL', trim: true),
    string(description: '内核下载链接', name: 'kernel_download_url', trim: true), 
    string(description: 'rootfs下载链接', name: 'rootfs_download_url', trim: true), 
]

kernel_build_params_keys = [
    "pr_id",
    "pr_id_url",
    "REPO",
    'dst_pr',
    "dst_pr_sha",
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

return this;