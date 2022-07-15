import discord
from discord.ext import commands
import json
import random
import math
import time
from pathlib import Path
import requests
import os
import ml_detect
from helper import make_embed
from nms_wrapper import NMSType, NMSWrapper
from faster_rcnn_wrapper import FasterRCNNSlim
from _tf_compat_import import compat_tensorflow as tf
import numpy as np
import cv2

class Special(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        os.environ["DISCORD_TOKEN"] = "OTk2OTcwMzQ1Mjk2ODIyMzYy.GgL2yM.Q-7PG3F2tigt78VnQw28MN2_ToxpedB3IGBCPI"

    @commands.command(aliases=[])
    async def load_images(self, ctx):
        guild = ctx.guild.id

        imgpath = "img_" + str(guild) + "/"
        if not os.path.exists(imgpath):
            os.makedirs(imgpath)

        for member in ctx.guild.members:
            img_data = requests.get(member.avatar_url).content
            with open(imgpath + str(member.id) + '.jpg', 'wb') as handler:
                handler.write(img_data)
        await ctx.send("loaded images from " + str(guild))

    @commands.command(aliases=[])
    async def frakawaii(self, ctx):
        imgpath = "img_" + str(ctx.guild.id) + "/"
        await self.load_images(ctx)

        assert os.path.exists(imgpath), 'The input path does not exists'

        files = ml_detect.load_file_from_dir(imgpath)
        file_len = len(files)

        nms = NMSWrapper(NMSType.CPU_NMS)

        cfg = tf.ConfigProto()
        cfg.gpu_options.allow_growth = True
        sess = tf.Session(config=cfg)

        net = FasterRCNNSlim()
        saver = tf.train.Saver()

        saver.restore(sess, "model/res101_faster_rcnn_iter_60000.ckpt")

        result = {}

        time_start = time.time()

        for idx, file in enumerate(files):
            elapsed = time.time() - time_start
            eta = (file_len - idx) * elapsed / idx * 1.1 if idx > 0 else 0
            if idx % 4 == 1:
                await ctx.send('Current ETA: ' + ml_detect.fmt_time(eta) + ' until fraction kawaii calculated')

            print('[%d/%d] Elapsed: %s, ETA: %s >> %s' % (idx+1, file_len, ml_detect.fmt_time(elapsed), ml_detect.fmt_time(eta), file))
            img = cv2.imread(file)
            if img is None:
                continue
            scores, boxes = ml_detect.detect(sess, net, img)
            boxes = boxes[:, 4:8]
            scores = scores[:, 1]
            keep = nms(np.hstack([boxes, scores[:, np.newaxis]]).astype(np.float32), 0.2)
            boxes = boxes[keep, :]
            scores = scores[keep]
            inds = np.where(scores >= 0.5)[0]
            scores = scores[inds]
            boxes = boxes[inds, :]

            result[os.path.basename(file)] = []
            for i in range(scores.shape[0]):
                x1, y1, x2, y2 = boxes[i, :].tolist()
                new_result = {'score': float(scores[i])}
                result[os.path.basename(file)].append(new_result)

        count_anime = 0
        for key, value in result.items():
            user = ctx.guild.get_member(int(key[:-4]))
            username = user.name + "#" + user.discriminator
            if len(value) > 0:
                count_anime = count_anime + 1
                await ctx.send(username + " uses anime pfp with confidence " + str(value[0]["score"] * 100) + "%")
            print('Key : ' + str(key) + ', Value : ' + str(value))

        await ctx.send("frac kawaii: " + str(count_anime) + "/" + str(len(result.items())))
