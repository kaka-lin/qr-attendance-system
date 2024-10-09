# QR Codes Attendance System

## Usage

1. Install Python packages

    ```sh
    $ pip3 install -r requirements.txt
    ```

2. Running to generate QR Code

    ```sh
    $ python3 qrcode_tool.py
    ```

## Packing

if you want to packing Python programs into stand-alone executables

    Converting *.qrc (a collection of resource) files into *.py (Python source) file

    $ pyrcc5 -o src/qml.py src/qml.qrc

    $ pyrcc5 -o src/components.py src/resources/components/components.qrc

## Features

- [ ] 桌面程式
  - [x] 使用 GUI 產生 QRCode
    - [x] Only Email
    - [x] Google Sheet
  - [ ] 使用 GUI 掃描 QRCode
    - [x] 掃描 QRCode 並顯示資料
    - [ ] QRCode 顯示已經掃過

## Issues

### - `pyzbar` decode 中文亂碼

如標題，pyzbar 在解碼中文 QRCODE 時，會有亂碼出現

#### 解法

棄用 `pyzbar`，改用 [cv::QRCodeDetector()](https://docs.opencv.org/4.x/de/dc3/classcv_1_1QRCodeDetector.html)。

### - ImportError: Unable to find zbar shared library

在 mac 上，當我們用 `homebrew` 安裝完 `zbar` 後仍然會出現 ImportError 如下:

```sh
Traceback (most recent call last):
  File "qrcode_helper.py", line 6, in <module>
    from pyzbar import pyzbar
  File "/Users/kaka/opt/miniconda3/envs/py38/lib/python3.8/site-packages/pyzbar/pyzbar.py", line 7, in <module>
    from .wrapper import (
  File "/Users/kaka/opt/miniconda3/envs/py38/lib/python3.8/site-packages/pyzbar/wrapper.py", line 151, in <module>
    zbar_version = zbar_function(
  File "/Users/kaka/opt/miniconda3/envs/py38/lib/python3.8/site-packages/pyzbar/wrapper.py", line 148, in zbar_function
    return prototype((fname, load_libzbar()))
  File "/Users/kaka/opt/miniconda3/envs/py38/lib/python3.8/site-packages/pyzbar/wrapper.py", line 127, in load_libzbar
    libzbar, dependencies = zbar_library.load()
  File "/Users/kaka/opt/miniconda3/envs/py38/lib/python3.8/site-packages/pyzbar/zbar_library.py", line 65, in load
    raise ImportError('Unable to find zbar shared library')
ImportError: Unable to find zbar shared library
```

#### 解法

此時我們需要建立一個 `zbar library 的 link` 至你的 Python 環境的 lib 裡面，如下範例:

```sh
$ ln -s $(brew --prefix zbar)/lib/libzbar.dylib  /Users/kaka/opt/miniconda3/envs/py38/lib/libzbar.dylib
```

#### Reference

- [NaturalHistoryMuseum/pyzbar/issues:  ImportError: Unable to find zbar shared library #37 ](https://github.com/NaturalHistoryMuseum/pyzbar/issues/37)

