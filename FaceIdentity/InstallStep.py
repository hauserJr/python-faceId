#############################################
#   Windows 10 system install dlib package  #
#############################################
#1. 開啟CMD(Administrator) 輸入cl
# > cl
#Microsoft (R) C/C++ Optimizing Compiler Version 19.16.27030.1 for x64
#Copyright (C) Microsoft Corporation.  著作權所有，並保留一切權利。
#使用方式: cl [ option... ] filename... [ /link linkoption... ]
#代表 cl.exe 安裝成功
# => 失敗 請把cl.exe加入環境設定內

#2. pip install cmake
#開啟CMD(Administrator) 
# > cmake
#Usage
#  cmake [options] <path-to-source>
#  cmake [options] <path-to-existing-build>
#  cmake [options] -S <path-to-source> -B <path-to-build>
#Specify a source directory to (re-)generate a build system for it in the
#current working directory.  Specify an existing build directory to
#re-generate its build system.
# => 失敗 請google想辦法安裝好

#3. 至http://dlib.net/files/ 下載原始碼
#此專案使用dlib-19.16.zip
#下載後解壓縮
#開啟CMD CD至解壓縮路徑,執行python setup.py install
# Ps. 此步驟會很久
# 安裝失敗可以換個版本試試看

#4. 步驟3完成後會出現3個資料夾分別是dist、dlib、dlib.egg-info
#請將三個資料夾複製到../Anaconda3/Lib底下

#5. 步驟4完成後再將dlib-19.16/build/lib.win-amd64-3.7底下的dlib.cp37-win_amd64.pyd移至../Anaconda3/DLLs底下




###########
#   備註  #
###########
#
#可參考https://www.itread01.com/content/1546342937.html
#沒有安裝Anaconda可至https://www.anaconda.com/distribution/下載

