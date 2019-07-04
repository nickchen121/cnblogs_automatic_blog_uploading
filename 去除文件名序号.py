#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

BATH = '/Users/mac/Desktop/jupyter/cnblogs_automatic_blog_uploading/articles'
for filename in os.listdir(BATH):
    if filename.endswith('md'):
        old_name = os.path.join(BATH, filename)
        new_name = os.path.join(BATH, filename.split()[1])
        # print(old_name,new_name)
        os.rename(old_name, new_name)
