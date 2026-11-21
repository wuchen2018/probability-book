# 贝叶斯检测实验

[打开在线实验](https://wuchen2018.github.io/probability-book/demos/bayes/)

配套《大白话概率论》第3.4节。先把10万人分成患者和健康人，再做检测，最后只看测出阳性的人。默认参数与书中相同：患病率0.1%，灵敏度99%，假阳性率1%。

看完三步后，可以改变患病率，比较真阳性与假阳性人数；也可以展开“也改变检测方法”，调整灵敏度和假阳性率。

页面不需要安装Python，也不依赖外部脚本。源码为同目录的HTML、CSS和JavaScript。开发时在仓库根目录运行 `python -m http.server 8000`，浏览器访问 `http://localhost:8000/demos/bayes/`。
