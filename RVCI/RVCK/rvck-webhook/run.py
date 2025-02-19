#!/bin/python3

import json
import os

# 需要获取并传递的变量
all_keys = {
    "pr_id",
    "pr_id_url",
    "REPO",
    'dst_pr',
    "dst_pr_sha",
    'lava_template',
    'testcase_url',
    'testcase',
}


def write_properties_file(info: dict):
    assert all([k in all_keys for k in info])
    for k, v in info.items():
        if v is None:
            continue
        open(k, 'w').write(str(v))


def parse_comment(comment: str):
    """解析comment内容, /check ${lava_template} ${testcase_url} ${testcase}"""

    params_keys = ["lava_template", "testcase_url", "testcase"]
    items = comment.strip().split()
    if items[0] != "/check" or not (len(items) == len(params_keys) + 1 or len(items) == 1):
        print("comment:", comment.strip(), "| ignore")
        return None

    return {
        k: items[idx + 1] if idx + 1 < len(items) else None
        for idx, k in enumerate(params_keys)
    }


def issue_comment(payload: dict):
    """pr|issue comment 触发"""

    # comment 创建
    if payload["action"] != "created":
        return

    if "pull_request" in payload["issue"]:  # pr
        # 解析评论内容
        res = parse_comment(str(payload["comment"]["body"]))
        if res is None:
            return

        cmd_output = os.popen(
            f'gh pr view {payload["issue"]["number"]} --json baseRefOid,baseRefName -R {payload["repository"]["clone_url"]}').read()
        print("gh pr view:", cmd_output)
        pr_info = json.loads(cmd_output)

        # 保存参数
        print("from pr comment")
        res["pr_id"] = payload["issue"]["number"]
        res["pr_id_url"] = payload["issue"]["pull_request"]["html_url"]
        res["REPO"] = payload["repository"]["clone_url"]
        res['dst_pr'] = pr_info["baseRefName"]
        res["dst_pr_sha"] = pr_info["baseRefOid"]

        write_properties_file(res)

    else:  # 普通issue
        pass


def pull_request(payload: dict):
    # pr 创建
    if payload["action"] != "opened":
        return
    res = parse_comment(str(payload["pull_request"]["body"]))
    if res is None:
        return

    print("from pr opened")

    res["pr_id"] = payload["number"]
    res["pr_id_url"] = payload["pull_request"]["url"]
    res["REPO"] = payload["repository"]["clone_url"]
    res["dst_pr"] = payload["pull_request"]["base"]["sha"]["ref"]
    res["dst_pr_sha"] = payload["pull_request"]["base"]["sha"]

    write_properties_file(res)


def issues(payload: dict):
    pass


support_actions = {
    i.__name__: i
    for i in [issue_comment, pull_request, issues]
}


def main():
    gh_event = os.getenv("x_github_event", "")

    if gh_event not in support_actions:
        raise Exception("unknown event:", gh_event)

    support_actions[gh_event](payload=json.loads(os.getenv("payload", '{}')))


if __name__ == "__main__":
    main()
