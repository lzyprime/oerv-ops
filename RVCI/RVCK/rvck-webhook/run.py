#!/bin/python3

import json
import os


def write_properties_file(info: dict):
    for k, v in info.items():
        if v is None:
            continue
        open(k, 'w').write(str(v))

def check_params(params: dict):
    """检查参数是否合法"""

    # 检查文件是否存在
    for k in ['lava_template','testcase_url',]:
        if k in params and os.system(f'gh api repos/RVCK-Project/lavaci/contents/{params[k]}'):
            raise Exception(f"{k}={params[k]} not found in RVCK-Project/lavaci")
    
    # 检查testcase是否支持
    if 'testcase_url' in params and len(params['testcase']):
        import yaml,json,base64
        file_content = yaml.safe_load(base64.b64decode(json.loads(os.popen(f'gh api repos/RVCK-Project/lavaci/contents/{params["testcase_url"]}').read())["content"]).decode())
        print("all support testcase:", file_content["params"]["TST_CMDFILES"])
        if params['testcase'] not in file_content["params"]["TST_CMDFILES"]:
            raise Exception(f"testcase={params['testcase']} not support")

    return params

def parse_comment(comment: str):
    """解析comment内容, /check"""
    if not comment.strip().startswith("/check"):
        print(comment.strip(), "| not found /check, ignore")
        return None
    
    if len("/check") == len(comment.strip()):
        return {}

    import shlex
    res = check_params({
        item[0]: item[1].strip("'\"") if len(item) == 2 else ""
        for item in [
            str(i).split('=',maxsplit=1)
        for i in shlex.split(comment.strip()[6:])]
    })
    
    for k, v in res.items():
        print(f"{k} = '{v}'")
    
    return res


def issue_comment(payload: dict):
    """pr|issue comment 触发"""

    # comment 创建
    if payload["action"] != "created":
        return

    res = parse_comment(str(payload["comment"]["body"]))

    if res is None:
        return

    res["REPO"] = payload["repository"]["clone_url"]
    res["ISSUE_ID"] = payload["issue"]["number"]

    # FETCH_REF
    if "pull_request" in payload["issue"]:  # pr
        res["FETCH_REF"] = f"pull/{res['ISSUE_ID']}/head"

    if not len(res.get("fetch", "")) and "FETCH_REF" not in res:
        raise Exception("params:fetch is required")

    res["FETCH_REF"] = res["fetch"]
    
    write_properties_file(res)


def pull_request(payload: dict):
    # pr 创建
    if payload["action"] != "opened":
        return
    res = parse_comment(str(payload["pull_request"]["body"]))
    if res is None:
        return

    print("from pr opened")

    res["REPO"] = payload["repository"]["clone_url"]
    res["ISSUE_ID"] = payload["number"]
    res["FETCH_REF"] = f"pull/{res['ISSUE_ID']}/head"

    write_properties_file(res)


def issues(payload: dict):
    # issue 创建
    if payload["action"] != "opened":
        return
    
    # 解析内容
    res = parse_comment(str(payload["issue"]["body"]))
    if res is None:
        return

    if not len(res.get("fetch", "")):
        raise Exception("params:fetch is required")
    res["FETCH_REF"] = res["fetch"]
    res["REPO"] = payload["repository"]["clone_url"]
    res["ISSUE_ID"] = payload["issue"]["number"]

    write_properties_file(res)



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
    p= os.getenv("payload", "")
    if len(p):
        main()

