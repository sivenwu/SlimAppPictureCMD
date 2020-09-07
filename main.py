import os
import sys
import os.path
import click
import tinify

tinify.key = ""  # API KEY
# test config
testDir = ""


@click.command()
@click.option('-d', "--dir", type=str, default=None, help="指定查找的项目根路径")
@click.option('-s', "--size", type=int, default=3072, help="默认查找3kb的图片进行压缩")
@click.option('-m', "--max", type=int, default=None, help="压缩限制数量")
@click.option('-o', "--opt", type=int, default=0, help="是否启用自动化压缩，0不开启 1开启")
def main(dir, size, max, opt):
    dirResult = "."
    sizeResult = 3072
    maxResult = 1
    optResult = 0
    if dir is not None:
        dirResult = dir
        pass
    if size is not None:
        sizeResult = size
        pass
    if max is not None:
        maxResult = max
    if opt is not None:
        optResult = opt
    ppPitureOpt(dirResult, sizeResult, maxResult, optResult)


# 目前代码支持遍历查询的图片格式是jpg、png
class ppPitureOpt(object):

    def __init__(self, dir, size, max, opt):
        """图片优化脚本类初始化"""
        print("初始化阶段...")
        self.dir = dir
        self.size = size
        self.max = max
        self.opt = opt
        print("指定查找路径为：", self.dir)
        print("指定查找的图片最大大小为(b,默认为3kb)：", self.size / 1024 )
        print("是否启用压缩", self.opt)
        if self.opt == 1:
            print("压缩最大限制数量", self.max)

        self.picturePaths = []  # 查找的图片路径集合
        # self.doTestConfig()  # 运行测试配置参数，正式环境可以屏蔽
        self.findPictures()

    def findPictures(self):
        """遍历查找图片"""
        for root, dirs, files in os.walk(self.dir):
            for fileName in files:
                if ((fileName.endswith('.png') or fileName.endswith('.jpg') or fileName.endswith(
                        '.jpeg')) and os.path.getsize(
                    os.path.join(root, fileName)) > self.size):
                    # print("*" * 100)
                    # print(os.path.join(root, fileName))
                    self.picturePaths.append(os.path.join(root, fileName))
                    pass
        print("picture size ", len(self.picturePaths))
        if len(self.picturePaths) > 0 and self.opt == 1:
            if(self.max > len(self.picturePaths)):
                self.max = len(self.picturePaths)
            for index in range(self.max):
                filePath = self.picturePaths[index]
                print("准备压缩文件路径为", filePath)
                self.compress_file(filePath, )

    def doTestConfig(self):
        self.dir = testDir

    def compress_file(self, inputFile):
        """指定文件压缩"""
        if not os.path.isfile(inputFile):
            print("文件路径有异常")
            return
        dirname = os.path.dirname(inputFile)
        basename = os.path.basename(inputFile)
        fileName, fileSuffix = os.path.splitext(basename)
        if fileSuffix == '.png' or fileSuffix == '.jpg' or fileSuffix == '.jpeg':
            self.compress_core(inputFile, dirname + "/syTiny_" + basename)
            print("压缩完成,""/ppTiny_" + basename)
            print("*" * 100)
        else:
            print("不支持该文件类型!")

    def compress_core(self, inputFile, outputFile):
        source = tinify.from_file(inputFile)
        source.to_file(outputFile)


if __name__ == "__main__":
    main()
