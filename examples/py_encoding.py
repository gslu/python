mport sys
import chardet

#系统默认编码
print sys.getdefaultencoding()

#系统中文编码
# echo $LANG

#decode解码，encode编码,unicode作为中间码　decode --> unicode -->encode

string = "辅导书链接"
print type(string)

#str to unicode
s2=string.decode("utf-8")
print type(s2)

#unicode to gbk
s3=s2.encode("gbk")
print type(s3)

#gbk to unicode
s4=s3.decode("gbk")
print type(s4)

print string,s2,s3,s4

#查看非unicode的字符编码
print chardet.detect(string)
print chardet.detect(s3)

if not isinstance(s2,unicode):
    print chardet.detect(s2)


