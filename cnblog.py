#! /usr/bin/env python
# coding=utf-8

# 使用python xmlrpc 发送内容到博客园
# http://rpc.cnblogs.com/metaweblog/WeyneChen 从链接可以看到支持的metaweblog API
import xmlrpc.client as xmlrpclib
import glob
import os
import sys
import json
import time
import datetime

# 发布文章路径(article path)
art_path = "./articles/"
# 不发布文章路径(unpublished article path)
unp_path = "./unpublished/"
# 博客配置路径(config path)
cfg_path = "blog_config.json"
# 备份路径(backup path)
bak_path = "./backup/"
# 获取文章篇数
recentnum = 99999

# 创建路径
for path in [art_path, unp_path, bak_path]:
    if not os.path.exists(path):
        os.makedirs(path)

# -----配置读写操作-----
'''
配置字典：
type | description(example)
str  | metaWeblog url, 博客设置中有('https://rpc.cnblogs.com/metaweblog/nickchen121')
str  | appkey, Blog地址名('nickchen121')
str  | blogid, 这个无需手动输入，通过getUsersBlogs得到
str  | usr, 登录用户名
str  | passwd, 登录密码
'''


def exist_cfg():
    '''
    返回配置是否存在
    '''
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            try:
                cfg = json.load(f)
                if cfg == {}:
                    return False
                else:
                    return True
            except json.decoder.JSONDecodeError:  # 文件为空
                return False
    except:
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump({}, f)
            return False


def create_cfg():
    '''
    创建配置
    '''
    while True:
        cfg = {}
        for item in [("url", "metaWeblog url, 博客设置中有\
            ('https://rpc.cnblogs.com/metaweblog/blogaddress')"),
                     ("appkey", "Blog地址名('blogaddress')"),
                     ("usr", "登录用户名"),
                     ("passwd", "登录密码")]:
            cfg[item[0]] = input("输入" + item[1])
        try:
            server = xmlrpclib.ServerProxy(cfg["url"])
            userInfo = server.blogger.getUsersBlogs(
                cfg["appkey"], cfg["usr"], cfg["passwd"])
            print(userInfo[0])
            # {'blogid': 'xxx', 'url': 'xxx', 'blogName': 'xxx'}
            cfg["blogid"] = userInfo[0]["blogid"]
            break
        except:
            print("发生错误！")
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)


url = appkey = blogid = usr = passwd = ""
server = None
mwb = None
title2id = {}


def get_cfg():
    global url, appkey, blogid, usr, passwd, server, mwb, title2id
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
        url = cfg["url"]
        appkey = cfg["appkey"]
        blogid = cfg["blogid"]
        usr = cfg["usr"]
        passwd = cfg["passwd"]
        server = xmlrpclib.ServerProxy(cfg["url"])
        mwb = server.metaWeblog
        # title2id[title]=postid  储存博客中文章标题对应的postid
        print(cfg["blogid"], cfg["usr"], cfg["passwd"], recentnum)
        recentPost = mwb.getRecentPosts(
            cfg["blogid"], cfg["usr"], cfg["passwd"], recentnum)
        for post in recentPost:
            # 1.把datetime转成字符串
            dt = post["dateCreated"]
            # post["dateCreated"] = dt.strftime("%Y%m%dT%H:%M:%S")
            post["dateCreated"] = dt.__str__()
            # 2.把字符串转成datetime
            # datetime.datetime.strptime(st, "%Y%m%dT%H:%M:%S")
            # datetime.datetime.fromisoformat(str)
            title2id[post["title"]] = post["postid"]
        # 格式化成20160320-114539形式
        filename = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        with open(bak_path + filename + ".json", "w", encoding="utf-8") as f:
            json.dump(recentPost, f, indent=4)


# server = xmlrpclib.ServerProxy(url)
# userInfo = server.blogger.getUsersBlogs(appkey, usr, passwd)
# recentPost = mwb.getRecentPosts(blogid, usr, passwd, 9)
def newPost(blogid, usr, passwd, post, publish):
    while True:
        try:
            postid = mwb.newPost(blogid, usr, passwd, post, publish)
            break
        except:
            time.sleep(5)
    return postid


def post_art(path, publish=True):
    title = os.path.basename(path)  # 获取文件名做博客文章标题
    [title, fename] = os.path.splitext(title)  # 去除扩展名
    with open(mdfile, "r", encoding="utf-8") as f:
        post = dict(description=f.read(), title=title)
        post["categories"] = ["[Markdown]"]
        # 不发布
        if not publish:
            # 对于已经发布的文章，直接修改为未发布会报错：
            # xmlrpc.client.Fault: <'published post can not be saved as draft'>
            # 所以先删除这个文章
            # if title in title2id.keys():
            #     server.blogger.deletePost(
            #         appkey, title2id[title], usr, passwd, True)
            if title not in title2id.keys():
                post["categories"].append('[随笔分类]unpublished')  # 标记未发布
                # post["postid"] = title2id[title]
                postid = newPost(blogid, usr, passwd, post, publish)
                print("New:[title=%s][postid=%s][publish=%r]" %
                      (title, postid, publish))
        # 发布
        else:
            if title in title2id.keys():  # 博客里已经存在这篇文章
                mwb.editPost(title2id[title], usr, passwd, post, publish)
                print("Update:[title=%s][postid=%s][publish=%r]" %
                      (title, title2id[title], publish))
            else:  # 博客里还不存在这篇文章
                postid = newPost(blogid, usr, passwd, post, publish)
                print("New:[title=%s][postid=%s][publish=%r]" %
                      (title, postid, publish))


def download_art():
    recentPost = mwb.getRecentPosts(blogid, usr, passwd, recentnum)
    for post in recentPost:
        if "categories" in post.keys():
            if '[随笔分类]unpublished' in post["categories"]:
                with open(unp_path + post["title"] + ".md",
                          "w", encoding="utf-8") as f:
                    f.write(post["description"])
        else:
            with open(art_path + post["title"] + ".md",
                      "w", encoding="utf-8") as f:
                f.write(post["description"])


if __name__ == "__main__":
    if not exist_cfg():
        create_cfg()
    get_cfg()
    if len(sys.argv) > 1:
        if sys.argv[1] == "download":
            download_art()
        elif sys.argv[1] == "config":
            create_cfg()
            get_cfg()
    for mdfile in glob.glob(art_path + "*.md"):
        post_art(mdfile, True)
    for mdfile in glob.glob(unp_path + "*.md"):
        post_art(mdfile, False)
