#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
import io
import sqlite3
import cgi
import cgitb
cgitb.enable()
# windowsにおける文字化け回避
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#print("Content-type: text/html; charset=utf-8")
print('Content-Type: text/html; charset=UTF-8\n')
print(
"""
<html lang="ja">
<head>
<meta charset="utf-8">
<TITLE></TITLE>
</HEAD>
<BODY>
<P>HELLO</P><BR>
</BODY>
</HTML>
"""
)
