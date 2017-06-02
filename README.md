# Youku-Android-APP-Sniffer

这个运用“WiFi钓鱼”与python实现的“优酷视频安卓APP嗅探器”是在我的博客《[通过实时解析JSON获知优酷APP用户的播放内容](https://mp.weixin.qq.com/s/4aATocK5k88M1owf_rqjeA)》的基础上进行修改的。

该项目目前由以下4个文件组成：

  （1）YoukuVideo.py，优酷视频对象
  
  （2）create_dataset.py，用于创建数据集“dataset.csv”
  
  （3）classifier.py，用于操作数据集“dataset.csv”从而做分类
  
  （4）dataset.csv，数据集
  
该实验的运行环境：

  （1）Kali Linux 2 虚拟机
  
  （2）USB无线网卡
