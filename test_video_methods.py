import VideoMethods as vm

import os
import json
import csv
# vm.saveVidMP4('https://v16-webapp.tiktok.com/9df68411f06364a86afc3b1ab17be808/62d1b256/video/tos/useast2a/tos-useast2a-ve-0068c004/41c79f9beb7a40a79ebfdf475050c13e/?a=1988&ch=0&cr=0&dr=0&lr=tiktok_m&cd=0%7C0%7C1%7C0&cv=1&br=1728&bt=864&btag=80000&cs=0&ds=3&ft=eXd.6H1pMyq8ZyYTgwe2NiS6yl7Gb&mime_type=video_mp4&qs=0&rc=Ojk8ODc4OTY7ZDU7NThlZUBpMzhqbTo6ZnRzZDMzNzgzM0A1NGA1X18xNi0xLS5fYV40YSNxMnJxcjRfaGxgLS1kLzZzcw%3D%3D&l=20220715123036010192049166000B37FF',
#             'sample_media/tiktok2.mp4')

# vm.playVid('https://v16-webapp.tiktok.com/9df68411f06364a86afc3b1ab17be808/62d1b256/video/tos/useast2a/tos-useast2a-ve-0068c004/41c79f9beb7a40a79ebfdf475050c13e/?a=1988&ch=0&cr=0&dr=0&lr=tiktok_m&cd=0%7C0%7C1%7C0&cv=1&br=1728&bt=864&btag=80000&cs=0&ds=3&ft=eXd.6H1pMyq8ZyYTgwe2NiS6yl7Gb&mime_type=video_mp4&qs=0&rc=Ojk8ODc4OTY7ZDU7NThlZUBpMzhqbTo6ZnRzZDMzNzgzM0A1NGA1X18xNi0xLS5fYV40YSNxMnJxcjRfaGxgLS1kLzZzcw%3D%3D&l=20220715123036010192049166000B37FF')

# Saving every 50 frames from saved Mercedes TikTok to new folder mercedes_frames i.e., 'mercedes_frames/frame[x]'
# vm.saveFrames("sample_media/MercEg.mp4", "sample_media/mercedes_frames", 100)

# for entry in os.scandir("sample_media/mercedes_frames"):
#     # run_detector(detector, entry.path)
#     print(entry.path.replace(os.sep, '/'))

# vm.saveFrames("BMW.mp4", "sample_media/BMW", 100)

# vm.saveVidMP4("https://v16-webapp.tiktok.com/64649e2c3d61bae9109a5073bfefbdde/62d44782/video/tos/maliva/tos-maliva-ve-0068c799-us/c7f76768a554488aaa4021fc8343bd61/?a=1988&ch=0&cr=0&dr=0&lr=tiktok_m&cd=0%7C0%7C1%7C0&cv=1&br=1606&bt=803&btag=80000&cs=0&ds=3&ft=eXd.6H1pMyq8ZWK~gwe2Nj5eyl7Gb&mime_type=video_mp4&qs=0&rc=PDU1Z2hlZ2g0NGQ7Z2VmZ0BpM283bTM6ZjNpZDMzZzczNEBfNTEzNS8tNWIxMDI2Yl4tYSNhbjFxcjRfXzVgLS1kMS9zcw%3D%3D&l=20220717113132010217086207110BAD27", "sample_media/BMWmytest.mp4")

vm.saveVidMP4("https://www.tiktok.com/@bmwusa/video/7102446673347054891", "sample_media/bmw1.mp4")

