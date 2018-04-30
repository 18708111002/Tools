/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.github.tonydeng.fmj.utils;

/**
 *
 * @author zj
 */
import java.awt.image.BufferedImage;
import java.io.File;

import javax.imageio.ImageIO;

public class RemoveBlackBorder {
    /**
     * 读取一张图片的RGB值
     *
     * @throws Exception
     */
    public  BufferedImage cropImage(BufferedImage bufferedImage, int startX, int startY, int endX, int endY) {
        int width = bufferedImage.getWidth();
        int height = bufferedImage.getHeight();
        if (startX == -1) {
            startX = 0;
        }
        if (startY == -1) {
            startY = 0;
        }
        if (endX == -1) {
            endX = width - 1;
        }
        if (endY == -1) {
            endY = height - 1;
        }
        BufferedImage result = new BufferedImage(endX - startX, endY - startY, 4);
        for (int x = startX; x < endX; ++x) {
            for (int y = startY; y < endY; ++y) {
                int rgb = bufferedImage.getRGB(x, y);
                result.setRGB(x - startX, y - startY, rgb);
            }
        }
        return result;
    }


    public void removeBlackBorder(File file) throws Exception {
        int[] rgb = new int[3];
        BufferedImage bi = null;
        try {
            bi = ImageIO.read(file);
        } catch (Exception e) {
            e.printStackTrace();
        }
        int width = bi.getWidth();
        int height = bi.getHeight();
        int minx = bi.getMinX();
        int miny = bi.getMinY();
        int startX = minx;
        int endX = width;
        int startY = miny;
        int endY = height;

        System.out.print(width + " " + height);

        System.out.println("width=" + width + ",height=" + height + ".");
        System.out.println("minx=" + minx + ",miniy=" + miny + ".");
        for (int i = minx; i < width; i++) {
            for (int j = miny; j < height; j++) {
                int pixel = bi.getRGB(i, j); // 下面三行代码将一个数字转换为RGB数字
                rgb[0] = (pixel & 0xff0000) >> 16;
                rgb[1] = (pixel & 0xff00) >> 8;
                rgb[2] = (pixel & 0xff);
                if(rgb[0] >50 && rgb[1] >50 && rgb[2] > 50)
                {
//                    System.out.print("x:" + i + "  y:" + j);
                    startX = i;
                    startY = j;
                    i = width;
                    break;
                }
            }
        }
        for (int i = width - 1; i >= minx; i--) {
            for (int j = height - 1; j >= miny; j--) {
                int pixel = bi.getRGB(i, j); // 下面三行代码将一个数字转换为RGB数字
                rgb[0] = (pixel & 0xff0000) >> 16;
                rgb[1] = (pixel & 0xff00) >> 8;
                rgb[2] = (pixel & 0xff);
                if(rgb[0] > 50 && rgb[1] > 50 && rgb[2] > 50)
                {
//                    System.out.print("x:" + i + "  y:" + j);
                    endX = i;
                    endY = j;
                    i = -1;
                    break;
                }
            }
        }

        bi = this.cropImage(bi,startX,startY,endX,endY);
        ImageIO.write((BufferedImage) bi, "jpg", file);      //输出压缩图片

    }
}

