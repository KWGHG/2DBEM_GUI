# README 2DBEM GUI
透過二維邊界元素法（BEM）求解２維翼型的升力係數（CL）與壓力分佈（-CP）

![image](https://github.com/KWGHG/2DBEM_GUI/blob/master/2DBEM_GUI.jpg)

## 用法
可參考example資料夾內的範例  
:book:example資料夾內容
+ `2DBEM.exe`  GUI持行檔
+ `/input` 輸入檔資料夾，內有常見翼型幾何

##翼型文件格式
只包含x y座標，翼型全長縮放至[0,1]，並且點順序須從Trailing Edge順時針回來，範例如下  
| x | y |
|:-:|:-:|
| 1 | 0 |
| 0.9 | -0.05 |
| . | . |
| . | . |
| 0.9 | 0.05 |
| 1 | 0 |
## 安裝
此專案由python開發，需要套件如`requirements.txt`所示。  
套件：  
+ `PyQt5`
+ `matplotlib`
+ `numpy`
+ `scipy`
+ `pyinstaller`
