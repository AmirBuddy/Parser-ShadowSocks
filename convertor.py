import base64


def bugfix(string):
    index = string.rindex('@')
    var_list = [string[:index], string[index + 1:]]
    return var_list


class Shadowsocks:
    def __init__(self, link):
        self.link = link
        self.convertible = link[(link.find("ss://") + len("ss://")): link.rindex('#')]

    def credentials(self):
        try:
            if '@' in self.convertible:
                raise TypeError("Invalid 'convertible' format")
            decoded_link = base64.b64decode(f"{self.convertible}{'=' * ((4 - len(self.convertible) % 4) % 4)}").decode(
                'utf-8')
            info = decoded_link.split(':')
            temp = bugfix(info[1])
            info[1] = temp[0]
            info.insert(2, temp[1])
            return info
        except TypeError:
            temp = self.convertible.split('@')
            decoded_link = base64.b64decode(f"{temp[0]}{'=' * ((4 - len(temp[0]) % 4) % 4)}").decode('utf-8')
            info = decoded_link.split(':') + temp[1].split(':')
            return info

    def get_type(self):
        return self.link[: self.link.find('://')]

    def get_name(self):
        try:
            if '_' not in self.link:
                raise ArithmeticError("Invalid 'link' format")
            name = self.link[self.link.rindex('#') + 1:].split('_')
            name = name[-2] + '_' + name[-1]
            return name[:-1]
        except ArithmeticError:
            return self.link[self.link.rindex('#') + 1: -1]

    def get_encryption(self):
        return self.credentials()[0]

    def get_password(self):
        return self.credentials()[1]

    def get_ip(self):
        return self.credentials()[2]

    def get_port(self):
        return self.credentials()[3]


with open('shadowsocks.txt', 'r') as fin, open('config.conf', 'wt') as fout:
    intro = """#!MANAGED-CONFIG https://oss.v2rayse.com/proxies/data/2022-09-18/RIcV8t.txt interval=86400 strict=false
[General]
skip-proxy = 127.0.0.1, 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12, 100.64.0.0/10, localhost, *.local
dns-server = 114.114.114.114, 223.5.5.5, system
always-real-ip = stun.l.google.com
doh-server = https://doh.pub/dns-query

[Proxy]\n"""

    fout.write(intro)

    proxy_list = []
    for ss in fin:
        proxy = Shadowsocks(ss.strip())
        proxy_list.append(proxy.get_name())
        fout.write(
            f"{proxy.get_name()} = {proxy.get_type()}, {proxy.get_ip()}, {proxy.get_port()}, "
            f"encrypt-method={proxy.get_encryption()}, password={proxy.get_password()}, udp-relay=false\n"
        )

    fout.write('\n[Proxy Group]\nSelectGroup = select')

    for x in proxy_list:
        fout.write(f', {x}')

    outro = """\n\n[Rule]
# Apple
DOMAIN-SUFFIX,appsto.re,SelectGroup
DOMAIN-SUFFIX,s.mzstatic.com,SelectGroup
DOMAIN,gspe1-ssl.ls.apple.com,SelectGroup
DOMAIN,news-events.apple.com,SelectGroup
DOMAIN,news-client.apple.com,SelectGroup
DOMAIN-SUFFIX,itunes.apple.com,SelectGroup
DOMAIN-SUFFIX,lookup-api.apple.com,SelectGroup
DOMAIN-SUFFIX,lcdn-registration.apple.com,DIRECT
DOMAIN-SUFFIX,mzstatic.com,DIRECT

# Facebook
DOMAIN-SUFFIX,cdninstagram.com,SelectGroup,force-remote-dns
DOMAIN-SUFFIX,facebook.com,SelectGroup,force-remote-dns
DOMAIN-SUFFIX,facebook.net,SelectGroup,force-remote-dns
DOMAIN-SUFFIX,fb.com,SelectGroup,force-remote-dns
DOMAIN-SUFFIX,fb.me,SelectGroup,force-remote-dns
DOMAIN-SUFFIX,fbcdn.net,SelectGroup,force-remote-dns
DOMAIN-SUFFIX,instagram.com,SelectGroup,force-remote-dns
DOMAIN-SUFFIX,whatsapp.net,SelectGroup,force-remote-dns
DOMAIN-SUFFIX,whatsapp.com,SelectGroup,force-remote-dns

# Twitter
DOMAIN-SUFFIX,t.co,SelectGroup,force-remote-dns
DOMAIN-SUFFIX,twimg.com,SelectGroup,force-remote-dns
DOMAIN-SUFFIX,twitter.com,SelectGroup,force-remote-dns

# Google
DOMAIN-SUFFIX,ampproject.com,SelectGroup
DOMAIN-SUFFIX,ampproject.net,SelectGroup
DOMAIN-SUFFIX,ampproject.org,SelectGroup
DOMAIN-SUFFIX,android.com,SelectGroup
DOMAIN-SUFFIX,blogspot.com,SelectGroup
DOMAIN-SUFFIX,blogspot.hk,SelectGroup
DOMAIN-SUFFIX,g.co,SelectGroup
DOMAIN-SUFFIX,ggpht.com,SelectGroup
DOMAIN-SUFFIX,goo.gl,SelectGroup
DOMAIN-SUFFIX,googleusercontent.com,SelectGroup
DOMAIN-SUFFIX,googlevideo.com,SelectGroup
DOMAIN-SUFFIX,gstatic.com,SelectGroup
DOMAIN-SUFFIX,gstatic.cn,SelectGroup
DOMAIN-SUFFIX,gvt0.com,SelectGroup
DOMAIN-SUFFIX,gvt1.com,SelectGroup
DOMAIN-SUFFIX,gvt2.com,SelectGroup
DOMAIN-SUFFIX,gvt3.com,SelectGroup
DOMAIN-SUFFIX,youtu.be,SelectGroup
DOMAIN-SUFFIX,youtube.com,SelectGroup,force-remote-dns
DOMAIN-SUFFIX,youtube-nocookie.com,SelectGroup
DOMAIN-SUFFIX,ytimg.com,SelectGroup
DOMAIN,accounts.google.com,SelectGroup,force-remote-dns,enhanced-mode
DOMAIN-SUFFIX,appspot.com,SelectGroup,force-remote-dns
DOMAIN-SUFFIX,googleapis.cn,SelectGroup,force-remote-dns,enhanced-mode
DOMAIN-SUFFIX,googleapis.com,SelectGroup,force-remote-dns,enhanced-mode
DOMAIN-SUFFIX,googlesource.com,SelectGroup,force-remote-dns,enhanced-mode
DOMAIN-SUFFIX,google.com,SelectGroup,force-remote-dns,enhanced-mode
DOMAIN-SUFFIX,gmail.com,SelectGroup,force-remote-dns
DOMAIN-KEYWORD,google,SelectGroup,force-remote-dns

# Netflix
DOMAIN-SUFFIX,netflix.com,SelectGroup
DOMAIN-SUFFIX,netflix.net,SelectGroup
DOMAIN-SUFFIX,nflxext.com,SelectGroup
DOMAIN-SUFFIX,nflximg.com,SelectGroup
DOMAIN-SUFFIX,nflximg.net,SelectGroup
DOMAIN-SUFFIX,nflxso.net,SelectGroup
DOMAIN-SUFFIX,nflxvideo.net,SelectGroup

# BAT
DOMAIN-SUFFIX,baidu.com,DIRECT
DOMAIN-SUFFIX,baidupcs.com,DIRECT
DOMAIN-SUFFIX,bdimg.com,DIRECT
DOMAIN-SUFFIX,bdstatic.com,DIRECT
DOMAIN-SUFFIX,alipay.com,DIRECT
DOMAIN-SUFFIX,alipayobjects.com,DIRECT
DOMAIN-SUFFIX,alicdn.com,DIRECT
DOMAIN-SUFFIX,aliyun.com,DIRECT
DOMAIN-SUFFIX,aliyuncs.com,DIRECT
DOMAIN-SUFFIX,taobao.com,DIRECT
DOMAIN-SUFFIX,tmall.com,DIRECT
DOMAIN-SUFFIX,qq.com,DIRECT
DOMAIN-SUFFIX,qqurl.com,DIRECT

# China
DOMAIN-SUFFIX,cn,DIRECT
DOMAIN-SUFFIX,126.net,DIRECT
DOMAIN-SUFFIX,163.com,DIRECT
DOMAIN-SUFFIX,163.net,DIRECT
DOMAIN-SUFFIX,amap.com,DIRECT
DOMAIN-SUFFIX,autonavi.com,DIRECT
DOMAIN-SUFFIX,ccgslb.com,DIRECT
DOMAIN-SUFFIX,ccgslb.net,DIRECT
DOMAIN-SUFFIX,cnbeta.com,DIRECT
DOMAIN-SUFFIX,cnbetacdn.com,DIRECT
DOMAIN-SUFFIX,douban.com,DIRECT
DOMAIN-SUFFIX,doubanio.com,DIRECT
DOMAIN-SUFFIX,gtimg.com,DIRECT
DOMAIN-SUFFIX,hao123.com,DIRECT
DOMAIN-SUFFIX,haosou.com,DIRECT
DOMAIN-SUFFIX,ifeng.com,DIRECT
DOMAIN-SUFFIX,iqiyi.com,DIRECT
DOMAIN-SUFFIX,jd.com,DIRECT
DOMAIN-SUFFIX,mi.com,DIRECT
DOMAIN-SUFFIX,miui.com,DIRECT
DOMAIN-SUFFIX,netease.com,DIRECT
DOMAIN-SUFFIX,netease.im,DIRECT
DOMAIN-SUFFIX,qdaily.com,DIRECT
DOMAIN-SUFFIX,qhimg.com,DIRECT
DOMAIN-SUFFIX,qihucdn.com,DIRECT
DOMAIN-SUFFIX,qiniucdn.com,DIRECT
DOMAIN-SUFFIX,qiniudn.com,DIRECT
DOMAIN-SUFFIX,sogou.com,DIRECT
DOMAIN-SUFFIX,sogoucdn.com,DIRECT
DOMAIN-SUFFIX,sohu.com,DIRECT
DOMAIN-SUFFIX,steamstatic.com,DIRECT
DOMAIN-SUFFIX,suning.com,DIRECT
DOMAIN-SUFFIX,tudou.com,DIRECT
DOMAIN-SUFFIX,upaiyun.com,DIRECT
DOMAIN-SUFFIX,clouddn.com,DIRECT
DOMAIN-SUFFIX,upyun.com,DIRECT
DOMAIN-SUFFIX,weibo.com,DIRECT
DOMAIN-SUFFIX,youku.com,DIRECT
DOMAIN-SUFFIX,xunlei.com,DIRECT
DOMAIN-SUFFIX,zhihu.com,DIRECT
DOMAIN-SUFFIX,zhimg.com,DIRECT

DOMAIN,ip.bjango.com,DIRECT

# Blocked
DOMAIN-SUFFIX,9to5mac.com,SelectGroup
DOMAIN-SUFFIX,abpchina.org,SelectGroup
DOMAIN-SUFFIX,adblockplus.org,SelectGroup
DOMAIN-SUFFIX,akamaihd.net,SelectGroup
DOMAIN-SUFFIX,amazon.com,SelectGroup
DOMAIN-SUFFIX,amazonaws.com,SelectGroup,enhanced-mode
DOMAIN-SUFFIX,amplitude.com,SelectGroup
DOMAIN-SUFFIX,angularjs.org,SelectGroup
DOMAIN-SUFFIX,aol.com,SelectGroup
DOMAIN-SUFFIX,aolcdn.com,SelectGroup
DOMAIN-SUFFIX,arcgis.com,SelectGroup
DOMAIN-SUFFIX,archive.org,SelectGroup
DOMAIN-SUFFIX,aspnetcdn.com,SelectGroup
DOMAIN-SUFFIX,att.com,SelectGroup
DOMAIN-SUFFIX,awsstatic.com,SelectGroup
DOMAIN-SUFFIX,azureedge.net,SelectGroup
DOMAIN-SUFFIX,azurewebsites.net,SelectGroup
DOMAIN-SUFFIX,bbc.com,SelectGroup
DOMAIN-SUFFIX,bbc.co,SelectGroup
DOMAIN-SUFFIX,bintray.com,SelectGroup,enhanced-mode
DOMAIN-SUFFIX,bit.com,SelectGroup
DOMAIN-SUFFIX,bit.ly,SelectGroup
DOMAIN-SUFFIX,bitbucket.org,SelectGroup
DOMAIN-SUFFIX,blog.com,SelectGroup
DOMAIN-SUFFIX,blogcdn.com,SelectGroup
DOMAIN-SUFFIX,blogger.com,SelectGroup
DOMAIN-SUFFIX,blogsmithmedia.com,SelectGroup
DOMAIN-SUFFIX,bloomberg.com,SelectGroup
DOMAIN-SUFFIX,box.net,SelectGroup
DOMAIN-SUFFIX,box.com,SelectGroup
DOMAIN-SUFFIX,cachefly.net,SelectGroup
DOMAIN-SUFFIX,chromium.org,SelectGroup
DOMAIN-SUFFIX,cl.ly,SelectGroup
DOMAIN-SUFFIX,cloudflare.com,SelectGroup
DOMAIN-SUFFIX,cloudfront.net,SelectGroup
DOMAIN-SUFFIX,cloudmagic.com,SelectGroup
DOMAIN-SUFFIX,cnet.com,SelectGroup
DOMAIN-SUFFIX,cocoapods.org,SelectGroup
DOMAIN-SUFFIX,cocoapods.org,SelectGroup
DOMAIN-SUFFIX,culturedcode.com,SelectGroup
DOMAIN-SUFFIX,d.pr,SelectGroup
DOMAIN-SUFFIX,dayone.me,SelectGroup
DOMAIN-SUFFIX,digicert.com,SelectGroup
DOMAIN-SUFFIX,discord.gg,SelectGroup
DOMAIN-SUFFIX,discordapp.com,SelectGroup
DOMAIN-SUFFIX,discordapp.net,SelectGroup
DOMAIN-SUFFIX,disq.us,SelectGroup
DOMAIN-SUFFIX,disqus.com,SelectGroup
DOMAIN-SUFFIX,disquscdn.com,SelectGroup
DOMAIN-SUFFIX,dnsimple.com,SelectGroup
DOMAIN-SUFFIX,docker.com,SelectGroup
DOMAIN-SUFFIX,dribbble.com,SelectGroup
DOMAIN-SUFFIX,dropbox.com,SelectGroup
DOMAIN-SUFFIX,dropboxapi.com,SelectGroup
DOMAIN-SUFFIX,dropboxstatic.com,SelectGroup
DOMAIN-SUFFIX,dropboxusercontent.com,SelectGroup
DOMAIN-SUFFIX,droplr.com,SelectGroup
DOMAIN-SUFFIX,duckduckgo.com,SelectGroup
DOMAIN-SUFFIX,edgecastcdn.net,SelectGroup
DOMAIN-SUFFIX,edgesuite.net,SelectGroup
DOMAIN-SUFFIX,engadget.com,SelectGroup
DOMAIN-SUFFIX,entrust.net,SelectGroup
DOMAIN-SUFFIX,evernote.com,SelectGroup
DOMAIN-SUFFIX,fabric.io,SelectGroup
DOMAIN-SUFFIX,fastly.net,SelectGroup
DOMAIN-SUFFIX,fc2.com,SelectGroup
DOMAIN-SUFFIX,feedburner.com,SelectGroup
DOMAIN-SUFFIX,feedly.com,SelectGroup
DOMAIN-SUFFIX,feedsportal.com,SelectGroup
DOMAIN-SUFFIX,flickr.com,SelectGroup
DOMAIN-SUFFIX,gitbooks.io,SelectGroup
DOMAIN-SUFFIX,git.io,SelectGroup
DOMAIN-SUFFIX,github.com,SelectGroup,enhanced-mode
DOMAIN-SUFFIX,github.io,SelectGroup
DOMAIN-SUFFIX,githubapp.com,SelectGroup
DOMAIN-SUFFIX,githubusercontent.com,SelectGroup,enhanced-mode
DOMAIN-SUFFIX,globalsign.com,SelectGroup
DOMAIN-SUFFIX,gmodules.com,SelectGroup
DOMAIN-SUFFIX,godaddy.com,SelectGroup
DOMAIN-SUFFIX,golang.org,SelectGroup
DOMAIN-SUFFIX,goodreaders.com,SelectGroup
DOMAIN-SUFFIX,goodreads.com,SelectGroup
DOMAIN-SUFFIX,graphql.org,SelectGroup
DOMAIN-SUFFIX,gravatar.com,SelectGroup
DOMAIN-SUFFIX,gumroad.com,SelectGroup
DOMAIN-SUFFIX,heroku.com,SelectGroup
DOMAIN-SUFFIX,herokucdn.com,SelectGroup
DOMAIN-SUFFIX,hotmail.com,SelectGroup
DOMAIN-SUFFIX,ift.tt,SelectGroup
DOMAIN-SUFFIX,ifttt.com,SelectGroup
DOMAIN-SUFFIX,imageshack.us,SelectGroup
DOMAIN-SUFFIX,img.ly,SelectGroup
DOMAIN-SUFFIX,imgur.com,SelectGroup
DOMAIN-SUFFIX,instapaper.com,SelectGroup
DOMAIN-SUFFIX,ipfs.io,SelectGroup
DOMAIN-SUFFIX,ipn.li,SelectGroup
DOMAIN-SUFFIX,is.gd,SelectGroup
DOMAIN-SUFFIX,j.mp,SelectGroup
DOMAIN-SUFFIX,jshint.com,SelectGroup
DOMAIN-SUFFIX,kat.cr,SelectGroup
DOMAIN-SUFFIX,libsyn.com,SelectGroup
DOMAIN-SUFFIX,licdn.com,SelectGroup
DOMAIN-SUFFIX,linkedin.com,SelectGroup
DOMAIN-SUFFIX,linode.com,SelectGroup
DOMAIN-SUFFIX,lithium.com,SelectGroup
DOMAIN-SUFFIX,littlehj.com,SelectGroup
DOMAIN-SUFFIX,live.com,SelectGroup
DOMAIN-SUFFIX,live.net,SelectGroup
DOMAIN-SUFFIX,mathjax.org,SelectGroup
DOMAIN-SUFFIX,medium.com,SelectGroup
DOMAIN-SUFFIX,mega.co.nz,SelectGroup
DOMAIN-SUFFIX,mega.nz,SelectGroup
DOMAIN-SUFFIX,megaupload.com,SelectGroup
DOMAIN-SUFFIX,mobile01.com,SelectGroup
DOMAIN-SUFFIX,modmyi.com,SelectGroup
DOMAIN-SUFFIX,name.com,SelectGroup
DOMAIN-SUFFIX,nextmedia.com,SelectGroup
DOMAIN-SUFFIX,nintendo.com,SelectGroup
DOMAIN-SUFFIX,nyti.ms,SelectGroup
DOMAIN-SUFFIX,nytimes.com,SelectGroup
DOMAIN-SUFFIX,nytimg.com,SelectGroup
DOMAIN-SUFFIX,nytstyle.com,SelectGroup
DOMAIN-SUFFIX,nyt.com,SelectGroup
DOMAIN-SUFFIX,omnigroup.com,SelectGroup
DOMAIN-SUFFIX,onenote.com,SelectGroup
DOMAIN-SUFFIX,openvpn.net,SelectGroup
DOMAIN-SUFFIX,openwrt.org,SelectGroup
DOMAIN-SUFFIX,ow.ly,SelectGroup
DOMAIN-SUFFIX,pastebin.com,SelectGroup
DOMAIN-SUFFIX,pandora.com,SelectGroup
DOMAIN-SUFFIX,pinterest.com,SelectGroup
DOMAIN-SUFFIX,pinimg.com,SelectGroup
DOMAIN-SUFFIX,periscope.tv,SelectGroup
DOMAIN-SUFFIX,pinboard.in,SelectGroup
DOMAIN-SUFFIX,pixiv.net,SelectGroup
DOMAIN-SUFFIX,pixiv.org,SelectGroup
DOMAIN-SUFFIX,playpcesor.com,SelectGroup
DOMAIN-SUFFIX,skype.com,SelectGroup
DOMAIN-SUFFIX,slack.com,SelectGroup
DOMAIN-SUFFIX,slack-edge.com,SelectGroup
DOMAIN-SUFFIX,slack-msgs.com,SelectGroup
DOMAIN-SUFFIX,smartmailcloud.com,SelectGroup
DOMAIN-SUFFIX,sndcdn.com,SelectGroup
DOMAIN-SUFFIX,soundcloud.com,SelectGroup
DOMAIN-SUFFIX,sourceforge.net,SelectGroup,enhanced-mode
DOMAIN-SUFFIX,sourceforge.io,SelectGroup,enhanced-mode
DOMAIN-SUFFIX,speakerdeck.com,SelectGroup
DOMAIN-SUFFIX,spotify.com,SelectGroup
DOMAIN-SUFFIX,squarespace.com,SelectGroup
DOMAIN-SUFFIX,sstatic.net,SelectGroup
DOMAIN-SUFFIX,stackoverflow.com,SelectGroup
DOMAIN-SUFFIX,staticflickr.com,SelectGroup
DOMAIN-SUFFIX,steamcommunity.com,SelectGroup
DOMAIN-SUFFIX,symauth.com,SelectGroup
DOMAIN-SUFFIX,symcb.com,SelectGroup
DOMAIN-SUFFIX,symcd.com,SelectGroup
DOMAIN-SUFFIX,tapbots.com,SelectGroup
DOMAIN-SUFFIX,tapbots.net,SelectGroup
DOMAIN-SUFFIX,techcrunch.com,SelectGroup
DOMAIN-SUFFIX,textnow.me,SelectGroup
DOMAIN-SUFFIX,theinitium.com,SelectGroup
DOMAIN-SUFFIX,telegram.org,SelectGroup
DOMAIN-SUFFIX,telegram.me,SelectGroup
DOMAIN-SUFFIX,telegra.ph,SelectGroup
DOMAIN-SUFFIX,tdesktop.com,SelectGroup
DOMAIN-SUFFIX,t.me,SelectGroup
DOMAIN-SUFFIX,thepiratebay.org,SelectGroup
DOMAIN-SUFFIX,tiny.cc,SelectGroup
DOMAIN-SUFFIX,tinypic.com,SelectGroup
DOMAIN-SUFFIX,tmblr.co,SelectGroup
DOMAIN-SUFFIX,trello.com,SelectGroup
DOMAIN-SUFFIX,trellocdn.com,SelectGroup
DOMAIN-SUFFIX,tumblr.com,SelectGroup
DOMAIN-SUFFIX,twitch.tv,SelectGroup
DOMAIN-SUFFIX,txmblr.com,SelectGroup
DOMAIN-SUFFIX,typekit.net,SelectGroup
DOMAIN-SUFFIX,ubnt.com,SelectGroup
DOMAIN-SUFFIX,urchin.com,SelectGroup
DOMAIN-SUFFIX,v.gd,SelectGroup
DOMAIN-SUFFIX,vimeo.com,SelectGroup
DOMAIN-SUFFIX,vimeocdn.com,SelectGroup
DOMAIN-SUFFIX,vine.co,SelectGroup
DOMAIN-SUFFIX,vox-cdn.com,SelectGroup
DOMAIN-SUFFIX,vsco.co,SelectGroup
DOMAIN-SUFFIX,w3schools.com,SelectGroup
DOMAIN-SUFFIX,weather.com,SelectGroup
DOMAIN-SUFFIX,wikimedia.org,SelectGroup
DOMAIN-SUFFIX,wikipedia.com,SelectGroup
DOMAIN-SUFFIX,wikipedia.org,SelectGroup
DOMAIN-SUFFIX,windows.net,SelectGroup
DOMAIN-SUFFIX,wordpress.com,SelectGroup
DOMAIN-SUFFIX,wp.com,SelectGroup
DOMAIN-SUFFIX,wsj.com,SelectGroup
DOMAIN-SUFFIX,wsj.net,SelectGroup
DOMAIN-SUFFIX,yahoo.com,SelectGroup
DOMAIN-SUFFIX,yahoo.net,SelectGroup
DOMAIN-SUFFIX,yimg.com,SelectGroup
DOMAIN-SUFFIX,ying.com,SelectGroup

# Line
DOMAIN-SUFFIX,scdn.co,SelectGroup,force-remote-dns
DOMAIN-SUFFIX,line.naver.jp,SelectGroup,force-remote-dns
DOMAIN-SUFFIX,line.me,SelectGroup
DOMAIN-SUFFIX,line-apps.com,SelectGroup
DOMAIN-SUFFIX,line-cdn.net,SelectGroup
DOMAIN-SUFFIX,line-scdn.net,SelectGroup

# Telegram
IP-CIDR,91.108.56.0/22,SelectGroup,no-resolve
IP-CIDR,91.108.4.0/22,SelectGroup,no-resolve
IP-CIDR,91.108.8.0/22,SelectGroup,no-resolve
IP-CIDR,109.239.140.0/24,SelectGroup,no-resolve
IP-CIDR,149.154.160.0/20,SelectGroup,no-resolve
IP-CIDR,149.154.164.0/22,SelectGroup,no-resolve

# LAN
DOMAIN-SUFFIX,local,DIRECT
IP-CIDR,192.168.0.0/16,DIRECT
IP-CIDR,10.0.0.0/8,DIRECT
IP-CIDR,172.16.0.0/12,DIRECT
IP-CIDR,127.0.0.0/8,DIRECT
IP-CIDR,100.64.0.0/10,DIRECT

# Final
GEOIP,CN,DIRECT
FINAL,SelectGroup"""
    fout.write(outro)
