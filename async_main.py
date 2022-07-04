#! /usr/bin/python3


import requests
from Cryptodome.Cipher import AES
import os
from Cryptodome.Util.Padding import pad
import asyncio
import aiohttp

#  设置最大并发量是10
CONCURRENCY = 10
semaphore = asyncio.Semaphore(CONCURRENCY)


# https://www.kmff1.com/ 爬取快猫视频
def get_m3u8_list(o_url):
    # 得到m3u8文件
    host = o_url.split('/', 3)[0] + '//' + o_url.split('/', 3)[2]
    url = f'{o_url}' + '000'
    # 给文件夹命名
    file_name = url.split('/', 4)[-2]
    ts_filename = file_name + '_ts'
    mp4_filename = file_name + '_mp4'

    os.makedirs(f'./video/{file_name}/{ts_filename}')
    os.makedirs(f'./video/{file_name}/{mp4_filename}')
    resp = requests.get(url=url)
    m3u8_str = resp.text
    m3u8_list = []
    # print(resp.text)

    # 提取出ts文件
    with open(f'./video/{file_name}/{ts_filename}.list', 'w', encoding='utf-8') as f:
        f.write(m3u8_str)

    with open(f'./video/{file_name}/{ts_filename}.list', 'r', encoding='utf-8') as f:
        for line in f.readlines():

            if line.startswith('#'):
                continue
            else:
                # print(line)
                line = line.strip()
                m3u8_list.append(f'{host}{line}')
        # print(m3u8_list)
    return m3u8_list, file_name


# 下载ts文件,key

def get_key(m3u8_list, file_name):
    params = {'Host': 'v0623.sanzhuliang.cc',
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0',
              'Accept': '*/*',
              'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
              'Accept-Encoding': 'gzip, deflate, br',
              'Origin': 'https://www.kmff2.com',
              'Connection': 'keep-alive',
              'Referer': 'https://www.kmff2.com/',
              'Sec-Fetch-Dest': 'empty',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Site': 'cross-site',
              'TE': 'trailers'}
    key_url = m3u8_list[0].rsplit('/', 1)[0] + '/key.key'
    key_rsp = requests.get(url=key_url, params=params)
    key = key_rsp.text.encode('utf-8')
    print(f'获取密钥{key}')
    with open(f'./video/{file_name}/{file_name}.key', 'wb') as f:
        f.write(key)


async def get_one_ts(url, file_name, m3u8_list):
    ts_filename = file_name + '_ts'
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                with open(f"./video/{file_name}/{ts_filename}/{url.rsplit('/', 1)[1]}", 'wb') as b:
                    b.write(await resp.content.read())
                    print(f"{url.rsplit('/', 1)[1]}下载完成")
                    global x
                    print(f'{x}/{len(m3u8_list)}')
                    x += 1


async def get_ts(m3u8_list, file_name):
    tasks = []

    for url in m3u8_list:
        tasks.append(asyncio.create_task(get_one_ts(url, file_name, m3u8_list)))
        await asyncio.wait(tasks)


# 解密
def decrypt_ts(file_name):
    ts_filename = file_name + '_ts'
    mp4_filename = file_name + '_mp4'
    with open(f'./video/{file_name}/{file_name}.key', 'rb') as f:
        key = f.read()

    aes = AES.new(key=key, mode=AES.MODE_CBC, IV=b'0000000000000000')
    ts_name = os.listdir(f'./video/{file_name}/{ts_filename}')
    for name in ts_name:
        with open(f'./video/{file_name}/{ts_filename}/{name}', 'rb') as c, open(
                f'./video/{file_name}/{mp4_filename}/{name}',
                'wb') as d:
            bs = c.read()
            bs_len = len(bs)
            if bs_len != 16:
                bs = pad(bs, 16)
            d.write(aes.decrypt(bs))
            print(f"{name}转码成功")


# ts文件拼接

def cat_ts(file_name):
    mp4_filename = f'{file_name}' + '_mp4'
    ts_file_name_list = []
    with open(f'./video/{file_name}/{file_name}_ts.list', 'r') as f:
        for line in f.readlines():

            if line.startswith('#'):
                continue
            else:
                # print(line)
                line1 = line.rsplit('/', 1)[1].strip()
                line2 = f'./video/{file_name}/{mp4_filename}/{line1}'
                ts_file_name_list.append(line2)
    ts_str = ' '.join(ts_file_name_list)
    os.system(f'cat {ts_str} > ./video/{file_name}/{file_name}.mp4')


def del_temp_file(file_name):
    os.system(f'rm -rf /home/luo/桌面/kuaimao/video/{file_name}/{file_name}_mp4')
    os.system(f'rm -rf /home/luo/桌面/kuaimao/video/{file_name}/{file_name}_ts')
    os.system(f'rm -rf /home/luo/桌面/kuaimao/video/{file_name}/{file_name}.key')
    os.system(f'rm -rf /home/luo/桌面/kuaimao/video/{file_name}/{file_name}_ts.list')
    print('临时文件已清除。')

x = 1


def main(k):
    m3u8_return_list = get_m3u8_list(k)
    get_key(m3u8_return_list[0], m3u8_return_list[1])
    asyncio.run(get_ts(m3u8_return_list[0], m3u8_return_list[1]))
    decrypt_ts(m3u8_return_list[1])
    cat_ts(m3u8_return_list[1])
    del_temp_file(m3u8_return_list[1])
    print(f'{m3u8_return_list[1]}下载成功')
    x = 1
