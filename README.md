# cnblogs_githook
基于rpcxml协议，利用githook，在commit时自动发布本地markdown文章到博客园。
## 使用说明
本脚本用`python3`编写，请配置好运行环境。
1. 第一次使用前先把`./hooks/commit-msg`文件复制到`./.git/hooks/`中。
1. 运行`cnblogs.py`：
    1. 程序有一个可选参数。
        - `config` 设置博客信息。
        - `download` 下载文章。
    1. 第一次运行`cnblogs.py`时默认选择`config`参数，设置博客信息。
    1. 此后每次运行程序时，`./articles/*.md`将被上传到博客并发布；`./unpublished/*.md`将被上传到博客，但不发布（并标注分类“unpublished”）。文章均**以文件名为题**，且不发布的文章。**如果博客中已经存在同名文章，将替换其内容！**
1. 编辑`./articles/`，`./unpublished/`中markdown文件，在本地git仓库`commit`更改，自动运行`./cnblogs.py`（需要使用终端命令才能查看返回信息）。
## 注意事项/已知Bug
1. **本程序不保证稳定性**，为防止数据丢失，建议使用前预先备份博客。
1. clone仓库不能下载`.git`文件夹，因此需要手动复制调用`cnblogs.py`的脚本`./hooks/commit-msg`到`.git`。
1. 由于metaWeBlog本身没有提供查看文章是否已发布的接口，所有使用“unpublished”分类标注未发布文章。也就是说，**当执行`python cnblogs.py download`命令时，博客中没有发布也没有“unpublished”分类的文章也会存到`./articles/`，下次运行时将被自动发布。**
2. 由于接口不允许将已经发布的文章设置为未发布，所以若`./unpublished/`内的文章在博客内有同名文章时不会被上传。