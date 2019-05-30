#   功能說明  #
臉部追蹤、辨識、資料訓練

#   Windows 10 system install dlib package  #

1. 開啟CMD(Administrator) 輸入cl，出現下列訊息就代表成功

 `Microsoft (R) C/C++ Optimizing Compiler Version 19.16.27030.1 for x64
Copyright (C) Microsoft Corporation.  著作權所有，並保留一切權利。
使用方式: cl [ option... ] filename... [ /link linkoption... ] `

    失敗 請把cl.exe加入環境設定內
    
 
2. pip install cmake後開啟CMD(Administrator)輸入cmake，出現下列訊息就代表成功

`
Usage
  cmake [options] <path-to-source>
  cmake [options] <path-to-existing-build>
  cmake [options] -S <path-to-source> -B <path-to-build>
Specify a source directory to (re-)generate a build system for it in the
current working directory.  Specify an existing build directory to
re-generate its build system.
`

    失敗 請google想辦法安裝好cmake

3. [dlib原始碼載點 dlib-download](http://dlib.net/files/)，此專案使用dlib-19.16.zip

    下載後解壓縮

    開啟CMD CD至解壓縮路徑,執行python setup.py install
 
    Ps. 此步驟會很久，安裝失敗可以換個版本試試看

4. 步驟3完成後會出現3個資料夾分別是dist、dlib、dlib.egg-info

    請將三個資料夾複製到..\Anaconda3\Lib底下

5. 步驟4完成後

    將dlib-19.16\build\lib.win-amd64-3.7底下的dlib.cp37-win_amd64.pyd移至..\Anaconda3\DLLs底下




#   備註  #

[安裝dlib可參考此文章](https://www.itread01.com/content/1546342937.html)

[Anaconda載點](https://www.anaconda.com/distribution/下載)

